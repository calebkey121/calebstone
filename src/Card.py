class Card:
    def __init__(self, cost=-1, name=None, effect=None, text=None):
        self._cost = cost
        self._name = name
        self._effect = effect
        self._text = text or (effect.text if effect else "")
    
    def __repr__(self):
        return self._name

    # test eq
    # def __eq__(self, other: 'Card') -> bool:
    #     if not isinstance(other, Card):
    #         return NotImplemented
    #     return (
    #         self._cost == other._cost and
    #         self._name == other._name and
    #         self._effect == other._effect and
    #         self._text == other._text
    #     )
