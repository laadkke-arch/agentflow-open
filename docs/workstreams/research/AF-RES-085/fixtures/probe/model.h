#pragma once

#include <QDateTime>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <cstdio>

#include "chord.h"
#include "note.h"
#include "score.h"
#include "segment.h"
#include "textbase.h"
#include "undo.h"

namespace Ms {
namespace Af085 {

inline bool enabled()
{
    static const bool trace = qEnvironmentVariableIsSet("AF085_TRACE");
    return trace;
}

inline QString identity(const void* pointer)
{
    return pointer ? QString::number(quintptr(pointer), 16) : QString();
}

inline void record(const char* event, QJsonObject details = {})
{
    if (!enabled())
        return;
    static int sequence = 0;
    details["event"] = event;
    details["seq"] = ++sequence;
    details["utc"] = QDateTime::currentDateTimeUtc().toString(Qt::ISODateWithMs);
    const QByteArray line = QJsonDocument(details).toJson(QJsonDocument::Compact);
    std::fprintf(stdout, "%s\n", line.constData());
    std::fflush(stdout);
}

inline QJsonObject selection(const Selection& selection)
{
    QJsonArray elements;
    for (const Element* element : selection.elements())
        elements.append(identity(element));
    const QString mode = selection.isRange() ? "RANGE" : selection.isList() ? "LIST" : "NONE";
    QJsonObject state{{"mode", mode}, {"list", elements}, {"active_track", selection.activeTrack()},
                      {"staff_start", selection.staffStart()}, {"staff_end", selection.staffEnd()}};
    if (selection.startSegment()) {
        state["tick_start"] = selection.tickStart().ticks();
        state["tick_end"] = selection.tickEnd().ticks();
    }
    return state;
}

inline QJsonObject elementState(const Element* element)
{
    const auto score = element->score();
    const Note* note = element->isNote() ? toNote(element) : nullptr;
    const Element* parent = element->parent();
    const Note* owner = parent && parent->isNote() ? toNote(parent) : note;
    const ChordRest* cr = owner ? owner->chord() : element->isChordRest() ? toChordRest(element) : nullptr;
    QJsonArray peers;
    for (const ScoreElement* peer : element->linkList()) {
        if (peer == element)
            continue;
        const auto linked = static_cast<const Element*>(peer);
        const auto linkedScore = linked->score();
        peers.append(QJsonObject{{"id", identity(linked)}, {"score_id", identity(linkedScore)},
                                 {"track", linked->track()}, {"type", linked->name()}});
    }
    QJsonObject state{
        {"id", identity(element)}, {"parent_id", identity(parent)}, {"type", element->name()},
        {"score_id", identity(score)}, {"track", element->track()}, {"staff", element->staffIdx()},
        {"flag", element->selected()}, {"member", score->selection().elements().contains(const_cast<Element*>(element))},
        {"tag", static_cast<int>(element->tag())}, {"tag_valid", score->tagIsValid(element->tag())},
        {"visible", element->visible()}, {"cur_color", element->curColor().name(QColor::HexArgb)}, {"peers", peers}
    };
    if (owner)
        state["pitch"] = owner->pitch();
    if (note)
        state["mark"] = note->mark();
    if (cr && cr->segment()) {
        state["tick"] = cr->segment()->tick().ticks();
        state["duration"] = cr->durationType().name();
        state["duration_ticks"] = cr->ticks().ticks();
    }
    if (element->isFingering())
        state["text"] = static_cast<const TextBase*>(element)->plainText();
    return state;
}

inline void collect(const ChordRest* cr, QList<const Element*>& elements)
{
    elements.append(cr);
    if (cr->isChord()) {
        for (const Note* note : toChord(cr)->notes()) {
            elements.append(note);
            for (const Element* child : note->el())
                elements.append(child);
        }
    }
}

inline QJsonArray objects(const Score* score)
{
    QJsonArray result;
    for (const Segment* segment = score->firstSegment(SegmentType::ChordRest); segment; segment = segment->next1()) {
        if (!segment->isChordRestType())
            continue;
        for (int track = 0; track < score->nstaves() * VOICES; ++track) {
            const Element* item = segment->element(track);
            if (!item || !item->isChordRest())
                continue;
            QList<const Element*> elements;
            collect(toChordRest(item), elements);
            for (const Element* element : elements)
                result.append(elementState(element));
        }
    }
    return result;
}

inline QJsonObject scoreState(const Score* score)
{
    return {{"id", identity(score)}, {"title", score->title()}, {"master", score->isMaster()},
            {"selection", selection(score->selection())}, {"undo_index", score->undoStack()->getCurIdx()},
            {"layer_index", score->currentLayer()}, {"layer_mask", static_cast<int>(score->currentLayerMask())},
            {"objects", objects(score)}};
}

inline QJsonArray scoreStates(const Score* focus)
{
    QJsonArray values;
    if (focus) {
        for (const Score* score : focus->masterScore()->scoreList())
            values.append(scoreState(score));
    }
    return values;
}

inline void snapshot(const char* event, const Score* focus)
{
    if (enabled() && focus)
        record(event, {{"active_score_id", identity(focus)}, {"scores", scoreStates(focus)}});
}

inline void pairedInsertion(const Element* source, const Element* destination, int tick)
{
    if (!enabled())
        return;
    QList<const Element*> sourceElements, destinationElements;
    collect(toChordRest(source), sourceElements);
    collect(toChordRest(destination), destinationElements);
    QJsonArray from, to;
    for (const Element* element : sourceElements)
        from.append(elementState(element));
    for (const Element* element : destinationElements)
        to.append(elementState(element));
    record("cloneVoice_insert", {{"tick", tick}, {"source", from}, {"destination", to}});
}

// This state labels observer output only. The application's scan and callback are unchanged.
inline const Score*& tracedPart()
{
    static const Score* part = nullptr;
    return part;
}

inline const char*& partStage()
{
    static const char* stage = "";
    return stage;
}

class ObservePart {
    const Score* previousPart;
    const char* previousStage;
public:
    ObservePart(const Score* source, const Score* part)
        : previousPart(tracedPart()), previousStage(partStage())
    {
        if (enabled()) {
            tracedPart() = part;
            partStage() = "create";
            record("excerpt_enter", {{"source", scoreState(source)}, {"destination_id", identity(part)}});
        }
    }

    ~ObservePart()
    {
        tracedPart() = previousPart;
        partStage() = previousStage;
    }
};

} // namespace Af085
} // namespace Ms
