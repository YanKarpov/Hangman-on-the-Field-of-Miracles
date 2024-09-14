from PyQt6.QtWidgets import QApplication, QStackedWidget
from src.core.data_loader import load_words, load_json_data, load_stylesheet
from src.ui.main_menu import MainMenu
from src.ui.game_window import HangmanGame
from src.ui.settings_window import SettingsMenu

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.words = load_words('assets/data/words.json')
        self.hangman_stages = load_json_data('assets/data/hangman_stages.json')['stages']
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

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
