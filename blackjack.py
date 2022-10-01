#!/usr/bin/env python3
# Joshua Elmer
# CPSC 386-04
# 2022-04-04
# joshuaelmer@csu.fullerton.edu
# @Joshua-El
#
# Lab 03-00
#
# This is the file that will be runnable
# It is kept as a simple file to run the game
#

"""This is the main program that will run the blackjack game"""

from blackjackgame import game


def main():
    """The game will now be run"""
    blackjack_game = game.BlackjackGame()
    return blackjack_game.run()


if __name__ == "__main__":
    main()
