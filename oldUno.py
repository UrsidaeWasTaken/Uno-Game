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
from random import SystemRandom

# Base Cards = Cards & Settings that'll be needed throughout the program
rand = SystemRandom()
colours = ["Red", "Yellow", "Green", "Blue"]
wild_cards = ["Wild 4+", "Wild"]
action_cards = ["Reverse", "Skip", "2+"]


# Settings - Sets the amount of players in the game
def game_settings():
    while True:
        player_count = input("\nSelect number of players: ")
        if player_count.isdigit():
            if 1 < int(player_count) < 5:
                return int(player_count)
            print("ERROR: %s is not allowed. Please select a number between 2-4..." % player_count)
        else:
            print("ERROR: Please enter a valid input between 2-4")


# Draw Card - Randomly generates a card
def get_card():
    colour, number = rand.choice(colours), rand.randint(1, 9)
    chance = rand.randint(1, 16)
    if chance == 1:
        card = rand.choice(wild_cards)
    elif chance >= 12:
        card = "%s %s" % (colour, rand.choice(action_cards))
    else:
        card = "%s %s" % (colour, number)
    return card


# Deal Cards - Deals 7 cards to each player
def deal_cards(player_count):
    starting_card = "%s %s" % (rand.choice(colours), rand.randint(1, 9))
    players = {}
    for x in range(player_count):
        cards = []
        for z in range(7):
            card = get_card()
            cards.append(card)
        players[x] = cards
    print("\n...loading...")
    sleep(1)
    return players, starting_card


# Choose Colour - Allows player to select new colour when wild card is used
def select_colour(cp):
    while True:
        colour_choice = (input("Select the new colour: ")).lower()
        if colour_choice == "blue":
            last_card = "Blue Wild"
            break
        elif colour_choice == "red":
            last_card = "Red Wild"
            break
        elif colour_choice == "green":
            last_card = "Green Wild"
            break
        elif colour_choice == "yellow":
            last_card = "Yellow Wild"
            break
        else:
            print("ERROR: Select either 'Yellow', 'Red', 'Green' or 'Blue'...")
    print("Player %s has changed the colour to %s!" % (str(cp + 1), colour_choice.title()))
    return last_card


# Base Game - The main game with all the relevant functions
def game(players, starting_card, player_count):
    playing = True
    current_player = 0
    last_card = starting_card
    is_reversed = False
    two_card, four_card = False, False
    multiplier = 0

    print("\n-=- STARTING GAME -=-")
    sleep(2)
    while playing:
        x = current_player
        print("\nIt is player %s's turn!" % str(current_player + 1))
        input("Press ENTER when you're ready!")
        print("Last Card: %s" % last_card)
        print("\n- YOUR CARDS -")
        for card in players[current_player]:
            print(card)
        player_turn = True
        while player_turn:
            player_choice = input("Choose a card to play or type 'SKIP' to pick up a card: ")
            if player_choice == "SKIP":
                if two_card or four_card:
                    print("You must pick up %s cards!\n" % str(multiplier))
                    sleep(1)
                    for i in range(multiplier):
                        card = get_card()
                        print("You picked up a '%s'!" % card)
                        players[current_player].append(card)
                    multiplier = 0
                    four_card, two_card = False, False
                    player_turn = False
                else:
                    card = get_card()
                    print("You picked up a '%s'!" % card)
                    players[current_player].append(card)
                    player_turn = False
            elif player_choice in players[current_player]:
                if "Wild" in player_choice:
                    if "4+" in player_choice:
                        multiplier += 4
                        four_card = True
                        last_card = select_colour(current_player)
                        players[current_player].remove(player_choice)
                    elif four_card or two_card:
                        print("You must pick up %s cards!\n" % str(multiplier))
                        sleep(1)
                        for i in range(multiplier):
                            card = get_card()
                            print("You picked up a '%s'!" % card)
                            players[current_player].append(card)
                        multiplier = 0
                        four_card, two_card = False, False
                    else:
                        last_card = select_colour(current_player)
                        players[current_player].remove(player_choice)
                    player_turn = False
                else:
                    compare = player_choice.split()
                    for word in compare:
                        if word in last_card:
                            player_turn = False
                            break
                    if player_turn:
                        print("ERROR: You must place down a card with the same colour, \
symbol or number as the last card.\n")
                    else:
                        if four_card:
                            print("You didn't place a 4+ card. You must pick up %s cards!\n" % str(multiplier))
                            sleep(1)
                            for i in range(multiplier):
                                card = get_card()
                                print("You picked up a '%s'!" % card)
                                players[current_player].append(card)
                            multiplier = 0
                            four_card, two_card = False, False
                        elif two_card:
                            if "2+" in player_choice:
                                multiplier += 2
                                last_card = player_choice
                                players[current_player].remove(last_card)
                            else:
                                print("You didn't place a 2+ card. You must pick up %s cards!\n" % str(multiplier))
                                sleep(1)
                                for i in range(multiplier):
                                    card = get_card()
                                    print("You picked up a '%s'!" % card)
                                    players[current_player].append(card)
                                multiplier = 0
                                two_card = False
                        else:
                            last_card = player_choice
                            players[current_player].remove(last_card)
                            if "Reverse" in player_choice:
                                is_reversed = not is_reversed
                            elif "Skip" in player_choice:
                                if is_reversed:
                                    current_player -= 1
                                else:
                                    current_player += 1
                            elif "2+" in player_choice:
                                multiplier += 2
                                two_card = True
                            else:
                                pass
            else:
                print("INVALID OPTION\n")

            if not players[x]:
                print("\nCONGRATULATIONS PLAYER %s! YOU ARE THE WINNER!!!" % str(x + 1))
                sleep(3)
                print("...returning to menu...")
                return None
            elif len(players[x]) == 1:
                print("\nPlayer %s has UNO!" % str(x + 1))
                sleep(1)

            if is_reversed:
                current_player -= 1
                if current_player < 0:
                    current_player = current_player % player_count
            else:
                current_player = (current_player + 1) % player_count


