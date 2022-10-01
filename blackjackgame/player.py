#!/usr/bin/env python3
# Joshua Elmer
# CPSC 386-04
# 2022-04-04
# joshuaelmer@csu.fullerton.edu
# @Joshua-El
#
#
#
# This is the file that will hold the functionality for Players
#

"""This is where the Player functions will all be defined"""
from time import sleep
from random import randrange
from blackjackgame import cards


class Player:
    """The Player Class creation"""

    def __init__(self, name, unique_id):
        """Initialization"""
        self._name = name
        self._unique_id = unique_id
        self._score = 0
        self._split_score = 0
        self._hand = []
        self._split_hand = []
        self._wager = 0
        self._split_wager = 0
        self._insurance = 0
        self._balance = 10000
        self._bust = False
        self._split_bust = False
        self._ace = False
        self._split_ace = False
        self._double = False
        self._split_double = False

    @property
    def name(self):
        """Getter function for name"""
        return self._name

    @property
    def unique_id(self):
        """Getter function for unique_id"""
        return self._unique_id

    @property
    def score(self):
        """Getter function for score"""
        return self._score

    @property
    def split_score(self):
        """Getter function for split_score"""
        return self._split_score

    @property
    def split_hand(self):
        """Getter function for split_hand"""
        return self._split_hand

    @property
    def hand(self):
        """Getter function for hand"""
        return self._hand

    @property
    def balance(self):
        """Getter function for balance"""
        return self._balance

    @property
    def wager(self):
        """Getter function for wager"""
        return self._wager

    @property
    def split_wager(self):
        """Getter function for split_wager"""
        return self._split_wager

    @property
    def insurance(self):
        """Getter function for insurance"""
        return self._insurance

    @property
    def bust(self):
        """Getter function for bust"""
        return self._bust

    @property
    def split_bust(self):
        """Getter function for bust for the split hand"""
        return self._split_bust

    @property
    def ace(self):
        """Getter function for ace"""
        return self._ace

    @property
    def split_ace(self):
        """Getter function for ace"""
        return self._split_ace

    @property
    def double(self):
        """Getter function for double"""
        return self._double

    @property
    def split_double(self):
        """Getter function for double for the split hand"""
        return self._split_double

    @hand.setter
    def hand(self, new_card):
        self._hand.append(new_card)

    @split_hand.setter
    def split_hand(self, new_card):
        self._split_hand.append(new_card)

    @balance.setter
    def balance(self, new_balance):
        self._balance = new_balance

    @wager.setter
    def wager(self, new_wager):
        self._wager = new_wager

    @split_wager.setter
    def split_wager(self, new_wager):
        self._split_wager = new_wager

    @insurance.setter
    def insurance(self, new_insurance):
        self._insurance = new_insurance

    @score.setter
    def score(self, new_score):
        self._score = new_score

    @split_score.setter
    def split_score(self, new_score):
        self._split_score = new_score

    @bust.setter
    def bust(self, new_value):
        self._bust = new_value

    @split_bust.setter
    def split_bust(self, new_value):
        self._split_bust = new_value

    @ace.setter
    def ace(self, new_value):
        self._ace = new_value

    @split_ace.setter
    def split_ace(self, new_value):
        self._split_ace = new_value

    @double.setter
    def double(self, new_double):
        self._double = new_double

    @split_double.setter
    def split_double(self, new_double):
        self._split_double = new_double

    def hit_or_stand(self):
        """Function to ask players to double, hit or stand"""
        if len(self.hand) < 3:
            # ensures that the player can only double if they have 2 cards
            while True:
                # loop to ensure if the player doubles they have the balance to do so
                response = input("Do you want to double/hit/stand?").lower()
                if response == "d" or response == "double":
                    if self._wager > self._balance:
                        print(
                            "you do not have the funds to double. Please choose another option"
                        )
                    else:
                        self._double = True
                        self._balance -= self._wager
                        self._wager += self._wager
                        return True
                if response == "h" or response == "hit":
                    return True
                else:
                    return False
        else:
            response = input("Do you want to hit/stand?").lower()
            if response == "h" or response == "hit":
                return True
        return False

    def split_hit_or_stand(self):
        """Function to ask players to double, hit or stand for their split hand"""
        if len(self.split_hand) < 3:
            # ensures that the player can only double if they have 2 cards
            while True:
                # loop to ensure if the player doubles they have the balance to do so
                response = input("Do you want to double/hit/stand?").lower()
                sleep(0.5)
                if response == "d" or response == "double":
                    if self._split_wager > self._balance:
                        print(
                            "you do not have the funds to double. Please choose another option"
                        )
                    else:
                        self._split_double = True
                        self._balance -= self._split_wager
                        self._split_wager += self._split_wager
                        return True
                if response == "h" or response == "hit":
                    return True
                else:
                    return False
        else:
            response = input("Do you want to hit/stand?").lower()
            sleep(0.5)
            if response == "h" or response == "hit":
                return True
        return False

    def would_you_like_to_split(self):
        """Function to ask players to split"""
        response = input("Do you want to split your hand? yes/no: ").lower()
        sleep(0.5)
        if response == "yes" or response == "y":
            if self._wager > self._balance:
                # if the player does not have the balance to split they are not allowed to
                print("Sorry, you do not have the funds to split.")
                return False
            return True
        return False

    def __str__(self):
        return self._name


class Dealer(Player):
    """The Dealer subclass creation"""

    def __init__(self, num_decks=8):
        super().__init__("Ray Babbitt", "dealer")
        self._deck = cards.Deck()
        self._cut_card_postition = 0
        for _ in range(num_decks - 1):
            self._deck.merge(cards.Deck())

    def deal_to(self, hand):
        """Dealer function to deal cards to players"""
        hand.append(self._deck.deal())

    def prepare_deck(self):
        """Dealer function to shuffle and cut deck"""
        self._deck.shuffle()
        self._deck.cut()
        self._cut_card_postition = randrange(60, 81)

    def hit_or_stand(self):
        """Defining when the dealer hits or stands"""
        if self.score < 17:
            return True
        return False

    def would_you_like_to_split(self):
        return False

    def check_shoe(self):
        """Check to see if the dealer has reached the cut\
            card, if so re-prepare the shoe"""
        if len(self._deck) <= self._cut_card_postition:
            self._deck.clear()
            self._deck = cards.Deck()
            for _ in range(7):
                self._deck.merge(cards.Deck())
            self._deck.shuffle()
            self._deck.cut()
            self._cut_card_postition = randrange(60, 81)
