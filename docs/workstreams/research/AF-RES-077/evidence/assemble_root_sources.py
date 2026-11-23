"""Normalize actually read primary-source sections; no network or outcome inference."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# One work may have several receipts. Editions/sections are never extra works.
DEFINITIONS = [
    ('kdenlive_proxy', 'KDENLIVE-MANUAL', 'Kdenlive documentation contributors', 'same_domain', '26.08; displayed documentation revision 8a74558', 'Proxy Settings; #proxy-settings',
     'Editing substitutes low-resolution proxy clips, while rendering can use originals. This establishes media roles and a storage choice.',
     'A later documentation edition, not evidence of Shotcut 20.09.13 behavior or collision-safe relinking. Only the main section was read; navigation is not substantive evidence.'),
    ('kdenlive_camera', 'KDENLIVE-MANUAL', 'Kdenlive documentation contributors', 'same_domain', '26.08; displayed documentation revision 8a74558', 'Using Camera Proxy Clips; #using-camera-proxy-clips',
     'Relative folders, prefixes and suffixes encode bidirectional camera-proxy naming relationships; the six-field configuration is a naming convention.',
     'Naming correspondence does not authenticate source bytes. Same handbook lineage as Proxy Settings; copied Kdenlive hash code in Shotcut is not independent corroboration.'),
    ('darktable_sidecar', 'DARKTABLE-MANUAL', 'darktable manual contributors', 'provided_external', '4.8 official release branch at 9d2c663bbe2a3390fd3750fdce780025933a5045', 'overview/sidecar-files/sidecar.md; entire main text',
     'Each edit version gets its own sidecar; imported database state takes precedence, with an optional startup conflict check and explicit overwrite/update choice.',
     'This does not establish a persistent physical-image identity, proxy/original inverse, content digest, transaction protocol, or safety after shared input replacement.'),
    ('darktable_duplicates', 'DARKTABLE-MANUAL', 'darktable manual contributors', 'provided_external', '4.8 at 9d2c663bbe2a3390fd3750fdce780025933a5045', 'module-reference/utility-modules/darkroom/duplicate-manager.md; entire main text',
     'Multiple versions share the underlying image but keep independent edit histories in independent sidecars.',
     'Shared source bytes are a premise. Independent metadata cannot preserve all versions if those source bytes are changed. Same work as the sidecar section.'),
    ('musescore3_book', 'MUSESCORE3-HANDBOOK', 'MuseScore handbook contributors', 'same_domain', 'live MuseScore 3 printable handbook retrieved 2026-11-23; includes later 3.x material', 'Parts: overview and Save Parts; Undo and redo; bounded chapter excerpts',
     'Parts are viewing profiles of linked musical data, can have independent presentation, and are saved with the score. Undo/redo is documented as an interaction.',
     'This is not a frozen 3.0.1 manual. No durable undo across sessions or constructor-level selection policy is warranted. The entire 687052-character book was fetched, but only the named sections were directly read.'),
    ('TEI48', 'TEI-P5-TC', 'TEI Consortium', 'provided_external', 'P5 4.8.0, 2024-09-02; revision 4e6e41b0b', 'Critical Apparatus §13.1.2 Readings #TCAPLR; §13.1.4.3 Witness Information #TCAPWL; fragmentary-witness caveats',
     'Readings explicitly identify witnesses; witness lists and the witnesses active at a location determine legitimate attribution/complement operations. Explicit enumeration can prevent mistaken omission.',
     'Witness identity and textual attribution are not command history, prior pitch values, or inverses. The live supplied URL showed 4.12.0, so the archived 4.8.0 edition was used. Only selected sections, not the whole chapter, were read.'),
    ('epub33_2023', 'EPUB33', 'W3C EPUB 3 Working Group', 'same_domain', 'W3C Recommendation 2023-05-25', '§4.2.5 URLs in the OCF abstract container #sec-container-iri; §6.1.2 XHTML requirements #sec-xhtml-req',
     'Container content URLs and the referring document base govern relative URL parsing. XHTML inherits HTML semantics subject to EPUB constraints.',
     'Does not prescribe Sigil split implementation or recovery. A content digest alone is not an element identity. The supplied comparison is retrospective; only these sections were read from the large specification.'),
    ('ocfl11', 'OCFL11', 'OCFL editors and contributors', 'provided_external', '1.1, published 2022-10-07, displayed update 2024-11-07', '§3.5.2 #manifest; §3.5.3.1 #version; object-at-rest scope and path constraints',
     'Manifest maps content digests to physical paths; version state maps digests to logical paths, allowing multiple paths for identical content while constraining each logical path. The specification describes objects at rest.',
     'A split changes chapter bytes. Digest equality cannot identify the intended duplicate anchor or supply an inverse, atomic write order or crash recovery. Inventory path restrictions must not be copied blindly into relative href syntax.'),
    ('rfc3986', 'RFC3986', 'Tim Berners-Lee; Roy Fielding; Larry Masinter', 'counterexample', 'RFC 3986, January 2005', '§3.5 Fragment; §5.2.1–5.2.4 Relative Resolution',
     'A fragment identifies a secondary resource relative to a primary resource and media-type semantics. Relative references resolve against a base; fragment spelling alone is insufficient across documents.',
     'Syntax resolution does not recover author intent, validate fragment existence, or choose between duplicate IDs. This is a same-domain alternative to attributing document scope uniquely to OCFL.'),
    ('xml10', 'XML10', 'W3C XML Working Group', 'counterexample', 'XML 1.0 Fifth Edition, 2008-11-26', '§3.3.1 Attribute Types; Validity constraints ID and IDREF',
     'Values of an attribute declared as type ID must be unique within one XML document; IDREF addresses that document scope.',
     'This is a typed-ID validity rule, not proof that any arbitrary attribute named id is validated as type ID. The Sigil user guide independently states same-file ID uniqueness for this application.'),
    ('qt5undo', 'QT5-UNDO-DOC', 'The Qt Company and Qt documentation contributors', 'counterexample', 'Qt 5.15 archived documentation', 'Overview of Qt Undo Framework; command pattern, undo stacks, macros, undo groups; main page',
     'Command objects implement operations and undo; stacks store and traverse commands. Groups choose an active stack; macros/compression group commands.',
     'This framework overview does not prove MuseScore uses QUndoStack or persists history. It demonstrates an alternative operational requirement: inverse-bearing records, absent from TEI witness attribution.'),
    ('bagit', 'RFC8493-BAGIT', 'John Kunze et al.; BagIt authors', 'counterexample', 'RFC 8493, October 2018, Informational', 'Introduction and §3 Complete and Valid Bags',
     'Complete bags contain all required/listed files; valid bags additionally verify the manifest checksums. Payloads are opaque to this packaging protocol.',
     'A checksum-valid package can contain semantically wrong internal links. File completeness/fixity is not referential correctness, and BagIt is not a target GUI test.'),
    ('gitobjects', 'PROGIT-OBJECTS', 'Scott Chacon; Ben Straub; Pro Git contributors', 'counterexample', 'Pro Git 2nd edition online snapshot retrieved 2026-11-23', '§10.2 Git Objects; blobs and Tree Objects',
     'Blobs identify stored content; trees separately associate names, modes and blob/subtree identifiers. A filename is not inside a blob.',
     'The book page is a live edition pinned here by retrieval hash, not a target-era artifact. A byte-identical file rename is useful analogy, but splitting and href rewriting change bytes and need additional provenance.'),
    ('prov_dm', 'PROV-DM', 'Luc Moreau; Paolo Missier; W3C Provenance Working Group', 'counterexample', 'W3C Recommendation 2013-04-30', '§2.1.2 Derivation; §2.3 Revision; §5.2.1 Derivation',
     'Derivation can relate entities with optional activity, generation and usage identifiers; more detailed provenance describes a derivation path.',
     'A derivation assertion does not encode the operation or its executable inverse. Absence of prior values cannot be repaired by adding provenance vocabulary.'),
    ('mltxml', 'MLT-XML-DOC', 'MLT project authors', 'target_support', 'official live document snapshot; target-era equivalence unverified', 'MLT XML: Preamble, Introduction, Rules, Basic Producers and Playlists',
     'Producer IDs are separate from resource properties; playlist entries reference producers with in/out points. Shared producer identity can fan out to multiple edits.',
     'Not a pinned 2020 MLT dependency release and not an executed XML-reader receipt. The fetched bytes are hashed, but historical interface equivalence remains unverified.'),
    ('shotcut_proxy_doc', 'SHOTCUT-PROXY-GUIDE', 'Shotcut official forum account shotcut; project documentation', 'target_support', 'page first dated 2020-06-05; current edited snapshot retrieved 2026-11-23', 'Settings > Proxy Editing: introduction, use, storage, limitations; main page',
     'Proxy switching reopens a project; opening can reuse available proxies without generating them. The guide distinguishes generation/activation and notes that proxies can conceal original seeking problems.',
     'Current page revision is not established as its 2020 first edition. The guide does not prove the #910 cause, correct relinking, or run any frozen case. PDF republications would be the same work.'),
    ('sigil_guide_splitting_and_merging', 'SIGIL-USER-GUIDE', 'Sigil user guide authors; repository snapshot by Doug Massay', 'target_support', 'd101fa2b5dc09ea0d2e1ac987d061c3338745710, 2019-06-25', 'Splitting and Merging; complete chapter',
     'Split At Cursor keeps the first part under the original filename and puts the remaining content in a new file. Multiple split markers and renaming are documented; users are advised to save before splitting/merging.',
     'Contemporary guide, not a proof that every link is correctly rewritten. It does not promise a crash-atomic multi-file operation or arbitrary folder movement.'),
    ('sigil_guide_links', 'SIGIL-USER-GUIDE', 'Sigil user guide authors', 'target_support', 'd101fa2b5dc09ea0d2e1ac987d061c3338745710', 'Links and IDs; complete chapter',
     'Same-file identical IDs are forbidden. The target picker lists files and IDs with current-file targets first, distinguishing document context from a bare fragment name.',
     'This same-domain source already supplies a key negative control. It does not reveal what the old split code actually does with malformed duplicate IDs.'),
    ('sigil_guide_opening_and_saving_files', 'SIGIL-USER-GUIDE', 'Sigil user guide authors', 'target_support', 'd101fa2b5dc09ea0d2e1ac987d061c3338745710', 'Opening and Saving Files; complete chapter',
     'EPUB members are organized into standard folders on opening; saving packages the book and may clean source according to preferences. Separate validation is recommended.',
     'A save action or valid ZIP does not establish referential correctness. This raises an expressibility problem for the frozen arbitrary nested-folder move in SG-E; do not silently substitute a modern version.'),
]

def main():
    receipts = {x['id']: x for x in map(json.loads, (ROOT/'reading/receipts.jsonl').read_text().splitlines())}
    rows = []
    seen = set()
    for key,work,author,purpose,version,section,confirmed,limit in DEFINITIONS:
        r = receipts[key]
        assert r['status'] == 200
        row = dict(id='ROOT-'+key.upper().replace('_','-'), author_lineage=author,
                   independent_work_id=work, purpose=purpose, url=r['url'],
                   version_or_sha=version, retrieved_utc=r['utc'], utc_basis='per-request start',
                   section_or_symbol=section, confirmed=[confirmed], unverified=[limit],
                   access_failures=[], local_receipt='reading/receipts.jsonl#'+key,
                   direct_read=True, read_scope='only named sections; retrieval is not whole-work reading',
                   core20_eligible=True, independent_work_contribution=int(work not in seen),
                   raw_sha256=r['sha256'], downloaded_bytes=r['bytes'], actor='root',
                   phase='compiler/supplemental; never additional reader exposure')
        if key.startswith('darktable_'):
            row['access_failures'] = ['Requested 4.8 landing page returned HTTP403; one web sidecar result rewrote to current 5.6; duplicate URL returned404. Recovered the same work from its official immutable 4.8 source commit.']
        if key == 'musescore3_book':
            row['access_failures'] = ['Part-page route redirected to MuseScore4; exact MuseScore3 printable book recovered.']
        if key == 'qt5undo':
            row['access_failures'] = ['Web open failed; direct public HTTPS retrieval succeeded.']
        seen.add(work);rows.append(row)
    (ROOT/'evidence/root-sources.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
    (ROOT/'reading/NOTES.jsonl').write_text(''.join(json.dumps({k:v for k,v in x.items() if k not in ('independent_work_contribution',)},ensure_ascii=False)+'\n' for x in rows))
    print(json.dumps({'direct_read_receipts':len(rows),'distinct_original_works':len(seen)}))

if __name__ == '__main__':
    main()
