#!/usr/bin/env python3
# Joshua Elmer
# CPSC 386-04
# 2022-04-04
# joshuaelmer@csu.fullerton.edu
# @Joshua-El
#
#
#
# This is the file that will hold the functionality for the game itself
#

"""This is the game. All functionality for the game is coded here"""
from time import sleep
import pickle
from blackjackgame import player


class BlackjackGame:
    """The game's class"""

    def __init__(self):
        """Initialization"""
        self._players = []
        self._game_is_not_over = True

    def to_file(self, pickle_file, players):
        """Write the list players to the file pickle_file."""
        with open(pickle_file, 'wb') as file_handle:
            pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)

    def from_file(self, pickle_file):
        """Read the contents of pickle_file, decode it, and return it as players."""
        with open(pickle_file, 'rb') as file_handle:
            players = pickle.load(file_handle)
        return players

    def check_for_user(self, unique_id):
        """Checks the pickle file to find the returning user's information"""
        player_list = self.from_file("players.pickl")
        for _ in player_list:
            if _.unique_id == unique_id:
                return _
        failure = player.Player("failed", "failed")
        return failure

    def display_hand(self, crr_player):
        """prints out player's hand"""
        print("Player {}'s hand:".format(crr_player.name), end=" ")
        for _ in range(len(crr_player.hand)):
            if _ == len(crr_player.hand) - 1:
                print("{}".format(crr_player.hand[_][0]))
            else:
                print("{}".format(crr_player.hand[_][0]), end=", ")

    def display_split_hand(self, crr_player):
        """prints out player's split hand"""
        print("Player {}'s split hand:".format(crr_player.name), end=" ")
        for _ in range(len(crr_player.split_hand)):
            if _ == len(crr_player.hand) - 1:
                print("{}".format(crr_player.split_hand[_][0]))
            else:
                print("{}".format(crr_player.split_hand[_][0]), end=", ")

    def display_dealer_hand(self, dealer):
        """Prints out dealer's hand hiding second card"""
        print("Dealer {}'s hand: ".format(dealer.name), end=" ")
        print("{}, Card Face Down".format(dealer.hand[0][0]))

    def hand_score(self, crr_player):
        """Returns the player's score"""
        crr_player.score = 0
        crr_player.ace = False
        for _ in range(len(crr_player.hand)):
            temp_score = int(crr_player.hand[_][0])
            if temp_score == 1 and crr_player.ace is False:
                temp_score += 10
                crr_player.ace = True
            crr_player.score += temp_score
        return crr_player.score

    def split_hand_score(self, crr_player):
        """Returns the player's score for their split hand"""
        crr_player.split_score = 0
        crr_player.split_ace = False
        for _ in range(len(crr_player.split_hand)):
            temp_score = int(crr_player.split_hand[_][0])
            if temp_score == 1 and crr_player.split_ace is False:
                temp_score += 10
                crr_player.split_ace = True
            crr_player.split_score += temp_score
        return crr_player.split_score

    def player_wins(self, crr_player):
        """Outputs player's winnings"""
        crr_player.balance += 2 * crr_player.wager
        print(
            "Congradulations Player {}, you won {}!!! your new balance"
            " is ${}".format(
                crr_player.name, 2 * crr_player.wager, crr_player.balance
            )
        )
        sleep(1)

    def split_player_wins(self, crr_player):
        """Outputs player's winnings"""
        crr_player.balance += 2 * crr_player.split_wager
        print(
            "Congradulations Player {}, you won {} with your split hand!!!"
            " Your new balance is ${}".format(
                crr_player.name, 2 * crr_player.split_wager, crr_player.balance
            )
        )
        sleep(1)

    def reset_data(self, crr_player):
        """Resets all necessary data for next loop"""
        crr_player.hand.clear()
        crr_player.split_hand.clear()
        crr_player.score = 0
        crr_player.split_score = 0
        crr_player.ace = False
        crr_player.split_ace = False
        crr_player.bust = False
        crr_player.split_bust = False
        crr_player.double = False
        crr_player.split_double = False
        crr_player.insurance = 0

    def run(self):
        """Function to run the game"""
        num_players = int(input("Number of players 1-4: "))
        num_players += 1
        for _ in range(num_players - 1):
            # loop through the number of players to add them into the game
            while True:
                # this loop ensures that the game doesn't crash if an incorrect id is entered
                returning_player = input(
                    "Have you played here before? (yes/no): "
                )
                if returning_player in ("yes", "y"):
                    player_id = input(
                        "Welcome back, please enter your unique identifier: "
                    )
                    check_player = self.check_for_user(player_id)
                    if (
                        check_player.name == "failed"
                        and check_player.unique_id == "failed"
                    ):
                        print(
                            "Sorry, we were unable to find a record of a player with that id"
                        )
                    else:
                        self._players.append(check_player)
                        break
                else:
                    name = input("Please enter your name: ")
                    player_id = input(
                        "Please also enter a unique identifier that can be used to "
                        "identify that it is you in the future.\nSome examples could be and email "
                        "address or a password that you feel is unique: "
                    )
                    self._players.append(player.Player(name, player_id))
                    break
        self._players.append(player.Dealer())
        current_player_index = 0
        dealer = self._players[len(self._players) - 1]
        dealer.prepare_deck()
        while self._game_is_not_over:
            # The main game loop
            for _ in range(num_players - 1):
                # loop though each player to get their bet
                crr_player = self._players[current_player_index]
                while True:
                    # This loop ensures that a player does not bet more than their balance
                    crr_player.wager = int(
                        input(
                            "{}, what would you like to bet? $".format(
                                crr_player.name
                            )
                        )
                    )
                    if crr_player.wager > crr_player.balance:
                        print(
                            "Wager exceeds your current balance. Please try again."
                        )
                    else:
                        break
                sleep(1)
                crr_player.balance -= crr_player.wager
                current_player_index += 1
            current_player_index = 0
            for _ in range(num_players * 2):
                # loop through the players twice to deal them each two cards one card at a time
                crr_player = self._players[current_player_index]
                dealer.deal_to(crr_player.hand)
                current_player_index += 1
                if current_player_index == num_players:
                    current_player_index = 0
                if crr_player == dealer and len(dealer.hand) > 1:
                    self.display_dealer_hand(dealer)
                    sleep(1)
                else:
                    self.display_hand(crr_player)
                    sleep(1)
                if crr_player != dealer and len(dealer.hand) == 1:
                    if self.hand_score(dealer) > 9:
                        print(
                            "The Dealer {} is showing {}.".format(
                                dealer.name, dealer.hand[0][0]
                            )
                        )
                        sleep(1)
                        while True:
                            # this loop ensures that a player does not make an insurance bet exceeding their balance
                            insurance = input(
                                "Would you like to make an insurance bet yes/no: "
                            ).lower()
                            sleep(1)
                            if insurance in ("yes", "y"):
                                insurance_wager = int(
                                    input(
                                        "what would you like to bet for insurance? $"
                                    )
                                )
                                if insurance_wager > crr_player.balance:
                                    print(
                                        "Wager exceeds balance. Please try again"
                                    )
                                else:
                                    crr_player.insurance = insurance_wager
                                    crr_player.balance -= crr_player.insurance
                                    break
                sleep(2)
                if (
                    len(crr_player.hand) > 1
                    and crr_player.hand[0][0][0] == crr_player.hand[1][0][0]
                ):
                    if crr_player.would_you_like_to_split():
                        # handles the act of splitting a hand
                        crr_player.split_hand.append(crr_player.hand.pop(1))
                        crr_player.split_wager = crr_player.wager
                        crr_player.balance -= crr_player.wager
                        dealer.deal_to(crr_player.hand)
                        dealer.deal_to(crr_player.split_hand)
                        self.display_hand(crr_player)
                        self.display_split_hand(crr_player)
            current_player_index = 0
            for _ in range(num_players - 1):
                # loops through te players to have them take their turn
                crr_player = self._players[current_player_index]
                print("It is {}'s turn:".format(crr_player.name))
                sleep(0.5)
                self.display_hand(crr_player)
                sleep(1)
                print("Your score is {}".format(self.hand_score(crr_player)))
                sleep(0.5)
                print("The dealer is showing a {}".format(dealer.hand[0][0]))
                sleep(0.5)
                while crr_player.hit_or_stand() and not crr_player.bust:
                    # this is the loop to continue the offer to hit or stand
                    dealer.deal_to(crr_player.hand)
                    self.display_hand(crr_player)
                    sleep(1)
                    card_index = len(crr_player.hand) - 1
                    temp_value = int(crr_player.hand[card_index][0])
                    if temp_value == 1 and crr_player.score + 11 < 21:
                        # this handles the value of an ace being 1 or 11
                        temp_value += 10
                        crr_player.ace = True
                    crr_player.score += temp_value
                    if crr_player.score > 21 and crr_player.ace is True:
                        # this changed an ace back to a 1 if the player would otherwise bust
                        crr_player.score -= 10
                        crr_player.ace = False
                    print("Your score is {}".format(crr_player.score))
                    sleep(0.5)
                    if crr_player.score > 21:
                        print("Uh oh you busted, your turn is over")
                        sleep(2)
                        crr_player.bust = True
                        break
                    if crr_player.double is True:
                        break
                if crr_player.split_wager != 0:
                    # allows the player to now play their split hand
                    print("It is still {}'s turn:".format(crr_player.name))
                    sleep(0.5)
                    self.display_split_hand(crr_player)
                    sleep(1)
                    print(
                        "Your score for split hand is {}".format(
                            self.split_hand_score(crr_player)
                        )
                    )
                    sleep(0.5)
                    print(
                        "The dealer is showing a {}".format(dealer.hand[0][0])
                    )
                    sleep(0.5)
                    while (
                        crr_player.split_hit_or_stand()
                        and not crr_player.split_bust
                    ):
                        dealer.deal_to(crr_player.split_hand)
                        self.display_split_hand(crr_player)
                        sleep(1)
                        card_index = len(crr_player.split_hand) - 1
                        temp_value = int(crr_player.split_hand[card_index][0])
                        if temp_value == 1 and crr_player.split_score + 11 < 21:
                            # manages the ace value for split hand
                            temp_value += 10
                            crr_player.split_ace = True
                        crr_player.split_score += temp_value
                        if (
                            crr_player.split_score > 21
                            and crr_player.split_ace is True
                        ):
                            # returns the aces value to a 1 if the player would
                            # otherwise bust for the split hand
                            crr_player.split_score -= 10
                            crr_player.split_ace = False
                        print("Your score is {}".format(crr_player.split_score))
                        sleep(0.5)
                        if crr_player.split_score > 21:
                            print("Uhoh you busted, your turn is over")
                            sleep(2)
                            crr_player.split_bust = True
                            break
                        if crr_player.split_double is True:
                            break
                current_player_index += 1
            current_player_index = 0
            print("It is the dealer {}'s turn:".format(dealer.name))
            self.display_hand(dealer)
            sleep(1)
            print("making a total score of {}".format(self.hand_score(dealer)))
            sleep(0.5)
            while dealer.hit_or_stand():
                # loop to run for the dealers turn
                dealer.deal_to(dealer.hand)
                self.display_hand(dealer)
                sleep(0.5)
                card_index = len(dealer.hand) - 1
                temp_value = int(dealer.hand[card_index][0])
                if temp_value == 1 and dealer.score + 11 < 21:
                    # handles ace value being 1 or 11 for the dealer
                    temp_value += 10
                    dealer.ace = True
                dealer.score += temp_value
                dealer.score += temp_value
                if dealer.score > 21 and dealer.ace is True:
                    # returns the ace value to a 1 if the dealer would otherwise bust
                    dealer.score -= 10
                    dealer.ace = False
                print("making a total score of {}".format(dealer.score))
                sleep(0.5)
                if dealer.score > 21:
                    print("The Dealer has busted!!")
                    sleep(2)
                    dealer.bust = True
            for _ in range(num_players - 1):
                # loop to determine if a player won/lost/pushed
                crr_player = self._players[current_player_index]
                if crr_player.insurance != 0:
                    if len(dealer.hand) == 2 and dealer.score == 21:
                        # manages the insurance bet win/loss
                        print(
                            "Player {} you have won your insurance bet".format(
                                crr_player.name
                            )
                        )
                        sleep(1)
                        crr_player.balance += 2 * crr_player.insurance
                    else:
                        print(
                            "Player {} you have lost your insurance bet".format(
                                crr_player.name
                            )
                        )
                        sleep(1)
                if crr_player.bust:
                    # if the player busted they lose
                    print(
                        "Player {} you have lost. Your remaining balance is ${}".format(
                            crr_player.name, crr_player.balance
                        )
                    )
                    sleep(1)
                elif dealer.bust:
                    # if the dealer busted the player that has not busted wins
                    self.player_wins(crr_player)
                elif dealer.score < crr_player.score:
                    # if neither dealer nor player busted than the
                    # player wins if they have a higher score
                    self.player_wins(crr_player)
                elif dealer.score == crr_player.score:
                    # if neither dealer nor player busted than the
                    # player pushes if they are tied with dealer
                    crr_player.balance += crr_player.wager
                    print(
                        "Player {} pushed with dealer {}. Your wager has been returned and your"
                        " current balance is still ${}".format(
                            crr_player.name, dealer.name, crr_player.balance
                        )
                    )
                    sleep(1)
                else:
                    # if they have not won/pushed/busted and the
                    # dealer has not busted then they lose
                    print(
                        "Player {} you have lost. Your remaining balance is ${}".format(
                            crr_player.name, crr_player.balance
                        )
                    )
                    sleep(1)
                if crr_player.split_wager != 0:
                    # checks win/lose/push conditions for split hand
                    if crr_player.split_bust:
                        # player loese if they busted for split hand
                        print(
                            "Player {} you have lost with your split hand. Your remaining balance is ${}".format(
                                crr_player.name, crr_player.balance
                            )
                        )
                        sleep(1)
                    elif dealer.bust:
                        # if dealer busted the player wins for split hand
                        self.split_player_wins(crr_player)
                    elif dealer.score < crr_player.split_score:
                        # player wins their split hand if they have the
                        # higher score and neither have busted
                        self.split_player_wins(crr_player)
                    elif dealer.score == crr_player.split_score:
                        # the players split hand pushes the dealer if neither have busted
                        crr_player.balance += crr_player.split_wager
                        print(
                            "Player {} pushed with dealer {} with your split hand. Your "
                            "wager has been returned and your current balance is still {}".format(
                                crr_player.name, dealer.name, crr_player.balance
                            )
                        )
                        sleep(1)
                    else:
                        # the player loses their split hand if
                        # they have not won/pushed/busted
                        print(
                            "Player {} you have lost with your split hand. Your remaining balance is ${}".format(
                                crr_player.name, crr_player.balance
                            )
                        )
                        sleep(1)
                sleep(1)
                self.reset_data(crr_player)
                current_player_index += 1
            current_player_index = 0
            dealer.check_shoe()
            self.reset_data(dealer)
            stop_playing = input(
                "Would you like to play again? (yes/no): "
            ).lower()
            if stop_playing not in ("yes", "y"):
                self._game_is_not_over = False
            try:
                # trys to write to pickle file
                saved_players = self.from_file("players.pickl")
                saved_counter = 0
                for first in saved_players:
                    # loops through the files list of players
                    saved_counter += 1
                    for second in self._players:
                        # compares them to the games list of players and if
                        # they match it removes the payer from the file
                        if first.unique_id == second.unique_id:
                            saved_players.pop(saved_counter - 1)
                for _ in self._players:
                    # stores the games players data at the end of the file
                    saved_players.append(_)
                self.to_file("players.pickl", saved_players)
            except (OSError, IOError) as error:
                # if the file does not exist it will create the file
                pickle.dump(self._players, open("players.pickl", "wb"))
