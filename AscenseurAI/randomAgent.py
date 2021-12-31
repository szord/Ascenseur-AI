import numpy as np
import random

from joueur import Joueur
from tools import Debug

DEBUG_RAGENT = 0
debug_rAgent = Debug(DEBUG_RAGENT)

class RandomAgent(Joueur):
    """Implements a player whose strategies are:
    sigmoid function to estimate bet as a function of hand strength
    play random legal cards."""
    
    def __init__(self, name):
        super().__init__(name)
        
    def bet_fn(self, hand_v, turn, n_joueurs):
        mid = turn*9
        amp = 2*turn/n_joueurs
        y_offset = np.pi/2
        scale = 2*turn
        return  amp / (1 + np.exp(-(hand_v-mid)/scale))
    
    def hand_value(self, edge):
        return sum([card.rank + 13*(card.suit == edge.suit) for card in self.hand])

    def bet(self, edge, n_joueurs):
        turn = len(self.hand)
        hand_v = self.hand_value(edge)
        self.mise = round(self.bet_fn(hand_v, turn, n_joueurs))
        debug_rAgent.log("{}/{}".format(self.mise, hand_v), 3, 4)
        #self.mise = random.randint(0, turn)
        
    def play_round(self, opening_suit, strongest_card, edge_suit):
        legal_indexes = self.legal_moves(opening_suit, strongest_card, edge_suit)
        card_index = random.randint(0, len(legal_indexes)-1)
        card = self.hand[card_index]
        self.hand.pop(card_index)
        debug_rAgent.log("card played:" + card.__str__(), 1, 1)
        return card
    
