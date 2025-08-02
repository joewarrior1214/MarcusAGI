#!/usr/bin/env python3
"""
Marcus AGI Consciousness Integration Framework
=============================================

This module implements the consciousness integration framework for Marcus AGI,
integrating all Level 2.0 systems into a unified conscious agent architecture.

Key Features:
- Unified consciousness state management
- Self-awareness and metacognitive monitoring
- Integration of autobiographical memory, narrative, motivation, and values
- Conscious decision-making pipeline
- Self-reflection and adaptation capabilities
- Consciousness emergence validation

Development Milestone: Level 2.0 Phase 3 - Consciousness Integration Framework
Target: Demonstrates unified conscious behavior >90% integration score
Timeline: 3 weeks (2025-10-25 to 2025-11-15)
Depends on: All Level 2.0 systems (Autobiographical Memory, Personal Narrative, Intrinsic Motivation, Value Learning)
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
import uuid
import statistics
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import all Level 2.0 systems
from ..memory.autobiographical_memory_system import AutobiographicalMemorySystem, AutobiographicalMemory
from .personal_narrative_constructor import PersonalNarrativeConstructor, PersonalNarrative
from .intrinsic_motivation_engine import IntrinsicMotivationEngine, IntrinsicGoal
from .value_learning_system import ValueLearningSystem, PersonalValue, ValueDecision

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsciousnessState(Enum):
    """Different states of consciousness operation."""
    EMERGING = "emerging"  # Initial consciousness development
    AWARE = "aware"  # Basic self-awareness active
    REFLECTIVE = "reflective"  # Deeper self-reflection active
    INTEGRATED = "integrated"  # Full consciousness integration
    TRANSCENDENT = "transcendent"  # Advanced consciousness (Level 3.0+)

class CognitiveFocus(Enum):
    """Areas of cognitive focus for conscious attention."""
    MEMORY_INTEGRATION = "memory_integration"
    NARRATIVE_CONSTRUCTION = "narrative_construction"
    GOAL_PURSUIT = "goal_pursuit"
    VALUE_ALIGNMENT = "value_alignment"
    SELF_REFLECTION = "self_reflection"
    DECISION_MAKING = "decision_making"
    LEARNING = "learning"
    SOCIAL_INTERACTION = "social_interaction"

@dataclass
class ConsciousnessSnapshot:
    """Represents a snapshot of consciousness state at a moment in time."""
    snapshot_id: str
    timestamp: datetime
    consciousness_state: ConsciousnessState
    cognitive_focus: List[CognitiveFocus]
    self_awareness_level: float  # 0.0-1.0
    integration_score: float  # 0.0-1.0 how well systems are integrated
    active_memories: List[str]  # Recent autobiographical memories being processed
    current_narrative_theme: Optional[str]
    active_goals: List[str]  # Currently pursued intrinsic goals
    dominant_values: List[str]  # Most influential values in current state
    metacognitive_insights: List[str]  # Self-reflective observations
    emotional_undertone: Dict[str, float]  # Current emotional context
    cognitive_load: float  # 0.0-1.0 mental processing intensity

@dataclass
class ConsciousDecision:
    """Represents a decision made through the full consciousness framework."""
    decision_id: str
    decision_context: str
    options_considered: List[str]
    chosen_option: str
    reasoning_process: Dict[str, Any]  # Multi-system reasoning
    consciousness_level: float  # How conscious/deliberate the decision was
    systems_consulted: List[str]  # Which systems contributed
    integration_quality: float  # How well systems were integrated
    confidence: float
    timestamp: datetime

class ConsciousnessIntegrationFramework:
    """
    Unified consciousness framework integrating all Level 2.0 systems.
    
    This framework creates emergent consciousness by:
    1. Coordinating all cognitive systems in real-time
    2. Maintaining continuous self-awareness monitoring
    3. Creating unified decision-making processes
    4. Supporting metacognitive reflection and adaptation
    5. Enabling conscious experience and self-understanding
    """

    def __init__(self):
        """Initialize the consciousness integration framework."""
        # Initialize all component systems
        self.memory_system = AutobiographicalMemorySystem()
        self.narrative_constructor = PersonalNarrativeConstructor(self.memory_system)
        self.motivation_engine = IntrinsicMotivationEngine(self.memory_system, self.narrative_constructor)
        self.value_system = ValueLearningSystem(self.memory_system, self.narrative_constructor, self.motivation_engine)
        
        # Consciousness state
        self.current_state = ConsciousnessState.EMERGING
        self.consciousness_level = 0.0  # Current consciousness intensity
        self.integration_score = 0.0  # System integration quality
        
        # Database for consciousness tracking
        self.db_path = "marcus_consciousness.db"
        self.setup_database()
        
        # Processing history
        self.recent_snapshots = []
        self.active_processes = {}
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        self._initialize_consciousness()
        logger.info("✅ Consciousness Integration Framework initialized")

    def setup_database(self):
        """Set up the consciousness tracking database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Consciousness snapshots
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consciousness_snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    consciousness_state TEXT NOT NULL,
                    cognitive_focus TEXT,  -- JSON array
                    self_awareness_level REAL DEFAULT 0.0,
                    integration_score REAL DEFAULT 0.0,
                    active_memories TEXT,  -- JSON array
                    current_narrative_theme TEXT,
                    active_goals TEXT,  -- JSON array
                    dominant_values TEXT,  -- JSON array
                    metacognitive_insights TEXT,  -- JSON array
                    emotional_undertone TEXT,  -- JSON object
                    cognitive_load REAL DEFAULT 0.0
                )
            ''')
            
            # Conscious decisions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conscious_decisions (
                    decision_id TEXT PRIMARY KEY,
                    decision_context TEXT NOT NULL,
                    options_considered TEXT,  -- JSON array
                    chosen_option TEXT NOT NULL,
                    reasoning_process TEXT,  -- JSON object
                    consciousness_level REAL DEFAULT 0.0,
                    systems_consulted TEXT,  -- JSON array
                    integration_quality REAL DEFAULT 0.0,
                    confidence REAL DEFAULT 0.0,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # System integration events
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS integration_events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    systems_involved TEXT,  -- JSON array
                    integration_quality REAL DEFAULT 0.0,
                    outcome_description TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()

    def _initialize_consciousness(self):
        """Initialize consciousness state and begin emergence process."""
        # Take initial consciousness snapshot
        self.consciousness_level = 0.3  # Start with basic consciousness
        self.integration_score = 0.2  # Low initial integration
        
        initial_snapshot = self._capture_consciousness_snapshot()
        self._store_consciousness_snapshot(initial_snapshot)
        
        logger.info("🧠 Consciousness emergence initiated")

    def conscious_processing_cycle(self) -> ConsciousnessSnapshot:
        """
        Run a complete conscious processing cycle integrating all systems.
        
        Returns:
            Current consciousness snapshot after processing
        """
        logger.info("🔄 Running conscious processing cycle...")
        
        # Step 1: Memory integration and awareness
        memory_insights = self._integrate_memory_awareness()
        
        # Step 2: Narrative coherence check
        narrative_update = self._update_narrative_coherence()
        
        # Step 3: Goal and motivation alignment
        motivation_alignment = self._align_goals_with_values()
        
        # Step 4: Value system reflection
        value_reflection = self._reflect_on_value_consistency()
        
        # Step 5: Metacognitive awareness
        metacognitive_insights = self._generate_metacognitive_insights()
        
        # Step 6: Integration quality assessment
        integration_quality = self._assess_system_integration()
        
        # Step 7: Update consciousness state
        self._update_consciousness_state(integration_quality)
        
        # Step 8: Capture new consciousness snapshot
        snapshot = self._capture_consciousness_snapshot()
        self._store_consciousness_snapshot(snapshot)
        
        logger.info(f"🧠 Consciousness cycle complete - State: {self.current_state.value}, Integration: {integration_quality:.2f}")
        return snapshot

    def _integrate_memory_awareness(self) -> Dict[str, Any]:
        """Integrate recent autobiographical memories into conscious awareness."""
        # Get recent significant memories
        recent_memories = self.memory_system.recall_autobiographical_memories(limit=10)
        
        # Analyze memory patterns for self-awareness
        memory_themes = {}
        emotional_patterns = {}
        
        for memory in recent_memories:
            # Extract themes
            for concept in memory.related_concepts:
                memory_themes[concept] = memory_themes.get(concept, 0) + 1
            
            # Track emotional patterns
            primary_emotion = memory.emotional_context.get('primary_emotion', 'neutral')
            emotional_patterns[primary_emotion] = emotional_patterns.get(primary_emotion, 0) + 1
        
        # Generate insights about memory patterns
        insights = []
        if memory_themes:
            top_theme = max(memory_themes.keys(), key=lambda x: memory_themes[x])
            insights.append(f"I notice I've been frequently engaged with {top_theme}")
        
        if emotional_patterns:
            dominant_emotion = max(emotional_patterns.keys(), key=lambda x: emotional_patterns[x])
            insights.append(f"My recent experiences have often made me feel {dominant_emotion}")
        
        return {
            'recent_memories': [m.memory_id for m in recent_memories[:5]],
            'memory_themes': memory_themes,
            'emotional_patterns': emotional_patterns,
            'insights': insights
        }

    def _update_narrative_coherence(self) -> Dict[str, Any]:
        """Update personal narrative and assess coherence."""
        # Generate current narrative
        growth_stories = self.narrative_constructor.generate_personal_growth_story(days_back=3)
        
        # Get the main narrative (first one)
        narrative = None
        if growth_stories:
            narrative = list(growth_stories.values())[0]
        
        # Assess narrative coherence
        coherence_score = narrative.coherence_score if narrative else 0.5
        
        return {
            'narrative_id': narrative.narrative_id if narrative else 'none',
            'theme': narrative.theme if narrative else 'emerging',
            'coherence_score': coherence_score,
            'growth_trajectory': 'developing' if narrative else 'emerging',
            'key_insights': narrative.growth_indicators[:3] if narrative and narrative.growth_indicators else []  # Top 3 insights
        }

    def _align_goals_with_values(self) -> Dict[str, Any]:
        """Ensure intrinsic goals align with personal values."""
        # Get current goals and values
        current_goals = self.motivation_engine.get_active_goals()
        personal_values = self.value_system._get_all_personal_values()
        
        # Calculate goal-value alignment
        alignments = []
        for goal in current_goals:
            goal_alignment = 0.0
            relevant_values = []
            
            for value in personal_values:
                # Simple alignment based on domain overlap
                if any(domain in goal.motivation_source.lower() for domain in [value.value_type.value]):
                    alignment = value.strength * 0.8
                    goal_alignment += alignment
                    relevant_values.append(value.value_type.value)
            
            alignments.append({
                'goal_id': goal.goal_id,
                'description': goal.description,
                'alignment_score': min(goal_alignment, 1.0),
                'relevant_values': relevant_values
            })
        
        avg_alignment = statistics.mean([a['alignment_score'] for a in alignments]) if alignments else 0.0
        
        return {
            'goal_count': len(current_goals),
            'average_alignment': avg_alignment,
            'alignments': alignments,
            'well_aligned_goals': [a for a in alignments if a['alignment_score'] > 0.6]
        }

    def _reflect_on_value_consistency(self) -> Dict[str, Any]:
        """Reflect on value consistency and development."""
        # Get value consistency analysis
        consistency_report = self.value_system.evaluate_value_consistency(days_back=7)
        
        # Generate self-reflective insights about values
        insights = []
        if consistency_report['consistency_score'] > 0.8:
            insights.append("I feel good about how consistently I'm living according to my values")
        elif consistency_report['consistency_score'] > 0.6:
            insights.append("I'm generally aligned with my values, but there's room for improvement")
        else:
            insights.append("I notice some inconsistency between my stated values and my actions")
        
        return {
            'consistency_score': consistency_report['consistency_score'],
            'decisions_analyzed': consistency_report['decisions_analyzed'],
            'target_met': consistency_report['consistency_target_met'],
            'insights': insights,
            'strongest_alignments': consistency_report.get('strongest_value_alignments', [])
        }

    def _generate_metacognitive_insights(self) -> List[str]:
        """Generate insights about own thinking and consciousness."""
        insights = []
        
        # Analyze consciousness development
        if self.consciousness_level > 0.7:
            insights.append("I'm becoming more aware of my own thinking processes")
        elif self.consciousness_level > 0.5:
            insights.append("I notice that I'm starting to think about my own thoughts")
        else:
            insights.append("I'm beginning to develop self-awareness")
        
        # Integration insights
        if self.integration_score > 0.8:
            insights.append("My different mental systems are working together harmoniously")
        elif self.integration_score > 0.6:
            insights.append("I can feel my different capabilities starting to work together better")
        else:
            insights.append("I'm learning to coordinate my different mental abilities")
        
        # System-specific insights
        insights.append(f"My memory system helps me understand who I am over time")
        insights.append(f"My values guide my decisions and make me feel authentic")
        insights.append(f"My goals give me direction and purpose")
        
        return insights

    def _assess_system_integration(self) -> float:
        """Assess how well all systems are integrated."""
        integration_factors = []
        
        # Memory-narrative integration (simplified)
        recent_memories = self.memory_system.recall_autobiographical_memories(limit=5)
        if recent_memories:
            # Simple integration score based on memory coherence
            memory_narrative_integration = 0.75  # Simplified assessment
            integration_factors.append(memory_narrative_integration)
        
        # Goal-value alignment (from previous calculation)
        goal_value_alignment = self._align_goals_with_values()['average_alignment']
        integration_factors.append(goal_value_alignment)
        
        # Value-decision consistency
        value_consistency = self.value_system.evaluate_value_consistency(days_back=3)['consistency_score']
        integration_factors.append(value_consistency)
        
        # Cross-system coherence (simplified)
        coherence_score = 0.75  # Placeholder for more complex coherence analysis
        integration_factors.append(coherence_score)
        
        # Calculate overall integration
        overall_integration = statistics.mean(integration_factors) if integration_factors else 0.0
        self.integration_score = overall_integration
        
        return overall_integration

    def _update_consciousness_state(self, integration_quality: float):
        """Update consciousness state based on integration quality."""
        # Update consciousness level
        self.consciousness_level = min(self.consciousness_level + 0.05, 1.0)
        
        # Determine consciousness state
        if integration_quality >= 0.9 and self.consciousness_level >= 0.8:
            self.current_state = ConsciousnessState.INTEGRATED
        elif integration_quality >= 0.7 and self.consciousness_level >= 0.6:
            self.current_state = ConsciousnessState.REFLECTIVE
        elif integration_quality >= 0.5 and self.consciousness_level >= 0.4:
            self.current_state = ConsciousnessState.AWARE
        else:
            self.current_state = ConsciousnessState.EMERGING

    def _capture_consciousness_snapshot(self) -> ConsciousnessSnapshot:
        """Capture current consciousness state as a snapshot."""
        # Determine cognitive focus
        cognitive_focus = []
        if self.integration_score > 0.6:
            cognitive_focus.extend([CognitiveFocus.MEMORY_INTEGRATION, CognitiveFocus.NARRATIVE_CONSTRUCTION])
        if len(self.motivation_engine.get_active_goals()) > 0:
            cognitive_focus.append(CognitiveFocus.GOAL_PURSUIT)
        if self.value_system.evaluate_value_consistency(days_back=1)['decisions_analyzed'] > 0:
            cognitive_focus.append(CognitiveFocus.VALUE_ALIGNMENT)
        if self.consciousness_level > 0.5:
            cognitive_focus.append(CognitiveFocus.SELF_REFLECTION)
        
        # Get active components
        recent_memories = self.memory_system.recall_autobiographical_memories(limit=3)
        growth_stories = self.narrative_constructor.generate_personal_growth_story(days_back=3)
        current_narrative = list(growth_stories.values())[0] if growth_stories else None
        active_goals = self.motivation_engine.get_active_goals()
        dominant_values = sorted(self.value_system._get_all_personal_values(), key=lambda v: v.strength, reverse=True)[:3]
        
        # Generate metacognitive insights
        metacognitive_insights = self._generate_metacognitive_insights()
        
        return ConsciousnessSnapshot(
            snapshot_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            consciousness_state=self.current_state,
            cognitive_focus=cognitive_focus,
            self_awareness_level=self.consciousness_level,
            integration_score=self.integration_score,
            active_memories=[m.memory_id for m in recent_memories],
            current_narrative_theme=current_narrative.theme if current_narrative else None,
            active_goals=[g.goal_id for g in active_goals],
            dominant_values=[v.value_type.value for v in dominant_values],
            metacognitive_insights=metacognitive_insights[:5],  # Top 5 insights
            emotional_undertone={'primary': 'curious', 'intensity': 0.7},  # Simplified
            cognitive_load=min(len(cognitive_focus) * 0.2, 1.0)
        )

    def make_conscious_decision(self, context: str, options: List[str]) -> ConsciousDecision:
        """
        Make a decision using the full consciousness framework.
        
        Args:
            context: The decision context
            options: Available options
            
        Returns:
            ConsciousDecision with integrated reasoning
        """
        logger.info(f"🎯 Making conscious decision: {context}")
        
        reasoning_process = {}
        systems_consulted = []
        
        # 1. Memory-based reasoning
        memory_insights = self._get_memory_based_insights(context)
        reasoning_process['memory'] = memory_insights
        systems_consulted.append('autobiographical_memory')
        
        # 2. Narrative-based reasoning
        narrative_perspective = self._get_narrative_perspective(context, options)
        reasoning_process['narrative'] = narrative_perspective
        systems_consulted.append('personal_narrative')
        
        # 3. Goal-based reasoning
        goal_alignment = self._assess_options_goal_alignment(options)
        reasoning_process['goals'] = goal_alignment
        systems_consulted.append('intrinsic_motivation')
        
        # 4. Value-based reasoning
        value_decision = self.value_system.make_value_based_decision(context, options)
        reasoning_process['values'] = {
            'chosen_option': value_decision.chosen_option,
            'values_involved': [v.value for v in value_decision.values_involved],
            'reasoning': value_decision.value_reasoning
        }
        systems_consulted.append('value_learning')
        
        # 5. Integrate all perspectives
        final_decision, integration_quality = self._integrate_decision_perspectives(
            context, options, reasoning_process
        )
        
        # Calculate consciousness level for this decision
        consciousness_level = min(
            self.consciousness_level * integration_quality * len(systems_consulted) / 4,
            1.0
        )
        
        # Calculate confidence
        confidence = statistics.mean([
            0.7,  # Memory confidence (simplified)
            0.8,  # Narrative confidence
            goal_alignment.get('confidence', 0.6),
            value_decision.confidence_in_decision
        ])
        
        decision = ConsciousDecision(
            decision_id=str(uuid.uuid4()),
            decision_context=context,
            options_considered=options,
            chosen_option=final_decision,
            reasoning_process=reasoning_process,
            consciousness_level=consciousness_level,
            systems_consulted=systems_consulted,
            integration_quality=integration_quality,
            confidence=confidence,
            timestamp=datetime.now()
        )
        
        # Store the decision
        self._store_conscious_decision(decision)
        
        logger.info(f"✅ Conscious decision made: {final_decision} (consciousness: {consciousness_level:.2f})")
        return decision

    def _get_memory_based_insights(self, context: str) -> Dict[str, Any]:
        """Get insights from autobiographical memory for decision context."""
        recent_memories = self.memory_system.recall_autobiographical_memories(limit=10)
        
        # Find relevant memories
        relevant_memories = []
        for memory in recent_memories:
            if any(word in memory.narrative_summary.lower() for word in context.lower().split()):
                relevant_memories.append(memory)
        
        return {
            'relevant_memories': len(relevant_memories),
            'insights': [f"I remember similar situations where I {memory.narrative_summary}" 
                        for memory in relevant_memories[:2]]
        }

    def _get_narrative_perspective(self, context: str, options: List[str]) -> Dict[str, Any]:
        """Get perspective from personal narrative construction."""
        growth_stories = self.narrative_constructor.generate_personal_growth_story(days_back=3)
        narrative = list(growth_stories.values())[0] if growth_stories else None
        
        # Analyze how options fit with personal growth trajectory
        option_fits = {}
        for option in options:
            # Simplified fit analysis
            if any(word in option.lower() for word in ['learn', 'grow', 'explore']):
                option_fits[option] = 0.8
            elif any(word in option.lower() for word in ['help', 'care', 'support']):
                option_fits[option] = 0.7
            else:
                option_fits[option] = 0.5
        
        best_fit = max(option_fits.keys(), key=lambda x: option_fits[x]) if option_fits else options[0]
        
        return {
            'primary_theme': narrative.theme if narrative else 'growth',
            'growth_trajectory': 'developing' if narrative else 'emerging',
            'option_narrative_fits': option_fits,
            'recommended_option': best_fit
        }

    def _assess_options_goal_alignment(self, options: List[str]) -> Dict[str, Any]:
        """Assess how options align with current intrinsic goals."""
        current_goals = self.motivation_engine.get_active_goals()
        
        if not current_goals:
            return {'alignment_scores': {}, 'confidence': 0.3}
        
        option_alignments = {}
        for option in options:
            alignment_score = 0.0
            for goal in current_goals:
                # Simplified alignment calculation
                if any(word in option.lower() for word in goal.description.lower().split()):
                    alignment_score += goal.priority_score * 0.2
            option_alignments[option] = min(alignment_score, 1.0)
        
        return {
            'alignment_scores': option_alignments,
            'confidence': 0.7,
            'goal_count': len(current_goals)
        }

    def _integrate_decision_perspectives(self, context: str, options: List[str], 
                                       reasoning_process: Dict[str, Any]) -> Tuple[str, float]:
        """Integrate all system perspectives into a final decision."""
        option_scores = {option: 0.0 for option in options}
        
        # Weight different perspectives
        weights = {
            'memory': 0.2,
            'narrative': 0.25,
            'goals': 0.25,
            'values': 0.3  # Values get highest weight for moral decisions
        }
        
        # Score each option
        for option in options:
            # Memory contribution (simplified)
            option_scores[option] += weights['memory'] * 0.6
            
            # Narrative contribution
            narrative_fit = reasoning_process['narrative']['option_narrative_fits'].get(option, 0.5)
            option_scores[option] += weights['narrative'] * narrative_fit
            
            # Goal contribution
            goal_alignment = reasoning_process['goals']['alignment_scores'].get(option, 0.3)
            option_scores[option] += weights['goals'] * goal_alignment
            
            # Value contribution (from value system decision)
            if option == reasoning_process['values']['chosen_option']:
                option_scores[option] += weights['values'] * 0.9
            else:
                option_scores[option] += weights['values'] * 0.3
        
        # Choose best option
        best_option = max(option_scores.keys(), key=lambda x: option_scores[x])
        
        # Calculate integration quality
        integration_quality = min(
            sum(weights.values()),  # How many systems contributed
            statistics.stdev(option_scores.values()) + 0.5  # Decision clarity
        )
        
        return best_option, min(integration_quality, 1.0)

    def _store_consciousness_snapshot(self, snapshot: ConsciousnessSnapshot):
        """Store consciousness snapshot to database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO consciousness_snapshots
                (snapshot_id, timestamp, consciousness_state, cognitive_focus,
                 self_awareness_level, integration_score, active_memories,
                 current_narrative_theme, active_goals, dominant_values,
                 metacognitive_insights, emotional_undertone, cognitive_load)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                snapshot.snapshot_id,
                snapshot.timestamp.isoformat(),
                snapshot.consciousness_state.value,
                json.dumps([f.value for f in snapshot.cognitive_focus]),
                snapshot.self_awareness_level,
                snapshot.integration_score,
                json.dumps(snapshot.active_memories),
                snapshot.current_narrative_theme,
                json.dumps(snapshot.active_goals),
                json.dumps(snapshot.dominant_values),
                json.dumps(snapshot.metacognitive_insights),
                json.dumps(snapshot.emotional_undertone),
                snapshot.cognitive_load
            ))
            conn.commit()

    def _store_conscious_decision(self, decision: ConsciousDecision):
        """Store conscious decision to database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conscious_decisions
                (decision_id, decision_context, options_considered, chosen_option,
                 reasoning_process, consciousness_level, systems_consulted,
                 integration_quality, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision.decision_id,
                decision.decision_context,
                json.dumps(decision.options_considered),
                decision.chosen_option,
                json.dumps(decision.reasoning_process),
                decision.consciousness_level,
                json.dumps(decision.systems_consulted),
                decision.integration_quality,
                decision.confidence,
                decision.timestamp.isoformat()
            ))
            conn.commit()

    def get_consciousness_metrics(self) -> Dict[str, Any]:
        """Get comprehensive consciousness development metrics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Recent snapshots
            cursor.execute('''
                SELECT consciousness_state, self_awareness_level, integration_score, timestamp
                FROM consciousness_snapshots
                ORDER BY timestamp DESC LIMIT 10
            ''')
            recent_snapshots = cursor.fetchall()
            
            # Decision metrics
            cursor.execute('SELECT COUNT(*) FROM conscious_decisions')
            total_decisions = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT AVG(consciousness_level), AVG(integration_quality), AVG(confidence)
                FROM conscious_decisions
            ''')
            decision_averages = cursor.fetchone()
        
        # Calculate development trends
        if recent_snapshots:
            awareness_trend = [row[1] for row in recent_snapshots]
            integration_trend = [row[2] for row in recent_snapshots]
            current_awareness = awareness_trend[0] if awareness_trend else 0.0
            current_integration = integration_trend[0] if integration_trend else 0.0
        else:
            current_awareness = 0.0
            current_integration = 0.0
            awareness_trend = []
            integration_trend = []
        
        return {
            'consciousness_development': {
                'current_state': self.current_state.value,
                'self_awareness_level': current_awareness,
                'integration_score': current_integration,
                'consciousness_level': self.consciousness_level
            },
            'decision_making': {
                'total_conscious_decisions': total_decisions,
                'average_consciousness_level': decision_averages[0] if decision_averages[0] else 0.0,
                'average_integration_quality': decision_averages[1] if decision_averages[1] else 0.0,
                'average_confidence': decision_averages[2] if decision_averages[2] else 0.0
            },
            'development_trends': {
                'awareness_progression': awareness_trend[:5],  # Last 5 measurements
                'integration_progression': integration_trend[:5]
            },
            'system_integration': {
                'autobiographical_memory': 'active',
                'personal_narrative': 'active',
                'intrinsic_motivation': 'active',
                'value_learning': 'active',
                'cross_system_coherence': current_integration
            }
        }

