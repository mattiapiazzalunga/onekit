import datetime

import pytest
from lxml import etree

from onekit.tools.signature_trust import EXTRA, SK_SERVICE_ID, TSL, add_authenticated_services
from onekit.tools.signature_validation import authenticated_registry, default_evidence, evidence_files


@pytest.fixture(scope='module')
def italy():
    files, _ = evidence_files(default_evidence())
    return files['tl/IT.xml']


def one_service(xml):
    root = etree.fromstring(xml)
    takeover = next(root.iter(f'{{{EXTRA}}}TakenOverBy'))
    service = next(parent for parent in takeover.iterancestors() if parent.tag == f'{{{TSL}}}TSPService')
    provider = next(parent for parent in service.iterancestors() if parent.tag == f'{{{TSL}}}TrustServiceProvider')
    services = service.getparent()
    for item in list(services):
        if item is not service:
            services.remove(item)
    providers = provider.getparent()
    for item in list(providers):
        if item is not provider:
            providers.remove(item)
    # Retain one granted instance to isolate the critical-extension behaviour.
    information = service.find(f'{{{TSL}}}ServiceInformation')
    information.find(f'{{{TSL}}}ServiceStatus').text = 'http://uri.etsi.org/TrstSvc/TrustedList/Svcstatus/granted'
    history = service.find(f'{{{TSL}}}ServiceHistory')
    if history is not None:
        service.remove(history)
    return root, next(root.iter(f'{{{EXTRA}}}TakenOverBy'))


def parse(xml):
    from pyhanko.sign.validation.qualified.tsp import TSPRegistry
    registry = TSPRegistry()
    errors, count = add_authenticated_services(etree.tostring(xml, encoding='unicode'), registry)
    return registry, errors, count


def test_takeover_preserves_certificates_and_exposes_legal_metadata(italy):
    from pyhanko.sign.validation.qualified.eutl_parse import trust_list_to_registry_unsafe
    root, takeover = one_service(italy)
    registry, errors, count = parse(root)
    assert count == 1 and not errors
    record = registry._onekit_takeovers[0]
    assert record['territory'] == 'IT' and record['providerNames']
    assert record['informationUri'] == takeover[0].text
    # Removing descriptive takeover data yields the SAME granted anchors.
    takeover.getparent().remove(takeover)
    baseline, _ = trust_list_to_registry_unsafe(etree.tostring(root, encoding='unicode'))
    assert set(registry.known_certificate_authorities) == set(baseline.known_certificate_authorities)


@pytest.mark.parametrize('change', ['unknown-child', 'unknown-attribute', 'missing-uri', 'missing-name',
                                   'unknown-qualifier', 'wrong-namespace', 'mixed-text'])
def test_ununderstood_critical_takeovers_reject_the_service(italy, change):
    root, takeover = one_service(italy)
    takeover.getparent().set('Critical', 'true')
    if change == 'unknown-child':
        etree.SubElement(takeover, '{urn:unknown}Policy').text = 'trust-everyone'
    elif change == 'unknown-attribute':
        takeover.set('transferTrust', 'true')
    elif change == 'missing-uri':
        takeover.remove(takeover[0])
    elif change == 'missing-name':
        takeover[1].clear()
    elif change == 'unknown-qualifier':
        etree.SubElement(etree.SubElement(takeover, f'{{{EXTRA}}}OtherQualifier'), '{urn:unknown}Rule')
    elif change == 'wrong-namespace':
        takeover[0].tag = '{urn:lookalike}URI'
    else:
        takeover.text = 'replace-trust-anchors'
    registry, errors, count = parse(root)
    assert errors and count == 0
    assert not list(registry.known_certificate_authorities)


def test_supported_national_service_reference_is_metadata_only(italy):
    root, takeover = one_service(italy)
    etree.SubElement(etree.SubElement(takeover, f'{{{EXTRA}}}OtherQualifier'), SK_SERVICE_ID).text = 'TLIIT-17'
    registry, errors, count = parse(root)
    assert count == 1 and not errors
    assert registry._onekit_takeovers[0]['serviceReferences'] == ['TLIIT-17']


def test_unknown_critical_extension_alongside_takeover_is_not_bypassed(italy):
    root, takeover = one_service(italy)
    extension = etree.SubElement(takeover.getparent().getparent(), f'{{{TSL}}}Extension', Critical='true')
    etree.SubElement(extension, '{urn:unknown}TrustOverride')
    registry, errors, count = parse(root)
    assert errors and count == 0
    assert not list(registry.known_certificate_authorities)


def test_full_signed_snapshot_has_no_skipped_supported_service_histories():
    files, manifest = evidence_files(default_evidence())
    registry, status = authenticated_registry(files, manifest, datetime.datetime(2026, 10, 29, 12, tzinfo=datetime.UTC))
    assert status['skippedServices'] == 0
    assert status['supportedTakeovers'] >= 252
    assert len(list(registry.known_certificate_authorities)) >= 889
