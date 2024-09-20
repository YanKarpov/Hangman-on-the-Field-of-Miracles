from src.ui.settings_window import SettingsMenu
import pygame

class SettingsController:
    def __init__(self, parent):
        self.settings = SettingsMenu(parent)
        self.settings.save_button.clicked.connect(self.save_settings)
        self.settings.back_button.clicked.connect(self.back_to_menu)

        # Инициализация Pygame
        pygame.mixer.init()  # Инициализируем здесь
        self.music_playing = True
        self.update_music()

    def save_settings(self):
        difficulty = "Easy" if self.settings.easy_checkbox.isChecked() else \
                     "Medium" if self.settings.medium_checkbox.isChecked() else \
                     "Hard" if self.settings.hard_checkbox.isChecked() else \
                     "None"
        resolution = self.settings.resolution_combo.currentText()
        display_mode = "Fullscreen" if self.settings.fullscreen_radio.isChecked() else "Windowed"
        music_enabled = self.settings.music_checkbox.isChecked()

        print(f"Уровень сложности: {difficulty}, Разрешение окна: {resolution}, Режим отображения: {display_mode}, Музыка: {'Включена' if music_enabled else 'Выключена'}")

        if display_mode == "Fullscreen":
            self.settings.saved_geometry = self.settings.parentWidget().geometry()  
            self.settings.parentWidget().showFullScreen()
        else:
            if self.settings.saved_geometry:
                self.settings.parentWidget().setGeometry(self.settings.saved_geometry) 
            else:
                width, height = map(int, resolution.split('x'))
                self.settings.parentWidget().resize(width, height)
            self.settings.parentWidget().showNormal()

        self.music_playing = music_enabled
        self.update_music()

    def update_music(self):
        if self.music_playing:
            pygame.mixer.music.load("assets/data/background_music.mp3")
            pygame.mixer.music.play(-1)  
        else:
            pygame.mixer.music.stop()

    def back_to_menu(self):
        self.settings.parentWidget().setCurrentIndex(0)