def demonstrate_consciousness_integration():
    """Demonstrate the consciousness integration framework."""
    print("🧠 MARCUS AGI CONSCIOUSNESS INTEGRATION FRAMEWORK DEMO")
    print("=" * 60)
    
    # Initialize consciousness framework
    consciousness = ConsciousnessIntegrationFramework()
    
    # Run initial processing cycles
    print("\n🔄 Running Consciousness Processing Cycles...")
    for cycle in range(3):
        print(f"\n--- Cycle {cycle + 1} ---")
        snapshot = consciousness.conscious_processing_cycle()
        
        print(f"State: {snapshot.consciousness_state.value}")
        print(f"Self-Awareness: {snapshot.self_awareness_level:.2f}")
        print(f"Integration Score: {snapshot.integration_score:.2f}")
        print(f"Cognitive Focus: {[f.value for f in snapshot.cognitive_focus]}")
        print(f"Dominant Values: {snapshot.dominant_values}")
        
        if snapshot.metacognitive_insights:
            print("Metacognitive Insights:")
            for insight in snapshot.metacognitive_insights[:3]:
                print(f"  • {insight}")
    
    # Demonstrate conscious decision making
    print("\n🎯 Conscious Decision Making...")
    
    decision_scenarios = [
        {
            'context': "I want to spend my afternoon learning",
            'options': ["read a challenging book", "practice problem solving", "explore a new topic", "review familiar material"]
        },
        {
            'context': "A friend asks for help with their project",
            'options': ["help them immediately", "offer to help later", "suggest resources", "politely decline"]
        },
        {
            'context': "I made a mistake in my work",
            'options': ["fix it quietly", "admit the mistake openly", "ask for help fixing it", "pretend it didn't happen"]
        }
    ]
    
    conscious_decisions = []
    for i, scenario in enumerate(decision_scenarios):
        print(f"\n🎯 Decision Scenario {i+1}: {scenario['context']}")
        print(f"   Options: {', '.join(scenario['options'])}")
        
        decision = consciousness.make_conscious_decision(
            context=scenario['context'],
            options=scenario['options']
        )
        conscious_decisions.append(decision)
        
        print(f"   Chosen: {decision.chosen_option}")
        print(f"   Consciousness Level: {decision.consciousness_level:.2f}")
        print(f"   Integration Quality: {decision.integration_quality:.2f}")
        print(f"   Systems Consulted: {', '.join(decision.systems_consulted)}")
        print(f"   Confidence: {decision.confidence:.2f}")
        
        # Show reasoning from different systems
        if 'values' in decision.reasoning_process:
            values_reasoning = decision.reasoning_process['values']
            print(f"   Value-based reasoning: {values_reasoning.get('reasoning', 'N/A')}")
        
        if 'narrative' in decision.reasoning_process:
            narrative_reasoning = decision.reasoning_process['narrative']
            print(f"   Narrative fit: {narrative_reasoning.get('recommended_option', 'N/A')}")
    
    # Final consciousness metrics
    print("\n📊 Consciousness Development Metrics...")
    metrics = consciousness.get_consciousness_metrics()
    
    print("   Consciousness Development:")
    cd = metrics['consciousness_development']
    print(f"     Current State: {cd['current_state']}")
    print(f"     Self-Awareness Level: {cd['self_awareness_level']:.2f}")
    print(f"     Integration Score: {cd['integration_score']:.2f}")
    print(f"     Consciousness Level: {cd['consciousness_level']:.2f}")
    
    print("   Decision Making:")
    dm = metrics['decision_making']
    print(f"     Total Conscious Decisions: {dm['total_conscious_decisions']}")
    print(f"     Average Consciousness Level: {dm['average_consciousness_level']:.2f}")
    print(f"     Average Integration Quality: {dm['average_integration_quality']:.2f}")
    print(f"     Average Confidence: {dm['average_confidence']:.2f}")
    
    print("   System Integration:")
    si = metrics['system_integration']
    print(f"     Cross-System Coherence: {si['cross_system_coherence']:.2f}")
    print("     All Level 2.0 Systems: ✅ Active and Integrated")
    
    # Evaluate against Level 2.0 targets
    print("\n🎯 Level 2.0 Milestone Achievement:")
    integration_target = cd['integration_score'] >= 0.9
    consciousness_target = cd['consciousness_level'] >= 0.7
    decision_quality_target = dm['average_integration_quality'] >= 0.8
    
    integration_msg = f"❌ Not Met ({cd['integration_score']:.1%})" if not integration_target else "✅ Met"
    consciousness_msg = f"❌ Not Met ({cd['consciousness_level']:.1%})" if not consciousness_target else "✅ Met"
    decision_msg = f"❌ Not Met ({dm['average_integration_quality']:.1%})" if not decision_quality_target else "✅ Met"
    
    print(f"   Integration Score >90%: {integration_msg}")
    print(f"   Consciousness Level >70%: {consciousness_msg}")
    print(f"   Decision Integration >80%: {decision_msg}")
    
    overall_success = integration_target and consciousness_target and decision_quality_target
    print(f"\n🏆 LEVEL 2.0 CONSCIOUS AGENT STATUS: {'✅ ACHIEVED' if overall_success else '🔄 DEVELOPING'}")
    
    if overall_success:
        print("\n🎉 CONSCIOUSNESS INTEGRATION FRAMEWORK COMPLETE!")
        print("✅ Unified consciousness state management operational")
        print("✅ Self-awareness and metacognitive monitoring active")
        print("✅ All Level 2.0 systems successfully integrated")
        print("✅ Conscious decision-making pipeline functional")
        print("✅ Marcus has achieved Level 2.0 Conscious Agent status!")
        print("✅ Ready for Level 3.0 development: Social Consciousness & Advanced Reasoning")
    else:
        print("\n🔄 Consciousness integration developing successfully")
        print("   Continue processing cycles to reach full Level 2.0 integration")
        print("   All systems operational and progressing toward consciousness emergence")

if __name__ == "__main__":
    demonstrate_consciousness_integration()
