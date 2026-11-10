# Copyright 2026 Mattia Piazzalunga
# SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0
import datetime
from typing import ClassVar

from pyhanko_certvalidator.policy_decl import AlgorithmUsageConstraint, AlgorithmUsagePolicy


class DSSAlgorithmPolicy(AlgorithmUsagePolicy):
    # Policy parameter facts from DSS 6.5.1's default constraint.xml, commit
    # 98ab6c136fc90bfca78352b4e673e2eae72b7d5a. Independent implementation;
    # no Java runtime/code is embedded. Algorithm verification and policy
    # acceptability are separate: e.g. a valid EdDSA signature is not automatically
    # acceptable under DSS's default ETSI/SOGIS policy.
    digest_expiry: ClassVar[dict[str, str | None]] = {'md5': '2004-08-01', 'sha1': '2012-08-01', 'sha224': '2029-01-01',
                     'sha256': None, 'sha384': None, 'sha512': None, 'sha3_256': None,
                     'sha3_384': None, 'sha3_512': None, 'ripemd160': '2014-08-01', 'whirlpool': '2020-12-01'}
    key_expiry: ClassVar[dict[str, list[tuple[int, str | None]]]] = {
        'rsassa_pkcs1v15': [(786, '2010-08-01'), (1024, '2019-10-01'), (1536, '2019-10-01'), (1900, '2027-01-01'), (3000, '2035-01-01')],
        'rsassa_pss': [(786, '2010-08-01'), (1024, '2019-10-01'), (1536, '2019-10-01'), (1900, '2027-01-01'), (3000, None)],
        'dsa': [(1024, '2015-12-01'), (1900, '2027-01-01'), (3000, None)],
        'ecdsa': [(160, '2012-08-01'), (163, '2012-08-01'), (224, '2021-10-01'), (256, None)],
    }

    @staticmethod
    def _until(date, moment):
        cutoff = datetime.datetime.fromisoformat(date).replace(tzinfo=datetime.UTC) if date else None
        return AlgorithmUsageConstraint(allowed=cutoff is None or moment is not None and moment < cutoff,
            not_allowed_after=cutoff, failure_reason='dss_6_5_1_algorithm_policy' if cutoff else None)

    def digest_algorithm_allowed(self, algo, moment):
        name = algo['algorithm'].native
        if name not in self.digest_expiry:
            return AlgorithmUsageConstraint(False, failure_reason='dss_6_5_1_algorithm_policy')
        return self._until(self.digest_expiry[name], moment)

    def signature_algorithm_allowed(self, algo, moment, public_key):
        try:
            name = algo.signature_algo
        except ValueError:
            name = algo['algorithm'].native
        if name not in self.key_expiry:
            return AlgorithmUsageConstraint(False, failure_reason='dss_6_5_1_algorithm_policy')
        if public_key is not None:
            applicable = [date for size, date in self.key_expiry[name] if public_key.bit_size >= size]
            if not applicable:
                return AlgorithmUsageConstraint(False, failure_reason='dss_6_5_1_algorithm_policy')
            key_allowed = self._until(applicable[-1], moment)
            if not key_allowed:
                return key_allowed
        try:
            digest = algo.hash_algo
        except ValueError:
            digest = None
        if digest is not None:
            from asn1crypto import algos
            return self.digest_algorithm_allowed(algos.DigestAlgorithm({'algorithm': digest}), moment)
        return AlgorithmUsageConstraint(True)
