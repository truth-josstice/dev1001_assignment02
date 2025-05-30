import colorama as co
import csv as c
import json as j
import random as r
from playingcards import *

# sets up initial decks for all tables
deck1 = Deck()
deck2 = Deck()
deck3 = Deck()
deck4 = Deck()
deck1.shuffle()
deck2.shuffle()
deck3.shuffle()
deck4.shuffle()

player_stats = []

# variables for outside data files
stats_csv = 'playerstats.csv'
stats_json = 'playerstats.json'
dealer = 'dealerasciicards.csv'
player = 'playerasciicards.csv'

#trying to set up tables with a subclass for the nolimit table which is slightly different than the rest
class Table():
    def __init__(self, name, deck, bank, max_bet, min_bet, r17):
        """Sets up the table with deck to deal from, and other params for each."""
        self.deck = deck
        self.name = name
        self.bank = bank
        self.max = max_bet
        self.min = min_bet
        self.r17 = r17

    def new_deal(self):
        """for ever new hand this will occur"""
        self.hand = self.deck.draw_n(2)
        self.d_hand = self.deck.draw_n(2)
        
    def t_rules(self):
        print(f"""=====  {self.name} Table Rules  =====
        Hands cannot be split.
        Deck size: {len(self.deck)}.
        Chips to win: ${self.bank}.
        Maximum bet: ${self.max}.
        Minimum bet: ${self.min}.
        This dealer will {self.r17} on 17.
        """)

    def dealer_hand(self):
        """ASCII display function for dealer's hand in each game"""
        self.d_cards = [x for x in self.d_hand]
        self.d_score = self.scores(self.d_cards)
        if len(self.d_cards) == 2:
            self.cards = [self.d_cards[0].img, self.d_cards[1].img1]
        elif len(self.d_cards) > 2:
            self.cards = [x.img for x in self.d_hand]
        print("=" * 20 + "Dealer Cards" + "=" * 20)
        asciicards(dealer, *self.cards)
        print(f'Dealer score: {self.d_score}')        
        if self.d_score > 21:
            print(co.Fore.RED + co.Style.BRIGHT + 'Dealer Bust!\n' + co.Style.RESET_ALL)
        elif len(self.d_cards) == 2 and self.d_score == 21:
            print(co.Fore.GREEN + co.Style.BRIGHT + 'Dealar has Blackjack!' + co.Style.RESET_ALL)

    def player_hand(self):
        """ASCII display function for player's hand in each game"""
        self.p_cards = [x for x in self.hand]
        self.p_score = self.scores(self.p_cards)
        self.cards = [x.img for x in self.hand]     
        print("=" * 20 + "Player Cards" + "=" * 20)
        asciicards(player, *self.cards)
        print(f'Player score: {self.p_score}')
        if self.p_score > 21:
            print(co.Fore.RED + co.Style.BRIGHT + 'Bust!\n' + co.Style.RESET_ALL)
        elif len(self.p_cards) == 2 and self.p_score == 21:
            print(co.Fore.GREEN + co.Style.BRIGHT + 'Blackjack!' + co.Style.RESET_ALL)
          
    def scores(self, hand):
        """Calculates scores with conversion functionality for aces"""
        if hand == self.p_cards:
            score = 0
            for card in self.p_cards:
                if score >= 11:
                    if card.rank == 'Ace':
                        score += 1
                else:    
                    match card.rank:
                        case 'Ace':
                            score += 11
                        case 'King' | 'Queen' | 'Jack':
                            score += 10
                        case _:
                            score += card.value
                
            return score
        else:
            score = 0
            if score >= 11:
                if card.rank == 'Ace':
                    score += 1
            if len(self.d_cards) == 2:
                match self.d_cards[0].rank:
                    case 'Ace':
                        score += 11
                    case 'King' | 'Queen' | 'Jack':
                        score +=10
                    case _:
                        score += self.d_cards[0].value
            elif len(self.d_cards) >2 :
                for card in self.d_cards:
                    match card.rank:
                        case 'Ace':
                            score += 11
                        case 'King' | 'Queen' | 'Jack':
                            score +=10
                        case _:
                            score += card.value
            return score
    

    def hit(self, hand):
        match hand:
            case 'player':
                self.hand += self.deck.draw_n(1)
                self.player_hand()
            case 'dealer':
                self.d_hand += self.deck.draw_n(1)
                self.dealer_hand()
                


