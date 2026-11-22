"""Run the game: python main.py"""
from cards import CHARACTERS
from player import Player
from game import Game
from utils import ask_yes_no, ask_num_players

def main():
    print("Kimberly Harding CS670 Project 2")
    print("Welcome to Cluedo")

    if not ask_yes_no("Would you like to play? (y/n) "):
        print("Goodbye!")
        return

    num_players = ask_num_players()
    players = [Player(f"Player {i + 1}", CHARACTERS[i]) for i in range(num_players)] 
    game = Game(players)

    game.play()

if __name__ == "__main__":
    main()