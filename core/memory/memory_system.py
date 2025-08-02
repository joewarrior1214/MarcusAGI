#!/usr/bin/env python3

"""
Marcus Memory System - Core memory implementation for developmental AGI
Handles both episodic memories and concept learning with spaced repetition
"""

import sqlite3
import json
import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MemoryRecord:
    """Enhanced memory record with types"""
    concept_id: str
    memory_type: str = "semantic"  # semantic, episodic, procedural
    context_vector: List[float] = field(default_factory=list)
    related_concepts: Dict[str, float] = field(default_factory=dict)
    emotional_strength: float = 0.0
    mastery_level: int = 0
    ease_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    success_streak: int = 0
    total_attempts: int = 0

@dataclass
class Concept:
    """Represents a learned concept in Marcus's knowledge base"""
    id: str
    content: str
    subject: str = "general"
    grade_level: str = "kindergarten"
    emotional_context: str = "neutral"
    created_at: Optional[str] = None

class MarcusMemorySystem:
    """Core memory system for Marcus AGI with spaced repetition learning"""
    
    def __init__(self, db_path: str = "marcus_memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with proper schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create memory_records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory_records (
                    concept_id TEXT PRIMARY KEY,
                    memory_type TEXT NOT NULL DEFAULT 'semantic',
                    context_vector TEXT NOT NULL DEFAULT '[]',
                    related_concepts TEXT NOT NULL DEFAULT '{}',
                    emotional_strength REAL NOT NULL DEFAULT 0.0,
                    mastery_level INTEGER NOT NULL DEFAULT 0,
                    ease_factor REAL NOT NULL DEFAULT 2.5,
                    interval_days INTEGER NOT NULL DEFAULT 1,
                    repetitions INTEGER NOT NULL DEFAULT 0,
                    last_reviewed TEXT,
                    next_review TEXT,
                    success_streak INTEGER NOT NULL DEFAULT 0,
                    total_attempts INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (concept_id) REFERENCES concepts (id) ON DELETE CASCADE
                )
            """)
            
            # Create concepts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS concepts (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    subject TEXT NOT NULL DEFAULT 'general',
                    grade_level TEXT NOT NULL DEFAULT 'kindergarten',
                    emotional_context TEXT DEFAULT 'neutral',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create concept_relationships table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS concept_relationships (
                    concept_id TEXT,
                    related_id TEXT,
                    strength REAL DEFAULT 1.0,
                    PRIMARY KEY (concept_id, related_id),
                    FOREIGN KEY (concept_id) REFERENCES concepts (id) ON DELETE CASCADE,
                    FOREIGN KEY (related_id) REFERENCES concepts (id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memory_next_review 
                ON memory_records(next_review)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_concepts_subject_grade 
                ON concepts(subject, grade_level)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_next_review_mastery
                ON memory_records(next_review, mastery_level)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_concepts_emotion_grade
                ON concepts(emotional_context, grade_level)
            """)

            conn.commit()
        
        logger.info(f"Database initialized at {self.db_path}")
    
    def learn_concept(self, concept: Concept) -> bool:
        """Add a new concept to Marcus's knowledge base"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert concept
                cursor.execute("""
                    INSERT OR REPLACE INTO concepts 
                    (id, content, subject, grade_level, emotional_context, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    concept.id,
                    concept.content,
                    concept.subject,
                    concept.grade_level,
                    concept.emotional_context,
                    concept.created_at or datetime.datetime.now().isoformat()
                ))
                
                # Initialize memory record
                memory_record = MemoryRecord(
                    concept_id=concept.id,
                    next_review=datetime.datetime.now().isoformat()
                )
                
                cursor.execute("""
                    INSERT OR REPLACE INTO memory_records 
                    (concept_id, memory_type, context_vector, related_concepts, emotional_strength, 
                     mastery_level, ease_factor, interval_days, repetitions, next_review, 
                     success_streak, total_attempts)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    memory_record.concept_id,
                    memory_record.memory_type,
                    json.dumps(memory_record.context_vector),
                    json.dumps(memory_record.related_concepts),
                    memory_record.emotional_strength,
                    memory_record.mastery_level,
                    memory_record.ease_factor,
                    memory_record.interval_days,
                    memory_record.repetitions,
                    memory_record.next_review,
                    memory_record.success_streak,
                    memory_record.total_attempts
                ))
                
                conn.commit()
                logger.info(f"Learned new concept: {concept.id}")
                return True
                
        except Exception as e:
            logger.error(f"Error learning concept {concept.id}: {e}")
            return False
        
        
    def fetch_all_concepts(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            rows = cursor.execute("""
                SELECT id, content, subject, grade_level, emotional_context, created_at
                FROM concepts
            """).fetchall()
            return [Concept(*row) for row in rows]

    def review_concept(self, concept_id: str, success: bool) -> bool:
        """Review a concept and update spaced repetition parameters"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current memory record
                cursor.execute("""
                    SELECT * FROM memory_records WHERE concept_id = ?
                """, (concept_id,))
                
                row = cursor.fetchone()
                if not row:
                    logger.error(f"No memory record found for concept: {concept_id}")
                    return False
                
                # Parse current state
                memory = MemoryRecord(
                    concept_id=row[0],
                    memory_type=row[1],
                    context_vector=json.loads(row[2]),
                    related_concepts=json.loads(row[3]),
                    emotional_strength=row[4],
                    mastery_level=row[5],
                    ease_factor=row[6],
                    interval_days=row[7],
                    repetitions=row[8],
                    last_reviewed=row[9],
                    next_review=row[10],
                    success_streak=row[11],
                    total_attempts=row[12]
                )
                
                # Update based on SuperMemo-2 algorithm
                memory.total_attempts += 1
                memory.last_reviewed = datetime.datetime.now().isoformat()
                
                if success:
                    memory.success_streak += 1
                    memory.repetitions += 1
                    
                    if memory.repetitions == 1:
                        memory.interval_days = 1
                    elif memory.repetitions == 2:
                        memory.interval_days = 6
                    else:
                        memory.interval_days = int(memory.interval_days * memory.ease_factor)
                    
                    memory.ease_factor = max(1.3, memory.ease_factor + (0.1 - (5 - 4) * (0.08 + (5 - 4) * 0.02)))
                    memory.mastery_level = min(10, memory.mastery_level + 1)
                    
                else:
                    memory.success_streak = 0
                    memory.repetitions = 0
                    memory.interval_days = 1
                    memory.ease_factor = max(1.3, memory.ease_factor - 0.2)
                    memory.mastery_level = max(0, memory.mastery_level - 1)
                
                # Calculate next review date
                next_review_date = datetime.datetime.now() + datetime.timedelta(days=memory.interval_days)
                memory.next_review = next_review_date.isoformat()
                
                # Update database
                cursor.execute("""
                    UPDATE memory_records SET
                        mastery_level = ?, ease_factor = ?, interval_days = ?,
                        repetitions = ?, last_reviewed = ?, next_review = ?,
                        success_streak = ?, total_attempts = ?
                    WHERE concept_id = ?
                """, (
                    memory.mastery_level, memory.ease_factor, memory.interval_days,
                    memory.repetitions, memory.last_reviewed, memory.next_review,
                    memory.success_streak, memory.total_attempts, concept_id
                ))
                
                conn.commit()
                logger.info(f"Updated memory for concept: {concept_id} (success: {success})")
                return True
                
        except Exception as e:
            logger.error(f"Error reviewing concept {concept_id}: {e}")
            return False
    
    def get_due_reviews(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get concepts that are due for review"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                current_time = datetime.datetime.now().isoformat()
                
                cursor.execute("""
                    SELECT c.id, c.content, c.subject, c.grade_level,
                           m.mastery_level, m.next_review
                    FROM concepts c
                    JOIN memory_records m ON c.id = m.concept_id
                    WHERE m.next_review <= ?
                    ORDER BY m.next_review ASC
                    LIMIT ?
                """, (current_time, limit))
                
                rows = cursor.fetchall()
                due_concepts = []
                
                for row in rows:
                    due_concepts.append({
                        'id': row[0],
                        'content': row[1],
                        'subject': row[2],
                        'grade_level': row[3],
                        'mastery_level': row[4],
                        'next_review': row[5]
                    })
                
                return due_concepts
                
        except Exception as e:
            logger.error(f"Error getting due reviews: {e}")
            return []
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total concepts learned
                cursor.execute("SELECT COUNT(*) FROM concepts")
                total_concepts = cursor.fetchone()[0]
                
                # Mastery level distribution
                cursor.execute("""
                    SELECT mastery_level, COUNT(*) 
                    FROM memory_records 
                    GROUP BY mastery_level
                    ORDER BY mastery_level
                """)
                mastery_distribution = dict(cursor.fetchall())
                
                # Subject breakdown
                cursor.execute("""
                    SELECT subject, COUNT(*) 
                    FROM concepts 
                    GROUP BY subject
                """)
                subject_breakdown = dict(cursor.fetchall())
                
                # Average mastery level
                cursor.execute("SELECT AVG(mastery_level) FROM memory_records")
                avg_mastery = cursor.fetchone()[0] or 0
                
                # Due for review count
                current_time = datetime.datetime.now().isoformat()
                cursor.execute("""
                    SELECT COUNT(*) FROM memory_records 
                    WHERE next_review <= ?
                """, (current_time,))
                due_count = cursor.fetchone()[0]
                
                return {
                    'total_concepts': total_concepts,
                    'average_mastery': round(avg_mastery, 2),
                    'mastery_distribution': mastery_distribution,
                    'subject_breakdown': subject_breakdown,
                    'due_for_review': due_count
                }
                
        except Exception as e:
            logger.error(f"Error getting learning stats: {e}")
            return {}
    
    def recall_concept(self, concept_id: str) -> Optional[Dict[str, Any]]:
        """Recall a specific concept from memory"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT c.*, m.mastery_level, m.success_streak
                    FROM concepts c
                    JOIN memory_records m ON c.id = m.concept_id
                    WHERE c.id = ?
                """, (concept_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'content': row[1],
                        'subject': row[2],
                        'grade_level': row[3],
                        'emotional_context': row[4],
                        'created_at': row[5],
                        'mastery_level': row[6],
                        'success_streak': row[7]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error recalling concept {concept_id}: {e}")
            return None
    
    def reflect_on_learning(self) -> str:
        """Generate a reflection on Marcus's learning progress"""
        stats = self.get_learning_stats()
        
        if not stats:
            return "I'm still getting started with my learning journey."
        
        reflection = f"""
        Learning Reflection:
        
        I've learned {stats['total_concepts']} concepts so far, with an average mastery level of {stats['average_mastery']}/10.
        
        My strongest subjects are: {', '.join([f"{subject} ({count} concepts)" for subject, count in sorted(stats['subject_breakdown'].items(), key=lambda x: x[1], reverse=True)])}
        
        I have {stats['due_for_review']} concepts ready for review today. This helps me strengthen my memory through spaced repetition.
        
        My mastery distribution shows I'm making steady progress across different difficulty levels.
        """
        
        return reflection.strip()

    def strengthen_connections(self, concept_id: str, related_ids: List[str], strength: float):
        """Build neural-like memory connections"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for related_id in related_ids:
                cursor.execute("""
                    INSERT OR REPLACE INTO concept_relationships
                    (concept_id, related_id, strength)
                    VALUES (?, ?, ?)
                """, (concept_id, related_id, strength))

    def deep_reflection(self) -> Dict[str, Any]:
        """Generate deeper learning insights"""
        return {
            'knowledge_clusters': self._find_concept_clusters(),
            'learning_patterns': self._analyze_learning_patterns(),
            'memory_strength': self._calculate_memory_strength(),
            'knowledge_gaps': self._identify_knowledge_gaps()
        }

    def process_emotional_memory(
        self, 
        concept_id: str,
        emotional_context: Dict[str, float]
    ) -> bool:
        """Process and store emotional context of memories"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE concepts 
                    SET emotional_context = ?
                    WHERE id = ?
                """, (json.dumps(emotional_context), concept_id))
                return True
        except Exception as e:
            logger.error(f"Error processing emotional memory: {e}")
            return False

    def consolidate_memories(self) -> None:
        """Daily memory consolidation process"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            today = datetime.datetime.now().date()
            
            # Strengthen frequently accessed memories
            cursor.execute("""
                UPDATE memory_records 
                SET strength = strength * 1.2
                WHERE last_accessed >= ? 
                AND access_count > 5
            """, (today - datetime.timedelta(days=1),))

# Example usage and testing functions
def test_marcus_memory():
    """Test the Marcus memory system"""
    print("🧠 Testing Marcus Memory System...")
    
    # Initialize memory system
    memory = MarcusMemorySystem("test_marcus_memory.db")
    
    # Test learning concepts (kindergarten level)
    kindergarten_concepts = [
        Concept("colors_primary", "Red, blue, and yellow are primary colors", "art", "kindergarten", "curious"),
        Concept("numbers_1to10", "I can count from 1 to 10: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10", "math", "kindergarten", "proud"),
        Concept("kindness", "Being kind means helping others and using nice words", "social", "kindergarten", "warm"),
        Concept("alphabet_song", "A-B-C-D-E-F-G, H-I-J-K-L-M-N-O-P", "language", "kindergarten", "happy")
    ]
    
    # Learn the concepts
    for concept in kindergarten_concepts:
        success = memory.learn_concept(concept)
        print(f"✅ Learned: {concept.id} - {success}")
    
    # Get initial stats
    print("\n📊 Initial Learning Stats:")
    stats = memory.get_learning_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test reviewing concepts
    print("\n🔄 Testing concept reviews...")
    due_reviews = memory.get_due_reviews()
    for concept in due_reviews[:2]:
        # Simulate successful review
        memory.review_concept(concept['id'], success=True)
        print(f"✅ Successfully reviewed: {concept['id']}")
    
    # Test recall
    print("\n🧐 Testing concept recall...")
    recalled = memory.recall_concept("kindness")
    if recalled:
        print(f"💭 Recalled: {recalled['content']} (Mastery: {recalled['mastery_level']})")
    
    # Generate reflection
    print("\n🤔 Marcus's Learning Reflection:")
    reflection = memory.reflect_on_learning()
    print(reflection)
    
    print("\n🎉 Marcus Memory System test completed!")

if __name__ == "__main__":
    test_marcus_memory()