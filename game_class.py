# Imports - Imports being used in program
from time import sleep
import random

# Base Cards = Cards & Settings that'll be needed throughout the program
colours = ["Red", "Yellow", "Green", "Blue"]
actions = ["Reverse", "Skip", "2+", "4+", ""]

# Display borders
thin_borders = "-" * 35
thick_borders = "=" * 35


# Each Card contains a value and a type
class Card(object):
    def __init__(self, colour=None, card_type=None):
        self.colour = colour
        self.type = card_type
        self.card = "%s %s" % (self.colour, self.type)

        # Randomly generates a card 
        if not colour:
            chance = random.random()

            if chance >= 0.4 or self.type == "starter":
                self.colour = random.choice(colours)
                self.type = random.randint(1,9)
            elif chance <= 0.1:
                self.colour = "Wild"
                self.type = random.choice(actions[3:])
            else:
                self.colour = random.choice(colours)
                self.type = random.choice(actions[:3])

            self.card = "%s %s" % (self.colour, self.type)


class Deck(object):
    def __init__(self):
        self.deck = []

        for i in range(7):
            self.deck.append(Card())
    
    def __str__(self): return self.deck


# Each Table contains a Deck for each player    
class Table(object):
    def __init__(self, number_of_players):
        self.decks = []

        for i in range(number_of_players):
            self.decks.append(Deck())

    @property
    def table(self):
        return self.decks


class PlayerCycle(object):
    def __init__(self, table):
        self.cycle = table.table
        self._current_player = 0
        self.is_reversed = False  
    
    @property
    def current_player(self):
        return self._current_player
    
    @current_player.setter
    def current_player(self, value):
        self._current_player = value % len(self.cycle)

    @property
    def current_deck(self):
        return self.cycle[self.current_player].deck
    
    @property
    def continue_cycle(self):
        if self.current_player is None:
            return -1 if self.is_reversed else 0
        else:
            return self.current_player-1 if self.is_reversed else self.current_player+1
    
    def reverse_cycle(self):
        self.is_reversed = not self.is_reversed


class Game(object):
    def __init__(self):
        self.table = None
        self.round = 1
        self.pile_card = Card(None,"starter")

    def __next__(self):
        self.table.current_player = self.table.continue_cycle
    
    def settings(self):
        options = {"2 Players": '2', "3 Players": '3', "4 Players": '4'}
        def display_settings():
            print(thick_borders+"\n\nSelect Number of Players\n\n"+thin_borders+"\n")

            for i, option in enumerate(options):
                print('-  '+str(option))
            print("\n"+thick_borders+"\n")
            
        def prompt():
            display_settings()
            while True:
                prompt_choice = input("Select Option: ")

                if prompt_choice.title() in options.keys() or prompt_choice in options.values():
                    temp = Table(int(prompt_choice[0]))
                    self.table = PlayerCycle(temp)
                    break

        return prompt()

    def game(self):
        def prompts(choice):
            def player_turn():
                print("\nIt is PLAYER %s's turn!" % str(self.table.current_player + 1))
                input("Press ENTER when you're ready!")

                print("\n\n"+thin_borders+"\n-> YOUR HAND\n"+thin_borders+"\n")
                for i, card in enumerate(self.table.current_deck):
                    print("%s| %s" % (i+1, card.card))
                print("\n"+thin_borders)
                
                while True:
                    print("LAST CARD: %s" % self.pile_card.card)
                    user_choice = input("Select a card or (D)raw: ")
                    try:
                        user_choice = int(user_choice)
                        if 0 < int(user_choice) <= len(self.table.current_deck):
                            if not vaildate_card(self.table.current_deck[int(user_choice) - 1]):
                                print(("\nERROR: {} does not match the symbol or colour of {}...").format(self.table.current_deck[int(user_choice) - 1].card, self.pile_card.card))
                            else:
                                print("\nMatch")
                                break
                        else:
                            if len(self.table.current_deck) < 3:
                                print(("\nERROR: You only have {} card/s to select from...").format(len(self.table.current_deck)))
                            else:
                                print(("\nERROR: {} is not within range 1 and {}...").format(user_choice, len(self.table.current_deck)))
                    except ValueError:
                        if user_choice.lower() == "d" or user_choice.lower() == "draw":
                            print("draw")
                            # Draw function
                        else:
                            print(("\nERROR: {} is not an option. Please select a card or (D)raw...").format(user_choice))

            if choice == 1:
                return player_turn()
        
        def vaildate_card(user_card, valid_card=self.pile_card):
            if user_card.colour is not "Wild":
                if (user_card.colour != valid_card.colour) and (user_card.type != valid_card.type):
                    return False
                else:
                    self.pile_card = user_card
                    return True
            else:
                return True
        