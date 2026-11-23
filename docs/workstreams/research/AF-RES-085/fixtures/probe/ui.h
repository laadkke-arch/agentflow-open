#pragma once

#include <QAbstractButton>
#include <QAbstractItemView>
#include <QApplication>
#include <QComboBox>
#include <QFile>
#include <QImage>
#include <QMenu>
#include <QMenuBar>
#include <QTabBar>
#include <QTimer>

#include "libmscore/af085_model.h"
#include "scoreview.h"

namespace Ms {
namespace Af085 {

inline QJsonArray rectangle(const QRect& rect)
{
    return {rect.x(), rect.y(), rect.width(), rect.height()};
}

inline QJsonObject item(const QWidget* widget, const QRect& local, const QString& text)
{
    const QRect screen(widget->mapToGlobal(local.topLeft()), local.size());
    return {{"text", text}, {"name", widget->objectName()}, {"rect", rectangle(screen)},
            {"enabled", widget->isEnabled()}, {"class", widget->metaObject()->className()}};
}

inline QJsonArray viewGeometry(const ScoreView* view)
{
    QJsonArray objects;
    if (!view)
        return objects;
    const auto score = view->score();
    if (!score)
        return objects;
    for (const Segment* segment = score->firstSegment(SegmentType::ChordRest); segment; segment = segment->next1()) {
        if (!segment->isChordRestType())
            continue;
        for (int track = 0; track < score->nstaves() * VOICES; ++track) {
            const Element* element = segment->element(track);
            if (!element || !element->isChordRest())
                continue;
            QList<const Element*> elements;
            collect(toChordRest(element), elements);
            for (const Element* object : elements) {
                if (object->isChord())
                    continue;
                const QRect local = view->toPhysical(object->canvasBoundingRect());
                auto state = item(view, local, object->name());
                state["id"] = identity(object);
                objects.append(state);
            }
        }
    }
    return objects;
}

inline QJsonArray widgets(MuseScore* main)
{
    QJsonArray result;
    const auto menubar = main->menuBar();
    for (QAction* action : menubar->actions()) {
        if (action->isVisible()) {
            auto widget = item(menubar, menubar->actionGeometry(action), action->text());
            widget["kind"] = "menu";
            result.append(widget);
        }
    }
    const auto popup = QApplication::activePopupWidget();
    if (const auto menu = qobject_cast<const QMenu*>(popup)) {
        for (QAction* action : menu->actions()) {
            if (action->isVisible() && !action->isSeparator()) {
                auto widget = item(menu, menu->actionGeometry(action), action->text());
                widget["kind"] = "action";
                widget["action"] = action->data().toString();
                widget["enabled"] = action->isEnabled();
                result.append(widget);
            }
        }
    }
    if (const auto dialog = QApplication::activeModalWidget()) {
        auto widget = item(dialog, dialog->rect(), dialog->windowTitle());
        widget["kind"] = "dialog";
        result.append(widget);
        for (const auto button : dialog->findChildren<QAbstractButton*>()) {
            if (button->isVisible()) {
                auto control = item(button, button->rect(), button->text());
                control["kind"] = "button";
                result.append(control);
            }
        }
    }
    for (const auto tab : main->findChildren<QTabBar*>()) {
        if (tab->isVisible()) {
            for (int index = 0; index < tab->count(); ++index) {
                auto widget = item(tab, tab->tabRect(index), tab->tabText(index));
                widget["kind"] = "tab";
                widget["current"] = index == tab->currentIndex();
                result.append(widget);
            }
        }
    }
    for (const auto combo : main->findChildren<QComboBox*>()) {
        if (combo->isVisible() && combo->toolTip() == "Switch layer") {
            auto widget = item(combo, combo->rect(), combo->currentText());
            widget["kind"] = "layer_combo";
            result.append(widget);
            for (int index = 0; index < combo->count(); ++index) {
                const auto view = combo->view();
                if (view->isVisible()) {
                    auto choice = item(view->viewport(), view->visualRect(combo->model()->index(index, 0)),
                                       combo->itemText(index));
                    choice["kind"] = "layer_choice";
                    result.append(choice);
                }
            }
        }
    }
    return result;
}

inline void observeRequestedSnapshots(MuseScore* main)
{
    const QString path = QString::fromLocal8Bit(qgetenv("AF085_SNAPSHOT_REQUEST"));
    if (!enabled() || path.isEmpty())
        return;
    auto timer = new QTimer(main);
    QObject::connect(timer, &QTimer::timeout, main, [main, path] {
        QFile request(path);
        if (!request.open(QIODevice::ReadOnly))
            return;
        const QString label = QString::fromUtf8(request.readAll()).trimmed();
        static QString previousLabel;
        if (label.isEmpty() || label == previousLabel)
            return;
        previousLabel = label;
        const auto view = main->currentScoreView();
        const Score* score = view ? view->score() : nullptr;
        const QWidget* focus = QApplication::focusWidget();
        record("ui_snapshot", {{"label", label}, {"active_score_id", identity(score)}, {"scores", scoreStates(score)},
                              {"objects_on_screen", viewGeometry(view)}, {"widgets", widgets(main)},
                              {"window_title", main->windowTitle()},
                              {"focus_class", focus ? focus->metaObject()->className() : ""}});
    });
    timer->start(40);
}

} // namespace Af085
} // namespace Ms
