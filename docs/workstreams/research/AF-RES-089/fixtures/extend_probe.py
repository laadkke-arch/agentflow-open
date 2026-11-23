#!/usr/bin/env python3
"""Add command/undo observations to the fixed 085 observer without editing model state."""
import sys
from pathlib import Path


def replace(source, anchor, replacement):
    if source.count(anchor) != 1:
        raise ValueError(f"Unexpected source at {anchor!r}")
    return source.replace(anchor, replacement)


def main(source_dir):
    path = source_dir / "libmscore/cmd.cpp"
    source = path.read_text()
    source = replace(
        source,
        '''            if (!spannerSegment || !spanners.contains(toSpannerSegment(e)->spanner()))
                  e->undoChangeProperty(Pid::VISIBLE, !e->getProperty(Pid::VISIBLE).toBool());''',
        '''            if (!spannerSegment || !spanners.contains(toSpannerSegment(e)->spanner())) {
                  const bool af089VisibleBefore = e->getProperty(Pid::VISIBLE).toBool();
                  e->undoChangeProperty(Pid::VISIBLE, !af089VisibleBefore);
                  if (Af085::enabled())
                        Af085::record("visibility_target", {{"visible_before", af089VisibleBefore},
                              {"target", Af085::elementState(e)}});
                  }''',
    )
    source = replace(
        source,
        '''                  if (af085Command)
                        Af085::snapshot("score_action_ended", this);''',
        '''                  if (af085Command && Af085::enabled())
                        Af085::record("score_action_ended", {{"action", cmd},
                              {"active_score_id", Af085::identity(this)}, {"scores", Af085::scoreStates(this)}});''',
    )
    source = replace(
        source,
        '''      if (undo)
            undoStack()->undo(ed);
      else
            undoStack()->redo(ed);
      update();
      updateSelection();
      }''',
        '''      Af085::snapshot(undo ? "undo_enter" : "redo_enter", this);
      if (undo)
            undoStack()->undo(ed);
      else
            undoStack()->redo(ed);
      update();
      updateSelection();
      Af085::snapshot(undo ? "undo_exit" : "redo_exit", this);
      }''',
    )
    path.write_text(source)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
