from PyQt6.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QCheckBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("Настройки игры")
        title.setFont(QFont('Arial', 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.difficulty_slider = QSlider(Qt.Orientation.Horizontal)
        self.difficulty_slider.setMinimum(1)
        self.difficulty_slider.setMaximum(10)
        self.difficulty_slider.setValue(6)
        layout.addWidget(QLabel("Уровень сложности (попытки):"))
        layout.addWidget(self.difficulty_slider)

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
        difficulty = self.difficulty_slider.value()
        music_enabled = self.music_checkbox.isChecked()
        print(f"Сложность: {difficulty}, Музыка: {'включена' if music_enabled else 'выключена'}")

    def back_to_menu(self):
        self.parentWidget().setCurrentIndex(0)