# Play - All functions used once the game is started (Setting up, creating and playing game)
def uno_game():
    player_count = game_settings()
    players, sc = deal_cards(player_count)
    game(players, sc, player_count)
    return None


# Help Pg. 4 - Page 4 of the helper function
def page_4():
    while True:
        sleep(.5)
        print("\n-=- UNO: OVERVIEW  -=-")
        print("When you start the game, you will need to set the number of players from 2-4. Each player will have their\n\
cards shown to them on their turn. You must type the EXACT name of the card you want to play.\n\
If you don't have a card to play or don't want to play a card, type 'SKIP' to pick up a card instead. The game\n\
continues as explained until someone has won.")
        page_choice = (input("> Prev\n> Exit\n")).lower()
        if page_choice == "exit":
            return "exit"
        elif page_choice == "prev" or page_choice == "previous" or page_choice == "back":
            return


# Help Pg. 3 - Page 3 of the helper function
def page_3():
    while True:
        sleep(.5)
        print("\n-=- UNO: OVERVIEW  -=-")
        print("Uno has a variety of cards in 4 colours (Red, Blue, Yellow and Green), all of which does different things that can change the game.\n")
        print("- NORMAL CARD -\nThese cards can only be played if the colour and/or symbol matches the previous card.\n")
        print("NORMAL - These cards consist of a number and a colour (For example: 'Yellow 5'). They do not do anything special.\n\
REVERSE - These cards consist of a colour and REVERSE tag (For example: 'Yellow Reverse'). They reverse the order of play.\n\
SKIP - These cards consist of a colour and SKIP tag (For example: 'Yellow Skip'). They skip the next player's turn\n\
DRAW 2 - These cards consist of a colour and 2+ tag (For example: 'Yellow 2+'). The next player has to skip their turn and\n\
pick up 2 cards. If the next player also plays a 2+ card or a Wild 4+ card, they can play it and the total is added up and sent to the next player\n\
until someone no longer has a 2+ or 4+ card; they will have to pick up the final total amount.\n\n")
        print("- WILD CARD -\n These cards can be played on any colour or number.\n")
        print("WILD - These cards consist of a WILD tag (For example: Wild). The player can choose a new colour, the game will continue with the colour they chose.\n\
WILD DRAW 4 - These cards consist of a WILD and 4+ tag (For example: Wild 4+). The player can choose a new colour, the game will continue with the colour they chose.\n\
The next player also has to skip their turn and pick up 4 cards. If the next player also plays a 4+ card,\n\
the total is added up and sent to the next player until someone no longer has a 4+ card; they will have to pick up the final total amount.\n\n")
        print("(Note: You cannot deflect a 2+ or 4+ card with a Wild Card that isn't 4+, you will still need to pick up the total amount given.\n")
        page_choice = (input("> Next\n> Prev\n> Exit\n")).lower()
        if page_choice == "next":
            if page_4() == "exit":
                return "exit"
        elif page_choice == "exit":
            return "exit"
        elif page_choice == "prev" or page_choice == "previous" or page_choice == "back":
            return


# Help Pg. 2 - Page 2 of the helper function
def page_2():
    while True:
        sleep(.5)
        print("\n-=- UNO: OVERVIEW  -=-")
        print("Each player gets given 7 cards. Each card has a colour and symbol/number.\n\
The first player will start by placing a card that matches either the colour or symbol of the starting card (picked at random).\n\
The next player will then have to place a card that matches either the colour or symbol of the previous card and so on.\n")
        print("If a player does not have a card that matches the previous card played. They must pick up a new card and their turn is skipped.")
        page_choice = (input("> Next\n> Prev\n> Exit\n")).lower()
        if page_choice == "next":
            if page_3() == "exit":
                return "exit"
        elif page_choice == "exit":
            return "exit"
        elif page_choice == "prev" or page_choice == "previous" or page_choice == "back":
            return


# Help Pg. 1 - Page 1 of the helper function
def page_1():
    while True:
        sleep(.5)
        print("\n-=- UNO: OVERVIEW -=-")
        print("WELCOME TO UNO! In this game, the objective is to get rid of all your cards before anyone else does.\n\
You have a variety of different cards you can use to slow down your opponents and boost yourself further.\n")
        page_choice = (input("> Next\n> Exit\n")).lower()
        if page_choice == "next":
            if page_2() == "exit":
                return
        elif page_choice == "exit":
            return


# Main Menu - Allows the player to select 'Play' or 'Quit
print("...starting game...")
sleep(2)
in_menu = True

while in_menu:
    print("\n-=- UNO -=-\nO Play\nO Help\nO Quit\n")
    menu_option = (input("Select Option: ")).lower()
    if menu_option == "play":
        uno_game()
    elif menu_option == "quit":
        print("THANKS FOR PLAYING!")
        break
    elif menu_option == "help":
        page_1()
    else:
        print("INVALID OPTION\nPlease select 'Play', 'Help' or 'Quit'.")
