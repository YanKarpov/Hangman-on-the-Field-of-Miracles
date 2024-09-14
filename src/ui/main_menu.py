from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

class MainMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Добро пожаловать в игру Виселица!")
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        start_button = QPushButton("Начать новую игру", self)
        start_button.setFont(QFont('Arial', 14))
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        settings_button = QPushButton("Настройки", self)
        settings_button.setFont(QFont('Arial', 14))
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)

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