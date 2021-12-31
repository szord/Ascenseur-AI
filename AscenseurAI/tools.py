import matplotlib.pyplot as plt
import time
import math
import copy
import numpy as np

import carte
import deck
import joueur
import partie
import randomAgent

COLORS = ["tab:orange", "tab:green", "tab:red",
          "tab:purple", "tab:brown", "tab:pink", "tab:gray",
          "tab:olive", "tab:cyan", "k"]


class Debug:
    def __init__(self, debug_level, file=None):
        self.debug_level = debug_level
        self.file = file
        
    def log(self, msg, level, indent):
        log_str = "\t"*indent + msg
        if level <= self.debug_level:
            print(log_str)


def hand_limit_values(turn, edge_value=13):
    """Compute maximum and minimum values possibe
    of a hand for certain amounts of cards."""
    edge_cards = min(13,turn)
    max_v = edge_cards*(13+13) - sum(range(edge_cards))
    
    non_edge_cards, i = turn-13, 0
    while non_edge_cards > 0:
        max_v += (max_rank_left - i//3)
        i += 1
    
    min_v = 3 * sum(range((turn//3)+1))
    for _ in range(turn%3):
        min_v += 1 + turn//3
    
    return (min_v, max_v)


def savefig(fig, savename, plotname):
    if savename:
        print("Saved")
        l = time.localtime(time.time())
        fig.savefig("plots/{}_{}_{}-{}.png".format(savename, plotname, str(l.tm_mon), str(l.tm_mday)))
      
    
def benchmark_sum_scores(joueurs, savename="", n_games=100):
    scores = []
    for _ in range(n_games):
        copy_joueurs = copy.deepcopy(joueurs)
        g = partie.Partie(n_joueurs=len(joueurs), joueurs=copy_joueurs, variante=0)
        g.play_game()
        scores.append(g.get_score_sum())

    fig, ax = plt.subplots(1,1)
    ax.hist(scores, bins=math.ceil(n_games/3), density=True, histtype='stepfilled')
    title = "{} players - {} runs".format(g.n_joueurs, n_games)
    ax.set_title(title)
    savefig(fig, savename, plotname="sum_scores")
    return fig


def plot_betting_fn(joueurs, tour, savename=""):
    n_joueurs = len(joueurs)
    hand_values = []
    mises = []

    g = partie.Partie(n_joueurs=n_joueurs,
                      joueurs=joueurs,
                      variante=0)
    g.tour = tour
    g.deal_cards()
    edge = g.deck.edge

    min_v, max_v = hand_limit_values(g.tour)
    for j in g.joueurs:
        hand_values.append(j.hand_value(edge))
        j.bet(edge, n_joueurs)
        mises.append(j.mise)

    X = np.linspace(min_v, max_v, 100)
    fig, ax = plt.subplots()
    ax.plot(X, [j.bet_fn(x, tour, n_joueurs) for x in X])
    ax.set_title("tour {}, sum j.mise {}".format(tour, sum(mises)))
    #ax.axvline(min_v, c='orange')
    #ax.axvline(max_v, c='red')
    for c_index, h_v in enumerate(hand_values):
        ax.axvline(h_v, c=COLORS[c_index], 
                   label=str(round(j.bet_fn(h_v, tour, n_joueurs)))
                  )
    ax.legend()

    title = "{} players - turn n°{}".format(g.n_joueurs, g.tour)
    ax.set_title(title)

    savefig(fig, savename, plotname="bet_fn")
    return fig