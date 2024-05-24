from hangman_game import play_single_game
import json

if __name__ == "__main__":
    with open('words.json', 'r', encoding='utf-8') as file:
     words = json.load(file)
    play_single_game(words)