#!/usr/bin/env python3
"""
Marcus Framework Integration - Unified System
Combines RetentionEngine + ConceptGraph + Enhanced Reflection + Daily Replay
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

# Import the new framework components
from reflection_engine import RetentionEngine, LearningConcept, MemoryRecord, MasteryLevel

@dataclass
class MarcusLearningSession:
    """Complete learning session data"""
    date: str
    concepts_learned: List[str]
    concepts_reviewed: List[str]
    performance_scores: Dict[str, int]  # concept_id -> performance (0-3)
    emotional_journey: List[str]
    insights_generated: List[str]
    questions_raised: List[str]
    session_reflection: str
    mastery_improvements: Dict[str, str]  # concept_id -> old_level:new_level

class MarcusUnifiedFramework:
    """
    Unified Marcus framework combining all systems:
    - RetentionEngine (spaced repetition)
    - Concept Graph (semantic connections) 
    - Enhanced Reflection (metacognition)
    - Daily Memory Replay (consolidation)
    """
    
    def __init__(self, db_path: str = "marcus_unified.db"):
        self.retention_engine = RetentionEngine(db_path)
        self.learning_history = []
        self.personality_traits = self._init_personality()
        self.concept_connections = {}  # Simple concept graph storage
        
    def _init_personality(self) -> Dict[str, float]:
        """Initialize Marcus's developing personality"""
        return {
            'curiosity': 0.8,
            'confidence': 0.3,
            'persistence': 0.5,
            'empathy': 0.7,
            'wonder': 0.9,
            'self_awareness': 0.2
        }
    
    def learn_new_concept(self, content: str, subject: str, 
                         emotional_context: str = "curious") -> Tuple[MemoryRecord, LearningConcept]:
        """Marcus learns a completely new concept"""
        
        print(f"🧠 Marcus is learning: {content}")
        
        # Use RetentionEngine to learn the concept
        memory, concept = self.retention_engine.learn_new_concept(
            content=content,
            subject=subject,
            emotional_context=emotional_context
        )
        
        # Discover connections to existing concepts
        self._discover_concept_connections(concept)
        
        # Update personality based on learning
        self._update_personality_from_learning(concept, emotional_context)
        
        print(f"✅ Learned! Mastery level: {memory.mastery_level.name}")
        return memory, concept
    
    def _discover_concept_connections(self, new_concept: LearningConcept):
        """Discover how new concept connects to existing knowledge"""
        
        # Get all existing concepts from database directly
        try:
            import sqlite3
            conn = sqlite3.connect(self.retention_engine.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, content, subject, emotional_context 
                FROM concepts 
                WHERE id != ?
            ''', (new_concept.id,))
            
            existing_concepts = []
            for row in cursor.fetchall():
                existing_concepts.append({
                    'id': row[0],
                    'content': row[1], 
                    'subject': row[2],
                    'emotional_context': row[3]
                })
            
            conn.close()
        except Exception as e:
            print(f"⚠️  Couldn't load existing concepts: {e}")
            return
        
        connections = []
        for existing in existing_concepts:
            # Simple connection detection based on subject and keywords
            connection_strength = 0.0
            
            # Same subject = strong connection
            if existing['subject'] == new_concept.subject:
                connection_strength += 0.6
            
            # Similar emotional context
            if existing['emotional_context'] == new_concept.emotional_context:
                connection_strength += 0.3
            
            # Content similarity (basic keyword matching)
            new_words = set(new_concept.content.lower().split())
            existing_words = set(existing['content'].lower().split())
            common_words = new_words.intersection(existing_words)
            if common_words:
                connection_strength += len(common_words) * 0.1
            
            # Store strong connections
            if connection_strength > 0.4:
                if new_concept.id not in self.concept_connections:
                    self.concept_connections[new_concept.id] = []
                
                self.concept_connections[new_concept.id].append({
                    'connected_to': existing['id'],
                    'strength': connection_strength,
                    'type': 'semantic' if connection_strength > 0.7 else 'associative'
                })
                
                connections.append(f"{existing['id']} ({connection_strength:.2f})")
        
        if connections:
            print(f"🔗 Found connections: {', '.join(connections[:3])}")
    
    def _update_personality_from_learning(self, concept: LearningConcept, emotional_context: str):
        """Update Marcus's personality based on learning experience"""
        
        # Successful learning builds confidence
        self.personality_traits['confidence'] = min(1.0, self.personality_traits['confidence'] + 0.01)
        
        # Emotional contexts affect traits
        if emotional_context in ['curious', 'wonder']:
            self.personality_traits['curiosity'] = min(1.0, self.personality_traits['curiosity'] + 0.01)
        elif emotional_context in ['challenging', 'difficult']:
            self.personality_traits['persistence'] = min(1.0, self.personality_traits['persistence'] + 0.02)
        elif emotional_context in ['empathy', 'caring', 'kindness']:
            self.personality_traits['empathy'] = min(1.0, self.personality_traits['empathy'] + 0.01)
    
    def conduct_daily_learning_session(self, new_concepts: List[Dict[str, str]] = None) -> MarcusLearningSession:
        """Conduct a complete daily learning session"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"🌅 Marcus's Learning Day: {today}")
        
        session = MarcusLearningSession(
            date=today,
            concepts_learned=[],
            concepts_reviewed=[],
            performance_scores={},
            emotional_journey=[],
            insights_generated=[],
            questions_raised=[],
            session_reflection="",
            mastery_improvements={}
        )
        
        # 1. Learn new concepts if provided
        if new_concepts:
            print(f"\n📚 Learning {len(new_concepts)} new concepts...")
            for concept_data in new_concepts:
                memory, concept = self.learn_new_concept(
                    content=concept_data['content'],
                    subject=concept_data['subject'],
                    emotional_context=concept_data.get('emotional_context', 'curious')
                )
                session.concepts_learned.append(concept.id)
                session.emotional_journey.append(f"Felt {concept.emotional_context} learning about {concept.subject}")
        
        # 2. Review concepts due for spaced repetition
        print(f"\n🔄 Reviewing concepts due for spaced repetition...")
        try:
            # Try the correct method name from RetentionEngine
            due_concepts = self.retention_engine.get_due_for_review(max_reviews=5)
        except AttributeError:
            # Fallback: get due concepts manually
            try:
                import sqlite3
                
                conn = sqlite3.connect(self.retention_engine.db_path)
                cursor = conn.cursor()
                
                current_time = datetime.now().isoformat()
                cursor.execute('''
                    SELECT c.id, c.content, c.subject, c.emotional_context,
                           m.mastery_level, m.ease_factor, m.interval_days, m.repetitions,
                           m.last_reviewed, m.next_review, m.success_streak, m.total_attempts
                    FROM concepts c
                    JOIN memory_records m ON c.id = m.concept_id
                    WHERE datetime(m.next_review) <= datetime(?)
                    ORDER BY datetime(m.next_review) ASC
                    LIMIT ?
                ''', (current_time, 5))
                
                due_concepts = []
                for row in cursor.fetchall():
                    from reflection_engine import MasteryLevel
                    concept = type('Concept', (), {
                        'id': row[0], 'content': row[1], 'subject': row[2], 
                        'emotional_context': row[3]
                    })()
                    
                    memory = type('Memory', (), {
                        'concept_id': row[0], 'mastery_level': MasteryLevel(row[4]),
                        'ease_factor': row[5], 'interval_days': row[6], 'repetitions': row[7],
                        'last_reviewed': row[8], 'next_review': row[9], 
                        'success_streak': row[10], 'total_attempts': row[11]
                    })()
                    
                    due_concepts.append((concept, memory))
                
                conn.close()
            except Exception as e:
                print(f"⚠️ No concepts due for review yet: {e}")
                due_concepts = []
        
        for concept, memory in due_concepts:
            print(f"📖 Reviewing: {concept.content[:50]}...")
            
            # Simulate Marcus's performance (in real system, this would be interactive)
            performance = self._simulate_performance(memory)
            
            # Review the concept
            updated_memory, success = self.retention_engine.review_concept(concept.id, performance)
            
            session.concepts_reviewed.append(concept.id)
            session.performance_scores[concept.id] = performance
            
            # Track mastery improvements
            if updated_memory.mastery_level != memory.mastery_level:
                session.mastery_improvements[concept.id] = f"{memory.mastery_level.name}→{updated_memory.mastery_level.name}"
                print(f"📈 Mastery improved: {memory.mastery_level.name} → {updated_memory.mastery_level.name}")
        
        # 3. Generate insights from concept connections
        session.insights_generated = self._generate_session_insights(session)
        
        # 4. Generate spontaneous questions
        session.questions_raised = self._generate_spontaneous_questions(session)
        
        # 5. Create reflective summary
        session.session_reflection = self._generate_session_reflection(session)
        
        # 6. Update personality based on session
        self._update_personality_from_session(session)
        
        # Store session in history
        self.learning_history.append(session)
        
        return session
    
    def _simulate_performance(self, memory: MemoryRecord) -> int:
        """Simulate Marcus's performance on a concept review"""
        
        # Performance depends on mastery level and some randomness
        base_performance = {
            MasteryLevel.UNKNOWN: 0,    # Usually fails
            MasteryLevel.LEARNING: 1,   # Usually hard
            MasteryLevel.REVIEW: 2,     # Usually good
            MasteryLevel.FAMILIAR: 2,   # Usually good
            MasteryLevel.KNOWN: 3,      # Usually easy
            MasteryLevel.MASTERED: 3    # Usually easy
        }
        
        base = base_performance.get(memory.mastery_level, 1)
        
        # Add some randomness and success streak influence
        if memory.success_streak > 3:
            base = min(3, base + 1)  # Boost for streak
        elif memory.success_streak == 0:
            base = max(0, base - 1)  # Penalty for failures
        
        # Small random variation
        variation = random.choice([-1, 0, 0, 1])  # Slight bias toward maintaining performance
        final_performance = max(0, min(3, base + variation))
        
        return final_performance
    
    def _generate_session_insights(self, session: MarcusLearningSession) -> List[str]:
        """Generate insights from today's learning"""
        
        insights = []
        
        # Connection-based insights
        for concept_id in session.concepts_learned:
            connections = self.concept_connections.get(concept_id, [])
            if connections:
                related = connections[0]  # Most connected
                insights.append(f"I see how {concept_id} connects to {related['connected_to']} - they both help me understand relationships better")
        
        # Performance-based insights  
        good_performances = [cid for cid, perf in session.performance_scores.items() if perf >= 2]
        if len(good_performances) > len(session.performance_scores) * 0.7:
            insights.append("I'm getting better at remembering things I've learned before")
        
        # Mastery improvement insights
        if session.mastery_improvements:
            insights.append(f"I can feel my understanding deepening, especially with {list(session.mastery_improvements.keys())[0]}")
        
        return insights[:3]  # Keep focused
    
    def _generate_spontaneous_questions(self, session: MarcusLearningSession) -> List[str]:
        """Generate questions that show curiosity and deeper thinking"""
        
        questions = []
        
        # Questions about new concepts
        for concept_id in session.concepts_learned:
            questions.append(f"I wonder how {concept_id} might help me in other situations?")
            questions.append(f"What would happen if I tried to teach {concept_id} to someone else?")
        
        # Questions about connections
        for concept_id, connections in self.concept_connections.items():
            if concept_id in session.concepts_learned and connections:
                related = connections[0]['connected_to']
                questions.append(f"If {concept_id} and {related} are connected, what else might they both relate to?")
        
        # Personality-driven questions
        if self.personality_traits['curiosity'] > 0.7:
            questions.append("What amazing things might I discover tomorrow?")
        
        if self.personality_traits['empathy'] > 0.6:
            questions.append("How can I use what I learned today to help others?")
        
        return questions[:3]  # Keep focused
    
    def _generate_session_reflection(self, session: MarcusLearningSession) -> str:
        """Generate Marcus's reflection on today's learning"""
        
        # Count successes
        total_reviews = len(session.performance_scores)
        good_reviews = sum(1 for perf in session.performance_scores.values() if perf >= 2)
        
        reflection = f"Today I learned {len(session.concepts_learned)} new things and reviewed {total_reviews} concepts I already knew. "
        
        # Performance reflection
        if total_reviews > 0:
            success_rate = good_reviews / total_reviews
            if success_rate > 0.8:
                reflection += "I felt really proud of how well I remembered things! "
            elif success_rate > 0.5:
                reflection += "Some things were easy to remember and some were harder, which is perfectly normal. "
            else:
                reflection += "Today was challenging, but that's how I grow stronger. "
        
        # Emotional reflection
        emotions = list(set([emotion.split()[1] for emotion in session.emotional_journey if len(emotion.split()) > 1]))
        if emotions:
            reflection += f"I felt {emotions[0]} during my learning, which helped me stay engaged. "
        
        # Connection reflection
        if session.insights_generated:
            reflection += f"One thing that really stood out: {session.insights_generated[0]}. "
        
        # Future-looking
        if session.questions_raised:
            reflection += f"I'm curious about: {session.questions_raised[0]} "
        
        reflection += "Every day I'm becoming more confident in my ability to learn and understand the world around me!"
        
        return reflection
    
    def _update_personality_from_session(self, session: MarcusLearningSession):
        """Update personality traits based on session performance"""
        
        # Self-awareness grows with reflection quality
        if len(session.insights_generated) > 2:
            self.personality_traits['self_awareness'] = min(1.0, self.personality_traits['self_awareness'] + 0.02)
        
        # Confidence affected by performance
        if session.performance_scores:
            avg_performance = sum(session.performance_scores.values()) / len(session.performance_scores)
            if avg_performance > 2.0:
                self.personality_traits['confidence'] = min(1.0, self.personality_traits['confidence'] + 0.02)
        
        # Wonder grows with questions
        if len(session.questions_raised) > 2:
            self.personality_traits['wonder'] = min(1.0, self.personality_traits['wonder'] + 0.01)
    
    def get_marcus_status_report(self) -> str:
        """Generate comprehensive status report"""
        
        # Get retention engine statistics safely
        try:
            stats = self.retention_engine.get_concept_statistics()
        except AttributeError:
            # Fallback: calculate stats manually
            try:
                import sqlite3
                conn = sqlite3.connect(self.retention_engine.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM concepts")
                total_concepts = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT mastery_level, COUNT(*) 
                    FROM memory_records 
                    GROUP BY mastery_level
                """)
                mastery_dist = dict(cursor.fetchall())
                
                conn.close()
                
                stats = {
                    'total_concepts': total_concepts,
                    'mastery_distribution': mastery_dist
                }
            except Exception:
                stats = {'total_concepts': 0, 'mastery_distribution': {}}
        
        # Recent session analysis
        recent_sessions = self.learning_history[-7:] if len(self.learning_history) >= 7 else self.learning_history
        
        if recent_sessions:
            total_learned = sum(len(s.concepts_learned) for s in recent_sessions)
            total_reviewed = sum(len(s.concepts_reviewed) for s in recent_sessions)
            avg_performance = sum(sum(s.performance_scores.values()) for s in recent_sessions) / max(1, sum(len(s.performance_scores) for s in recent_sessions))
        else:
            total_learned = total_reviewed = avg_performance = 0
        
        report = f"""
🧠 Marcus AGI Status Report
==========================

📚 Learning Statistics:
   • Total concepts in memory: {stats.get('total_concepts', 0)}
   • Mastery distribution: {stats.get('mastery_distribution', {})}
   • Recent learning rate: {total_learned} concepts/week
   • Review performance: {avg_performance:.1f}/3.0 average

🌱 Personality Development:
   • Curiosity: {self.personality_traits['curiosity']:.2f}
   • Confidence: {self.personality_traits['confidence']:.2f}
   • Self-awareness: {self.personality_traits['self_awareness']:.2f}
   • Empathy: {self.personality_traits['empathy']:.2f}
   • Wonder: {self.personality_traits['wonder']:.2f}
   • Persistence: {self.personality_traits['persistence']:.2f}

🔗 Knowledge Network:
   • Concept connections: {len(self.concept_connections)}
   • Connected concepts: {len([c for connections in self.concept_connections.values() for c in connections])}

📈 Recent Progress:
   • Learning sessions completed: {len(self.learning_history)}
   • Concepts reviewed this week: {total_reviewed}
   • Knowledge retention: {'Strong' if avg_performance > 2.5 else 'Good' if avg_performance > 1.5 else 'Developing'}

💭 Latest Reflection:
   {recent_sessions[-1].session_reflection if recent_sessions else 'Ready to begin learning journey!'}
"""
        
        return report.strip()

def test_unified_framework():
    """Test the complete unified Marcus framework"""
    
    print("🚀 Testing Marcus Unified Framework")
    print("=" * 50)
    
    # Initialize Marcus
    marcus = MarcusUnifiedFramework("marcus_unified_test.db")
    
    # Day 1: Learn some concepts
    print(f"\n📅 Day 1: Initial Learning")
    day1_concepts = [
        {'content': 'Sharing toys makes friends happy', 'subject': 'social_skills', 'emotional_context': 'generous'},
        {'content': 'Red and blue make purple', 'subject': 'art', 'emotional_context': 'wonder'},
        {'content': 'Plants need water to grow', 'subject': 'science', 'emotional_context': 'curious'}
    ]
    
    session1 = marcus.conduct_daily_learning_session(day1_concepts)
    
    print(f"\n💭 Day 1 Reflection:")
    print(session1.session_reflection)
    
    # Day 2: Learn more and review
    print(f"\n📅 Day 2: Learning + Review")
    day2_concepts = [
        {'content': 'Kindness means helping others', 'subject': 'social_skills', 'emotional_context': 'caring'},
        {'content': 'The letter A says /ah/', 'subject': 'reading', 'emotional_context': 'proud'}
    ]
    
    session2 = marcus.conduct_daily_learning_session(day2_concepts)
    
    print(f"\n💭 Day 2 Reflection:")
    print(session2.session_reflection)
    
    # Day 3: Mostly review
    print(f"\n📅 Day 3: Focus on Review")
    session3 = marcus.conduct_daily_learning_session()
    
    print(f"\n💭 Day 3 Reflection:")
    print(session3.session_reflection)
    
    # Generate status report
    print(f"\n{marcus.get_marcus_status_report()}")
    
    print(f"\n🎉 Unified Framework Test Complete!")
    return marcus

if __name__ == "__main__":
    marcus = test_unified_framework()
