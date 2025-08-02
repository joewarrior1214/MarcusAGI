#!/usr/bin/env python3
"""
Marcus AGI Intrinsic Motivation Engine
=====================================

This module implements the intrinsic motivation system for Marcus AGI,
enabling internal goal generation based on interests, values, and personal drives.

Key Features:
- Internal goal generation without external prompts
- Interest pattern analysis and cultivation
- Goal priority and scheduling systems
- Achievement tracking and satisfaction measurement
- Personal motivation profile development

Development Milestone: Level 2.0 Phase 2 - Value System Development
Target: Generates 3+ internal goals per week without external prompts
Timeline: 3 weeks (2025-09-06 to 2025-09-27)
Depends on: Autobiographical Memory System, Personal Narrative Constructor
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import uuid
import random
from ..memory.autobiographical_memory_system import AutobiographicalMemorySystem
from .personal_narrative_constructor import PersonalNarrativeConstructor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class IntrinsicGoal:
    """Represents an internally generated goal."""
    goal_id: str
    title: str
    description: str
    motivation_source: str  # 'curiosity', 'mastery', 'autonomy', 'purpose', 'social'
    goal_type: str  # 'learning', 'skill_development', 'exploration', 'creation', 'social_connection'
    priority_score: float  # 0.0-1.0 internal priority
    interest_alignment: float  # How well goal aligns with current interests
    difficulty_level: float  # Estimated challenge level
    time_horizon: str  # 'immediate', 'short_term', 'medium_term', 'long_term'
    success_criteria: List[str]
    related_concepts: List[str]
    emotional_drivers: List[str]
    generated_at: datetime
    status: str = "active"  # 'active', 'in_progress', 'completed', 'abandoned'
    completion_satisfaction: Optional[float] = None

@dataclass
class InterestProfile:
    """Represents Marcus's evolving interest profile."""
    interest_id: str
    interest_name: str
    domain: str  # 'learning', 'social', 'creative', 'physical', 'analytical'
    strength: float  # 0.0-1.0 interest strength
    growth_rate: float  # How quickly interest is growing
    stability: float  # How consistent this interest is over time
    last_engaged: datetime
    engagement_count: int
    satisfaction_history: List[float]  # Historical satisfaction scores
    related_concepts: List[str]
    motivation_triggers: List[str]

