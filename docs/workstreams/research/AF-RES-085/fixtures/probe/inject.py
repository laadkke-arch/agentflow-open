#!/usr/bin/env python3
"""Insert read-only probes at checked source anchors on the pinned tree."""
import argparse
import shutil
from pathlib import Path


def replace(contents, old, new):
    count = contents.count(old)
    if count != 1:
        raise ValueError(f"expected one anchor, got {count}: {old[:120]}")
    return contents.replace(old, new)


def instrument(root, name, changes, include='#include "af085_model.h"'):
    path = root / name
    contents = path.read_text(encoding="utf-8")
    head, sep, tail = contents.partition("#include")
    if not sep or include in contents:
        raise ValueError(f"unexpected include layout in {name}")
    contents = head + include + "\n" + sep + tail
    for anchor, edited in changes:
        contents = replace(contents, anchor, edited)
    path.write_text(contents, encoding="utf-8")


def excerpt(root):
    instrument(root, "libmscore/excerpt.cpp", [
        ("Score* score        = excerpt->partScore();",
         "Score* score        = excerpt->partScore();\n      Af085::ObservePart af085Part(oscore, score);"),
        ("cloneStaves(oscore, score, srcStaves, excerpt->tracks());",
         "cloneStaves(oscore, score, srcStaves, excerpt->tracks());\n"
         '      Af085::snapshot("excerpt_cloned", score);'),
        ("score->setLayoutAll();\n      score->doLayout();",
         "score->setLayoutAll();\n      score->doLayout();\n"
         '      Af085::partStage() = "after_final_layout";\n'
         '      Af085::snapshot("excerpt_before_cleanup", score);'),
        ("\n      }\n\n//---------------------------------------------------------\n//   deleteExcerpt",
         '\n      Af085::snapshot("excerpt_return", score);\n      }\n\n'
         "//---------------------------------------------------------\n//   deleteExcerpt"),
    ])


