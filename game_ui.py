import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QTextEdit)
from game_logic import load_words, get_word_and_description, create_hidden_word, update_hidden_word

class HangmanGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_hangman_stages('hangman_stages.json')  # Загрузить стадии виселицы до инициализации UI
        self.words = load_words('words.json')
        self.initUI()
        self.start_new_game()

    def initUI(self):
        self.setWindowTitle("Игра Виселица")
        self.setGeometry(100, 100, 600, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Метка для изображения виселицы
        self.hangman_text = QTextEdit(self)
        self.hangman_text.setReadOnly(True)
        self.hangman_text.setText(self.get_hangman_stage(0))  # По умолчанию показываем первый этап
        self.layout.addWidget(self.hangman_text)
        
        # Метка для отображения скрытого слова
        self.word_label = QLabel(" ", self)
        self.layout.addWidget(self.word_label)
        
        # Создание кнопок для ввода букв
        self.buttons_layout = QGridLayout()
        self.layout.addLayout(self.buttons_layout)
        self.create_alphabet_buttons()
        
        # Кнопка для новой игры
        self.new_game_button = QPushButton("Новая игра", self)
        self.new_game_button.clicked.connect(self.start_new_game)
        self.layout.addWidget(self.new_game_button)
        
        # Кнопка выхода
        self.exit_button = QPushButton("Выход", self)
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

    def create_alphabet_buttons(self):
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        for index, letter in enumerate(alphabet):
            button = QPushButton(letter.upper(), self)
            button.clicked.connect(self.handle_letter_click)
            self.buttons_layout.addWidget(button, index // 8, index % 8)

    def load_hangman_stages(self, file_path):
        """Загрузка стадий виселицы из JSON-файла."""
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.hangman_stages = data['stages']

    def get_hangman_stage(self, stage):
        if 0 <= stage < len(self.hangman_stages):
            return self.hangman_stages[stage]
        return "Ошибка загрузки изображения"


    def start_new_game(self):
        self.lives = len(self.hangman_stages) - 1  # Количество попыток равно числу стадий минус 1
        self.stage = 0
        self.word, self.description = get_word_and_description(self.words)
        self.hidden_word = create_hidden_word(self.word)
        self.update_ui()


    def update_ui(self):
        self.word_label.setText(" ".join(self.hidden_word))
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
                self.stage = len(self.hangman_stages) - 1  # Отобразить последнюю стадию
                self.update_ui()
                self.word_label.setText(f"Игра окончена! Слово было: {self.word}")
            else:
                self.update_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec())









