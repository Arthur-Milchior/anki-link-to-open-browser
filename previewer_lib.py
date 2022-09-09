from typing import List, Optional

from anki.cards import Card
from aqt.browser.previewer import MultiCardPreviewer
from aqt.main import AnkiQt


class CardPreviewer(MultiCardPreviewer):
    def __init__(self, mw: AnkiQt, cards: List[Card]) -> None:
        super().__init__(mw, mw, lambda: ())
        self._cards = cards
        self._selected = 0

    def card(self) -> Optional[Card]:
        if self._selected >= 0:
            return self._cards[self._selected]

    def card_changed(self) -> bool:
        return False

    def _on_prev_card(self) -> None:
        self._state = "question"
        self._selected -= 1
        return self.render_card()

    def _on_next_card(self) -> None:
        self._state = "question"
        self._selected = self._selected + 1
        return self.render_card()

    def _should_enable_prev(self) -> bool:
        return super()._should_enable_prev() or self._selected > 0

    def _should_enable_next(self) -> bool:
        return super()._should_enable_next() or self._selected < len(self._cards) - 1

    def _render_scheduled(self) -> None:
        super()._render_scheduled()
        self._updateButtons()
