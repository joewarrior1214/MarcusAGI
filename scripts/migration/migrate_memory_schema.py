import sqlite3
from datetime import datetime

def migrate_memory_schema(db_path="marcus_memory.db"):
    """Enhanced migration with version control and backup"""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    
    # Backup existing data
    backup_path = f"marcus_memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    print(f"📦 Creating backup at {backup_path}...")
    
    with sqlite3.connect(backup_path) as backup_conn:
        conn.backup(backup_conn)
    
    try:
        # Create concepts table first
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create enhanced memory records table
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
        
        # Create indexes
        create_indexes(cursor)
        
        conn.commit()
        print("✅ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Migration failed: {e}")
        print("⚠️ Rolling back to previous state...")
        
    finally:
        conn.close()

def create_indexes(cursor):
    """Create performance indexes"""
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_memory_mastery 
        ON memory_records(mastery_level)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_memory_review 
        ON memory_records(next_review)
    """)

