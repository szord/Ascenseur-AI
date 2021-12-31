class Carte:
    """Represents a standart playing card.
    
    Attributes:
        suit: integer 0-3
        rank: integer 0-12
    """
    suits = ["Pique", "Trefle", "Carreau", "Coeur"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", 
                  "Valet", "Dame", "Roi", "As"]
    
    def __init__(self, suit=0, rank=0):
        self.suit, self.rank = suit, rank
        
    def __str__(self):
        """Returns a human-readable string representation."""
        return Carte.ranks[self.rank] + " de " + Carte.suits[self.suit]
            
    def __repr__(self): return self.__str__()

    def compare(self, other, edge=None):
        """Compares self and other.
        self can be greater(1), lesser(-1) or not comparable(0) to other
        edge is the stronger suit, eventually None"""
        if other is None: return 1
        if self.suit == other.suit:
            return 1 if self.rank > other.rank else -1
        else:
            
            if edge is not None and (self.suit == edge or other.suit == edge):
                return 1 if self.suit == edge else -1
            else:
                return 0
