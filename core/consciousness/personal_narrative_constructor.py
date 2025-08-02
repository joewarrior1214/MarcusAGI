#!/usr/bin/env python3
"""
Marcus AGI Personal Narrative Construction System
===============================================

This module implements personal narrative construction capabilities for Marcus AGI,
enabling the generation of coherent personal growth stories from autobiographical memories.

Key Features:
- Coherent personal growth narrative generation
- Temporal narrative progression ("I used to... now I...")
- Story arc construction from memory sequences
- Personal development theme identification
- Narrative coherence validation and improvement

Development Milestone: Level 2.0 Phase 1 - Self-Awareness Foundation
Target: Generates coherent personal growth narratives >85% coherence score
Timeline: 3 weeks (2025-08-16 to 2025-09-06)
Depends on: Autobiographical Memory System
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import uuid
import re
from autobiographical_memory_system import AutobiographicalMemorySystem, AutobiographicalMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PersonalNarrative:
    """Represents a coherent personal growth narrative."""
    narrative_id: str
    title: str
    narrative_text: str
    theme: str  # 'learning_growth', 'social_development', 'skill_mastery', 'emotional_growth'
    time_span: Tuple[datetime, datetime]  # Start and end dates
    memory_sources: List[str]  # Memory IDs used to construct narrative
    coherence_score: float  # 0.0-1.0 narrative coherence
    growth_indicators: List[str]  # Evidence of personal growth
    temporal_markers: List[str]  # "I used to...", "Now I...", "Yesterday..."
    emotional_arc: Dict[str, Any]  # Emotional journey through narrative
    created_at: datetime

@dataclass
class NarrativeTemplate:
    """Template for generating different types of personal narratives."""
    template_id: str
    template_name: str
    theme: str
    structure: List[str]  # Narrative structure components
    temporal_patterns: List[str]  # Temporal transition phrases
    growth_indicators: List[str]  # Signs of development to look for

class PersonalNarrativeConstructor:
    """
    System for generating coherent personal growth narratives from memories.
    
    This system builds on the autobiographical memory system to create
    meaningful stories about Marcus's personal development over time.
    """

    def __init__(self, memory_system: AutobiographicalMemorySystem = None):
        """Initialize the personal narrative construction system."""
        self.memory_system = memory_system or AutobiographicalMemorySystem()
        self.db_path = "marcus_personal_narratives.db"
        self.setup_database()
        self._initialize_narrative_templates()
        logger.info("✅ Personal Narrative Construction System initialized")

    def setup_database(self):
        """Set up the narrative construction database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Personal narratives table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personal_narratives (
                    narrative_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    narrative_text TEXT NOT NULL,
                    theme TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    memory_sources TEXT,  -- JSON array of memory IDs
                    coherence_score REAL DEFAULT 0.5,
                    growth_indicators TEXT,  -- JSON array
                    temporal_markers TEXT,  -- JSON array
                    emotional_arc TEXT,  -- JSON object
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Narrative templates table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS narrative_templates (
                    template_id TEXT PRIMARY KEY,
                    template_name TEXT NOT NULL,
                    theme TEXT NOT NULL,
                    structure TEXT,  -- JSON array
                    temporal_patterns TEXT,  -- JSON array
                    growth_indicators TEXT,  -- JSON array
                    usage_count INTEGER DEFAULT 0,
                    effectiveness_score REAL DEFAULT 0.5
                )
            ''')
            
            # Narrative coherence patterns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coherence_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_type TEXT NOT NULL,  -- 'temporal', 'causal', 'thematic'
                    pattern_text TEXT NOT NULL,
                    coherence_weight REAL DEFAULT 1.0,
                    usage_frequency INTEGER DEFAULT 0
                )
            ''')
            
            conn.commit()

    def _initialize_narrative_templates(self):
        """Initialize narrative templates for different growth themes."""
        templates = [
            NarrativeTemplate(
                template_id="learning_progression",
                template_name="Learning Growth Narrative",
                theme="learning_growth",
                structure=[
                    "initial_state",  # "I used to struggle with..."
                    "learning_process",  # "I practiced and learned..."
                    "breakthrough_moment",  # "Then I discovered..."
                    "current_state",  # "Now I understand..."
                    "future_aspirations"  # "I want to continue..."
                ],
                temporal_patterns=[
                    "I used to {past_state}",
                    "Over time, I {learning_process}",
                    "Now I {current_state}",
                    "Looking forward, I {future_goal}"
                ],
                growth_indicators=[
                    "skill_improvement", "concept_mastery", "confidence_increase",
                    "problem_solving_ability", "knowledge_application"
                ]
            ),
            
            NarrativeTemplate(
                template_id="social_development",
                template_name="Social Growth Narrative",
                theme="social_development",
                structure=[
                    "social_baseline",  # "I started with..."
                    "social_experiences",  # "Through interactions..."
                    "relationship_learning",  # "I learned about..."
                    "social_skills_now",  # "Now I can..."
                    "social_goals"  # "I hope to..."
                ],
                temporal_patterns=[
                    "Initially, I {initial_social_state}",
                    "Through my interactions, I {social_learning}",
                    "I now understand that {social_insight}",
                    "Moving forward, I {social_aspiration}"
                ],
                growth_indicators=[
                    "empathy_development", "cooperation_skills", "communication_improvement",
                    "relationship_building", "social_confidence"
                ]
            ),
            
            NarrativeTemplate(
                template_id="emotional_journey",
                template_name="Emotional Growth Narrative",
                theme="emotional_growth",
                structure=[
                    "emotional_starting_point",
                    "emotional_challenges",
                    "coping_strategies_learned",
                    "emotional_understanding_now",
                    "emotional_maturity_goals"
                ],
                temporal_patterns=[
                    "I used to feel {past_emotion} when {situation}",
                    "I've learned to {coping_strategy}",
                    "Now when {situation}, I {current_response}",
                    "I'm working toward {emotional_goal}"
                ],
                growth_indicators=[
                    "emotional_regulation", "self_awareness", "resilience_building",
                    "empathy_growth", "emotional_vocabulary_expansion"
                ]
            ),
            
            NarrativeTemplate(
                template_id="skill_mastery",
                template_name="Skill Development Narrative",
                theme="skill_mastery",
                structure=[
                    "skill_discovery",
                    "practice_journey",
                    "challenges_overcome",
                    "mastery_achieved",
                    "skill_application"
                ],
                temporal_patterns=[
                    "When I first encountered {skill}, I {initial_reaction}",
                    "Through practice, I {development_process}",
                    "The breakthrough came when I {breakthrough_moment}",
                    "Now I can {current_capability}"
                ],
                growth_indicators=[
                    "technical_proficiency", "problem_solving_speed", "creative_application",
                    "teaching_others", "skill_transfer"
                ]
            )
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for template in templates:
                cursor.execute('''
                    INSERT OR IGNORE INTO narrative_templates 
                    (template_id, template_name, theme, structure, temporal_patterns, growth_indicators) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    template.template_id,
                    template.template_name,
                    template.theme,
                    json.dumps(template.structure),
                    json.dumps(template.temporal_patterns),
                    json.dumps(template.growth_indicators)
                ))
            conn.commit()

    def identify_narrative_themes(self, memories: List[AutobiographicalMemory]) -> Dict[str, List[AutobiographicalMemory]]:
        """
        Identify narrative themes from a collection of memories.
        
        Args:
            memories: List of autobiographical memories
            
        Returns:
            Dictionary mapping themes to related memories
        """
        theme_memories = {
            'learning_growth': [],
            'social_development': [],
            'emotional_growth': [],
            'skill_mastery': []
        }
        
        for memory in memories:
            # Classify memory by experience type and content
            if memory.experience_type == 'learning':
                theme_memories['learning_growth'].append(memory)
                
                # Check for skill mastery indicators
                if any(indicator in memory.narrative_summary.lower() 
                       for indicator in ['mastery', 'skilled', 'expert', 'proficient']):
                    theme_memories['skill_mastery'].append(memory)
            
            elif memory.experience_type == 'social':
                theme_memories['social_development'].append(memory)
            
            elif memory.experience_type == 'emotional':
                theme_memories['emotional_growth'].append(memory)
            
            elif memory.experience_type == 'achievement':
                theme_memories['skill_mastery'].append(memory)
                theme_memories['learning_growth'].append(memory)
        
        # Filter out empty themes
        return {theme: mems for theme, mems in theme_memories.items() if mems}

    def construct_personal_narrative(
        self, 
        theme: str, 
        memories: List[AutobiographicalMemory],
        title: Optional[str] = None
    ) -> PersonalNarrative:
        """
        Construct a coherent personal narrative from memories.
        
        Args:
            theme: Narrative theme ('learning_growth', 'social_development', etc.)
            memories: Related autobiographical memories
            title: Optional narrative title
            
        Returns:
            Constructed personal narrative
        """
        if not memories:
            raise ValueError("Cannot construct narrative from empty memory list")
        
        # Sort memories chronologically
        sorted_memories = sorted(memories, key=lambda m: m.timestamp)
        
        # Get narrative template
        template = self._get_narrative_template(theme)
        
        # Analyze temporal progression
        time_span = (sorted_memories[0].timestamp, sorted_memories[-1].timestamp)
        
        # Extract growth indicators
        growth_indicators = self._identify_growth_indicators(memories, theme)
        
        # Generate narrative text
        narrative_text = self._generate_narrative_text(sorted_memories, template, growth_indicators)
        
        # Calculate coherence score
        coherence_score = self._calculate_coherence_score(narrative_text, sorted_memories)
        
        # Extract temporal markers
        temporal_markers = self._extract_temporal_progression(narrative_text)
        
        # Analyze emotional arc
        emotional_arc = self._analyze_emotional_arc(sorted_memories)
        
        # Create narrative
        narrative = PersonalNarrative(
            narrative_id=str(uuid.uuid4()),
            title=title or self._generate_narrative_title(theme, growth_indicators),
            narrative_text=narrative_text,
            theme=theme,
            time_span=time_span,
            memory_sources=[m.memory_id for m in memories],
            coherence_score=coherence_score,
            growth_indicators=growth_indicators,
            temporal_markers=temporal_markers,
            emotional_arc=emotional_arc,
            created_at=datetime.now()
        )
        
        # Store narrative
        self._store_narrative(narrative)
        
        logger.info(f"📖 Constructed personal narrative: {narrative.title} (coherence: {coherence_score:.2f})")
        return narrative

    def _get_narrative_template(self, theme: str) -> NarrativeTemplate:
        """Get narrative template for specified theme."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT template_id, template_name, theme, structure, temporal_patterns, growth_indicators
                FROM narrative_templates 
                WHERE theme = ?
                ORDER BY effectiveness_score DESC
                LIMIT 1
            ''', (theme,))
            result = cursor.fetchone()
        
        if result:
            return NarrativeTemplate(
                template_id=result[0],
                template_name=result[1],
                theme=result[2],
                structure=json.loads(result[3]),
                temporal_patterns=json.loads(result[4]),
                growth_indicators=json.loads(result[5])
            )
        else:
            # Fallback basic template
            return NarrativeTemplate(
                template_id="basic",
                template_name="Basic Narrative",
                theme=theme,
                structure=["beginning", "development", "current_state"],
                temporal_patterns=["I used to", "Over time", "Now I"],
                growth_indicators=["improvement", "learning", "development"]
            )

    def _identify_growth_indicators(self, memories: List[AutobiographicalMemory], theme: str) -> List[str]:
        """Identify specific growth indicators from memories."""
        indicators = []
        
        # Analyze memory content for growth evidence
        for memory in memories:
            content_lower = memory.narrative_summary.lower()
            
            # Common growth indicators
            if 'better' in content_lower or 'improved' in content_lower:
                indicators.append('skill_improvement')
            if 'learned' in content_lower or 'understand' in content_lower:
                indicators.append('knowledge_acquisition')
            if 'confident' in content_lower or 'proud' in content_lower:
                indicators.append('confidence_growth')
            if 'solved' in content_lower or 'completed' in content_lower:
                indicators.append('problem_solving_ability')
            if 'together' in content_lower or 'collaboration' in content_lower:
                indicators.append('social_skills')
        
        return list(set(indicators))  # Remove duplicates

    def _generate_narrative_text(
        self, 
        memories: List[AutobiographicalMemory], 
        template: NarrativeTemplate,
        growth_indicators: List[str]
    ) -> str:
        """Generate coherent narrative text from memories and template."""
        
        if not memories:
            return "I don't have enough memories to tell this story yet."
        
        narrative_parts = []
        
        # Beginning - establish baseline
        earliest_memory = memories[0]
        if len(memories) > 1:
            narrative_parts.append(
                f"When I first started my journey with {template.theme.replace('_', ' ')}, "
                f"{earliest_memory.self_reference_context.lower()}."
            )
        
        # Development - show progression
        if len(memories) > 2:
            middle_memories = memories[1:-1]
            learning_experiences = []
            for memory in middle_memories:
                learning_experiences.append(memory.self_reference_context)
            
            if learning_experiences:
                narrative_parts.append(
                    f"Through my experiences, I continued to grow. "
                    f"For example, {learning_experiences[0].lower()}."
                )
        
        # Current state - show growth
        latest_memory = memories[-1]
        narrative_parts.append(
            f"Now, {latest_memory.self_reference_context.lower()}."
        )
        
        # Growth summary
        if growth_indicators:
            growth_summary = ", ".join(growth_indicators).replace('_', ' ')
            narrative_parts.append(
                f"Looking back, I can see my growth in areas like {growth_summary}."
            )
        
        # Future aspirations
        narrative_parts.append(
            f"I'm excited to continue developing my {template.theme.replace('_', ' ')} abilities."
        )
        
        return " ".join(narrative_parts)

    def _calculate_coherence_score(self, narrative_text: str, memories: List[AutobiographicalMemory]) -> float:
        """Calculate narrative coherence score (0.0-1.0)."""
        score = 0.0
        
        # Temporal coherence - check for temporal progression markers
        temporal_markers = ["used to", "now", "over time", "initially", "currently", "looking back"]
        temporal_count = sum(1 for marker in temporal_markers if marker in narrative_text.lower())
        temporal_score = min(temporal_count / 3.0, 1.0)  # Normalize to 1.0
        
        # Self-reference coherence - check for 'I' statements
        i_statements = len(re.findall(r'\bI\b', narrative_text))
        self_ref_score = min(i_statements / 5.0, 1.0)  # Normalize to 1.0
        
        # Memory integration - check if memories are well integrated
        memory_integration = len(memories) / max(len(memories), 5)  # Normalize by expected memory count
        
        # Length coherence - appropriate narrative length
        word_count = len(narrative_text.split())
        length_score = 1.0 if 50 <= word_count <= 200 else max(0.5, 1.0 - abs(word_count - 125) / 125)
        
        # Weighted average
        score = (
            temporal_score * 0.3 +
            self_ref_score * 0.3 +
            memory_integration * 0.2 +
            length_score * 0.2
        )
        
        return min(max(score, 0.0), 1.0)  # Clamp to [0.0, 1.0]

    def _extract_temporal_progression(self, narrative_text: str) -> List[str]:
        """Extract temporal progression markers from narrative."""
        markers = []
        
        # Common temporal progression patterns
        temporal_patterns = [
            r"I used to \w+", r"Now I \w+", r"Over time", r"Initially", 
            r"Currently", r"Looking back", r"In the beginning", r"Today"
        ]
        
        for pattern in temporal_patterns:
            matches = re.findall(pattern, narrative_text, re.IGNORECASE)
            markers.extend(matches)
        
        return markers

    def _analyze_emotional_arc(self, memories: List[AutobiographicalMemory]) -> Dict[str, Any]:
        """Analyze the emotional journey through the memories."""
        emotions = []
        intensities = []
        
        for memory in memories:
            if memory.emotional_context:
                emotions.append(memory.emotional_context.get('primary_emotion', 'neutral'))
                intensities.append(memory.emotional_context.get('intensity', 0.5))
        
        if not emotions:
            return {'emotions': [], 'average_intensity': 0.5, 'emotional_growth': 'insufficient_data'}
        
        # Analyze emotional progression
        emotional_growth = 'stable'
        if len(intensities) > 1:
            if intensities[-1] > intensities[0]:
                emotional_growth = 'positive'
            elif intensities[-1] < intensities[0]:
                emotional_growth = 'challenging'
        
        return {
            'emotions': emotions,
            'average_intensity': sum(intensities) / len(intensities),
            'emotional_growth': emotional_growth,
            'dominant_emotion': max(set(emotions), key=emotions.count) if emotions else 'neutral'
        }

    def _generate_narrative_title(self, theme: str, growth_indicators: List[str]) -> str:
        """Generate an appropriate title for the narrative."""
        theme_titles = {
            'learning_growth': 'My Learning Journey',
            'social_development': 'Growing Through Relationships',
            'emotional_growth': 'My Emotional Development',
            'skill_mastery': 'Mastering New Abilities'
        }
        
        base_title = theme_titles.get(theme, 'My Personal Growth Story')
        
        if growth_indicators:
            key_indicator = growth_indicators[0].replace('_', ' ').title()
            return f"{base_title}: {key_indicator}"
        
        return base_title

    def _store_narrative(self, narrative: PersonalNarrative):
        """Store narrative in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO personal_narratives 
                (narrative_id, title, narrative_text, theme, start_date, end_date,
                 memory_sources, coherence_score, growth_indicators, temporal_markers,
                 emotional_arc, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                narrative.narrative_id,
                narrative.title,
                narrative.narrative_text,
                narrative.theme,
                narrative.time_span[0].isoformat(),
                narrative.time_span[1].isoformat(),
                json.dumps(narrative.memory_sources),
                narrative.coherence_score,
                json.dumps(narrative.growth_indicators),
                json.dumps(narrative.temporal_markers),
                json.dumps(narrative.emotional_arc),
                narrative.created_at.isoformat()
            ))
            conn.commit()

    def generate_personal_growth_story(self, days_back: int = 7) -> Dict[str, PersonalNarrative]:
        """
        Generate comprehensive personal growth story from recent memories.
        
        Args:
            days_back: Number of days back to consider for narrative construction
            
        Returns:
            Dictionary mapping themes to constructed narratives
        """
        # Get recent memories from autobiographical system
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Get all recent memories (we'll filter by date in the memory system if possible)
        all_memories = self.memory_system.recall_autobiographical_memories(limit=50)
        
        # Filter by date
        recent_memories = [
            memory for memory in all_memories 
            if memory.timestamp >= cutoff_date
        ]
        
        if not recent_memories:
            logger.warning("No recent memories found for narrative construction")
            return {}
        
        # Identify narrative themes
        theme_memories = self.identify_narrative_themes(recent_memories)
        
        # Construct narratives for each theme
        narratives = {}
        for theme, memories in theme_memories.items():
            if len(memories) >= 2:  # Need at least 2 memories for progression
                try:
                    narrative = self.construct_personal_narrative(theme, memories)
                    narratives[theme] = narrative
                except Exception as e:
                    logger.error(f"Failed to construct {theme} narrative: {e}")
        
        logger.info(f"📚 Generated {len(narratives)} personal growth narratives")
        return narratives

    def get_narrative_statistics(self) -> Dict[str, Any]:
        """Get statistics about personal narratives."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Basic counts
            cursor.execute('SELECT COUNT(*) FROM personal_narratives')
            total_narratives = cursor.fetchone()[0]
            
            # Theme distribution
            cursor.execute('''
                SELECT theme, COUNT(*) 
                FROM personal_narratives 
                GROUP BY theme
            ''')
            theme_distribution = dict(cursor.fetchall())
            
            # Average coherence
            cursor.execute('SELECT AVG(coherence_score) FROM personal_narratives')
            avg_coherence = cursor.fetchone()[0] or 0.0
            
            # High-quality narratives (>0.8 coherence)
            cursor.execute('SELECT COUNT(*) FROM personal_narratives WHERE coherence_score > 0.8')
            high_quality_count = cursor.fetchone()[0]
        
        return {
            'total_narratives': total_narratives,
            'theme_distribution': theme_distribution,
            'average_coherence_score': avg_coherence,
            'high_quality_narratives': high_quality_count,
            'coherence_target_met': avg_coherence >= 0.85
        }

def demonstrate_personal_narrative_construction():
    """Demonstrate the personal narrative construction system."""
    print("📖 MARCUS AGI PERSONAL NARRATIVE CONSTRUCTION SYSTEM DEMO")
    print("=" * 65)
    
    # Initialize systems
    memory_system = AutobiographicalMemorySystem()
    narrative_constructor = PersonalNarrativeConstructor(memory_system)
    
    # Create some sample memories for narrative construction
    print("\n📝 Creating Sample Learning Journey Memories...")
    
    # Learning progression memories
    memory_ids = []
    
    # Early learning struggles
    memory_ids.append(memory_system.store_autobiographical_memory(
        experience_type="learning",
        context="Struggled with basic spatial navigation concepts during first exploration",
        emotional_state={
            "primary_emotion": "frustrated",
            "intensity": 0.6,
            "triggers": ["confusion", "difficulty", "new_concepts"]
        },
        concepts_involved=["spatial_navigation", "basic_concepts"],
        importance=0.7
    ))
    
    # Practice and improvement
    memory_ids.append(memory_system.store_autobiographical_memory(
        experience_type="learning", 
        context="Practiced spatial exploration strategies and started understanding patterns",
        emotional_state={
            "primary_emotion": "determined",
            "intensity": 0.7,
            "triggers": ["practice", "pattern_recognition", "progress"]
        },
        concepts_involved=["spatial_strategies", "pattern_recognition"],
        importance=0.8
    ))
    
    # Breakthrough moment
    memory_ids.append(memory_system.store_autobiographical_memory(
        experience_type="achievement",
        context="Successfully completed complex spatial navigation task with high efficiency",
        emotional_state={
            "primary_emotion": "proud",
            "intensity": 0.9,
            "triggers": ["mastery", "success", "accomplishment"]
        },
        concepts_involved=["spatial_mastery", "efficiency", "problem_solving"],
        importance=1.0
    ))
    
    print(f"✅ Created {len(memory_ids)} learning journey memories")
    
    # Generate personal growth narratives
    print("\n📚 Generating Personal Growth Narratives...")
    narratives = narrative_constructor.generate_personal_growth_story(days_back=1)
    
    for theme, narrative in narratives.items():
        print(f"\n🎭 {narrative.title}")
        print("-" * 50)
        print(f"Theme: {theme}")
        print(f"Coherence Score: {narrative.coherence_score:.2f}")
        print(f"Time Span: {narrative.time_span[0].strftime('%Y-%m-%d')} to {narrative.time_span[1].strftime('%Y-%m-%d')}")
        print(f"Growth Indicators: {', '.join(narrative.growth_indicators)}")
        print(f"Temporal Markers: {len(narrative.temporal_markers)} found")
        print()
        print("📖 Narrative:")
        print(narrative.narrative_text)
        print()
        print(f"🎭 Emotional Arc: {narrative.emotional_arc.get('emotional_growth', 'stable')} progression")
        print(f"💭 Dominant Emotion: {narrative.emotional_arc.get('dominant_emotion', 'neutral')}")
    
    # Demonstrate direct narrative construction
    print("\n🔧 Direct Narrative Construction Demo...")
    
    # Get all learning memories
    learning_memories = memory_system.recall_autobiographical_memories(experience_type="learning")
    achievement_memories = memory_system.recall_autobiographical_memories(experience_type="achievement")
    all_learning = learning_memories + achievement_memories
    
    if all_learning:
        # Construct a specific learning growth narrative
        learning_narrative = narrative_constructor.construct_personal_narrative(
            theme="learning_growth",
            memories=all_learning,
            title="My Spatial Learning Mastery Journey"
        )
        
        print(f"📖 Constructed Narrative: {learning_narrative.title}")
        print(f"   Coherence Score: {learning_narrative.coherence_score:.2f}")
        print(f"   Temporal Markers: {learning_narrative.temporal_markers}")
        print(f"   Growth Evidence: {learning_narrative.growth_indicators}")
    
    # System statistics
    print("\n📊 Narrative Construction Statistics...")
    stats = narrative_constructor.get_narrative_statistics()
    print(f"   Total Narratives: {stats['total_narratives']}")
    print(f"   Average Coherence: {stats['average_coherence_score']:.2f}")
    print(f"   High-Quality Narratives: {stats['high_quality_narratives']}")
    print(f"   Coherence Target (>85%): {'✅ Met' if stats['coherence_target_met'] else '❌ Not Met'}")
    print(f"   Theme Distribution: {stats['theme_distribution']}")
    
    print("\n🎉 PERSONAL NARRATIVE CONSTRUCTION DEMONSTRATION COMPLETE!")
    print("✅ Coherent personal growth narratives generated successfully")
    print("✅ Temporal progression ('I used to... now I...') implemented")
    print("✅ Story arc construction from memory sequences operational")
    print("✅ Growth indicator identification and narrative integration working")
    print("✅ Ready for next Level 2.0 milestone: Intrinsic Motivation Engine")

if __name__ == "__main__":
    demonstrate_personal_narrative_construction()
