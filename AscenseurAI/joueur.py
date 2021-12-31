import random
import numpy as np
import math

from carte import Carte
from tools import Debug


DEBUG_LEVEL_JOUEUR = 0
debug_joueur = Debug(DEBUG_LEVEL_JOUEUR)


class Joueur:
    """Abstact class representing a player.
    Create a subclass to define gameplay strategies by implementing bet() and play_round() methods.
    See randomAgent.py for an example"""
    
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.pli = 0
        self.mise = 0
        self.hand = []
        
    def __str__(self):
        joueur_str = "Joueur {}\tScore {}\t pli/mise {}/{}\n".format(self.name, self.score, self.pli, self.mise)    
        hand_str = self.hand_str()
        joueur_str += hand_str
        return joueur_str 
    
    def hand_str(self):
        """Returns a string of text to display a player hand"""
        break_chars = ["\t", "\t", "\n"]
        hand_str = ""
        for i, card in enumerate(self.hand):
            hand_str += str(i) + " " + card.__str__() + break_chars[i%len(break_chars)]
        #hand_str += "\n"
        return hand_str
    
    def add_card_to_hand(self, card):
        """Method to add a card to a player hand"""
        self.hand.append(card)
    
    def update_score(self):
        if self.mise == self.pli:
            self.score += 10*self.mise
        else:
            self.score -= 10*abs(self.mise - self.pli)
        self.pli = 0
        self.mise = 0
    
    def legal_moves(self, opening_suit, strongest_card, edge_suit):
        """Returns list of indexes of cards in hand that are legal to play."""
        legal_indexes = []
        debug_level = 3
        if opening_suit == None:
            legal_indexes = list(range(len(self.hand)))
            debug_joueur.log("opening rule", debug_level, debug_level)
            return legal_indexes

        edge_opening = opening_suit == edge_suit
        #1st rule: follow the non edge opening suit
        if not edge_opening:
            for index, card in enumerate(self.hand):
                if card.suit == opening_suit:
                    legal_indexes.append(index)
        if legal_indexes: 
            debug_joueur.log("1st rule", debug_level, debug_level)
            return legal_indexes
        
        #2nd rule: edge was played and you go for higher ranking 
        if strongest_card.suit == edge_suit:
            for index, card in enumerate(self.hand):
                if card.suit == edge_suit and card.rank > strongest_card.rank:
                    legal_indexes.append(index)
        if legal_indexes: 
            debug_joueur.log("2nd rule", debug_level, debug_level)
            return legal_indexes
        
        #3rd rule: edge was played and you cant go for higher ranking
        if strongest_card.suit == edge_suit:
            for index, card in enumerate(self.hand):
                if card.suit == edge_suit:
                    legal_indexes.append(index)
        if legal_indexes: 
            debug_joueur.log("3rd rule", debug_level, debug_level)
            return legal_indexes

        #4th rule: edge was not played yet and you play edge
        for index, card in enumerate(self.hand):
            if card.suit == edge_suit:
                legal_indexes.append(index)
        if legal_indexes: 
            debug_joueur.log("4th rule", debug_level, debug_level)
            return legal_indexes
        
        #5th rule: play whatever card you have in your hand
        legal_indexes = list(range(len(self.hand)))
        debug_joueur.log("5th rule", debug_level, debug_level)
        return legal_indexes
        

    def bet(self):
        """rules and strategies to place a bet(mise)"""
        raise NotImplementedError()
    
    def play_round(self):
        """rules and stratgies to play a card"""
        raise NotImplementedError()