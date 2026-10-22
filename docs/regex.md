<!-- Copyright 2026 Mattia Piazzalunga -->
<!-- SPDX-License-Identifier: LicenseRef-PolyForm-Shield-1.0.0 -->
# Regex tester

```sh
onekit run dev-regex-test input.txt -o regex-results.json --options '{"pattern":"(?<word>\\w+)","flags":"g","enable_replacement":true,"replacement":"[$<word>]"}'
onekit doctor dev-regex-test
```

The JSON report includes the pattern, flags, match count, truncation status, exact matched text, start/end positions, numbered capture groups and named groups. Unmatched groups are null. Positions use UTF-16 code units, as JavaScript does, so astral Unicode characters occupy two units. Empty global matches advance correctly, including under the Unicode flag.

Set `enable_replacement` to true and supply `replacement` to preview replacements. Supported substitution tokens match JavaScript string replacement: `$$`, `$&`, `$1`–`$99`, `$<name>`, `$'` and the dollar-plus-backtick prefix token. Replacements never change the test input. When match results are truncated, replacement is withheld rather than presenting an incomplete result.
