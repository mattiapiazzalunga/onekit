# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
"""Reports from a trusted local PDF validation engine, bound to exact bytes."""
import hashlib
import json
from datetime import datetime, timezone

from ..execution import current_context
from ..models import OneKitError, Result, output

PROFILES = ('1a', '1b', '2a', '2b', '2u', '3a', '3b', '3u', 'ua1')


def validate(file, options=None):
    profile = (options or {}).get('profile', 'ua1')
    if profile not in (*PROFILES, 'auto'):
        raise OneKitError('Choose a supported PDF/A or PDF/UA-1 profile.')
    validator = current_context().pdf_validator
    details = {'schema': 'onekit-pdf-conformance/v1', 'compliant': None,
               'machine_compliant': None, 'verdict': 'not_checked', 'profile': None if profile == 'auto' else profile,
               'standard': 'ISO 14289-1' if profile == 'ua1' else 'ISO 19005',
               'sha256': hashlib.sha256(file.data).hexdigest(),
               'checked_at': datetime.now(timezone.utc).isoformat(), 'reports': []}
    if validator is not None:
        envelope = validator(file, profile)
        if envelope.get('error_kind') in ('profile', 'safety_limit'):
            if envelope.get('sha256') != details['sha256']:
                raise OneKitError('The processing core failed its integrity check.')
            details.update(engine='page', engine_version=envelope['engine_version'],
                           reason='Some document features could not be checked. Compliance has not been established.')
            return Result([output(file, 'validation.json', json.dumps(details, indent=2))], details=details)
        raw = envelope['report']
        checked = raw.get('profile')
        if (envelope.get('sha256') != details['sha256'] or checked not in PROFILES
                or profile != 'auto' and checked != profile
                or type(raw.get('is_compliant')) is not bool
                or not isinstance(raw.get('failures'), list)
                or not isinstance(raw.get('rules'), dict)):
            raise OneKitError('The processing core failed its integrity check.')
        rules = raw['rules']
        if (any(type(rules.get(key)) is not int or rules[key] < 0 for key in ('total', 'passed', 'failed'))
                or rules['total'] < 1 or rules['passed'] + rules['failed'] != rules['total']
                or raw['is_compliant'] != (rules['failed'] == 0 and not raw['failures'])):
            raise OneKitError('The processing core failed its integrity check.')
        ua = checked == 'ua1'
        passed = raw['is_compliant']
        details.update(profile=checked, standard='ISO 14289-1' if ua else 'ISO 19005-' + checked[0],
                       engine='page', engine_version=envelope['engine_version'],
                       machine_compliant=passed, compliant=None if ua and passed else passed,
                       verdict='manual_review' if ua and passed else 'pass' if passed else 'fail',
                       rules=rules, raw_report=raw,
                       reports=[{'rule': f.get('rule_id', ''), 'message': f.get('message', ''),
                                 'where': f.get('context', ''), 'kind': 'failure'} for f in raw['failures']])
        if ua:
            details['requires_manual_review'] = True
            details['manual_checks'] = ['Reading order', 'Meaningful structure and headings',
                                       'Accurate alternative text', 'Language and content accuracy']
    else:
        details['reason'] = 'Some document features could not be checked. Compliance has not been established.'
    return Result([output(file, 'validation.json', json.dumps(details, indent=2))], details=details)


def run(tool, files, options):
    return validate(files[0], options)
