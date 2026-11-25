"""Read the local GoTo outlines and link annotations with pypdf in strict mode."""
import json
import sys

from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, NullObject


def reference(raw):
    if isinstance(raw, IndirectObject):
        return [raw.idnum, raw.generation]
    return None


def scalar(value):
    if isinstance(value, NullObject):
        return None
    if isinstance(value, str):
        return str(value)
    return float(value)


def inspect(filename):
    reader = PdfReader(filename, strict=True)
    catalog = reader.root_object
    pages = list(reader.pages)
    page_indices = {tuple(reference(page.indirect_reference)): i + 1
                    for i, page in enumerate(pages)}
    named = reader.named_destinations

    def target(node):
        route = "/Dest"
        if "/A" in node:
            action = node["/A"]
            if action["/S"] != "/GoTo":
                raise ValueError("Expected a local GoTo action")
            dest = action["/D"]
            route = "/A/GoTo/D"
        else:
            dest = node.get("/Dest")
            if dest is not None:
                dest = dest.get_object()
        if dest is None:
            raise ValueError("Expected a PDF destination")
        if isinstance(dest, DictionaryObject):
            dest = dest["/D"]
        name = str(dest) if isinstance(dest, str) else None
        array = named[name].dest_array if name is not None else dest
        if not isinstance(array, ArrayObject):
            raise ValueError(f"Unexpected destination: {array!r}")
        ref = reference(array[0])
        if ref is None:
            raise ValueError("Expected an indirect destination page")
        return {"route": route, "name": name, "page_object": ref,
                "page": page_indices[tuple(ref)], "mode": str(array[1]),
                "args": [scalar(arg) for arg in array[2:]]}

    nodes = []
    visited = set()

    def walk(first, ancestors, parent):
        current = first
        while current is not None:
            ref = reference(current)
            if ref is None or tuple(ref) in visited:
                raise ValueError("Outline node is direct or repeated")
            visited.add(tuple(ref))
            node = current.get_object()
            raw_parent = reference(node.raw_get("/Parent"))
            if raw_parent != parent:
                raise ValueError("Outline Parent does not match First/Next walk")
            title = node["/Title"]
            if not isinstance(title, str):
                raise ValueError("The outline title did not decode as text")
            nodes.append({"title": str(title), "parents": ancestors, "object": ref,
                          "parent_object": raw_parent, "count": node.get("/Count"),
                          "target": target(node)})
            if "/First" in node:
                walk(node.raw_get("/First"), ancestors + [str(title)], ref)
            current = node.raw_get("/Next") if "/Next" in node else None

    root_ref = None
    root_state = "absent"
    if "/Outlines" in catalog:
        root_ref = catalog.raw_get("/Outlines")
        root = root_ref.get_object()
        if not isinstance(root, DictionaryObject):
            raise ValueError("Outlines entry is not a dictionary")
        has_first = "/First" in root
        if has_first != ("/Last" in root):
            raise ValueError("Outline root has an incomplete First/Last pair")
        root_state = "populated" if has_first else "empty_dictionary"
        if has_first:
            walk(root.raw_get("/First"), [], reference(root_ref))
        elif root.get("/Count", 0) != 0:
            raise ValueError("Empty outline root has a nonzero Count")

    page_details = []
    for index, page in enumerate(pages, 1):
        annotations = []
        for annotation in page.get("/Annots", ()):
            node = annotation.get_object()
            if node["/Subtype"] == "/Link":
                annotations.append({"rect_pdf_pt": [float(x) for x in node["/Rect"]],
                                    "target": target(node)})
        page_details.append({"page": index, "object": reference(page.indirect_reference),
                             "media_box": [float(x) for x in page.mediabox],
                             "crop_box": [float(x) for x in page.cropbox],
                             "rotate": page.rotation, "links": annotations})
    metadata = {str(key): str(value) for key, value in (reader.metadata or {}).items()}
    return {"pdf_header": reader.pdf_header, "metadata": metadata,
            "pdf_ids_hex": [item.original_bytes.hex() for item in reader.trailer.get("/ID", ())],
            "page_mode": str(catalog.get("/PageMode", "")), "outline_root_state": root_state,
            "outline_root_object": reference(root_ref), "outline": nodes, "pages": page_details}


if __name__ == "__main__":
    print(json.dumps(inspect(sys.argv[1]), indent=2, ensure_ascii=False))
