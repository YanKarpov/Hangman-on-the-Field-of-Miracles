from PyQt6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QTextEdit, QStackedWidget, QSlider, QCheckBox, QApplication)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.game_logic import load_words, get_word_and_description, create_hidden_word, update_hidden_word
from src.data_loader import load_json_data


class MainMenu(QWidget):
    """Главное меню игры."""
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Добро пожаловать в игру Виселица!")
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Кнопка для начала новой игры
        start_button = QPushButton("Начать новую игру", self)
        start_button.setFont(QFont('Arial', 14))
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        # Кнопка настроек
        settings_button = QPushButton("Настройки", self)
        settings_button.setFont(QFont('Arial', 14))
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)

        # Кнопка выхода
        exit_button = QPushButton("Выход", self)
        exit_button.setFont(QFont('Arial', 14))
        exit_button.clicked.connect(self.close_app)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def start_game(self):
        self.parentWidget().setCurrentIndex(1)

    def open_settings(self):
        self.parentWidget().setCurrentIndex(2)

    def close_app(self):
        QApplication.quit()


class HangmanGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_hangman_stages('data/hangman_stages.json')  # Загрузить стадии виселицы до инициализации UI
        self.words = load_words('data/words.json')
        self.initUI()
        self.start_new_game()

    def initUI(self):
        layout = QVBoxLayout()

        # Метка для изображения виселицы
        self.hangman_text = QTextEdit(self)
        self.hangman_text.setReadOnly(True)
        self.hangman_text.setFont(QFont('Courier', 18))
        self.hangman_text.setStyleSheet("background-color: #f0f0f0; border: 2px solid #000;")
        self.hangman_text.setText(self.get_hangman_stage(0))  # По умолчанию показываем первый этап
        layout.addWidget(self.hangman_text)

        # Метка для отображения скрытого слова
        self.word_label = QLabel(" ", self)
        self.word_label.setFont(QFont('Arial', 20))
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.word_label)

        # Метка для подсказки
        self.description_label = QLabel("", self)
        self.description_label.setFont(QFont('Arial', 16))
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet("color: #555; padding: 10px;")
        layout.addWidget(self.description_label)

        # Создание кнопок для ввода букв
        self.buttons_layout = QGridLayout()
        layout.addLayout(self.buttons_layout)
        self.create_alphabet_buttons()

        # Кнопка для новой игры
        self.new_game_button = QPushButton("Новая игра", self)
        self.new_game_button.setFont(QFont('Arial', 14))
        self.new_game_button.clicked.connect(self.start_new_game)
        layout.addWidget(self.new_game_button)

        # Кнопка выхода в главное меню
        self.back_to_menu_button = QPushButton("Главное меню", self)
        self.back_to_menu_button.setFont(QFont('Arial', 14))
        self.back_to_menu_button.clicked.connect(self.back_to_menu)
        layout.addWidget(self.back_to_menu_button)

        self.setLayout(layout)

    def create_alphabet_buttons(self):
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        for index, letter in enumerate(alphabet):
            button = QPushButton(letter.upper(), self)
            button.setFont(QFont('Arial', 14))
            button.setFixedSize(40, 40)
            button.clicked.connect(self.handle_letter_click)
            self.buttons_layout.addWidget(button, index // 8, index % 8)

    def load_hangman_stages(self, file_path):
        """Загрузка стадий виселицы из JSON-файла."""
        data = load_json_data(file_path)
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
                self.stage = len(self.hangman_stages) - 1  # Отобразить последнюю стадию
                self.update_ui()
                self.word_label.setText(f"Игра окончена! Слово было: {self.word}")
            else:
                self.update_ui()

    def back_to_menu(self):
        # Переключаемся на главное меню
        self.parentWidget().setCurrentIndex(0)


class SettingsMenu(QWidget):
    """Меню настроек игры."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Настройки игры")
        title.setFont(QFont('Arial', 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Слайдер для выбора уровня сложности (количество жизней)
        self.difficulty_slider = QSlider(Qt.Orientation.Horizontal)
        self.difficulty_slider.setMinimum(1)
        self.difficulty_slider.setMaximum(10)
        self.difficulty_slider.setValue(6)  # Значение по умолчанию
        layout.addWidget(QLabel("Уровень сложности (попытки):"))
        layout.addWidget(self.difficulty_slider)

        # Чекбокс для включения/выключения музыки
        self.music_checkbox = QCheckBox("Включить музыку", self)
        self.music_checkbox.setChecked(True)  # По умолчанию музыка включена
        layout.addWidget(self.music_checkbox)

        # Кнопка сохранения настроек
        save_button = QPushButton("Сохранить настройки", self)
        save_button.setFont(QFont('Arial', 14))
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Кнопка для возврата в меню
        back_button = QPushButton("Назад в меню", self)
        back_button.setFont(QFont('Arial', 14))
        back_button.clicked.connect(self.back_to_menu)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_settings(self):
        """Сохраняем выбранные настройки."""
        difficulty = self.difficulty_slider.value()
        music_enabled = self.music_checkbox.isChecked()
        # Здесь можно сохранить настройки в файл или применить их к игре
        print(f"Сложность: {difficulty}, Музыка: {'включена' if music_enabled else 'выключена'}")

    def back_to_menu(self):
        # Возвращаемся в главное меню
        self.parentWidget().setCurrentIndex(0)


class MainApp(QStackedWidget):
    """Основное приложение с переключением между окнами."""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Добавляем главное меню
        self.menu = MainMenu(self)
        self.addWidget(self.menu)

        # Добавляем игру
        self.game = HangmanGame(self)
        self.addWidget(self.game)

        # Добавляем настройки
        self.settings = SettingsMenu(self)
        self.addWidget(self.settings)

        # Отображаем главное меню при запуске
        self.setCurrentIndex(0)












