#!/usr/bin/env python3
# Joshua Elmer
# CPSC 386-04
# 2022-04-04
# joshuaelmer@csu.fullerton.edu
# @Joshua-El
#
#
#
# This is the file that will hold the functionality for cards
#

"""The card functionality will be initialized here"""
from collections import namedtuple
from random import shuffle, randrange
from math import floor

Card = namedtuple("Card", ["rank", "suit"])


def pretty_print_card(card):
    """Prints out the card in a nice format"""
    return "{} of {}".format(card.rank, card.suit)


Card.__str__ = pretty_print_card


class Deck:
    """This is the Deck Class that will make decks of cards"""

    ranks = (
        ["Ace"] + list(map(str, list(range(2, 11)))) + "Jack Queen King".split()
    )
    suits = "Clubs Hearts Spades Diamonds".split()
    values = list(range(1, 11)) + [10, 10, 10]
    value_dict = dict(zip(ranks, values))

    def __init__(self):
        self._cards = [
            Card(rank, suit) for rank in Deck.ranks for suit in Deck.suits
        ]

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)

    def merge(self, the_other_deck):
        """This merges different decks together"""
        self._cards = self._cards + the_other_deck._cards

    def cut(self):
        """This will cut a deck of cards"""
        percent = floor(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + randrange(-percent, percent)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def shuffle(self, num_shuffles=1):
        """This function shuffles a deck of cards"""
        for _ in range(num_shuffles):
            shuffle(self._cards)

    def deal(self, num_cards=1):
        """This function deals a card from the deck"""
        return [self._cards.pop(0) for _ in range(num_cards)]

    def __str__(self):
        return "\n".join(
            ["{} {}".format(i, j) for i, j in enumerate(self._cards)]
        )


def convert_card_to_int(card):
    """Converts card values into integers"""
    return Deck.value_dict[card.rank]


Card.__int__ = convert_card_to_int
