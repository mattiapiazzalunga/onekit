# CLI localization

Languages: `en`, `it`, `fr`, `es`, `de`, `ru`, `zh` (Simplified Chinese).
Select one with `onekit --language it ...`, or `ONEKIT_LANGUAGE=it`.
The operating system locale is used when neither is set. Unsupported locales
use English. Command names, option keys, paths, format identifiers and machine
readable JSON contracts stay stable. Human help, status, warnings and known errors
are localized. External engine diagnostics retain their upstream text.

Every person or AI adding or changing a tool MUST update all seven presentation
catalogs in the same change. Names, help, descriptions, error messages, notices,
README and tool documentation must remain in a one-to-one correspondence.
Do not fill missing translations with English as a shortcut. Keep placeholders,
code examples, URLs and legally required verbatim notices intact. Review the
meaning and terminology in context.

Catalogs: `src/onekit/locales/{language}.json`. Presentation code: `i18n.py`.
English messages are normalized keys; processing algorithms remain independent.
The independent language registry is `src/onekit/locales/languages.json`, including
operating-system aliases. Add a registry entry and a complete catalog together.
Reviewed terminology is recorded in `scripts/localization-reviewed.json`; apply it
with `python scripts/apply_localization_review.py src/onekit/locales` before auditing.

1. Edit the English message or documentation in its original file.
2. Run `python scripts/localization_inventory.py`.
3. Update every other language catalog and remove obsolete entries. The authoring
   scripts can draft translations; generated text requires review.
4. Run `python scripts/audit_localization.py` and `pytest tests/test_i18n.py`.
5. Run `python scripts/localize_docs.py` to regenerate localized Markdown under
   `docs/locales/{language}/`, retaining the original relative document structure.

The offline authoring command takes a local Argos model directory followed by
catalog directories. CTranslate2 and SentencePiece are authoring dependencies,
not CLI runtime requirements. No translation service is contacted by the CLI.

The CLI's translations and documentation are maintained independently of any
website that embeds the processing library. Only public usage links belong here.
