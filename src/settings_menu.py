from PyQt6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget, QCheckBox, QComboBox, QRadioButton, QButtonGroup)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import pygame 

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.saved_geometry = None

        pygame.mixer.init()
        self.music_playing = True
        self.update_music()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Настройки игры")
        title.setFont(QFont('Arial', 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.easy_checkbox = QCheckBox("Легкий уровень", self)
        self.easy_checkbox.setChecked(True)
        layout.addWidget(self.easy_checkbox)

        self.medium_checkbox = QCheckBox("Средний уровень", self)
        layout.addWidget(self.medium_checkbox)

        self.hard_checkbox = QCheckBox("Сложный уровень", self)
        layout.addWidget(self.hard_checkbox)

        self.resolution_label = QLabel("Разрешение окна:", self)
        layout.addWidget(self.resolution_label)

        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItems(["800x600", "1024x768", "1280x720", "1920x1080"])
        layout.addWidget(self.resolution_combo)

        self.display_mode_label = QLabel("Режим отображения:", self)
        layout.addWidget(self.display_mode_label)

        self.windowed_radio = QRadioButton("Оконный режим", self)
        self.fullscreen_radio = QRadioButton("Полноэкранный режим", self)
        self.windowed_radio.setChecked(True) 

        self.display_mode_group = QButtonGroup(self)
        self.display_mode_group.addButton(self.windowed_radio)
        self.display_mode_group.addButton(self.fullscreen_radio)

        layout.addWidget(self.windowed_radio)
        layout.addWidget(self.fullscreen_radio)

        self.music_checkbox = QCheckBox("Включить музыку", self)
        self.music_checkbox.setChecked(True)  
        layout.addWidget(self.music_checkbox)

        save_button = QPushButton("Сохранить настройки", self)
        save_button.setFont(QFont('Arial', 14))
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        back_button = QPushButton("Назад в меню", self)
        back_button.setFont(QFont('Arial', 14))
        back_button.clicked.connect(self.back_to_menu)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def save_settings(self):
        difficulty = "Easy" if self.easy_checkbox.isChecked() else \
                     "Medium" if self.medium_checkbox.isChecked() else \
                     "Hard" if self.hard_checkbox.isChecked() else \
                     "None"
        resolution = self.resolution_combo.currentText()
        display_mode = "Fullscreen" if self.fullscreen_radio.isChecked() else "Windowed"
        music_enabled = self.music_checkbox.isChecked()

        print(f"Уровень сложности: {difficulty}, Разрешение окна: {resolution}, Режим отображения: {display_mode}, Музыка: {'Включена' if music_enabled else 'Выключена'}")

        if display_mode == "Fullscreen":
            self.saved_geometry = self.parentWidget().geometry()  
            self.parentWidget().showFullScreen()
        else:
            if self.saved_geometry:
                self.parentWidget().setGeometry(self.saved_geometry) 
            else:
                width, height = map(int, resolution.split('x'))
                self.parentWidget().resize(width, height)
            self.parentWidget().showNormal()

        
        self.music_playing = music_enabled
        self.update_music()

    def update_music(self):
        if self.music_playing:
            pygame.mixer.music.load("data/background_music.mp3")
            pygame.mixer.music.play(-1)  
        else:
            pygame.mixer.music.stop()

    def back_to_menu(self):
        self.parentWidget().setCurrentIndex(0)


