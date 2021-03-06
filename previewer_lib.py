import json
import re
import time
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from anki.cards import Card
from anki.lang import _
from aqt import AnkiQt, gui_hooks
from aqt.qt import (QAbstractItemView, QCheckBox, QDialog, QDialogButtonBox,
                    QKeySequence, Qt, QVBoxLayout, QWidget)
from aqt.sound import av_player, play_clicked_audio
from aqt.theme import theme_manager
from aqt.utils import restoreGeom, saveGeom
from aqt.webview import AnkiWebView


@dataclass
class PreviewDialog:
    dialog: QDialog
    parent: QWidget


class Previewer:
    _lastPreviewState = None
    _previewCardChanged = False
    _lastPreviewRender: Union[int, float] = 0
    _previewTimer = None

    def __init__(self, parent: QWidget, mw: AnkiQt):
        self.parent = parent
        self.mw = mw

    def card(self) -> Optional[Card]:
        raise NotImplementedError

    def _openPreview(self):
        self._previewState = "question"
        self._lastPreviewState = None
        self._create_gui()
        self._setupPreviewWebview()
        self._renderPreview(True)
        self._previewWindow.show()

    def _create_gui(self):
        self._previewWindow = QDialog(None, Qt.Window)
        self._previewWindow.setWindowTitle(_("Preview"))

        self._previewWindow.finished.connect(self._onPreviewFinished)
        self._previewWindow.silentlyClose = True
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self._previewWeb = AnkiWebView(title="previewer")
        self.vbox.addWidget(self._previewWeb)
        self.bbox = QDialogButtonBox()

        self._previewReplay = self.bbox.addButton(
            _("Replay Audio"), QDialogButtonBox.ActionRole
        )
        self._previewReplay.setAutoDefault(False)
        self._previewReplay.setShortcut(QKeySequence("R"))
        self._previewReplay.setToolTip(_("Shortcut key: %s" % "R"))
        self._previewReplay.clicked.connect(self._onReplayAudio)

        self.previewShowBothSides = QCheckBox(_("Show Both Sides"))
        self.previewShowBothSides.setShortcut(QKeySequence("B"))
        self.previewShowBothSides.setToolTip(_("Shortcut key: %s" % "B"))
        self.bbox.addButton(self.previewShowBothSides,
                            QDialogButtonBox.ActionRole)
        self._previewBothSides = self.mw.col.get_config(
            "previewBothSides", False)
        self.previewShowBothSides.setChecked(self._previewBothSides)
        self.previewShowBothSides.toggled.connect(self._onPreviewShowBothSides)

        self.vbox.addWidget(self.bbox)
        self._previewWindow.setLayout(self.vbox)
        restoreGeom(self._previewWindow, "preview")

    def _onPreviewFinished(self, ok):
        saveGeom(self._previewWindow, "preview")
        self.mw.progress.timer(100, self._onClosePreview, False)

    def _onReplayAudio(self):
        self.mw.reviewer.replayAudio(self)

    def _closePreview(self):
        if self._previewWindow:
            self._previewWindow.close()
            self._onClosePreview()

    def _onClosePreview(self):
        self._previewWindow = None

    def _setupPreviewWebview(self):
        jsinc = [
            "jquery.js",
            "browsersel.js",
            "mathjax/conf.js",
            "mathjax/MathJax.js",
            "reviewer.js",
        ]
        web_context = PreviewDialog(
            dialog=self._previewWindow, parent=self.parent)
        self._previewWeb.stdHtml(
            self.mw.reviewer.revHtml(),
            css=["reviewer.css"],
            js=jsinc,
            context=web_context,
        )
        self._previewWeb.set_bridge_command(
            self._on_preview_bridge_cmd, web_context,
        )

    def _on_preview_bridge_cmd(self, cmd: str) -> Any:
        if cmd.startswith("play:"):
            play_clicked_audio(cmd, self.card())

    def _renderPreview(self, cardChanged=False):
        self._cancelPreviewTimer()
        # Keep track of whether _renderPreview() has ever been called
        # with cardChanged=True since the last successful render
        self._previewCardChanged |= cardChanged
        # avoid rendering in quick succession
        elapMS = int((time.time() - self._lastPreviewRender) * 1000)
        delay = 300
        if elapMS < delay:
            self._previewTimer = self.mw.progress.timer(
                delay - elapMS, self._renderScheduledPreview, False
            )
        else:
            self._renderScheduledPreview()

    def _cancelPreviewTimer(self):
        if self._previewTimer:
            self._previewTimer.stop()
            self._previewTimer = None

    def _renderScheduledPreview(self) -> None:
        self._cancelPreviewTimer()
        self._lastPreviewRender = time.time()

        if not self._previewWindow:
            return
        c = self.card()
        func = "_showQuestion"
        if not c:
            txt = _("(please select 1 card)")
            bodyclass = ""
            self._lastPreviewState = None
        else:
            if self._previewBothSides:
                self._previewState = "answer"
            elif self._previewCardChanged:
                self._previewState = "question"

            currentState = self._previewStateAndMod()
            if currentState == self._lastPreviewState:
                # nothing has changed, avoid refreshing
                return

            # need to force reload even if answer
            txt = c.q(reload=True)

            if self._previewState == "answer":
                func = "_showAnswer"
                txt = c.a()
            txt = re.sub(r"\[\[type:[^]]+\]\]", "", txt)

            bodyclass = theme_manager.body_classes_for_card_ord(c.ord)

            if self.mw.reviewer.autoplay(c):
                if self._previewBothSides:
                    # if we're showing both sides at once, remove any audio
                    # from the answer that's appeared on the question already
                    question_audio = c.question_av_tags()
                    only_on_answer_audio = [
                        x for x in c.answer_av_tags() if x not in question_audio
                    ]
                    audio = question_audio + only_on_answer_audio
                elif self._previewState == "question":
                    audio = c.question_av_tags()
                else:
                    audio = c.answer_av_tags()
                av_player.play_tags(audio)
            else:
                av_player.clear_queue_and_maybe_interrupt()

            txt = self.mw.prepare_card_text_for_display(txt)
            txt = gui_hooks.card_will_show(
                txt, c, "preview" + self._previewState.capitalize()
            )
            self._lastPreviewState = self._previewStateAndMod()
        self._previewWeb.eval("{}({},'{}');".format(
            func, json.dumps(txt), bodyclass))
        self._previewCardChanged = False

    def _onPreviewShowBothSides(self, toggle):
        self._previewBothSides = toggle
        self.mw.col.set_config("previewBothSides", toggle)
        self.mw.col.setMod()
        if self._previewState == "answer" and not toggle:
            self._previewState = "question"
        self._renderPreview()

    def _previewStateAndMod(self):
        c = self.card()
        n = c.note()
        n.load()
        return (self._previewState, c.id, n.mod)


