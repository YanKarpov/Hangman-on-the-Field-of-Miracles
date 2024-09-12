from PyQt6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QTextEdit, QStackedWidget, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.game_logic import load_words, get_word_and_description, create_hidden_word, update_hidden_word
from src.data_loader import load_json_data, load_stylesheet
from src.main_menu import MainMenu  
from src.settings_menu import SettingsMenu  

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

class HangmanGame(QWidget):
    def __init__(self, parent=None, words=None, hangman_stages=None):
        super().__init__(parent)
        self.words = words
        self.hangman_stages = hangman_stages
        self.initUI()
        self.start_new_game()

    def initUI(self):
        layout = QVBoxLayout()

        self.hangman_text = QTextEdit(self)
        self.hangman_text.setReadOnly(True)
        self.hangman_text.setFont(QFont('Courier', 18))
        self.hangman_text.setStyleSheet("background-color: #f0f0f0; border: 2px solid #000;")
        self.hangman_text.setText(self.get_hangman_stage(0))
        layout.addWidget(self.hangman_text)

        self.word_label = QLabel(" ", self)
        self.word_label.setFont(QFont('Arial', 20))
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.word_label)

        self.description_label = QLabel("", self)
        self.description_label.setFont(QFont('Arial', 16))
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet("color: #555; padding: 10px;")
        layout.addWidget(self.description_label)

        self.buttons_layout = QGridLayout()
        layout.addLayout(self.buttons_layout)
        self.create_alphabet_buttons()

        self.new_game_button = QPushButton("Новая игра", self)
        self.new_game_button.setFont(QFont('Arial', 14))
        self.new_game_button.clicked.connect(self.start_new_game)
        layout.addWidget(self.new_game_button)

        self.back_to_menu_button = QPushButton("Главное меню", self)
        self.back_to_menu_button.setFont(QFont('Arial', 14))
        self.back_to_menu_button.clicked.connect(self.back_to_menu)
        layout.addWidget(self.back_to_menu_button)

        self.setLayout(layout)

    def create_alphabet_buttons(self):
        for index, letter in enumerate(ALPHABET):
            button = QPushButton(letter.upper(), self)
            button.setFont(QFont('Arial', 14))
            button.setFixedSize(40, 40)
            button.clicked.connect(self.handle_letter_click)
            self.buttons_layout.addWidget(button, index // 8, index % 8)

    def get_hangman_stage(self, stage):
        return self.hangman_stages[stage] if 0 <= stage < len(self.hangman_stages) else "Ошибка загрузки изображения"

    def start_new_game(self):
        self.lives = len(self.hangman_stages) - 1
        self.stage = 0
        self.word, self.description = get_word_and_description(self.words)
        self.hidden_word = create_hidden_word(self.word)
        self.update_ui()

    def update_ui(self):
        self.word_label.setText(" ".join(self.hidden_word))
        self.description_label.setText(self.description)
        self.hangman_text.setText(self.get_hangman_stage(self.stage))

    def handle_letter_click(self):
            sender = self.sender()
            letter = sender.text().lower()
            if letter in self.word:
                self.hidden_word = update_hidden_word(self.word, self.hidden_word, letter)
                self.update_ui()
                if ''.join(self.hidden_word) == self.word:
                    self.show_message("Поздравляю, ты выиграл!", QMessageBox.Icon.Information)
            else:
                self.lives -= 1
                self.stage += 1
                if self.lives == 0:
                    self.stage = len(self.hangman_stages) - 1
                    self.update_ui()
                    self.show_message(f"Игра окончена! Слово было: {self.word}", QMessageBox.Icon.Critical)
                else:
                    self.update_ui()

    def show_message(self, text, icon):
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle("Результат")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.buttonClicked.connect(self.handle_message_button_click)
        msg_box.exec()

    def handle_message_button_click(self, button):
        if self.sender().text() == "OK":
            self.start_new_game()


    def back_to_menu(self):
        self.parentWidget().setCurrentIndex(0)


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.words = load_words('data/words.json')  
        self.hangman_stages = load_json_data('data/hangman_stages.json')['stages']  
        self.initUI()

    def initUI(self):
        stylesheet = load_stylesheet("src/styles.css")
        if stylesheet:
            self.setStyleSheet(stylesheet)

        self.menu = MainMenu(self)
        self.addWidget(self.menu)

        self.game = HangmanGame(self, words=self.words, hangman_stages=self.hangman_stages)
        self.addWidget(self.game)

        self.settings = SettingsMenu(self)
        self.addWidget(self.settings)

        self.setCurrentIndex(0)