def common(root):
    here = Path(__file__).parent
    for name, path in (("model.h", "libmscore/af085_model.h"), ("ui.h", "mscore/af085_ui.h")):
        shutil.copyfile(here / name, root / path)

    instrument(root, "libmscore/cmd.cpp", [
        ("void Score::cmdExplode()\n      {", 'void Score::cmdExplode()\n      {\n      Af085::snapshot("explode_enter", this);'),
        ("// select exploded region\n      deselectAll();",
         '// select exploded region\n      Af085::snapshot("explode_before_reselect", this);\n      deselectAll();'),
        ("select(endMeasure, SelectType::RANGE, lastStaff - 1);\n      }",
         'select(endMeasure, SelectType::RANGE, lastStaff - 1);\n      Af085::snapshot("explode_reselected", this);\n      }'),
        ("void Score::cmdToggleVisible()\n      {",
         'void Score::cmdToggleVisible()\n      {\n      Af085::snapshot("toggle_visible_enter", this);'),
        ("if (cmd == c.name) {\n                  startCmd();\n                  c.cmd();\n                  endCmd();",
         'if (cmd == c.name) {\n                  const bool af085Command = cmd == "explode" || cmd == "pad-note-2" || cmd == "toggle-visible";\n'
         '                  if (af085Command && Af085::enabled())\n'
         '                        Af085::record("score_action", {{"action", cmd}, {"score_id", Af085::identity(this)}});\n'
         "                  startCmd();\n                  c.cmd();\n                  endCmd();\n"
         '                  if (af085Command)\n                        Af085::snapshot("score_action_ended", this);'),
    ])
    instrument(root, "libmscore/edit.cpp", [
        ("bool link, bool spanner)\n      {\n      Fraction start = sf->tick();",
         'bool link, bool spanner)\n      {\n'
         '      if (Af085::enabled())\n'
         '            Af085::record("cloneVoice_call", {{"source_track", strack}, {"destination_track", dtrack},\n'
         '                {"start_tick", sf->tick().ticks()}, {"end_tick", lTick.ticks()}, {"link", link}, {"spanner", spanner}});\n'
         "      Fraction start = sf->tick();"),
        ("undoAddCR(toChordRest(ne), dm, oseg->tick());\n                              }\n                        }",
         "undoAddCR(toChordRest(ne), dm, oseg->tick());\n                              }\n"
         "                        Af085::pairedInsertion(oe, ne, oseg->tick().ticks());\n                        }"),
    ])
    instrument(root, "libmscore/paste.cpp", [
        ("bool Score::pasteStaff(XmlReader& e, Segment* dst, int dstStaff)\n      {",
         'bool Score::pasteStaff(XmlReader& e, Segment* dst, int dstStaff)\n      {\n'
         '      if (Af085::enabled())\n'
         '            Af085::record("pasteStaff_call", {{"staff", dstStaff}, {"tick", dst->tick().ticks()}, {"paste_mode", e.pasteMode()}});'),
        ("pasteChordRest(cr, tick, e.transpose());\n                                    }",
         'pasteChordRest(cr, tick, e.transpose());\n'
         '                                    Af085::snapshot("pasteStaff_insert", this);\n                                    }'),
        ("_selection.setRangeTicks(dstTick, dstTick + tickLen, dstStaff, endStaff);",
         '_selection.setRangeTicks(dstTick, dstTick + tickLen, dstStaff, endStaff);\n'
         '            Af085::snapshot("pasteStaff_range_planned", this);'),
    ])
    instrument(root, "libmscore/select.cpp", [
        ("void Selection::clear()\n      {",
         'void Selection::clear()\n      {\n      if (Af085::enabled() && !isNone())\n'
         '            Af085::record("selection_clear", {{"score", Af085::identity(_score)}, {"before", Af085::selection(*this)}});'),
        ("      update();\n      }\n\n//---------------------------------------------------------\n//   setRange",
         '      update();\n      if (Af085::enabled())\n'
         '            Af085::record("range_members_rebuilt", {{"score", Af085::identity(_score)}, {"after", Af085::selection(*this)}});\n'
         "      }\n\n//---------------------------------------------------------\n//   setRange"),
    ])
    instrument(root, "libmscore/note.cpp", [
        ("if (score()->tagIsValid(e->tag()))\n                  e->scanElements(data, func, all);",
         "const bool pass = score()->tagIsValid(e->tag());\n"
         "            const bool trace = Af085::tracedPart() == score() && e->isFingering();\n"
         "            const bool before = trace && e->selected();\n"
         "            if (pass)\n                  e->scanElements(data, func, all);\n"
         '            if (trace)\n                  Af085::record("note_child_scan", {{"stage", Af085::partStage()},\n'
         '                        {"tag_pass", pass}, {"all", all}, {"flag_before", before}, {"child", Af085::elementState(e)}});'),
    ])
    instrument(root, "mscore/excerptsdialog.cpp", [
        ("Excerpt::createExcerpt(e);\n\n      // a new excerpt",
         'Excerpt::createExcerpt(e);\n      Af085::snapshot("excerpts_dialog_create_return", nscore);\n\n      // a new excerpt'),
    ], '#include "libmscore/af085_model.h"')
    instrument(root, "mscore/musescore.cpp", [
        ("_tourHandler->loadTours();\n\n      QScreen* screen",
         "_tourHandler->loadTours();\n      Af085::observeRequestedSnapshots(this);\n\n      QScreen* screen"),
        ("if (cs->switchLayer(s)) {\n            cs->setLayoutAll();\n            cs->update();\n            }",
         'Af085::snapshot("switch_layer_before", cs);\n      if (cs->switchLayer(s)) {\n'
         '            cs->setLayoutAll();\n            cs->update();\n            Af085::snapshot("switch_layer_after", cs);\n            }'),
        ("QString cmdn(a->data().toString());\n\n      if (MScore::debugMode)",
         'QString cmdn(a->data().toString());\n      if (Af085::enabled())\n'
         '            Af085::record("gui_action", {{"action", cmdn}, {"score_id", Af085::identity(cs)}});\n\n      if (MScore::debugMode)'),
    ], '#include "musescore.h"\n#include "af085_ui.h"')
    excerpt(root)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("upstream", type=Path)
    parser.add_argument("--excerpt-only", action="store_true")
    args = parser.parse_args()
    (excerpt if args.excerpt_only else common)(args.upstream)


if __name__ == "__main__":
    main()
