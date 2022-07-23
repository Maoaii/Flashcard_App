from symbol import Symbol


class Kanji(Symbol):

    def __init__(self, symbol, romaji, meaning):
        super().__init__(symbol, romaji)
        self.meaning = meaning
