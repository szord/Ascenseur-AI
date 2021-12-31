import random

from deck import Deck
from carte import Carte
from randomAgent import RandomAgent
from tools import Debug

# -1 to 4
DEBUG_LEVEL_PARTIE = -1
debug_partie = Debug(DEBUG_LEVEL_PARTIE)


class Partie:
    """Represents a game and its states."""
    
    variantes = ["Normale", "Officielle"]
    limites_joueurs = (3,10)
    # see https://fr.wikibooks.org/wiki/Bo%C3%AEte_%C3%A0_jeux/L%27ascenseur for offcial rules
    
    def __init__(self, n_joueurs=4, joueurs=None, variante=0):
        """Initializes a game
        
        n_joueurs: integer 3-10
        variante: integer 0-1"""
        self.n_joueurs = max(min(Partie.limites_joueurs[1], n_joueurs),Partie.limites_joueurs[0])
        self.joueurs = [RandomAgent(str(i)) for i in range(self.n_joueurs)] if joueurs is None else joueurs
        self.variante = max(min(len(Partie.variantes)-1, variante), 0)
        self.tour = 0 # current tour
        self.round = 0
        self.tours = int((52-1)/self.n_joueurs) if self.variante == 0 else int(52/self.n_joueurs)
        self.scores = [0]*self.n_joueurs
        self.deck = Deck()
        
    def __str__(self):
        game_str = ""
        game_str += "Variante: " + str(self.variante) + "\n"
        game_str += "Nombre de joueurs: " + str(self.n_joueurs) + "\n"
        game_str += "Tour / Tours: " + str(self.tour) + "/" + str(self.tours) + "\n"
        game_str += "Carte d'atout:" + self.deck.edge.__str__() + "\n"
        game_str += self.get_scoreboard_str()
        game_str += self.deck.__str__() + "\n"
        return game_str
    
    def get_scoreboard_str(self):
        """Returns a string of text to display results."""
        sum_score = 0
        scoreboard_str = "Joueurs:\tId \t Type \t\t Score \t\t pli/mise " + "\n"
        for i, j in enumerate(self.joueurs):
            scoreboard_str += "\t\t" + j.name + "\t" + type(j).__name__ + "\t" + str(j.score) + "\t\t" + str(j.pli) + "/" + str(j.mise) + "\n"
            sum_score += j.score
        return scoreboard_str
    
    def get_score_sum(self):
        """Returns the sum of all players scores.
        Useful to benchmark strategies."""
        return sum([j.score for j in self.joueurs])
        
    def get_edge(self):
        """Returns the card used as the edge"""
        return self.deck.edge
    
    def deal_cards(self):
        """Distribute cards to all players."""
        curr = 0
        for card in self.deck.deal_cards(self.n_joueurs*(self.tour),
                                         self.variante == 0):
            self.joueurs[curr].add_card_to_hand(card)
            curr = (curr+1)%self.n_joueurs
    
    def play_game(self):
        """Method to play an entire game"""
        for tour in range(self.tours):
            self.play_turn()
            self.deck.end_of_turn()
            
    def play_turn(self):
        """Play a turn"""
        self.tour += 1
        debug_partie.log("@@@ Début du tour n° {} @@@".format(self.tour), 0, 0)
        self.deal_cards()
        # players have to bet in order to play a turn
        for j in self.joueurs:
            j.bet(self.deck.edge, self.n_joueurs)
            debug_partie.log("Mise de joueur {}: {}".format(j.name, j.mise), 1, 1)
        debug_partie.log("Mise total {}".format(sum([j.mise for f in self.joueurs])), 0, 0)
        
        for round in range(1, self.tour+1):
            self.play_round()
        self.round = 0
        
        for j in self.joueurs:
            j.update_score()
        debug_partie.log("@@@ Fin du tour n° {} @@@".format(self.tour), 1, 0)
        
    def play_round(self):
        """Play a round"""
        self.round += 1
        #init round
        debug_partie.log("### Début tour n° {}, round n° {} ###".format(self.tour, self.round), 1, 1)
        edge = self.deck.edge
        debug_partie.log("Atout: " + edge.__str__(), 1, 2)
        stack = []
        curr_best = (None, None) #(player_id, best_card)        
        opening_suit = None
        # each player play one card
        for i in range(self.n_joueurs):
            player_id = (i+self.tour)%self.n_joueurs
            j = self.joueurs[player_id]
            debug_partie.log("Hand: " + j.hand_str(), 3, 3)
            card_played = j.play_round(opening_suit, curr_best[1], edge.suit)
            stack.append(card_played)
            
            if opening_suit is None: 
                opening_suit = card_played.suit
            if card_played.compare(curr_best[1], edge=edge.suit) == 1:
                curr_best = (player_id, card_played)
            
            debug_partie.log("Stack: {}".format(stack), 3, 3)
            debug_partie.log("Current best: {}".format(curr_best), 3, 3)
        
        #annouce pli winner and update score
        winner_pli = self.joueurs[curr_best[0]]
        debug_partie.log("Pli remporté par " + winner_pli.name, 1, 1)
        winner_pli.pli += 1
        debug_partie.log("### Fin tour n° {}, round n° {} ###".format(self.tour, self.round), 1, 1)    
        

            
