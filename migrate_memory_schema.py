import sqlite3
from datetime import datetime

def migrate_memory_schema(db_path="marcus_memory.db"):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Step 1: Fetch existing memory records
    print("📦 Backing up memory records...")
    cursor.execute("SELECT * FROM memory_records")
    memory_data = cursor.fetchall()

    # Step 2: Drop and recreate memory_records with proper FK
    print("🧱 Rebuilding memory_records with ON DELETE CASCADE...")
    cursor.execute("DROP TABLE IF EXISTS memory_records")
    
    cursor.execute("""
        CREATE TABLE memory_records (
            concept_id TEXT PRIMARY KEY,
            mastery_level INTEGER NOT NULL CHECK (mastery_level BETWEEN 0 AND 10),
            ease_factor REAL NOT NULL CHECK (ease_factor > 0),
            interval_days INTEGER NOT NULL CHECK (interval_days >= 0),
            repetitions INTEGER NOT NULL,
            last_reviewed TEXT NOT NULL,
            next_review TEXT NOT NULL,
            success_streak INTEGER NOT NULL,
            total_attempts INTEGER NOT NULL,
            FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
        )
    """)

    # Step 3: Restore data
    print("📥 Restoring memory data...")
    cursor.executemany("""
        INSERT INTO memory_records (
            concept_id, mastery_level, ease_factor, interval_days, repetitions,
            last_reviewed, next_review, success_streak, total_attempts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, memory_data)

    conn.commit()
    conn.close()
    print("✅ Migration complete! ON DELETE CASCADE is now active.")

if __name__ == "__main__":
    migrate_memory_schema("marcus_memory.db")

