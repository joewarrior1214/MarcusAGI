from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MemoryRecord:
    concept: str
    memory_type: str
    mastery: int
    emotion: float
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None

class MemoryManager:
    def __init__(self, db_path: str = "marcus_memory.db"):
        self.db_path = db_path

    def get_due_reviews(self) -> List[MemoryRecord]:
        """Get concepts due for review"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.content,
                    m.memory_type,
                    m.mastery_level,
                    m.emotional_strength,
                    m.last_reviewed,
                    m.next_review
                FROM memory_records m
                JOIN concepts c ON c.id = m.concept_id
                WHERE m.next_review <= ?
                ORDER BY m.next_review ASC
            """, (datetime.now().isoformat(),))
            
            return [MemoryRecord(*row) for row in cursor.fetchall()]

    def strengthen_memory(self, concept_id: str, quality: int) -> bool:
        """Update memory strength based on review quality (1-5)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                # Calculate new values based on review quality
                cursor.execute("""
                    UPDATE memory_records
                    SET mastery_level = MIN(mastery_level + ?, 10),
                        emotional_strength = MIN(emotional_strength + 0.1, 1.0),
                        success_streak = CASE WHEN ? >= 4 THEN success_streak + 1 ELSE 0 END,
                        last_reviewed = ?,
                        total_attempts = total_attempts + 1
                    WHERE concept_id = ?
                """, (
                    1 if quality >= 4 else -1,
                    quality,
                    datetime.now().isoformat(),
                    concept_id
                ))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error strengthening memory: {e}")
                return False