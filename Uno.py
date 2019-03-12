"""
UNO - CARD GAME

Allowing 2-4 people to play. Each player gets 7 cards each. The game follows basic Uno rules.
UNO RULES HERE: https://www.unorules.com/

-> Type Of Cards
Normal Card - Must match the top of the Discard Pile by number or colour
Swap Card - Will reverse the playing order. Must match the top of the Discard Pile by sign or colour.
Skip Card - Will skip the next person's turn. Must match the top of the Discard Pile by sign or colour.
2+ Card - The next player will pick up 2 cards. Must match the top of the Discard Pile by number or colour.
          If the previous one was also a 2+ card, the score will add up for the next player.
Wild Card - Allows the player to choose the next colour. Can be played on any type or colour.
4+ Wild Card - The next player picks up 4 cards and allows the current player to choose the next colour.
               Can be played on any type or colour.
"""

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
