# AF-RES-033 donor collection notes

## Independence and ordering

The donor collectors received only the three source fields, the fixed issuer frame, the publication/version horizon, and collection rules. They did not receive or read recipient questions, designs, input bodies, rankings, or other research outputs. The provider section of `SCOPE.md` was read after the first protocol commit, `cf10073b65a84002a889d37a2436a19b8f43d412`.

The first broad directory-discovery search unexpectedly exposed substantive search excerpts before that commit. This is preserved in `donor_attempts.jsonl`; it is not described as an unexposed pilot. No recipient information had been supplied. These documents were not excluded merely because their search excerpts appeared.

Each issuer subsequently received the sealed, field-only site query once. The finite returned title/URL sets were saved before substantive candidate fetches. The lists are search-result frames, not complete official-site inventories. Titles were normalised to lower case and sorted, with URL as the tie-break. Eligibility was assessed in that order. Official directory-linked alternatives were used only after the initial candidates failed. Links that resolve another representation or current edition of the same work do not create additional documents.

This is a researcher-chosen closed frame of English-language public issuers. It does not estimate the prevalence of practices across all libraries, transport operators, statistical agencies, or jurisdictions.

## Source identities and substantive reading

The main metadata uses candidate/source IDs `L01`–`L06`, `T01`–`T06`, and `S01`–`S06`. Selected sources have `counted_minimum=true`. Substantively read but excluded originals also appear in the source records, with `counted_minimum=false` and a concrete exclusion reason. Search-only discoveries, empty/challenge responses, and failed fetches remain in the attempt and candidate records.

The ABS national-accounts manual is one original work. The initially discovered 2020–21 edition led through its official latest-release link to Edition 8. Its complete revision section is the selected text; chapters and editions are not counted as additional original documents. The ABS government-finance quality-framework section belongs to a different, excluded manual.

Before any recipient-body reading, the integration agent clarified that the transport field requires an explicit operating-service change: timetable, frequency, span, route-service configuration, or a suspension/change procedure. Construction clearance or stop-location-only works without such a rule are outside the field. This excluded SFMTA's street-work Blue Book on the observed contents of its transit section. The already frozen title order then led to the Short Range Transit Plan family. Its official directory-family version check identified the FY2022–23 narrative as the latest edition in that finite result set; the older plan was not silently treated as current. The selected narrative's complete operating body is retained.

Dates are taken from visible release, effective, approval, or modification information when available. Undated current HTML is allowed under the protocol but does not establish historical availability before capture. HTTP `Last-Modified` response values are not silently substituted for publication dates. A mutable URL and an edition-labelled URL are distinguished in the source records.

## Text and hash boundaries

Search input is the original operational body or a complete expressly relevant section of a larger work. The page title, site navigation, cookie controls, and footer are excluded. No favorable sentences are stitched together. Internal subheadings, lists, qualifications, and exceptions within the selected body remain in their original order.

For HTML, `collect_document.py` captures the exact HTTP bytes and extracts visible text with `lxml`. The extraction normalises whitespace and removes non-rendered control characters. Later boundary removal is described per source. The selected text is UTF-8 with LF newlines. The raw-byte SHA256, initial/default extraction SHA256, and final selected-body SHA256 refer to different representations and are reported separately.

Toronto's direct request returned an HTTP 202 challenge. The full official-page web-reader transcript supplied its readable policy body; the transcript and derived body are retained and hashed. The failed HTTP representation is not presented as the policy's raw HTML. Stats NZ embeds its policy in the original page's `pageViewData` JSON; its featured text and ordered content blocks were decoded from those original HTML bytes. The initial empty visible-DOM extraction and the encoding correction are disclosed in the attempts.

The capture cache contains the exact material used during this task. Current public URLs can change later. The public metadata and eventual term-frequency exports permit identification and score replay but do not independently preserve every original visual layout or guarantee that a future refetch returns identical text.

## Public-repository handling

Full source HTML, PDFs, extracted bodies, and full search-reader transcripts stay in the ignored `cache/` directory. No open-reproduction permission is asserted for this collection. Public source metadata has no verbatim body excerpts; bibliographic titles, URLs, dates, and section identifiers support verification. A source's public-government status is not used as a blanket claim that all of its website material can be republished.

`assemble_library_statistics.py` creates the library/statistics metadata from the captured bodies. The transit collector supplies parallel source, attempt, and candidate manifests. The final aggregated `corpus_draft.jsonl` and `donor_sources.jsonl` are intended for the integration agent to freeze before any recipient-body reading.
