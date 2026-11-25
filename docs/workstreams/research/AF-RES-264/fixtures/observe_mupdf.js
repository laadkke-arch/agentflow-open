// MuPDF's own parser and name resolver. MuJS in mutool 1.25.1 runs this file.
var document = Document.openDocument(scriptArgs[0]);
var rows = [];
function walk(items, parents) {
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var dest = document.resolveLinkDestination(item.uri);
        if (dest.page < 0 || dest.page >= document.countPages()) {
            throw Error("Unresolved outline target: " + item.uri);
        }
        rows.push({
            title: item.title,
            parents: parents,
            uri: item.uri,
            resolved: dest,
            page_bounds: document.loadPage(dest.page).getBounds()
        });
        if (item.down) walk(item.down, parents.concat([item.title]));
    }
}
walk(document.loadOutline(), []);
print(JSON.stringify({ pages: document.countPages(), outline: rows }, null, 2));
