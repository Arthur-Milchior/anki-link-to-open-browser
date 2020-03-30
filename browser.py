from aqt import dialogs, gui_hooks, mw


def on_bridge_browser(handled, cmd, context):
    prefix = "Browser search:"
    if not cmd.startswith(prefix):
        return handled
    search = cmd[len(prefix):]
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(search)
    browser.onSearchActivated()
    return (True, None)


gui_hooks.webview_did_receive_js_message.append(on_bridge_browser)
