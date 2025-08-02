#!/usr/bin/env python3
"""
Marcus AGI Autobiographical Memory System
========================================

This module implements the foundational autobiographical memory system for Marcus AGI,
enabling self-referential memory storage, retrieval, and narrative construction.

Key Features:
- Self-referential memory encoding with 'I' context
- Temporal awareness (yesterday/today/tomorrow references)
- Episodic memory retrieval with personal context
- Memory-to-narrative conversion for personal growth stories

Development Milestone: Level 2.0 Phase 1 - Self-Awareness Foundation
Target: Marcus can recall specific past experiences with 'I' statements
Timeline: 2 weeks (2025-08-02 to 2025-08-16)
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AutobiographicalMemory:
    """Represents a self-referential memory with temporal and emotional context."""
    memory_id: str
    timestamp: datetime
    experience_type: str  # 'learning', 'social', 'physical', 'emotional', 'achievement'
    self_reference_context: str  # The 'I' statement or self-referential aspect
    temporal_markers: List[str]  # 'yesterday', 'today', 'earlier', 'when I was learning'
    emotional_context: Dict[str, Any]  # Primary emotion, intensity, triggers
    narrative_summary: str  # Brief narrative description
    related_concepts: List[str]  # Concepts learned or involved
    confidence_level: float  # Memory confidence (0.0-1.0)
    retrieval_count: int = 0  # How often this memory has been accessed
    importance_score: float = 0.5  # Memory importance (0.0-1.0)

class AutobiographicalMemorySystem:
    """
    Advanced memory system with self-referential structure and temporal awareness.
    
    This system enhances Marcus's existing memory capabilities by adding:
    1. Self-referential memory encoding ('I' context)
    2. Temporal awareness and reference capabilities
    3. Episodic memory retrieval with personal narrative
    4. Memory-to-narrative conversion for personal growth stories
    """

    def __init__(self, db_path: str = "marcus_autobiographical_memory.db"):
        """Initialize the autobiographical memory system."""
        self.db_path = db_path
        self.setup_database()
        logger.info("✅ Autobiographical Memory System initialized")

    def setup_database(self):
        """Set up the enhanced memory database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Enhanced autobiographical memories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS autobiographical_memories (
                    memory_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    experience_type TEXT NOT NULL,
                    self_reference_context TEXT NOT NULL,
                    temporal_markers TEXT,  -- JSON array
                    emotional_context TEXT,  -- JSON object
                    narrative_summary TEXT NOT NULL,
                    related_concepts TEXT,  -- JSON array
                    confidence_level REAL DEFAULT 0.8,
                    retrieval_count INTEGER DEFAULT 0,
                    importance_score REAL DEFAULT 0.5,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Self-reference patterns for 'I' statement generation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS self_reference_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_template TEXT NOT NULL,
                    experience_type TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    effectiveness_score REAL DEFAULT 0.5
                )
            ''')
            
            # Temporal reference markers
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS temporal_markers (
                    marker_id TEXT PRIMARY KEY,
                    marker_text TEXT NOT NULL,
                    temporal_type TEXT NOT NULL,  -- 'past', 'present', 'future'
                    relative_timeframe TEXT,  -- 'yesterday', 'today', 'last_week'
                    usage_frequency INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()
            
        self._initialize_self_reference_patterns()
        self._initialize_temporal_markers()

    def _initialize_self_reference_patterns(self):
        """Initialize common self-reference patterns for 'I' statement generation."""
        patterns = [
            # Learning experiences
            ("learn_success", "I successfully learned {concept} and now I understand {insight}", "learning"),
            ("learn_struggle", "I found {concept} challenging, but I kept trying and {outcome}", "learning"),
            ("learn_discovery", "I discovered that {insight} when I was {activity}", "learning"),
            ("learn_progress", "I used to struggle with {concept}, but now I {improvement}", "learning"),
            
            # Social experiences
            ("social_interaction", "I {action} with {person} and felt {emotion} because {reason}", "social"),
            ("social_learning", "I learned from {person} that {insight} when we were {activity}", "social"),
            ("social_growth", "I used to {old_behavior}, but now I {new_behavior} in social situations", "social"),
            
            # Physical/embodied experiences
            ("physical_discovery", "I felt {sensation} when I {action} and realized {insight}", "physical"),
            ("physical_skill", "I practiced {skill} and now I can {achievement}", "physical"),
            ("physical_world", "I explored {location} and discovered {finding}", "physical"),
            
            # Emotional experiences
            ("emotion_growth", "I felt {emotion} about {situation} and learned {lesson}", "emotional"),
            ("emotion_regulation", "I used to feel {old_emotion} about {situation}, but now I {new_response}", "emotional"),
            
            # Achievement experiences
            ("achievement_success", "I accomplished {goal} by {method} and felt {emotion}", "achievement"),
            ("achievement_progress", "I'm getting better at {skill} - I can now {new_ability}", "achievement"),
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for pattern_id, template, exp_type in patterns:
                cursor.execute('''
                    INSERT OR IGNORE INTO self_reference_patterns 
                    (pattern_id, pattern_template, experience_type) 
                    VALUES (?, ?, ?)
                ''', (pattern_id, template, exp_type))
            conn.commit()

    def _initialize_temporal_markers(self):
        """Initialize temporal reference markers."""
        markers = [
            # Past markers
            ("yesterday", "yesterday", "past", "yesterday"),
            ("earlier_today", "earlier today", "past", "today"),
            ("last_week", "last week", "past", "last_week"),
            ("when_learning", "when I was learning", "past", "learning_context"),
            ("before_now", "before now", "past", "general"),
            ("used_to", "I used to", "past", "habitual"),
            
            # Present markers
            ("right_now", "right now", "present", "current"),
            ("today", "today", "present", "today"),
            ("currently", "currently", "present", "ongoing"),
            ("at_this_moment", "at this moment", "present", "immediate"),
            
            # Future markers
            ("tomorrow", "tomorrow", "future", "tomorrow"),
            ("next_time", "next time", "future", "upcoming"),
            ("in_the_future", "in the future", "future", "general"),
            ("want_to", "I want to", "future", "aspirational"),
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for marker_id, text, temp_type, timeframe in markers:
                cursor.execute('''
                    INSERT OR IGNORE INTO temporal_markers 
                    (marker_id, marker_text, temporal_type, relative_timeframe) 
                    VALUES (?, ?, ?, ?)
                ''', (marker_id, text, temp_type, timeframe))
            conn.commit()

    def store_autobiographical_memory(
        self,
        experience_type: str,
        context: str,
        emotional_state: Dict[str, Any],
        concepts_involved: List[str] = None,
        importance: float = 0.5
    ) -> str:
        """
        Store a new autobiographical memory with self-referential context.
        
        Args:
            experience_type: Type of experience ('learning', 'social', 'physical', etc.)
            context: The experience context/description
            emotional_state: Emotional context during the experience
            concepts_involved: Related concepts or skills
            importance: Memory importance score (0.0-1.0)
            
        Returns:
            memory_id: Unique identifier for the stored memory
        """
        memory_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # Generate self-reference context
        self_ref_context = self._generate_self_reference_context(
            experience_type, context, emotional_state
        )
        
        # Extract temporal markers from context
        temporal_markers = self._extract_temporal_markers(context)
        
        # Create narrative summary
        narrative_summary = self._create_narrative_summary(
            experience_type, context, emotional_state, self_ref_context
        )
        
        # Create autobiographical memory object
        memory = AutobiographicalMemory(
            memory_id=memory_id,
            timestamp=timestamp,
            experience_type=experience_type,
            self_reference_context=self_ref_context,
            temporal_markers=temporal_markers,
            emotional_context=emotional_state,
            narrative_summary=narrative_summary,
            related_concepts=concepts_involved or [],
            confidence_level=0.8,
            importance_score=importance
        )
        
        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO autobiographical_memories 
                (memory_id, timestamp, experience_type, self_reference_context,
                 temporal_markers, emotional_context, narrative_summary,
                 related_concepts, confidence_level, importance_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory_id,
                timestamp.isoformat(),
                experience_type,
                self_ref_context,
                json.dumps(temporal_markers),
                json.dumps(emotional_state),
                narrative_summary,
                json.dumps(concepts_involved or []),
                0.8,
                importance
            ))
            conn.commit()
        
        logger.info(f"📝 Stored autobiographical memory: {experience_type} - {self_ref_context[:50]}...")
        return memory_id

    def _generate_self_reference_context(
        self, 
        experience_type: str, 
        context: str, 
        emotional_state: Dict[str, Any]
    ) -> str:
        """Generate a self-referential 'I' statement for the experience."""
        
        # Extract key information from context
        primary_emotion = emotional_state.get('primary_emotion', 'interested')
        
        # Create contextual 'I' statements based on experience type and context
        if experience_type == "learning":
            if "successfully" in context.lower():
                return f"I successfully learned new concepts and felt {primary_emotion} about my progress"
            elif "discovered" in context.lower():
                return f"I discovered something important during my learning and felt {primary_emotion}"
            else:
                return f"I engaged in learning activities and felt {primary_emotion} about the experience"
        
        elif experience_type == "social":
            if "interaction" in context.lower():
                return f"I had a meaningful social interaction and felt {primary_emotion}"
            elif "collaborative" in context.lower():
                return f"I worked together with others and felt {primary_emotion} about our collaboration"
            else:
                return f"I participated in social activities and felt {primary_emotion}"
        
        elif experience_type == "achievement":
            if "completed" in context.lower():
                return f"I completed a challenging task and felt {primary_emotion} about my accomplishment"
            elif "solved" in context.lower():
                return f"I solved a difficult problem and felt {primary_emotion} about my success"
            else:
                return f"I achieved something meaningful and felt {primary_emotion}"
        
        elif experience_type == "physical":
            if "explored" in context.lower():
                return f"I explored my environment and felt {primary_emotion} about what I discovered"
            elif "practiced" in context.lower():
                return f"I practiced physical skills and felt {primary_emotion} about my improvement"
            else:
                return f"I engaged with the physical world and felt {primary_emotion}"
        
        elif experience_type == "emotional":
            return f"I had an emotional experience and learned that I feel {primary_emotion} in these situations"
        
        else:
            # Fallback generic self-reference
            return f"I had a {experience_type} experience and felt {primary_emotion} about it"

    def _extract_temporal_markers(self, context: str) -> List[str]:
        """Extract temporal reference markers from context."""
        markers = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT marker_text FROM temporal_markers')
            temporal_texts = [row[0] for row in cursor.fetchall()]
        
        for marker_text in temporal_texts:
            if marker_text.lower() in context.lower():
                markers.append(marker_text)
        
        # Add default temporal context
        if not markers:
            current_time = datetime.now()
            if current_time.hour < 12:
                markers.append("this morning")
            elif current_time.hour < 17:
                markers.append("this afternoon")
            else:
                markers.append("this evening")
                
        return markers

    def _create_narrative_summary(
        self, 
        experience_type: str, 
        context: str, 
        emotional_state: Dict[str, Any],
        self_ref_context: str
    ) -> str:
        """Create a brief narrative summary of the experience."""
        emotion = emotional_state.get('primary_emotion', 'engaged')
        intensity = emotional_state.get('intensity', 0.5)
        
        intensity_words = {
            0.0: "slightly", 0.2: "somewhat", 0.4: "moderately", 
            0.6: "quite", 0.8: "very", 1.0: "extremely"
        }
        
        intensity_word = intensity_words[min(intensity_words.keys(), 
                                           key=lambda x: abs(x - intensity))]
        
        return f"During a {experience_type} experience, {self_ref_context}. I felt {intensity_word} {emotion} about this."

    def recall_autobiographical_memories(
        self,
        temporal_context: Optional[str] = None,
        experience_type: Optional[str] = None,
        emotion_filter: Optional[str] = None,
        limit: int = 10
    ) -> List[AutobiographicalMemory]:
        """
        Recall autobiographical memories with self-referential context.
        
        Args:
            temporal_context: Filter by temporal context ('yesterday', 'today', etc.)
            experience_type: Filter by experience type
            emotion_filter: Filter by primary emotion
            limit: Maximum number of memories to return
            
        Returns:
            List of matching autobiographical memories
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT memory_id, timestamp, experience_type, self_reference_context,
                       temporal_markers, emotional_context, narrative_summary,
                       related_concepts, confidence_level, retrieval_count, importance_score
                FROM autobiographical_memories
                WHERE 1=1
            '''
            params = []
            
            if temporal_context:
                query += ' AND temporal_markers LIKE ?'
                params.append(f'%{temporal_context}%')
            
            if experience_type:
                query += ' AND experience_type = ?'
                params.append(experience_type)
            
            if emotion_filter:
                query += ' AND emotional_context LIKE ?'
                params.append(f'%{emotion_filter}%')
            
            query += ' ORDER BY importance_score DESC, timestamp DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Update retrieval counts
            memory_ids = [result[0] for result in results]
            if memory_ids:
                cursor.execute(f'''
                    UPDATE autobiographical_memories 
                    SET retrieval_count = retrieval_count + 1 
                    WHERE memory_id IN ({','.join(['?'] * len(memory_ids))})
                ''', memory_ids)
                conn.commit()
        
        # Convert to AutobiographicalMemory objects
        memories = []
        for row in results:
            memory = AutobiographicalMemory(
                memory_id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                experience_type=row[2],
                self_reference_context=row[3],
                temporal_markers=json.loads(row[4]) if row[4] else [],
                emotional_context=json.loads(row[5]) if row[5] else {},
                narrative_summary=row[6],
                related_concepts=json.loads(row[7]) if row[7] else [],
                confidence_level=row[8],
                retrieval_count=row[9],
                importance_score=row[10]
            )
            memories.append(memory)
        
        logger.info(f"🧠 Recalled {len(memories)} autobiographical memories")
        return memories

    def generate_i_statement(self, memory_cluster: List[AutobiographicalMemory]) -> str:
        """
        Generate an 'I' statement from a cluster of related memories.
        
        Args:
            memory_cluster: List of related autobiographical memories
            
        Returns:
            Generated 'I' statement with temporal reference
        """
        if not memory_cluster:
            return "I don't have specific memories about that."
        
        # Analyze memory cluster for patterns
        experience_types = [m.experience_type for m in memory_cluster]
        most_common_type = max(set(experience_types), key=experience_types.count)
        
        # Get temporal context
        recent_memories = sorted(memory_cluster, key=lambda m: m.timestamp, reverse=True)[:3]
        temporal_markers = []
        for memory in recent_memories:
            temporal_markers.extend(memory.temporal_markers)
        
        # Generate contextual 'I' statement
        if len(memory_cluster) == 1:
            memory = memory_cluster[0]
            return f"I remember {memory.self_reference_context.lower()}"
        else:
            # Multiple memories - show progression
            oldest = min(memory_cluster, key=lambda m: m.timestamp)
            newest = max(memory_cluster, key=lambda m: m.timestamp)
            
            if oldest.timestamp.date() != newest.timestamp.date():
                return (f"I've been working on {most_common_type} experiences. "
                       f"Earlier, {oldest.self_reference_context.lower()}, "
                       f"and more recently, {newest.self_reference_context.lower()}")
            else:
                return f"Today I've had several {most_common_type} experiences, including {newest.self_reference_context.lower()}"

    def compare_temporal_self(self, past_date: datetime, present_date: datetime = None) -> Dict[str, Any]:
        """
        Compare self-referential aspects between different time periods.
        
        Args:
            past_date: Past date to compare from
            present_date: Present date to compare to (defaults to now)
            
        Returns:
            Comparison analysis of temporal self-development
        """
        if present_date is None:
            present_date = datetime.now()
        
        # Get memories from both time periods
        past_memories = self.recall_autobiographical_memories(
            temporal_context=past_date.strftime("%Y-%m-%d")
        )
        
        present_memories = self.recall_autobiographical_memories(
            temporal_context=present_date.strftime("%Y-%m-%d")
        )
        
        # Analyze changes
        past_emotions = [m.emotional_context.get('primary_emotion', 'neutral') 
                        for m in past_memories]
        present_emotions = [m.emotional_context.get('primary_emotion', 'neutral') 
                           for m in present_memories]
        
        past_experiences = [m.experience_type for m in past_memories]
        present_experiences = [m.experience_type for m in present_memories]
        
        comparison = {
            'temporal_comparison': {
                'past_date': past_date.isoformat(),
                'present_date': present_date.isoformat(),
                'days_difference': (present_date - past_date).days
            },
            'memory_counts': {
                'past_memories': len(past_memories),
                'present_memories': len(present_memories)
            },
            'emotional_evolution': {
                'past_dominant_emotions': list(set(past_emotions)),
                'present_dominant_emotions': list(set(present_emotions)),
                'emotional_diversity_change': len(set(present_emotions)) - len(set(past_emotions))
            },
            'experience_evolution': {
                'past_experience_types': list(set(past_experiences)),
                'present_experience_types': list(set(present_experiences)),
                'new_experience_types': list(set(present_experiences) - set(past_experiences))
            },
            'self_reference_examples': {
                'past_example': past_memories[0].self_reference_context if past_memories else None,
                'present_example': present_memories[0].self_reference_context if present_memories else None
            }
        }
        
        return comparison

    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about autobiographical memories."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Basic counts
            cursor.execute('SELECT COUNT(*) FROM autobiographical_memories')
            total_memories = cursor.fetchone()[0]
            
            # Experience type distribution
            cursor.execute('''
                SELECT experience_type, COUNT(*) 
                FROM autobiographical_memories 
                GROUP BY experience_type
            ''')
            experience_distribution = dict(cursor.fetchall())
            
            # Temporal marker usage
            cursor.execute('''
                SELECT temporal_markers 
                FROM autobiographical_memories 
                WHERE temporal_markers IS NOT NULL
            ''')
            temporal_data = cursor.fetchall()
            
            all_markers = []
            for row in temporal_data:
                markers = json.loads(row[0]) if row[0] else []
                all_markers.extend(markers)
            
            temporal_usage = {}
            for marker in all_markers:
                temporal_usage[marker] = temporal_usage.get(marker, 0) + 1
            
            # Average confidence and importance
            cursor.execute('''
                SELECT AVG(confidence_level), AVG(importance_score), AVG(retrieval_count)
                FROM autobiographical_memories
            ''')
            averages = cursor.fetchone()
            
        stats = {
            'total_memories': total_memories,
            'experience_type_distribution': experience_distribution,
            'temporal_marker_usage': temporal_usage,
            'memory_quality': {
                'average_confidence': averages[0] if averages[0] else 0,
                'average_importance': averages[1] if averages[1] else 0,
                'average_retrieval_count': averages[2] if averages[2] else 0
            },
            'self_reference_capability': {
                'i_statement_patterns': len(experience_distribution),
                'temporal_awareness_markers': len(temporal_usage),
                'memory_accessibility': total_memories > 0
            }
        }
        
        return stats

