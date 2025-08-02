from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List, Optional

class MemoryManager:
    def __init__(self, db_path: str = "marcus_memory.db"):
        self.db_path = db_path
    
    def update_mastery(self, concept_id: str, quality: int) -> bool:
        """Update mastery level based on review quality (1-5)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get current values
            cursor.execute("""
                SELECT mastery_level, ease_factor, success_streak
                FROM memory_records 
                WHERE concept_id = ?
            """, (concept_id,))
            mastery, ease, streak = cursor.fetchone()
            
            # Calculate new values
            new_mastery = min(10, mastery + (1 if quality >= 4 else -1))
            new_ease = max(1.3, ease + (0.1 if quality >= 4 else -0.15))
            new_streak = streak + 1 if quality >= 4 else 0
            
            # Update record
            cursor.execute("""
                UPDATE memory_records
                SET mastery_level = ?,
                    ease_factor = ?,
                    success_streak = ?,
                    last_reviewed = ?,
                    next_review = ?,
                    total_attempts = total_attempts + 1
                WHERE concept_id = ?
            """, (
                new_mastery,
                new_ease,
                new_streak,
                datetime.now().isoformat(),
                (datetime.now() + timedelta(days=int(new_ease * new_streak))).isoformat(),
                concept_id
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error updating mastery: {e}")
            return False
        finally:
            conn.close()