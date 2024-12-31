import sqlite3
import datetime

DB_FILE = "data/warnings.db"  # Chemin vers la base de données dans le conteneur

def setup_db():
    """Crée la table des avertissements si elle n'existe pas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            guild_id INTEGER,
            warner_id INTEGER,
            reason TEXT,
            date DATETIME
        )
    """)
    conn.commit()
    conn.close()

def add_warning(user_id, guild_id, warner_id, reason):
    """Ajoute un avertissement à la base de données."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO warnings (user_id, guild_id, warner_id, reason, date) VALUES (?, ?, ?, ?, ?)",
                   (user_id, guild_id, warner_id, reason, datetime.datetime.now()))
    conn.commit()
    conn.close()

def get_warnings(user_id, guild_id):
    """Récupère les avertissements d'un utilisateur."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, warner_id, reason, date FROM warnings WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
    warnings = cursor.fetchall()
    conn.close()
    return warnings

def clear_warnings(user_id, guild_id):
    """Supprime tous les avertissements d'un utilisateur."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM warnings WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
    conn.commit()
    conn.close()

# Appelez setup_db() au démarrage du bot pour créer la table si nécessaire.
setup_db()