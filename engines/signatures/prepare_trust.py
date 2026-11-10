"""Prepare public-only inputs; DSS must authenticate every list before compiling."""
import argparse
import datetime
import hashlib
from pathlib import Path

from pyhanko.sign.validation.qualified.eutl_parse import latest_known_lotl_tlso_certs

from onekit.signature_evidence import LOTL_URL
from onekit.tools.signature_validation import authenticated_registry, default_evidence, evidence_files

parser = argparse.ArgumentParser()
parser.add_argument('destination', type=Path)
parser.add_argument('--historical-uk', type=Path)
args = parser.parse_args()
destination = args.destination
destination.mkdir(parents=True, exist_ok=True)
data = default_evidence()
files, manifest = evidence_files(data)
moment = datetime.datetime.now(datetime.UTC)
_, status = authenticated_registry(files, manifest, moment)
rows = [(LOTL_URL, manifest['lotl'], None)] + [
    (item['url'], item['path'], item.get('territory', Path(item['path']).stem)) for item in manifest['trusted_lists']
]
if args.historical_uk is not None:
    if args.historical_uk.stat().st_size > 32 * 1024 * 1024:
        raise ValueError('historical_list_size')
    files['historical-uk.xml'] = args.historical_uk.read_bytes()
    rows.append(('https://ec.europa.eu/tools/lotl/Final_EU_TSL-UKsigned.xml', 'historical-uk.xml', 'UK'))
values = {'lotl': LOTL_URL, 'count': str(len(rows)), 'archiveSha256': hashlib.sha256(data).hexdigest(),
          'validFrom': moment.isoformat(), 'expires': status['expires']}
for index, (url, name, territory) in enumerate(rows):
    target = f'list-{index}.xml'
    (destination / target).write_bytes(files[name])
    values[f'url.{index}'] = url
    values[f'path.{index}'] = target
    if territory is not None:
        values[f'territory.{index}'] = territory
pins = list(latest_known_lotl_tlso_certs())
for index, certificate in enumerate(pins):
    (destination / f'pin-{index}.der').write_bytes(certificate.dump())
values['pins'] = str(len(pins))


def escape(value):
    return value.replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r')


(destination / 'source.properties').write_text(''.join(f'{key}={escape(value)}\n' for key, value in values.items()), encoding='utf-8')