class PreviewerMultipleCards(Previewer):
    def card(self) -> Optional[Card]:
        # need to state explicitly it's not implement to avoid W0223
        raise NotImplementedError

    def _create_gui(self):
        super()._create_gui()
        self._previewPrev = self.bbox.addButton(
            "<", QDialogButtonBox.ActionRole)
        self._previewPrev.setAutoDefault(False)
        self._previewPrev.setShortcut(QKeySequence("Left"))
        self._previewPrev.setToolTip(_("Shortcut key: Left arrow"))

        self._previewNext = self.bbox.addButton(
            ">", QDialogButtonBox.ActionRole)
        self._previewNext.setAutoDefault(True)
        self._previewNext.setShortcut(QKeySequence("Right"))
        self._previewNext.setToolTip(_("Shortcut key: Right arrow or Enter"))

        self._previewPrev.clicked.connect(self._onPreviewPrev)
        self._previewNext.clicked.connect(self._onPreviewNext)

    def _onPreviewPrev(self):
        if self._previewState == "answer" and not self._previewBothSides:
            self._previewState = "question"
            self._renderPreview()
        else:
            self._onPreviewPrevCard()

    def _onPreviewPrevCard(self):
        ...

    def _onPreviewNext(self):
        if self._previewState == "question":
            self._previewState = "answer"
            self._renderPreview()
        else:
            self._onPreviewNextCard()

    def _onPreviewNextCard(self):
        ...

    def _updatePreviewButtons(self):
        if not self._previewWindow:
            return
        self._previewPrev.setEnabled(self._should_enable_prev())
        self._previewNext.setEnabled(self._should_enable_next())

    def _should_enable_prev(self):
        return self._previewState == "answer" and not self._previewBothSides

    def _should_enable_next(self):
        return self._previewState == "question"

    def _onClosePreview(self):
        super()._onClosePreview()
        self._previewPrev = None
        self._previewNext = None


