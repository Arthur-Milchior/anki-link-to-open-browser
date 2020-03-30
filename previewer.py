from aqt import gui_hooks, mw

from .previewer_lib import PreviewerListCards, PreviewerSingleCard


def on_bridge_browser(handled, cmd, context):
    prefix = "Previewer:"
    if not cmd.startswith(prefix):
        return handled
    search = cmd[len(prefix):]
    cids = mw.col.find_cards(search)
    cards = [mw.col.getCard(cid) for cid in cids]
    if len(cards) == 0:
        return
    elif len(cards) == 1:
        card = cards[0]
        previewer = PreviewerSingleCard(card, context, mw)
    else:
        previewer = PreviewerListCards(cards, context, mw)
    previewer._openPreview()
    return (True, None)


gui_hooks.webview_did_receive_js_message.append(on_bridge_browser)
