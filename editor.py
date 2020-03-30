import json
import os

from aqt import mw
from anki.hooks import addHook
from aqt.editor import Editor
from aqt.qt import QDialog, QKeySequence, Qt

from .config import getUserOption, setUserOption
from . import link

addon_path = os.path.dirname(__file__)


def create_link(editor):
    dialog = QDialog(editor.parentWindow, Qt.Dialog)
    form = link.Ui_Dialog()
    form.setupUi(dialog)

    # Default values
    # Line of text
    form.line_display.setText(editor.web.selectedText())

    # open
    form.combo_open_in.setCurrentIndex(
        {"Browser": 0, "Previewer": 1}.get(getUserOption("Last open in", "Browser"), 0))

    # search
    form.combo_search_type.setCurrentIndex(
        {"Note": 0, "Card": 1, "Query": 2}.get(getUserOption("Last search type", "Note"), 0))

    # query
    form.line_search.setText(getUserOption("Last query", ""))

    ##
    dialog.exec()
    mw.setupDialogGC(dialog)
    # Get values

    # Line of text
    text = form.line_display.text()
    setUserOption("Last open in", text)

    # open
    open_in = ["Browser search",
               "Previewer"][form.combo_open_in.currentIndex()]
    setUserOption("Last open in", open_in)

    # search
    search_type = ["Note", "Card",
                   "Query"][form.combo_search_type.currentIndex()]
    setUserOption("Last search type", search_type)

    # query
    query = form.line_search.text()
    setUserOption("Last query", query)

    # Replace text
    if search_type == "Note":
        query = f"nid:{query}"
    elif search_type == "Card":
        query = f"cid:{query}"
    text = f"""<a onclick="pycmd('{open_in}:{query}')">{text}</a>"""
    editor.web.eval(
        f"document.execCommand('insertHTML', false, {json.dumps(text)});")


def setupEditorButtonsFilter(buttons, editor):
    shortcut = getUserOption("Shortcut", "Ctrl+Shift+L")
    in_tip = QKeySequence(shortcut).toString(QKeySequence.NativeText)
    buttons.append(
        editor.addButton(
            os.path.join(addon_path, "icons", "link.svg"),
            "card_button",
            create_link,
            tip=f"Link to card ({in_tip})",
            keys=shortcut
        )
    )
    return buttons


addHook("setupEditorButtons", setupEditorButtonsFilter)
