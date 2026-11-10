import asyncio
import json

import pytest

from onekit import Artifact
from onekit.tools.signature_dss import parse_reports, run_original


def reports(indication='INDETERMINATE', intact='true', valid='true', found='true', matched='true'):
    return {
        'simple.xml': f'''<SimpleReport xmlns="http://dss.esig.europa.eu/validation/simple-report"
            ValidationTime="2026-10-30T00:00:00Z"><SignaturesCount>1</SignaturesCount>
            <Signature Id="S-1" SignatureFormat="CAdES-BASELINE-B"><Indication>{indication}</Indication>
            <SubIndication>NO_CERTIFICATE_CHAIN_FOUND</SubIndication><SignatureLevel>N/A</SignatureLevel>
            </Signature></SimpleReport>'''.encode(),
        'diagnostic.xml': f'''<DiagnosticData xmlns="http://dss.esig.europa.eu/validation/diagnostic">
            <Signatures><Signature Id="S-1"><SigningCertificate Certificate="C-1"/>
            <BasicSignature><SignatureIntact>{intact}</SignatureIntact><SignatureValid>{valid}</SignatureValid></BasicSignature>
            <DigestMatchers><DigestMatcher><DataFound>{found}</DataFound><DataIntact>{matched}</DataIntact>
            </DigestMatcher></DigestMatchers></Signature></Signatures></DiagnosticData>'''.encode(),
        'detailed.xml': b'<DetailedReport xmlns="http://dss.esig.europa.eu/validation/detailed-report"/>',
        'etsi.xml': b'<ValidationReport xmlns="http://uri.etsi.org/19102/v1.4.1#"/>',
    }


def test_mathematical_match_does_not_establish_trust_or_qualification():
    result = parse_reports(reports())
    assert result['verdict'] == 'cryptographic_match'
    assert result['validation']['indication'] == 'INDETERMINATE'
    row = result['validation']['signatures'][0]
    assert row['trusted'] is None and row['revoked'] is None
    assert row['qualification'] == {'dssLevel': 'N/A'}


@pytest.mark.parametrize('field', ['intact', 'valid', 'matched'])
def test_explicit_mathematical_failure_is_not_a_match(field):
    assert parse_reports(reports(**{field: 'false'}))['verdict'] == 'mismatch'


def test_missing_original_is_not_a_mathematical_match():
    result = parse_reports(reports(found='false'))
    assert result['verdict'] == 'not_checked'


def test_unknown_diagnostic_flags_cannot_be_coerced_to_true():
    with pytest.raises(ValueError, match='dss_report_boolean'):
        parse_reports(reports(valid='yes'))


def test_report_namespace_and_signature_count_are_checked():
    data = reports()
    data['simple.xml'] = data['simple.xml'].replace(b'<SignaturesCount>1', b'<SignaturesCount>2')
    with pytest.raises(ValueError, match='dss_signature_count'):
        parse_reports(data)
    data = reports()
    data['simple.xml'] = data['simple.xml'].replace(b'/simple-report', b'/another-report')
    with pytest.raises(ValueError, match='dss_report_schema'):
        parse_reports(data)


def test_dtds_and_entities_are_rejected():
    data = reports()
    data['simple.xml'] = b'<!DOCTYPE SimpleReport [<!ENTITY x "payload">]>' + data['simple.xml']
    with pytest.raises(ValueError, match='dss_report_doctype'):
        parse_reports(data)


def test_missing_reports_are_not_a_complete_validation():
    data = reports()
    del data['etsi.xml']
    with pytest.raises(ValueError, match='dss_reports'):
        parse_reports(data)


@pytest.mark.parametrize('name', ['detailed.xml', 'etsi.xml'])
def test_unrelated_xml_cannot_complete_an_original_dss_report_set(name):
    data = reports()
    data[name] = b'<Unrelated/>'
    with pytest.raises(ValueError, match='dss_report_schema'):
        parse_reports(data)


def test_original_dss_reports_are_preserved_in_the_downloaded_json():
    original = reports()

    async def runtime(request):
        assert request['document']['data'] == b'signed-data'
        return original

    result = asyncio.run(run_original([Artifact('signature.p7m', b'signed-data')], None, runtime))
    assert len(result.files) == 1
    exported = json.loads(result.files[0].data)
    assert 'dssReports' not in result.details
    assert all(exported['dssReports'][name].encode() == data for name, data in original.items())
