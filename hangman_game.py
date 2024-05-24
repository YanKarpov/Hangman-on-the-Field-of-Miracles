import random
import time
import pygame
import json

# Загрузка списка слов из файла JSON
def load_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = json.load(file)
    random.shuffle(words)  # Перемешиваем слова для случайного выбора
    return words

# Получение слова и его описания из списка
def get_word_and_description(words):
    if not words:
        return None, None
    word_desc_pair = words.pop()  # Берем слово из конца списка
    return word_desc_pair['word'], word_desc_pair['description']

# Создание скрытой таблицы для слова
def create_hidden_table(word):
    return ['■' for _ in word]

# Получение начального количества жизней
def get_initial_lives():
    return 7

# Проверка, жив ли игрок
def is_player_alive(lives):
    return lives > 0

# Отображение скрытой таблицы
def display_table(table):
    print(" ".join(table))

# Получение ввода от пользователя
def user_input(message):
    return input(message).lower()

# Проверка, верно ли угадано слово
def is_guess_correct(word, guess):
    return word.lower() == guess.lower()

# Отображение изображения виселицы
def display_hangman(stage):
    hangman_stages_folder = "hangman_pictures"
    file_path = f'{hangman_stages_folder}/hangman_{stage}.txt'
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        pass  

def load_text_from_file(folder, filename):
    with open(f'{folder}/{filename}', 'r', encoding='utf-8') as file:
        return file.read()

def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)

def introduction_dialogue():
    introduction_text = load_text_from_file('Game_texts', 'introduction.txt')
    for char in introduction_text:
        print(char, end='', flush=True)
        time.sleep(0.01)

    response = user_input("\n(Да/Нет): ")
    return response == "да"

def outro_dialogue():
    outro_text = load_text_from_file('Game_texts', 'outro.txt')
    for char in outro_text:
        print(char, end='', flush=True)
        time.sleep(0.05)

# Функция обработки попытки угадать букву
def handle_single_letter_guess(guess, current_word, table, lives, stage):
    if guess in current_word:
        for i, letter in enumerate(current_word):
            if letter.lower() == guess:
                table[i] = letter
        if guess not in ''.join(table):
            print("Поздравляю, странник! Ты угадал слово и спас душу несчастного!")
    else:
        lives -= 1
        display_hangman(stage)
        print(f"Неверная буква! У вас осталось {lives} {'жизней' if lives != 1 else 'жизнь'}.")
    return lives

# Функция обработки попытки угадать слово
def handle_full_word_guess(guess, current_word, table, lives, stage):
    if is_guess_correct(current_word, guess):
        table = list(current_word)
        display_table(table)
    else:
        lives = 0
        display_hangman(stage)
        print(f"Игра окончена. Загаданное слово было: {current_word}")
    return lives

def play_single_game(words):
    if not words:
        print("Слова не найдены. Проверьте, что список слов на месте")
        return

    while True:
        current_word, description = get_word_and_description(words)
        if current_word is None:
            print("Сброс не удался, попробуйте снова...")
            if not restart_game(words):
                print("Увидимся, путешественник!")
                return False
            continue

        play_background_music()
        if not introduction_dialogue():
            outro_dialogue()
            return

        table = create_hidden_table(current_word)
        lives = get_initial_lives()
        stage = 0
        guessed_word = False

        print("Подсказка:", description)

        while is_player_alive(lives) and not guessed_word:
            display_table(table)
            guess = user_input("Назови мне одну букву или слово целиком: ")

            if len(guess) == 1 and guess.isalpha():  
                if guess in current_word:
                    for i, letter in enumerate(current_word):
                        if letter.lower() == guess:
                            table[i] = letter
                    if is_guess_correct(current_word, ''.join(table)):
                        print("Поздравляю, странник! Ты угадал слово и спас душу несчастного!")
                        guessed_word = True
                else:
                    lives -= 1
                    display_hangman(stage)
                    print(f"Неверная буква! У вас осталось {lives} {'жизней' if lives != 1 else 'жизнь'}.")
                    stage += 1
                    if lives == 0:
                        break
            elif len(guess) == len(current_word) and guess.isalpha():  
                if is_guess_correct(current_word, guess):
                    table = list(current_word)  
                    display_table(table)
                    print("Поздравляю, странник! Ты угадал слово и спас душу несчастного!")
                    guessed_word = True
                else:
                    lives = 0  
            else:
                print("Мхм, я тебя не совсем расслышал... Назови мне букву, либо если уверен всё слово.")

        if not guessed_word:
            display_hangman(stage)
            print(f"Игра окончена. Загаданное слово было: {current_word}")

        if not replay_game_prompt():
            break
def replay_game_prompt():
    replay = user_input("Хотите попытаться снова? (Да/Нет): ")
    return replay.lower() == 'да'

def restart_game(words):
    reset_words = user_input("Хотите перезапустить? (Да/Нет): ").lower()
    if reset_words == 'да':
        print("Произвожу сброс последнего сохранения... начинаем игру сначала!")
        random.shuffle(words)
        return True