class NoLimit(Table):
    def __init__(self, name, deck, min_bet, r17):
        """sets up specific nolimit params"""
        super().__init__(name, deck, None, None, 1, r17)
        self.name = name
        self.min = min_bet
        self.deck = deck
        self.r17 = r17
    
    def t_rules(self):
        print(f"""=====  {self.name} Table Rules  =====
        Deck size: {len(self.deck)}.
        Chips to win: Unlimited.
        Maximum bet: Unlimited.
        Minimum bet: ${self.min}.
        This dealer will {self.r17} on 17.
        """)





def asciicards(filename, *lists) -> str:
    """ 
    Creates a side by side ASCII of two or more cards
    """
    with open(filename, 'w', newline='') as f:
        writer = c.writer(f)
        for row in zip(*lists):
            writer.writerow(row)
    
    with open(filename) as f:
        reader = c.reader(f)
        for row in reader:
            print("   ".join(row))


# player class to hold player data
class Player():
    def __init__(self, name, chips=100, hands=0, wins=0, losses=0, chip_won=0, chip_lost=0):
        "sets up initial player stats, all default values are parsed in here"
        self.name = name
        self.chips = chips
        self.hands = hands
        self.wins = wins
        self.losses = losses
        self.chip_won = chip_won
        self.chip_lost = chip_lost

    def new_save(self):
        "saves a new players data to the save file"
        player_stats.append({'name': self.name, 'chips': self.chips, 'hands': self.hands, 'wins': self.wins, 'losses': self.losses, 'chip_won': self.chip_won, 'chip_lost': self.chip_lost})
    
    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            for x in player_stats[0]:
                if self.name in x['name']:
                    x[key] += value



    # def read_stats(self):
    #     self.stats = f"""=====  Player Stats =====
    #     Player: {self.name}
    #     Current chip total: ${self.chips}
    #     Total hands played: ${self.}
    #     """

 
def load_stats():
    """without this function, saves will not be carried over between multiple playthroughs, this loads all data in at the start of each session"""
    try:
        with open(stats_json, 'r') as f:
            save = j.load(f)
            player_stats.append(save)
    except j.decoder.JSONDecodeError:
        pass

def save_stats():
    """saves all stats of all currently saved players"""
    with open(stats_json, 'w') as f:
        j.dump(player_stats, f, indent=4)

player1=Player('joss')
player2=Player('sophie')
load_stats()

player1.update_stats(chips=1000,hands=1,)
player2.update_stats(chips=2000)
print(player_stats[0])
player1.update_stats(chips=-1500,hands=4,wins=5)
print(player_stats[0])


        

# low = Table("Low Roller's", deck1, 200, 20, 5, 'hit')
# mid = Table("Mid Roller's", deck2, 500, 50, 10, 'hit')
# high = Table("High Roller's", deck3, 1000, 100, 20, 'stand')
# nolimit = NoLimit('No Limit', deck4, 500, 'stand')

# low.new_deal()

# low.player_hand()
# low.dealer_hand()

# low.hit('player')
# low.hit('dealer')

# low.hit()
# low.t_rules()
# mid.t_rules()
# high.t_rules()
# nolimit.t_rules()

# """Code graveyard"""
    # def split(self):
    #     if self.p_cards[0].rank == self.p_cards[1].rank:
    #         self.split1.append(self.p_cards[0])
    #         self.s_cards = [x for x in self.split1]
    #         self.s1 = [x.img for x in self.split1]
    #         asciicards(player, *self.s1)
    #         self.split2.append(self.p_cards[1])
    #         self.scards1 = [x for x in self.split2]
    #         self.s2 = [x.img for x in self.split2]
    #         asciicards(player, *self.s2)
    #     else:
    #        print('Your hand is unable to be split.')

    # # class Hand(Deck):
# #     def __init__():


# class Player():
#     def __init__(self, name, hands_played):
#         self.name = name
#         self.hands_played = hands_played
#         self.chip_total = 0

#     def add_chips(self, chips):
#         self.chip_total += chips
    
#     def display_info(self):
#     return f"Player: {self.name}.\n Total hands played: {self.hands_played}.\n Chip total: ${self.chip_total}.