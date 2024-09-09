from PyQt6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QTextEdit, QStackedWidget, QApplication)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.game_logic import load_words, get_word_and_description, create_hidden_word, update_hidden_word
from src.data_loader import load_json_data, load_stylesheet
from src.main_menu import MainMenu  
from src.settings_menu import SettingsMenu  

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

class HangmanGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_hangman_stages('data/hangman_stages.json')
        self.words = load_words('data/words.json')
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

    def load_hangman_stages(self, file_path):
        data = load_json_data(file_path)
        self.hangman_stages = data.get('stages', [])

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
                self.word_label.setText("Поздравляю, ты выиграл!")
        else:
            self.lives -= 1
            self.stage += 1
            if self.lives == 0:
                self.stage = len(self.hangman_stages) - 1
                self.update_ui()
                self.word_label.setText(f"Игра окончена! Слово было: {self.word}")
            else:
                self.update_ui()

    def back_to_menu(self):
        self.parentWidget().setCurrentIndex(0)


class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        stylesheet = load_stylesheet("src/styles.css")
        if stylesheet:
            self.setStyleSheet(stylesheet)

        self.menu = MainMenu(self)
        self.addWidget(self.menu)

        self.game = HangmanGame(self)
        self.addWidget(self.game)

        self.settings = SettingsMenu(self)
        self.addWidget(self.settings)

        self.setCurrentIndex(0)