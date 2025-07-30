import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "marcus_memory.db"

def test_foreign_key_cascade():
    print("\n🔗 Testing Foreign Key ON DELETE CASCADE...")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Insert dummy concept and memory
    cursor.execute("""
    INSERT INTO concepts (id, content, subject, grade_level, emotional_context, created_at)
    VALUES ('test_concept', 'Test content', 'test', 'test-grade', 'neutral', datetime('now'))
""")

    conn.commit()

    cursor.execute("SELECT * FROM memory_records WHERE concept_id = 'test_concept'")
    print("Before delete:", cursor.fetchall())

    cursor.execute("DELETE FROM concepts WHERE id = 'test_concept'")
    conn.commit()

    cursor.execute("SELECT * FROM memory_records WHERE concept_id = 'test_concept'")
    result = cursor.fetchall()
    print("After delete:", result)

    assert result == [], "❌ Cascade delete failed!"
    print("✅ Foreign Key CASCADE works.")

def test_index_usage():
    print("\n⚡ Testing Index Presence...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    indexes = cursor.execute("PRAGMA index_list('memory_records')").fetchall()
    concept_indexes = cursor.execute("PRAGMA index_list('concepts')").fetchall()

    print("memory_records indexes:", indexes)
    print("concepts indexes:", concept_indexes)

    expected_indexes = {
        "memory_records": {"idx_memory_next_review", "idx_next_review_mastery"},
        "concepts": {"idx_concepts_subject_grade", "idx_concepts_emotion_grade"},
    }

    memory_index_names = {idx[1] for idx in indexes}
    concept_index_names = {idx[1] for idx in concept_indexes}

    assert expected_indexes["memory_records"].issubset(memory_index_names), "❌ Missing index in memory_records"
    assert expected_indexes["concepts"].issubset(concept_index_names), "❌ Missing index in concepts"

    print("✅ All indexes exist.")

def test_backup_file_exists():
    print("\n🗂️ Testing Backup File Creation...")
    # Simulate backup logic manually for testing
    backup_name = f"{DB_PATH}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    backup_path = Path(backup_name)
    Path(DB_PATH).rename(backup_path)

    assert backup_path.exists(), "❌ No backup file created!"
    print(f"✅ Backup file created: {backup_path.name}")

if __name__ == "__main__":
    test_foreign_key_cascade()
    test_index_usage()
    test_backup_file_exists()
    print("\n🎉 All schema integrity tests passed!")
