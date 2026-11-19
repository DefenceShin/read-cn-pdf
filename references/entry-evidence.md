# Entry boundaries and evidence

Use when a bounded PDF extraction will support rule data or an audit. These
lessons come from Court October and Carcass Front source reviews.

- Identify the document version/hash and physical page separately from its
  printed page. Preserve page markers in saved excerpts; a multi-page entry
  needs all supporting pages, not the chapter's first page by default.
- Check coverage before claiming whole-book review. A supplied scan may omit
  large printed-page ranges, and one physical PDF page may show a two-page
  spread. Record both printed pages and the relevant half/crop; do not convert
  between physical and printed pages with one assumed constant offset.
- Bound extraction by the named entry and the next actual peer heading. Titles
  can contain commas and wrap across lines. Do not end at a fixed character
  count or search the entire page for the first `Limit` or price.
- Follow a continuation only when it belongs to this entry. Stop at the next
  peer entry; do not append the next page unconditionally. Include referenced
  shared effects, base profiles, variant overrides, tables and footnotes with
  separate locators when needed.
- A short armoury list and a detailed entry can describe the same object.
  Resolve identity/version/context before combining them; list prices do not
  replace detailed mechanics. Never choose an excerpt because its price equals
  an application's current value.
- Render the relevant crop/page when a currency glyph, dash, column, strikeout,
  keyword or table association is uncertain. Plain text may retain the number
  but lose whether it means Ducats, Glory, a range or a limit. Blank extraction
  from a scan does not prove absence.
- Check OCR against the visible source for decisive negations, inequality
  words, numbers, units, dice modifiers, currencies and exception clauses.
  A matching Chinese translation is not independent confirmation of English
  OCR. Record a user resolution as a user resolution, not an official erratum.
- Keep complete clauses, exceptions and table rows in the saved evidence even
  when console output is bounded. A `--max-chars` preview is not automatically
  a complete source record. Read back the saved text with explicit UTF-8.

Historical failure examples: a flail's wrapped sentence lost FIRE/INNATE and a
currency exception; an action inherited another item's same-page Limit:1; two
pledge options omitted their shared base-size/movement subsection. Resolve
these by entry identity and visible source boundaries, not larger blind dumps.

Extraction proves what was read, not the correctness of its application model.
For source-to-data mapping, independent expectations and runtime validation,
use `implementing-source-backed-rules` when installed.
