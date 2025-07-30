import sqlite3

def add_missing_indexes(db_path="marcus_memory.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("🔧 Adding missing indexes...")

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_memory_next_review 
        ON memory_records(next_review)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_next_review_mastery
        ON memory_records(next_review, mastery_level)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_concepts_subject_grade 
        ON concepts(subject, grade_level)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_concepts_emotion_grade 
        ON concepts(emotional_context, grade_level)
    """)

    conn.commit()
    conn.close()
    print("✅ Index migration complete.")

if __name__ == "__main__":
    add_missing_indexes()