class PreviewerBrowser(PreviewerMultipleCards):
    def card(self) -> Optional[Card]:
        if self.parent.singleCard:
            return self.parent.card
        else:
            return None

    def _onPreviewFinished(self, ok):
        super()._onPreviewFinished(ok)
        self.parent.form.previewButton.setChecked(False)

    def _onPreviewPrevCard(self):
        self.parent.editor.saveNow(
            lambda: self.parent._moveCur(QAbstractItemView.MoveUp)
        )

    def _onPreviewNextCard(self):
        self.parent.editor.saveNow(
            lambda: self.parent._moveCur(QAbstractItemView.MoveDown)
        )

    def _should_enable_prev(self):
        return super()._should_enable_prev() or self.parent.currentRow() > 0

    def _should_enable_next(self):
        return (
            super()._should_enable_next()
            or self.parent.currentRow() < self.parent.model.rowCount(None) - 1
        )

    def _onClosePreview(self):
        super()._onClosePreview()
        self.parent.previewer = None

    def _renderScheduledPreview(self) -> None:
        super()._renderScheduledPreview()
        self._updatePreviewButtons()


class PreviewerListCards(PreviewerMultipleCards):
    def __init__(self, cards: List[Union[Card, int]], *args, **kwargs):
        """A previewer displaying a list of card.

        List can be changed by setting self.cards to a new value.

        self.cards contains both cid and card. So that card is loaded
        only when required and is not loaded twice.

        """
        self.index = 0
        self.cards = cards
        super().__init__(*args, **kwargs)

    def card(self):
        if not self.cards:
            return None
        if isinstance(self.cards[self.index], int):
            self.cards[self.index] = self.mw.col.getCard(
                self.cards[self.index])
        return self.cards[self.index]

    def _openPreview(self):
        if not self.cards:
            return
        super()._openPreview()

    def _onPreviewPrevCard(self):
        self.index -= 1
        self._renderPreview()

    def _onPreviewNextCard(self):
        self.index += 1
        self._renderPreview()

    def _should_enable_prev(self):
        return super()._should_enable_prev() or self.index > 0

    def _should_enable_next(self):
        return super()._should_enable_next() or self.index < len(self.cards) - 1

    def _on_other_side(self):
        if self._previewState == "question":
            self._previewState = "answer"
        else:
            self._previewState = "question"
        self._renderPreview()


class PreviewerSingleCard(Previewer):
    def __init__(self, card: Card, *args, **kwargs):
        self._card = card
        super().__init__(*args, **kwargs)

    def card(self) -> Card:
        return self._card

    def _create_gui(self):
        super()._create_gui()
        self._other_side = self.bbox.addButton(
            "Other side", QDialogButtonBox.ActionRole
        )
        self._other_side.setAutoDefault(False)
        self._other_side.setShortcut(QKeySequence("Right"))
        self._other_side.setShortcut(QKeySequence("Left"))
        self._other_side.setToolTip(_("Shortcut key: Left or Right arrow"))
        self._other_side.clicked.connect(self._on_other_side)

    def _on_other_side(self):
        if self._previewState == "question":
            self._previewState = "answer"
        else:
            self._previewState = "question"
        self._renderPreview()
