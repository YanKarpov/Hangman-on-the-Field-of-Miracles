from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QApplication
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt

class MainMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        title_image = QLabel()
        movie = QMovie("assets/images/test.gif")  
        title_image.setMovie(movie)
        title_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_image)

        movie.start()  # Запуск анимации

        title = QLabel("Добро пожаловать в игру Виселица!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        buttons = QWidget()
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_button = QPushButton("Начать новую игру", self)
        start_button.clicked.connect(self.start_game)
        button_layout.addWidget(start_button)

        stats_button = QPushButton("Статистика", self)
        stats_button.clicked.connect(self.open_stats)
        button_layout.addWidget(stats_button)

        settings_button = QPushButton("Настройки", self)
        settings_button.clicked.connect(self.open_settings)
        button_layout.addWidget(settings_button)

        exit_button = QPushButton("Выход", self)
        exit_button.clicked.connect(self.close_app)
        button_layout.addWidget(exit_button)

        buttons.setLayout(button_layout)
        layout.addWidget(buttons)

        self.setLayout(layout)

        
        self.resize(800, 600)  
        self.setMinimumSize(400, 300)  
        self.setMaximumSize(1200, 800)  

    def start_game(self):
        self.parentWidget().setCurrentIndex(1)

    def open_stats(self):
        self.parentWidget().setCurrentIndex(3)

    def open_settings(self):
        self.parentWidget().setCurrentIndex(2)

    def close_app(self):
        QApplication.quit()