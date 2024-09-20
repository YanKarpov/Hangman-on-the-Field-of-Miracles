from PyQt6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget, QCheckBox, QComboBox, QRadioButton, QButtonGroup)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.saved_geometry = None

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

        self.save_button = QPushButton("Сохранить настройки", self)
        self.save_button.setFont(QFont('Arial', 14))
        layout.addWidget(self.save_button)

        self.back_button = QPushButton("Назад в меню", self)
        self.back_button.setFont(QFont('Arial', 14))
        layout.addWidget(self.back_button)

        self.setLayout(layout)