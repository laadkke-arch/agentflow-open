# Reference comparison

See sources.json for exact URLs, check date and adoption reasons.

Python urllib.parse: selected component parser; validation is deliberately separate.
w3lib canonicalize_url: useful for generic crawler URLs but its query/fragment normalization is not our repository identity contract; deferred.
yarl.URL: a structured URL type; retained as a comparison, not a dependency.
GitHub REST repository reference: owner/repository parameters are case-insensitive; API verification is still needed for existence or renames.

No candidate is claimed universally superior. The workbench chooses a narrow offline contract because these acceptance tasks do not require crawling or HTTP.
