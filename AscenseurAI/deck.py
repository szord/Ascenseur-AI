import random
from carte import Carte

class Deck:
    """Represents a standart 52 cards deck."""
    
    def __init__(self):
        """Builds a deck of cards."""
        self.deck = []
        for suit in range(4):
            for rank in range(0, 13):
                self.deck.append(Carte(suit, rank))
        self.last_dealt = -1
        self.edge = None
        
    def __str__(self):
        deck_str = "Cartes non distribuées:\n"
        break_count = 0
        break_chars = ["\t", "\t", "\n"]
        for card_index in range(self.last_dealt+1, len(self.deck)):
            deck_str += "\t" + self.deck[card_index].__str__() + break_chars[break_count%len(break_chars)]
            break_count += 1
        return deck_str
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal_cards(self, total, edge=True):
        self.shuffle()
        if edge:
            self.edge = self.deck[total]
            #print("Atout: ", self.edge)

        self.last_dealt = total
        for card_index in range(total):
            yield self.deck[card_index]

    def end_of_turn(self):
        self.edge = None
        self.last_dealt = -1
        self.shuffle()