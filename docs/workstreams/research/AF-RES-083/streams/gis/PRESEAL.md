# G04 old guidance and A/B seal

Only old consumer content was read before this file. The root commit is the seal. Later content requires an explicit root signal.

Selected2/3: GeoPandas roundtrip (G04-1), GeoPandas schema selection (G04-2); G04-3 remains VACANT. Both selected records share one authored guide and one discovery lineage. Selected independent guide works1, consumer projects1. Arrow plain-table example is AUX-G04-A1 only, excluded for wrong target. Related-supplier flag applies to Arrow. None invokes GDAL Parquet.GEOARROW directly. A abstains2/2 real records because a single publisher-declared replacement for these literal references is absent; this is not an observed false-positive count. B keeps1, proposes preventive version/encoding scope for2; correction necessity is not yet established. The vacancy has no applied repair, so it is not scored.

## Fixed time boundary

GDAL3.9.0 release API published2024-05-10T14:03:47Z; May12 developer mailing-list followup quotes the May10 source release announcement. GeoPandas old0.14.4 / first1.0.0 / latest1.2.0. Arrow official release index dates old16.0.0 April20 and first16.1.0 May14; the16.1.0 tagger May9 predates actual formal publication and must not define old consumer edition. Latest26.0.1 November3,2026. QGIS-Documentation only two tags: manual_1.8_en (Jan25,2013) and pre-latex-removal (maintenance tag); version branches are not promoted to formal tags.

## Search and omissions

Full recursive old trees are untruncated. QGIS110 and GeoPandas60 authored-document paths were downloaded and searched:170 files, zero failed. Arrow231 eligible documentation/example paths were extracted from the exact16.0.0 archive (SHA256 in evidence); no consumer later content was acquired. Old-source regex included successor names retrospectively. Images, translations(.po), code outside docs/examples, C++ examples and R markdown are not all part of the primary extension set; Arrow .Rmd was included as an explicit extra but its names did not supply earlier eligible hits. Do not count bulk search-opened files as directly analyzed independent source works.

## Key contract distinction

GeoPandas old implementation writes WKB and rejects non-WKB metadata statically. Its own guide’s “any version” phrase is contextualized by1.0.0 and older schemas, not an explicit promise of future GeoArrow support. GN05’s silent GDAL3.8 geometry/CRS loss is therefore not transplanted to GeoPandas: this consumer would take a different validation path. GN04 is also a different caller/input, not a successful GeoPandas test. The excluded Arrow example has only primitive a/b/c columns and no spatial output requirement.

## Installed versions

GeoPandas declared lower bounds and CI requested pyarrow8.0.0 are not historical resolved builds. Its latest CI recipe leaves pyarrow unpinned. Arrow guide source tag16.0.0 identifies published code but not the environment a user installed or the exact documentation build. Historical redirect/arrival is unverified for all original external links.
