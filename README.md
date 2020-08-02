# Link in fields
## Rationale
One usual request in anki is to allow to link content together. This add-on does just this. In the editor, you have a button which allow to link to another note, another card, or an arbitrary query search, and allow to open the result in the browser or in the previewer.

## Usage
In the editor, the button ![link](icons/link.svg) allows to open a window. In this window, you can select wether you want to open the link in the browser or the previewer. You can state whether you want to see a particular note, card, or a search (as in browser and filtered deck). Notes and cards are represented by their ID.

You can create a link to current card/note. The link can then be copied and put in any other note. 

The ID can also be found in a multiple of other way. For example, using the [Advanced browser](https://ankiweb.net/shared/info/874215009) add-on, you can show the card-id and note-id columns. You can also select a card in the browser and do `Cards>Info` (Ctrl+Shit+I) to see a window with informations such as the card's and note's IDs.

## Advice
You may want to consider installing the add-on [Opening the same window multiple time](https://ankiweb.net/shared/info/354407385), so that you can have multiple instance of the browser opened at the same time and see your note in a new window.

## Warning
This won't work when you uninstall the add-on. It'll just leave useless links.

## Internal
### Browser
If any bridge receive a message starting by "Browser search:" followed by a `query`, it will open the browser and search `query` in it. You can send this message from any field by adding
```html
onclick="pycmd(Browser search:query')"
```
.

### Previewer
If any bridge receive a message starting by "Previewer:" followed by a `query`, it will open the previewer and show the result of the `query` (as in the browser). You can send this message from any field by adding
```html
onclick="pycmd(Previewer:query')"
```
.


## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU GPL, version 3 or later; http://www.gnu.org/licenses/gpl.html
Source in   | https://github.com/Arthur-Milchior/anki-link-to-open-browser
Addon number| [1126950429](https://ankiweb.net/shared/info/1126950429)
