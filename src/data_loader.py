import json
from PyQt6.QtCore import QFile, QTextStream

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def load_stylesheet(file_path):
    file = QFile(file_path)
    if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        print(f"Не удалось открыть файл стилей: {file_path}")
        return
    stream = QTextStream(file)
    stylesheet = stream.readAll()
    file.close()
    return stylesheet


