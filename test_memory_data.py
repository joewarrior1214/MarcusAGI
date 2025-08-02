import sqlite3
from datetime import datetime, timedelta

def create_tables():
    """Create necessary tables if they don't exist"""
    conn = sqlite3.connect('marcus_memory.db')
    cursor = conn.cursor()
    
    try:
        # Create concepts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create memory_records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_records (
                concept_id TEXT PRIMARY KEY,
                memory_type TEXT NOT NULL DEFAULT 'semantic',
                mastery_level INTEGER NOT NULL DEFAULT 0,
                ease_factor REAL NOT NULL DEFAULT 2.5,
                interval_days INTEGER NOT NULL DEFAULT 1,
                emotional_strength FLOAT DEFAULT 0.0,
                repetitions INTEGER NOT NULL DEFAULT 0,
                last_reviewed TEXT,
                next_review TEXT,
                FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        print("✅ Tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_test_data():
    """Insert test data into memory system"""
    conn = sqlite3.connect('marcus_memory.db')
    cursor = conn.cursor()
    
    try:
        # Insert test concepts
        concepts = [
            ('math_counting', 'Counting numbers 1-10'),
            ('reading_abc', 'Basic alphabet recognition'),
            ('social_sharing', 'Learning to share with others')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO concepts (id, content)
            VALUES (?, ?)
        """, concepts)
        
        # Insert memory records
        now = datetime.now()
        memory_records = [
            ('math_counting', 'semantic', 3, 2.5, 1, 0.7, 2, 
             now.isoformat(), (now + timedelta(days=1)).isoformat()),
            ('reading_abc', 'semantic', 2, 2.3, 2, 0.5, 1,
             now.isoformat(), (now + timedelta(days=2)).isoformat()),
            ('social_sharing', 'episodic', 1, 2.0, 1, 0.8, 1,
             now.isoformat(), (now + timedelta(days=1)).isoformat())
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO memory_records 
            (concept_id, memory_type, mastery_level, ease_factor, 
             interval_days, emotional_strength, repetitions,
             last_reviewed, next_review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, memory_records)
        
        conn.commit()
        print("✅ Test data inserted successfully!")
        
    except Exception as e:
        print(f"❌ Error inserting test data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()  # Create tables first
    insert_test_data()  # Then insert data