# Hangman-on-the-Field-of-Miracles

## Описание
**Hangman-on-the-Field-of-Miracles** - это игра "Виселица на поле чудес", где цель - угадать слово по буквам. При каждой ошибке часть человечка рисуется на виселице. Программа разработана в рамках обучения по дисциплине "Язык программирования Python".

### Основные функции
- **Угадывание слова по буквам**: Игроки пытаются угадать слово, вводя буквы.
- **Отрисовка виселицы**: При каждой ошибке рисуется часть человечка на виселице.
- **Случайный выбор слова**: Список слов хранится в файле формата JSON, и каждое слово выбирается случайным образом.

### Дополнительные функции
- **Фоновая музыка**: Программа включает фоновую музыку для создания атмосферы.
- **Вывод текстовых сообщений с задержкой**: Текстовые сообщения выводятся с небольшой задержкой по буквам, чтобы создать эффект визуальной новеллы с элементами хоррора.

### Недоработки
- **Графический интерфейс**: Попытка реализации графического интерфейса с использованием библиотеки pygame не увенчалась успехом. Графическая отрисовка виселицы осталась текстовой.

## Структура проекта
Весь код реализован в одном файле и разбит на функции. Программа запускается через модуль `main.py`.

### Файлы проекта
- `main.py`: Основной файл для запуска.
- `hangman_game.py`: Файл с кодом игры
- `words.json`: Файл с перечнем слов для угадывания.

## Запуск игры
1. Убедитесь, что у вас установлен Python.
2. Скачайте или клонируйте репозиторий.
3. Установите необходимые зависимости (если есть).
4. Запустите игру командой:
   ```bash
   python main.py