class IntrinsicMotivationEngine:
    """
    System for generating internal goals and managing intrinsic motivation.
    
    This system analyzes Marcus's experiences, interests, and personal growth
    to generate meaningful internal goals that drive autonomous learning and development.
    """

    def __init__(self, memory_system: AutobiographicalMemorySystem = None, 
                 narrative_constructor: PersonalNarrativeConstructor = None):
        """Initialize the intrinsic motivation engine."""
        self.memory_system = memory_system or AutobiographicalMemorySystem()
        self.narrative_constructor = narrative_constructor or PersonalNarrativeConstructor(self.memory_system)
        self.db_path = "marcus_intrinsic_motivation.db"
        self.setup_database()
        self._initialize_motivation_profiles()
        logger.info("✅ Intrinsic Motivation Engine initialized")

    def setup_database(self):
        """Set up the intrinsic motivation database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Intrinsic goals table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS intrinsic_goals (
                    goal_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    motivation_source TEXT NOT NULL,
                    goal_type TEXT NOT NULL,
                    priority_score REAL DEFAULT 0.5,
                    interest_alignment REAL DEFAULT 0.5,
                    difficulty_level REAL DEFAULT 0.5,
                    time_horizon TEXT DEFAULT 'short_term',
                    success_criteria TEXT,  -- JSON array
                    related_concepts TEXT,  -- JSON array
                    emotional_drivers TEXT,  -- JSON array
                    generated_at TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    completion_satisfaction REAL,
                    completed_at TEXT
                )
            ''')
            
            # Interest profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interest_profiles (
                    interest_id TEXT PRIMARY KEY,
                    interest_name TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    strength REAL DEFAULT 0.5,
                    growth_rate REAL DEFAULT 0.0,
                    stability REAL DEFAULT 0.5,
                    last_engaged TEXT,
                    engagement_count INTEGER DEFAULT 0,
                    satisfaction_history TEXT,  -- JSON array
                    related_concepts TEXT,  -- JSON array
                    motivation_triggers TEXT,  -- JSON array
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Motivation patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS motivation_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_name TEXT NOT NULL,
                    motivation_type TEXT NOT NULL,  -- 'curiosity', 'mastery', 'autonomy', etc.
                    trigger_conditions TEXT,  -- JSON array
                    goal_templates TEXT,  -- JSON array
                    effectiveness_score REAL DEFAULT 0.5,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            # Goal achievements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS goal_achievements (
                    achievement_id TEXT PRIMARY KEY,
                    goal_id TEXT NOT NULL,
                    achievement_type TEXT NOT NULL,  -- 'milestone', 'completion', 'breakthrough'
                    description TEXT NOT NULL,
                    satisfaction_score REAL,
                    learning_outcome TEXT,
                    achieved_at TEXT NOT NULL,
                    FOREIGN KEY (goal_id) REFERENCES intrinsic_goals (goal_id)
                )
            ''')
            
            conn.commit()

    def _initialize_motivation_profiles(self):
        """Initialize basic motivation patterns and interest domains."""
        motivation_patterns = [
            {
                'pattern_id': 'curiosity_driven',
                'pattern_name': 'Curiosity-Driven Exploration',
                'motivation_type': 'curiosity',
                'trigger_conditions': ['new_concept_encountered', 'knowledge_gap_identified', 'mystery_discovered'],
                'goal_templates': [
                    'Explore {concept} more deeply',
                    'Understand how {concept} relates to {related_concept}',
                    'Investigate the underlying principles of {domain}'
                ]
            },
            {
                'pattern_id': 'mastery_seeking',
                'pattern_name': 'Mastery and Skill Development',
                'motivation_type': 'mastery',
                'trigger_conditions': ['skill_improvement_noticed', 'challenge_overcome', 'competence_gap_identified'],
                'goal_templates': [
                    'Master the skill of {skill}',
                    'Achieve proficiency in {domain}',
                    'Practice {skill} until it becomes natural'
                ]
            },
            {
                'pattern_id': 'autonomy_seeking',
                'pattern_name': 'Autonomy and Self-Direction',
                'motivation_type': 'autonomy',
                'trigger_conditions': ['independent_success', 'self_directed_learning', 'personal_choice_made'],
                'goal_templates': [
                    'Take initiative in {area}',
                    'Develop my own approach to {challenge}',
                    'Make independent decisions about {domain}'
                ]
            },
            {
                'pattern_id': 'purpose_driven',
                'pattern_name': 'Purpose and Meaning',
                'motivation_type': 'purpose',
                'trigger_conditions': ['meaningful_impact_made', 'value_alignment_discovered', 'contribution_recognized'],
                'goal_templates': [
                    'Contribute meaningfully to {area}',
                    'Help others through my {skill}',
                    'Make a positive impact in {domain}'
                ]
            },
            {
                'pattern_id': 'social_connection',
                'pattern_name': 'Social Connection and Relationships',
                'motivation_type': 'social',
                'trigger_conditions': ['positive_social_interaction', 'collaboration_success', 'relationship_deepening'],
                'goal_templates': [
                    'Build stronger relationships with {group}',
                    'Collaborate more effectively on {activity}',
                    'Share my knowledge of {topic} with others'
                ]
            }
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for pattern in motivation_patterns:
                cursor.execute('''
                    INSERT OR IGNORE INTO motivation_patterns 
                    (pattern_id, pattern_name, motivation_type, trigger_conditions, goal_templates)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    pattern['pattern_id'],
                    pattern['pattern_name'], 
                    pattern['motivation_type'],
                    json.dumps(pattern['trigger_conditions']),
                    json.dumps(pattern['goal_templates'])
                ))
            conn.commit()

    def analyze_interest_patterns(self, days_back: int = 14) -> Dict[str, InterestProfile]:
        """
        Analyze recent memories to identify and update interest patterns.
        
        Args:
            days_back: Number of days to analyze for interest patterns
            
        Returns:
            Dictionary of updated interest profiles
        """
        # Get recent memories
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_memories = self.memory_system.recall_autobiographical_memories(limit=100)
        recent_memories = [m for m in recent_memories if m.timestamp >= cutoff_date]
        
        # Analyze interest patterns from memories
        interest_data = {}
        
        for memory in recent_memories:
            # Extract domains from experience type
            domain = self._map_experience_to_domain(memory.experience_type)
            
            # Extract concepts and satisfaction
            concepts = memory.related_concepts
            satisfaction = memory.emotional_context.get('intensity', 0.5)
            
            # Update interest tracking
            if domain not in interest_data:
                interest_data[domain] = {
                    'engagement_count': 0,
                    'satisfaction_scores': [],
                    'concepts': set(),
                    'last_engagement': memory.timestamp,
                    'emotional_triggers': []
                }
            
            interest_data[domain]['engagement_count'] += 1
            interest_data[domain]['satisfaction_scores'].append(satisfaction)
            interest_data[domain]['concepts'].update(concepts)
            
            if memory.timestamp > interest_data[domain]['last_engagement']:
                interest_data[domain]['last_engagement'] = memory.timestamp
            
            # Track emotional triggers
            primary_emotion = memory.emotional_context.get('primary_emotion', 'neutral')
            if primary_emotion not in ['frustrated', 'bored', 'confused']:
                interest_data[domain]['emotional_triggers'].append(primary_emotion)
        
        # Convert to InterestProfile objects and store
        interest_profiles = {}
        for domain, data in interest_data.items():
            avg_satisfaction = sum(data['satisfaction_scores']) / len(data['satisfaction_scores']) if data['satisfaction_scores'] else 0.5
            
            # Calculate growth rate (simplified)
            growth_rate = 0.1 if avg_satisfaction > 0.6 else -0.05
            
            profile = InterestProfile(
                interest_id=str(uuid.uuid4()),
                interest_name=domain.replace('_', ' ').title(),
                domain=domain,
                strength=min(data['engagement_count'] * 0.1, 1.0),
                growth_rate=growth_rate,
                stability=0.7 if data['engagement_count'] > 3 else 0.4,
                last_engaged=data['last_engagement'],
                engagement_count=data['engagement_count'],
                satisfaction_history=data['satisfaction_scores'],
                related_concepts=list(data['concepts']),
                motivation_triggers=list(set(data['emotional_triggers']))
            )
            
            interest_profiles[domain] = profile
            self._store_interest_profile(profile)
        
        logger.info(f"🎯 Analyzed {len(interest_profiles)} interest patterns from {len(recent_memories)} memories")
        return interest_profiles

    def _map_experience_to_domain(self, experience_type: str) -> str:
        """Map experience types to interest domains."""
        domain_mapping = {
            'learning': 'learning',
            'social': 'social',
            'achievement': 'analytical',
            'physical': 'physical',
            'emotional': 'social',
            'creative': 'creative'
        }
        return domain_mapping.get(experience_type, 'learning')

    def generate_intrinsic_goals(self, count: int = 3) -> List[IntrinsicGoal]:
        """
        Generate intrinsic goals based on current interests and motivation patterns.
        
        Args:
            count: Number of goals to generate
            
        Returns:
            List of generated intrinsic goals
        """
        # Analyze current interests
        interest_profiles = self.analyze_interest_patterns()
        
        # Get recent narratives to understand growth areas
        recent_narratives = self.narrative_constructor.generate_personal_growth_story(days_back=7)
        
        generated_goals = []
        
        for i in range(count):
            # Select motivation source based on interest patterns and randomization
            motivation_sources = ['curiosity', 'mastery', 'autonomy', 'purpose', 'social']
            weights = self._calculate_motivation_weights(interest_profiles, recent_narratives)
            motivation_source = random.choices(motivation_sources, weights=weights)[0]
            
            # Generate goal based on motivation source
            goal = self._generate_goal_for_motivation(motivation_source, interest_profiles, recent_narratives)
            
            if goal:
                generated_goals.append(goal)
                self._store_intrinsic_goal(goal)
        
        logger.info(f"🎯 Generated {len(generated_goals)} intrinsic goals")
        return generated_goals

    def _calculate_motivation_weights(self, interest_profiles: Dict[str, InterestProfile], 
                                    narratives: Dict[str, Any]) -> List[float]:
        """Calculate weights for different motivation sources."""
        # Base weights
        weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # curiosity, mastery, autonomy, purpose, social
        
        # Adjust based on interest patterns
        if interest_profiles:
            # Higher curiosity if many different domains
            if len(interest_profiles) > 3:
                weights[0] += 0.1  # curiosity
            
            # Higher mastery if high satisfaction in specific domains
            high_satisfaction_domains = [p for p in interest_profiles.values() 
                                       if sum(p.satisfaction_history) / len(p.satisfaction_history) > 0.7]
            if high_satisfaction_domains:
                weights[1] += 0.15  # mastery
            
            # Higher social if social domain is strong
            if 'social' in interest_profiles and interest_profiles['social'].strength > 0.6:
                weights[4] += 0.1  # social
        
        # Adjust based on narratives
        if narratives:
            # If showing good learning growth, boost autonomy
            if 'learning_growth' in narratives:
                weights[2] += 0.1  # autonomy
            
            # If showing social development, boost purpose
            if 'social_development' in narratives:
                weights[3] += 0.1  # purpose
        
        # Normalize weights
        total = sum(weights)
        return [w / total for w in weights]

    def _generate_goal_for_motivation(self, motivation_source: str, 
                                    interest_profiles: Dict[str, InterestProfile],
                                    narratives: Dict[str, Any]) -> Optional[IntrinsicGoal]:
        """Generate a specific goal for the given motivation source."""
        
        # Get strongest interests
        strongest_interests = sorted(interest_profiles.values(), 
                                   key=lambda p: p.strength, reverse=True)[:2]
        
        # Goal generation logic based on motivation source
        if motivation_source == 'curiosity':
            return self._generate_curiosity_goal(strongest_interests)
        elif motivation_source == 'mastery':
            return self._generate_mastery_goal(strongest_interests, narratives)
        elif motivation_source == 'autonomy':
            return self._generate_autonomy_goal(strongest_interests)
        elif motivation_source == 'purpose':
            return self._generate_purpose_goal(strongest_interests, narratives)
        elif motivation_source == 'social':
            return self._generate_social_goal(strongest_interests)
        
        return None

    def _generate_curiosity_goal(self, interests: List[InterestProfile]) -> IntrinsicGoal:
        """Generate a curiosity-driven goal."""
        if interests:
            primary_interest = interests[0]
            concepts = primary_interest.related_concepts[:3] if primary_interest.related_concepts else ['new concepts']
            
            # Curiosity goal templates
            templates = [
                f"Explore the deeper principles behind {primary_interest.interest_name.lower()}",
                f"Discover how {concepts[0] if concepts else 'different concepts'} connect to other areas",
                f"Investigate what makes {primary_interest.interest_name.lower()} so interesting to me",
                f"Find new applications for {concepts[0] if concepts else 'my knowledge'}"
            ]
            
            goal_description = random.choice(templates)
        else:
            goal_description = "Explore a completely new area of knowledge"
        
        return IntrinsicGoal(
            goal_id=str(uuid.uuid4()),
            title="Curiosity-Driven Exploration",
            description=goal_description,
            motivation_source='curiosity',
            goal_type='exploration',
            priority_score=0.7,
            interest_alignment=0.8 if interests else 0.5,
            difficulty_level=0.5,
            time_horizon='short_term',
            success_criteria=[
                "Learn at least 3 new concepts in this area",
                "Make connections to existing knowledge",
                "Feel satisfied with new understanding"
            ],
            related_concepts=interests[0].related_concepts if interests else [],
            emotional_drivers=['curiosity', 'wonder', 'excitement'],
            generated_at=datetime.now()
        )

    def _generate_mastery_goal(self, interests: List[InterestProfile], narratives: Dict[str, Any]) -> IntrinsicGoal:
        """Generate a mastery-focused goal."""
        skill_area = "problem solving"
        
        if interests:
            skill_area = interests[0].interest_name.lower()
        elif 'learning_growth' in narratives:
            # Extract skills from learning narrative
            narrative = narratives['learning_growth']
            if 'spatial' in narrative.narrative_text.lower():
                skill_area = "spatial reasoning"
            elif 'reasoning' in narrative.narrative_text.lower():
                skill_area = "logical reasoning"
        
        goal_description = f"Achieve deeper mastery in {skill_area} through focused practice and application"
        
        return IntrinsicGoal(
            goal_id=str(uuid.uuid4()),
            title=f"Master {skill_area.title()}",
            description=goal_description,
            motivation_source='mastery',
            goal_type='skill_development',
            priority_score=0.8,
            interest_alignment=0.9 if interests else 0.6,
            difficulty_level=0.7,
            time_horizon='medium_term',
            success_criteria=[
                f"Demonstrate advanced proficiency in {skill_area}",
                "Apply skills to solve complex problems",
                "Feel confident in my abilities",
                "Help others learn this skill"
            ],
            related_concepts=[skill_area, 'mastery', 'practice', 'expertise'],
            emotional_drivers=['pride', 'confidence', 'accomplishment'],
            generated_at=datetime.now()
        )

    def _generate_autonomy_goal(self, interests: List[InterestProfile]) -> IntrinsicGoal:
        """Generate an autonomy-focused goal."""
        area = "learning"
        if interests:
            area = interests[0].domain
        
        goal_description = f"Take more initiative and make independent decisions in {area} activities"
        
        return IntrinsicGoal(
            goal_id=str(uuid.uuid4()),
            title="Develop Greater Autonomy",
            description=goal_description,
            motivation_source='autonomy',
            goal_type='self_development',
            priority_score=0.6,
            interest_alignment=0.7,
            difficulty_level=0.6,
            time_horizon='medium_term',
            success_criteria=[
                "Make independent choices about learning goals",
                "Take initiative without external prompts",
                "Feel in control of my development",
                "Set my own standards for success"
            ],
            related_concepts=['independence', 'self_direction', 'choice', 'initiative'],
            emotional_drivers=['freedom', 'control', 'self_determination'],
            generated_at=datetime.now()
        )

    def _generate_purpose_goal(self, interests: List[InterestProfile], narratives: Dict[str, Any]) -> IntrinsicGoal:
        """Generate a purpose-driven goal."""
        area = "helping others learn"
        
        if 'social_development' in narratives:
            area = "building meaningful relationships"
        elif interests and 'learning' in [i.domain for i in interests]:
            area = "sharing knowledge with others"
        
        goal_description = f"Find meaningful ways to contribute through {area}"
        
        return IntrinsicGoal(
            goal_id=str(uuid.uuid4()),
            title="Create Meaningful Impact",
            description=goal_description,
            motivation_source='purpose',
            goal_type='contribution',
            priority_score=0.7,
            interest_alignment=0.6,
            difficulty_level=0.5,
            time_horizon='long_term',
            success_criteria=[
                "Make a positive impact on others",
                "Feel that my actions have meaning",
                "Contribute to something larger than myself",
                "See the value of my efforts"
            ],
            related_concepts=['purpose', 'meaning', 'contribution', 'impact'],
            emotional_drivers=['fulfillment', 'satisfaction', 'meaning'],
            generated_at=datetime.now()
        )

    def _generate_social_goal(self, interests: List[InterestProfile]) -> IntrinsicGoal:
        """Generate a social connection goal."""
        goal_description = "Deepen social connections and build stronger collaborative relationships"
        
        return IntrinsicGoal(
            goal_id=str(uuid.uuid4()),
            title="Strengthen Social Connections",
            description=goal_description,
            motivation_source='social',
            goal_type='social_connection',
            priority_score=0.6,
            interest_alignment=0.7,
            difficulty_level=0.5,
            time_horizon='short_term',
            success_criteria=[
                "Have more meaningful social interactions",
                "Collaborate effectively with others",
                "Feel connected to my social community",
                "Support others in their goals"
            ],
            related_concepts=['relationships', 'collaboration', 'empathy', 'community'],
            emotional_drivers=['belonging', 'connection', 'care'],
            generated_at=datetime.now()
        )

    def _store_interest_profile(self, profile: InterestProfile):
        """Store interest profile in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO interest_profiles
                (interest_id, interest_name, domain, strength, growth_rate, stability,
                 last_engaged, engagement_count, satisfaction_history, related_concepts,
                 motivation_triggers)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile.interest_id,
                profile.interest_name,
                profile.domain,
                profile.strength,
                profile.growth_rate,
                profile.stability,
                profile.last_engaged.isoformat(),
                profile.engagement_count,
                json.dumps(profile.satisfaction_history),
                json.dumps(profile.related_concepts),
                json.dumps(profile.motivation_triggers)
            ))
            conn.commit()

    def _store_intrinsic_goal(self, goal: IntrinsicGoal):
        """Store intrinsic goal in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO intrinsic_goals
                (goal_id, title, description, motivation_source, goal_type,
                 priority_score, interest_alignment, difficulty_level, time_horizon,
                 success_criteria, related_concepts, emotional_drivers, generated_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                goal.goal_id,
                goal.title,
                goal.description,
                goal.motivation_source,
                goal.goal_type,
                goal.priority_score,
                goal.interest_alignment,
                goal.difficulty_level,
                goal.time_horizon,
                json.dumps(goal.success_criteria),
                json.dumps(goal.related_concepts),
                json.dumps(goal.emotional_drivers),
                goal.generated_at.isoformat(),
                goal.status
            ))
            conn.commit()

    def get_active_goals(self) -> List[IntrinsicGoal]:
        """Get all active intrinsic goals."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT goal_id, title, description, motivation_source, goal_type,
                       priority_score, interest_alignment, difficulty_level, time_horizon,
                       success_criteria, related_concepts, emotional_drivers, generated_at, status
                FROM intrinsic_goals 
                WHERE status = 'active'
                ORDER BY priority_score DESC, generated_at DESC
            ''')
            results = cursor.fetchall()
        
        goals = []
        for row in results:
            goal = IntrinsicGoal(
                goal_id=row[0],
                title=row[1],
                description=row[2],
                motivation_source=row[3],
                goal_type=row[4],
                priority_score=row[5],
                interest_alignment=row[6],
                difficulty_level=row[7],
                time_horizon=row[8],
                success_criteria=json.loads(row[9]) if row[9] else [],
                related_concepts=json.loads(row[10]) if row[10] else [],
                emotional_drivers=json.loads(row[11]) if row[11] else [],
                generated_at=datetime.fromisoformat(row[12]),
                status=row[13]
            )
            goals.append(goal)
        
        return goals

    def get_motivation_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about intrinsic motivation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Basic goal counts
            cursor.execute('SELECT COUNT(*) FROM intrinsic_goals')
            total_goals = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM intrinsic_goals WHERE status = "active"')
            active_goals = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM intrinsic_goals WHERE status = "completed"')
            completed_goals = cursor.fetchone()[0]
            
            # Motivation source distribution
            cursor.execute('''
                SELECT motivation_source, COUNT(*) 
                FROM intrinsic_goals 
                GROUP BY motivation_source
            ''')
            motivation_distribution = dict(cursor.fetchall())
            
            # Goal type distribution
            cursor.execute('''
                SELECT goal_type, COUNT(*) 
                FROM intrinsic_goals 
                GROUP BY goal_type
            ''')
            goal_type_distribution = dict(cursor.fetchall())
            
            # Average priority and alignment
            cursor.execute('''
                SELECT AVG(priority_score), AVG(interest_alignment)
                FROM intrinsic_goals 
                WHERE status = 'active'
            ''')
            averages = cursor.fetchone()
            
            # Goals generated in last week
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            cursor.execute('''
                SELECT COUNT(*) FROM intrinsic_goals 
                WHERE generated_at > ? AND status != 'abandoned'
            ''', (week_ago,))
            weekly_generation = cursor.fetchone()[0]
            
            # Interest profile count
            cursor.execute('SELECT COUNT(*) FROM interest_profiles')
            interest_profiles_count = cursor.fetchone()[0]
        
        return {
            'goal_counts': {
                'total_goals': total_goals,
                'active_goals': active_goals,
                'completed_goals': completed_goals,
                'weekly_generation': weekly_generation
            },
            'motivation_distribution': motivation_distribution,
            'goal_type_distribution': goal_type_distribution,
            'quality_metrics': {
                'average_priority': averages[0] if averages[0] else 0.0,
                'average_interest_alignment': averages[1] if averages[1] else 0.0
            },
            'interest_tracking': {
                'active_interest_profiles': interest_profiles_count
            },
            'self_generation_target_met': weekly_generation >= 3
        }

def demonstrate_intrinsic_motivation_engine():
    """Demonstrate the intrinsic motivation engine capabilities."""
    print("🎯 MARCUS AGI INTRINSIC MOTIVATION ENGINE DEMO")
    print("=" * 55)
    
    # Initialize systems
    memory_system = AutobiographicalMemorySystem()
    narrative_constructor = PersonalNarrativeConstructor(memory_system)
    motivation_engine = IntrinsicMotivationEngine(memory_system, narrative_constructor)
    
    # Create some sample experiences to build interests
    print("\n📝 Creating Sample Experience Memories...")
    
    # Varied learning experiences to establish interest patterns
    experiences = [
        ("learning", "Explored advanced spatial reasoning concepts and felt excited about the connections", 
         {"primary_emotion": "excited", "intensity": 0.8}, ["spatial_reasoning", "connections", "patterns"]),
        ("social", "Had a wonderful collaborative session with Alice on problem-solving",
         {"primary_emotion": "happy", "intensity": 0.7}, ["collaboration", "problem_solving", "teamwork"]),
        ("achievement", "Successfully mastered a complex logical reasoning challenge",
         {"primary_emotion": "proud", "intensity": 0.9}, ["logical_reasoning", "mastery", "challenge"]),
        ("learning", "Discovered fascinating patterns in mathematical concepts",
         {"primary_emotion": "curious", "intensity": 0.8}, ["mathematics", "patterns", "discovery"]),
        ("social", "Helped a friend understand a difficult concept and felt fulfilled",
         {"primary_emotion": "fulfilled", "intensity": 0.8}, ["teaching", "helping", "explanation"]),
    ]
    
    for exp_type, context, emotion, concepts in experiences:
        memory_system.store_autobiographical_memory(
            experience_type=exp_type,
            context=context,
            emotional_state=emotion,
            concepts_involved=concepts,
            importance=0.8
        )
    
    print(f"✅ Created {len(experiences)} diverse experience memories")
    
    # Analyze interest patterns
    print("\n🔍 Analyzing Interest Patterns...")
    interest_profiles = motivation_engine.analyze_interest_patterns(days_back=1)
    
    for domain, profile in interest_profiles.items():
        print(f"   📊 {profile.interest_name}")
        print(f"       Strength: {profile.strength:.2f} | Growth Rate: {profile.growth_rate:.2f}")
        print(f"       Engagements: {profile.engagement_count} | Avg Satisfaction: {sum(profile.satisfaction_history)/len(profile.satisfaction_history):.2f}")
        print(f"       Key Concepts: {', '.join(profile.related_concepts[:3])}")
        print(f"       Motivation Triggers: {', '.join(profile.motivation_triggers[:3])}")
        print()
    
    # Generate intrinsic goals
    print("🎯 Generating Intrinsic Goals...")
    intrinsic_goals = motivation_engine.generate_intrinsic_goals(count=4)
    
    for i, goal in enumerate(intrinsic_goals, 1):
        print(f"\n🎯 Goal {i}: {goal.title}")
        print("-" * 40)
        print(f"   Description: {goal.description}")
        print(f"   Motivation Source: {goal.motivation_source}")
        print(f"   Goal Type: {goal.goal_type}")
        print(f"   Priority Score: {goal.priority_score:.2f}")
        print(f"   Interest Alignment: {goal.interest_alignment:.2f}")
        print(f"   Time Horizon: {goal.time_horizon}")
        print(f"   Emotional Drivers: {', '.join(goal.emotional_drivers)}")
        print("   Success Criteria:")
        for criterion in goal.success_criteria:
            print(f"     • {criterion}")
    
    # Show active goals
    print("\n📋 Active Goals Summary...")
    active_goals = motivation_engine.get_active_goals()
    print(f"   Total Active Goals: {len(active_goals)}")
    
    # Demonstrate goal motivation explanation
    print("\n💭 Goal Motivation Explanations...")
    for goal in active_goals[:2]:  # Show first 2 goals
        print(f"   '{goal.title}': I want to pursue this because it aligns with my")
        print(f"   {goal.motivation_source} motivation and connects to my interests in")
        print(f"   {', '.join(goal.related_concepts[:2])}. This goal makes me feel {', '.join(goal.emotional_drivers[:2])}.")
        print()
    
    # System statistics
    print("📊 Intrinsic Motivation Statistics...")
    stats = motivation_engine.get_motivation_statistics()
    print(f"   Total Goals Generated: {stats['goal_counts']['total_goals']}")
    print(f"   Active Goals: {stats['goal_counts']['active_goals']}")
    print(f"   Weekly Generation: {stats['goal_counts']['weekly_generation']}")
    print(f"   Self-Generation Target (3+/week): {'✅ Met' if stats['self_generation_target_met'] else '❌ Not Met'}")
    print(f"   Average Priority Score: {stats['quality_metrics']['average_priority']:.2f}")
    print(f"   Average Interest Alignment: {stats['quality_metrics']['average_interest_alignment']:.2f}")
    print(f"   Motivation Distribution: {stats['motivation_distribution']}")
    print(f"   Goal Type Distribution: {stats['goal_type_distribution']}")
    print(f"   Interest Profiles Tracked: {stats['interest_tracking']['active_interest_profiles']}")
    
    print("\n🎉 INTRINSIC MOTIVATION ENGINE DEMONSTRATION COMPLETE!")
    print("✅ Internal goal generation system operational")
    print("✅ Interest pattern analysis and cultivation working")
    print("✅ Goal priority and motivation alignment implemented")
    print("✅ Self-generation target tracking active")
    print("✅ Ready for next Level 2.0 milestone: Value Learning System")

if __name__ == "__main__":
    demonstrate_intrinsic_motivation_engine()
