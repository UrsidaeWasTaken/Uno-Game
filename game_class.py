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

            if chance <= 0.1:
                self.colour = "Wild"
                self.type = random.choice(actions[3:])
            elif chance >= 0.7:
                self.colour = random.choice(colours)
                self.type = random.choice(actions[:3])
            else:
                self.colour = random.choice(colours)
                self.type = random.randint(1,9)

            self.card = "%s %s" % (self.colour, self.type)


# Each Table contains a Deck for each player    
class Table(object):
    def __init__(self, number_of_players):
        self.players = number_of_players
        self.table = []

    # Each Deck contains 7 randomly generated Cards
    def generate_deck(self):
        deck = []
        for i in range(7):
            deck.append(Card())
        return deck
    
    def generate_table(self):
        for i in range(self.players):
            self.table.append(self.generate_deck())
        return self.table


class Game(object):
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
                    tmp = Table(int(prompt_choice[0]))
                    return tmp.generate_table()

        return prompt()

    def game(self):
        table = self.settings()
        round = 1
        current_player = 0
        starting_card = Card()

        def prompts(choice):
            def player_turn(deck):
                print("\nIt is PLAYER %s's turn!" % str(current_player + 1))
                input("Press ENTER when you're ready!")

                print("\n\n"+thin_borders+"\n-> YOUR HAND\n"+thin_borders+"\n")
                for i, card in enumerate(deck):
                    print("%s| %s" % (i+1, card.card))
                print("\n"+thin_borders)
                
                while True:
                    user_choice = input("Select a card or (D)raw: ")
                    try:
                        user_choice = int(user_choice)
                        if 0 < int(user_choice) <= len(deck):
                            return deck[int(user_choice) - 1].card
                        else:
                            if len(deck) < 3:
                                print(("\nERROR: You only have {} card/s to select from...").format(len(deck)))
                            else:
                                print(("\nERROR: {} is not within range 1 and {}...").format(user_choice, len(deck)))
                    except ValueError:
                        if user_choice.lower() == "d" or user_choice.lower() == "draw":
                            print("draw")
                            # Draw function
                        else:
                            print(("\nERROR: {} is not an option. Please select a card or (D)raw...").format(user_choice))

            if choice == 1:
                return player_turn(table[current_player])
