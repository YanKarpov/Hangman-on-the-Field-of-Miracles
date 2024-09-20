import sqlite3

DB_NAME = 'player_stats.db'

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            games_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            average_attempts REAL DEFAULT 0.0
        )
    ''')
    
    conn.commit()
    conn.close()

def add_player(player_name):
    """Добавляет нового игрока в базу данных."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO players (name) VALUES (?)", (player_name,))
    
    conn.commit()
    conn.close()
    print(f"Игрок {player_name} добавлен или уже существует.")

def update_stats(player_name, game_won, attempts):
    """Обновляет статистику игрока после игры."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT games_played, wins, losses, average_attempts FROM players WHERE name=?", (player_name,))
    player = cursor.fetchone()
    
    if player:
        games_played, wins, losses, avg_attempts = player
        
        games_played += 1
        if game_won:
            wins += 1
        else:
            losses += 1
        
        total_attempts = avg_attempts * (games_played - 1) + attempts
        avg_attempts = total_attempts / games_played
        
        cursor.execute("UPDATE players SET games_played=?, wins=?, losses=?, average_attempts=? WHERE name=?", 
                       (games_played, wins, losses, avg_attempts, player_name))
        conn.commit()
    
    conn.close()

def get_player_stats(player_name):
    """Возвращает статистику игрока."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM players WHERE name=?", (player_name,))
    player = cursor.fetchone()
    
    conn.close()
    return player