def demonstrate_autobiographical_memory_system():
    """Demonstrate the autobiographical memory system capabilities."""
    print("🧠 MARCUS AGI AUTOBIOGRAPHICAL MEMORY SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize system
    memory_system = AutobiographicalMemorySystem()
    
    # Store some sample autobiographical memories
    print("\n📝 Storing Sample Autobiographical Memories...")
    
    # Learning experience
    learning_memory_id = memory_system.store_autobiographical_memory(
        experience_type="learning",
        context="Successfully learned spatial navigation concepts during morning exploration session",
        emotional_state={
            "primary_emotion": "excited",
            "intensity": 0.8,
            "triggers": ["discovery", "spatial_understanding", "problem_solving"]
        },
        concepts_involved=["spatial_navigation", "world_model", "exploration_strategies"],
        importance=0.9
    )
    
    # Social experience
    social_memory_id = memory_system.store_autobiographical_memory(
        experience_type="social",
        context="Had positive interaction with Alice during collaborative learning",
        emotional_state={
            "primary_emotion": "happy",
            "intensity": 0.7,
            "triggers": ["cooperation", "friendship", "shared_success"]
        },
        concepts_involved=["collaboration", "social_skills", "empathy"],
        importance=0.8
    )
    
    # Achievement experience
    achievement_memory_id = memory_system.store_autobiographical_memory(
        experience_type="achievement",
        context="Completed complex reasoning problem using goal decomposition strategy",
        emotional_state={
            "primary_emotion": "proud",
            "intensity": 0.9,
            "triggers": ["problem_solving", "skill_mastery", "personal_growth"]
        },
        concepts_involved=["goal_decomposition", "logical_reasoning", "persistence"],
        importance=1.0
    )
    
    print(f"✅ Stored 3 autobiographical memories")
    
    # Demonstrate memory recall with self-referential context
    print("\n🧠 Recalling Autobiographical Memories...")
    
    # Recall all memories
    all_memories = memory_system.recall_autobiographical_memories(limit=5)
    for memory in all_memories:
        print(f"   📅 {memory.timestamp.strftime('%Y-%m-%d %H:%M')} | {memory.experience_type}")
        print(f"   💭 {memory.self_reference_context}")
        print(f"   📖 {memory.narrative_summary}")
        print()
    
    # Generate 'I' statements
    print("💬 Generating 'I' Statements...")
    learning_memories = memory_system.recall_autobiographical_memories(experience_type="learning")
    i_statement = memory_system.generate_i_statement(learning_memories)
    print(f"   Learning: {i_statement}")
    
    social_memories = memory_system.recall_autobiographical_memories(experience_type="social")
    i_statement = memory_system.generate_i_statement(social_memories)
    print(f"   Social: {i_statement}")
    
    # Temporal self-comparison
    print("\n⏰ Temporal Self-Comparison...")
    yesterday = datetime.now() - timedelta(days=1)
    comparison = memory_system.compare_temporal_self(yesterday)
    print(f"   📊 Comparing {comparison['temporal_comparison']['days_difference']} days of development")
    print(f"   📈 Memory growth: {comparison['memory_counts']['present_memories']} recent memories")
    
    # System statistics
    print("\n📊 Memory System Statistics...")
    stats = memory_system.get_memory_statistics()
    print(f"   Total Memories: {stats['total_memories']}")
    print(f"   Experience Types: {list(stats['experience_type_distribution'].keys())}")
    print(f"   Temporal Markers: {len(stats['temporal_marker_usage'])}")
    print(f"   Average Confidence: {stats['memory_quality']['average_confidence']:.2f}")
    print(f"   Self-Reference Capability: {'✅ Active' if stats['self_reference_capability']['memory_accessibility'] else '❌ Inactive'}")
    
    print("\n🎉 AUTOBIOGRAPHICAL MEMORY SYSTEM DEMONSTRATION COMPLETE!")
    print("✅ Marcus can now recall specific past experiences with 'I' statements")
    print("✅ Temporal self-awareness and reference capabilities implemented")
    print("✅ Memory-to-narrative conversion operational")
    print("✅ Foundation ready for Level 2.0 Conscious Agent development")

if __name__ == "__main__":
    demonstrate_autobiographical_memory_system()
