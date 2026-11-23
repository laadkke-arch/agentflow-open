# React Spring component release metadata

Reader: `/root/react_release`. Read interval: 2026-11-23T05:04:43Z–05:05:24Z. Exact per-request timestamps were not captured; the interval is deliberately retained instead of invented precision.

## Frozen component candidate

- Component: `@react-spring/core@10.0.3`.
- Official release: `v10.0.3`, stable, published **2025-09-18T14:40:58Z**.
- Annotated tag object: `abc0cd15a943440942aa7655dd6a4ca7bc543ac2`.
- Source commit: **`b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a`**.
- Tag creation: 2025-09-18T14:39:57Z.
- Cutoff: latest stable component release through 2025-12-31T23:59:59Z. The release list's next stable `v10.0.4` was published 2026-05-21T20:32:05Z and is excluded. `packages/core/package.json` explicitly identifies the selected component as version 10.0.3; the root is a private workspace and does not substitute for the component.
- Npm distribution byte-to-source mapping remains **미확인**. Registry metadata could not be opened with the web tool. GitHub official release, annotated tag, and component manifest mapping were verified.

## Declared environment

| Surface | Declared at the fixed source commit | Limit |
| --- | --- | --- |
| Core | React `^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0`; ESM import and CJS require exports | No Node minimum in this package manifest; not a browser compatibility test |
| Web target | Same React and react-dom ranges; core `~10.0.3` | Host manifest only |
| Native target | Same React range; react-native `>=0.78`; core `~10.0.3` | No Android/iOS minimum OS claim |
| Three target | `@react-three/fiber >=6.0`, `three >=0.126`, same React range | Supporting environment, not an additional implementation sample |

## Exposure disclosure

The first web search returned a long current release listing including 2026 change titles about settling precision, retargeting and cancellation. The reader therefore cannot later be counted as a wholly unexposed reader for those topics. No target-version implementation, SpringValue equations, unit-test assertion, measured output, physics original or issue outcome has been opened. Detailed future-release claims were not passed to the root reader. The metadata API response was parsed and only release date/tag/status fields were displayed; its release bodies were not displayed or read.

`sources.jsonl` contains the directly read metadata. R002–R009 belong to the same `react-spring-v10.0.3` lineage and count as one external work, with R002 the representative. `search-log.jsonl` records the search snippet and failed registry request, neither counted as direct external-work reading.

## Evidence URLs

- [Official releases metadata](https://api.github.com/repos/pmndrs/react-spring/releases?per_page=50)
- [Tag ref](https://api.github.com/repos/pmndrs/react-spring/git/ref/tags/v10.0.3)
- [Peeled annotated tag](https://api.github.com/repos/pmndrs/react-spring/git/tags/abc0cd15a943440942aa7655dd6a4ca7bc543ac2)
- [Fixed component manifest](https://github.com/pmndrs/react-spring/blob/b6fbb98101f2cf00a6668cffed6d1b4d0012ae3a/packages/core/package.json)

No implementation prediction, result, source formula or donor section is included in this metadata bundle.
