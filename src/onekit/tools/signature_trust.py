# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import hashlib
import re
from dataclasses import replace
from urllib.parse import urlsplit

TSL = 'http://uri.etsi.org/02231/v2#'
EXTRA = 'http://uri.etsi.org/02231/v2/additionaltypes#'
LANG = '{http://www.w3.org/XML/1998/namespace}lang'
SK_SERVICE_ID = '{http://ep.nbu.gov.sk/kca/tsl/x509types#}TLServiceIdentifier'


def _xml_takeover(element):
    expected = [f'{{{EXTRA}}}URI', f'{{{EXTRA}}}TSPName',
                f'{{{TSL}}}SchemeOperatorName', f'{{{TSL}}}SchemeTerritory']
    children = list(element)
    if (element.attrib or [child.tag for child in children[:4]] != expected
            or (element.text or '').strip() or any((child.tail or '').strip() for child in children)):
        raise ValueError('unsupported_takeover_content')
    uri, provider, operator, territory = children[:4]
    for qualifier in children[4:]:
        if (qualifier.tag != f'{{{EXTRA}}}OtherQualifier' or qualifier.attrib or len(qualifier) != 1
                or (qualifier.text or '').strip()):
            raise ValueError('unsupported_takeover_qualifier')
        identifier = qualifier[0]
        # NBU's published x509types schema: a reference to an indexed service,
        # not permission to replace its certificates, policies or approval status.
        if (identifier.tag != SK_SERVICE_ID or identifier.attrib or len(identifier)
                or (identifier.tail or '').strip()
                or not re.fullmatch(r'TLI[A-Z]{2}-(?:[1-9][0-9]*)?', identifier.text or '')):
            raise ValueError('unsupported_takeover_qualifier')
    if (len(uri) or set(uri.attrib) != {LANG} or not uri.text or not urlsplit(uri.text).scheme
            or not re.fullmatch(r'[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*', uri.get(LANG, ''))):
        raise ValueError('invalid_takeover_uri')
    for names in (provider, operator):
        if names.attrib or not len(names) or (names.text or '').strip():
            raise ValueError('invalid_takeover_names')
        for name in names:
            if (name.tag != f'{{{TSL}}}Name' or len(name) or set(name.attrib) != {LANG}
                    or not (name.text or '').strip()
                    or not re.fullmatch(r'[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*', name.get(LANG, ''))):
                raise ValueError('invalid_takeover_name')
    if territory.attrib or len(territory) or not re.fullmatch('[A-Z]{2}', territory.text or ''):
        raise ValueError('invalid_takeover_territory')


def _guard_takeover_content(xml):
    from lxml import etree
    parser = etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True, remove_comments=True)
    root = etree.fromstring(xml.encode('utf-8'), parser)
    for element in root.iter(f'{{{EXTRA}}}TakenOverBy'):
        try:
            _xml_takeover(element)
        except ValueError:
            # The upstream permissive schema parser otherwise drops unknown
            # children of known elements. Preserve rejection by treating the
            # ENTIRE unsupported extension as unknown, never by clearing critical.
            element.tag = '{urn:onekit:unsupported}TakenOverBy'
    return etree.tostring(root, encoding='unicode')


def add_authenticated_services(xml, registry):
    # Caller MUST authenticate this exact source XML first. Only the in-memory
    # interpretation is adapted; the signed archive and certificates never change.
    # ETSI TS 119 612 v2.4.1, 5.5.9.3: taking over is descriptive legal metadata,
    # not an instruction to transfer anchors or alter the service status/history.
    from pyhanko.generated.etsi import ServiceTypeIdentifier, ts_119612_extra
    from pyhanko.sign.validation.qualified import eutl_parse as upstream
    from pyhanko.sign.validation.qualified.tsp import CA_QC_URI, QTST_URI

    parsed = upstream._raw_tl_parse(_guard_takeover_content(xml))
    if parsed.trust_service_provider_list is None:
        return [], 0
    errors = []
    taken_over = 0
    records = getattr(registry, '_onekit_takeovers', [])

    def interpret(delegate):
        def read(service_info, next_update_at):
            nonlocal taken_over
            extensions = service_info.service_information_extensions
            takeovers, retained = [], []
            for extension in extensions.extension if extensions else ():
                remaining = []
                for item in extension.content:
                    if isinstance(item, ts_119612_extra.TakenOverBy):
                        # Raw XML was checked in full above. Unknown optional
                        # qualifiers and malformed fields never reach this branch.
                        takeovers.append({
                            'informationUri': item.uri.value,
                            'informationLanguage': item.uri.lang,
                            'providerNames': [{'language': name.lang, 'name': name.value} for name in item.tspname.name],
                            'schemeOperatorNames': [{'language': name.lang, 'name': name.value} for name in item.scheme_operator_name.name],
                            'territory': item.scheme_territory,
                            'critical': bool(extension.critical),
                            'serviceReferences': [node.text for qualifier in item.other_qualifier for node in qualifier.content],
                        })
                    else:
                        remaining.append(item)
                if remaining:
                    retained.append(replace(extension, content=tuple(remaining)))
            if takeovers:
                service_info = replace(service_info, service_information_extensions=replace(extensions, extension=tuple(retained)))
            result = delegate(service_info, next_update_at)
            # Only successful, granted service definitions reach the registry.
            # A second unknown critical extension still rejects the whole entry.
            for takeover in takeovers:
                records.append({**takeover, 'serviceName': result.base_info.service_name,
                    'validFrom': result.base_info.valid_from.isoformat(),
                    'validUntil': result.base_info.valid_until.isoformat() if result.base_info.valid_until else None,
                    'certificateSha256': [hashlib.sha256(cert.dump()).hexdigest() for cert in result.base_info.provider_certs]})
                taken_over += 1
            return result
        return read

    for provider in parsed.trust_service_provider_list.trust_service_provider:
        services = upstream._required(provider.tspservices, 'TSP services').tspservice
        for service_type, delegate, register in (
            (CA_QC_URI, upstream._interpret_historical_service_info_for_ca, registry.register_ca),
            (QTST_URI, upstream._interpret_historical_service_info_for_qtst, registry.register_tst),
        ):
            definitions = upstream._interpret_service_info_for_tsps(services, ServiceTypeIdentifier(service_type), interpret(delegate))
            while True:
                try:
                    register(next(definitions))
                except StopIteration as end:
                    errors.extend(end.value or [])
                    break
    registry._onekit_takeovers = records
    return errors, taken_over
