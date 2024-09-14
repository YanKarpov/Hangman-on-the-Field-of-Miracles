from .ui.main_window import MainApp
from .ui.settings_window import SettingsMenu
from .ui.game_window import HangmanGame
from .core.game_logic import get_word_and_description, create_hidden_word, update_hidden_word
from .core.data_loader import load_json_data, load_stylesheet