# ggplot2 stage 1 — old frame frozen

Old source v3.4.0 `63125db184b6e7d5516007574b5d15acbfd8f470` was deployed as gh-pages `57852124c86f770dd443fcf5064d30ea320a4731`. The official publication list in 2022-11-06–10 confirms this is the earlier of two deployments on release day and the one naming the exact release source. Old pages display Released version 3.4.0. New source v3.5.0 `a6f1a7c845bfe056ef952b839d2fd65b888ab5cd` and publication `392175bbb00b04025aa5d17a0c18b3896adeb40f` are metadata pins only at this stage. New body, image, tree and individual CI logs remain unopened.

`frame.csv` records first 40 eligible pages from the complete old stable reference tree, plus every earlier skipped path. Examples are the first explanatory images inside the `div.section.level2` containing `h2#ref-examples`; logos/badges excluded. `aes.html` and `aes_colour_fill_alpha.html` are inherited AF-RES-098 main logical examples and are excluded. Sections use relative `reference/page.html#ref-examples` strings for hashing.

General winners are **GG-G1 expansion** (bar-chart upper/lower expansion example) and **GG-G2 geom_count** (ordinary cty/hwy point plot serving as baseline for the later count-size examples). Selecting the first image does not select the page's most distinctive later figure.

The corresponding body source is exact same-name `man/<page>.Rd`. All 40 such paths exist in the old tag tree. The old general sources were opened directly and their examples agree with the rendered code. R author-source links are separately retained; they can be plural and their arbitrary first link is not the source-comparison rule.

Release metadata supplies official source archive URLs but contains no attached binary assets. Official source-distribution inspection will be completed after prediction sealing; this will not substitute source archives for published HTML. Fixed raw HTML represents the official preserved file; it is not advertised as a rendered historical website.

Only general bodies and their directly read sources are currently counted; automated old-frame scans do not add to the body minimum. Full HTML cache is ignored; committed receipts preserve URL/UTC/status/MIME/size/digest, and frame contains short attributes and source locations.
