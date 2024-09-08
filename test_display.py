import json

def load_hangman_stages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data['stages']

def display_hangman(stage, stages):
    print(stages[stage])

# Пример использования
if __name__ == "__main__":
    stages = load_hangman_stages('hangman_stages.json')
    current_stage = 0 
    display_hangman(current_stage, stages)

    # Симуляция прогресса игры
    for stage in range(len(stages)):
        input("Нажмите Enter для следующего этапа...")
        display_hangman(stage, stages)
