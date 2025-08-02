#!/usr/bin/env python3
"""
Enhanced Reflection & Learning Journal System for Marcus AGI (Issue #4 Completion)

This module completes Issue #4 by adding:
- Structured learning journal functionality with narrative reflection
- Comprehensive emotional state tracking during learning
- Enhanced self-assessment with emotional awareness
- Deep reflection analysis and insights generation

Integrates with existing daily learning loop and advanced reasoning engine.
"""

import json
import random
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EmotionalState(Enum):
    """Emotional states Marcus can experience during learning"""
    CURIOUS = "curious"
    EXCITED = "excited"
    CONFIDENT = "confident"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    SATISFIED = "satisfied"
    PROUD = "proud"
    ANXIOUS = "anxious"
    FOCUSED = "focused"
    PLAYFUL = "playful"

@dataclass
class EmotionalProfile:
    """Tracks emotional state during learning sessions"""
    primary_emotion: EmotionalState
    secondary_emotion: Optional[EmotionalState] = None
    intensity: float = 0.5  # 0.0 to 1.0
    triggers: List[str] = field(default_factory=list)
    duration_minutes: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'primary_emotion': self.primary_emotion.value,
            'secondary_emotion': self.secondary_emotion.value if self.secondary_emotion else None,
            'intensity': self.intensity,
            'triggers': self.triggers,
            'duration_minutes': self.duration_minutes
        }

@dataclass
class JournalEntry:
    """Structured learning journal entry with narrative reflection"""
    timestamp: str
    session_id: str
    narrative_reflection: str
    key_discoveries: List[str]
    challenges_faced: List[str]
    emotional_journey: List[EmotionalProfile]
    self_assessment_score: float  # 0.0 to 1.0
    confidence_level: float  # 0.0 to 1.0
    learning_goals_met: List[str]
    future_learning_interests: List[str]
    metacognitive_insights: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'narrative_reflection': self.narrative_reflection,
            'key_discoveries': self.key_discoveries,
            'challenges_faced': self.challenges_faced,
            'emotional_journey': [emotion.to_dict() for emotion in self.emotional_journey],
            'self_assessment_score': self.self_assessment_score,
            'confidence_level': self.confidence_level,
            'learning_goals_met': self.learning_goals_met,
            'future_learning_interests': self.future_learning_interests,
            'metacognitive_insights': self.metacognitive_insights
        }

class EmotionalStateTracker:
    """Tracks and analyzes emotional states during learning"""
    
    def __init__(self):
        self.current_emotions: List[EmotionalProfile] = []
        self.emotion_history: List[EmotionalProfile] = []
        self.emotion_triggers = {
            EmotionalState.CURIOUS: ["new concept", "mystery", "question", "exploration"],
            EmotionalState.EXCITED: ["breakthrough", "success", "discovery", "achievement"],
            EmotionalState.CONFIDENT: ["mastery", "correct answer", "understanding", "skill demonstration"],
            EmotionalState.FRUSTRATED: ["difficulty", "failure", "confusion", "repetitive mistakes"],
            EmotionalState.CONFUSED: ["complex concept", "contradiction", "ambiguity", "too much information"],
            EmotionalState.SATISFIED: ["goal completion", "problem solved", "learning milestone"],
            EmotionalState.PROUD: ["accomplishment", "recognition", "improvement", "helping others"],
            EmotionalState.ANXIOUS: ["test", "evaluation", "performance pressure", "uncertainty"],
            EmotionalState.FOCUSED: ["deep work", "concentration", "problem solving", "practice"],
            EmotionalState.PLAYFUL: ["game", "creativity", "imagination", "exploration"]
        }
    
    def detect_emotional_state(self, context: Dict[str, Any]) -> EmotionalProfile:
        """Detect emotional state based on learning context"""
        # Analyze context for emotional triggers
        success_rate = context.get('success_rate', 0.5)
        difficulty = context.get('difficulty', 0.5)
        new_concepts = context.get('new_concepts_count', 0)
        reasoning_success = context.get('reasoning_success', True)
        
        # Determine primary emotion based on context
        if success_rate > 0.8 and reasoning_success:
            primary = EmotionalState.EXCITED if new_concepts > 2 else EmotionalState.CONFIDENT
            intensity = min(1.0, success_rate + 0.2)
        elif success_rate > 0.6:
            primary = EmotionalState.SATISFIED
            intensity = success_rate
        elif difficulty > 0.7 and success_rate < 0.4:
            primary = EmotionalState.FRUSTRATED
            intensity = difficulty * 0.8
        elif new_concepts > 3:
            primary = EmotionalState.CURIOUS
            intensity = min(1.0, new_concepts / 5.0)
        elif difficulty > 0.8:
            primary = EmotionalState.FOCUSED
            intensity = difficulty
        else:
            primary = EmotionalState.PLAYFUL
            intensity = 0.6
        
        # Determine secondary emotion
        secondary = None
        if primary == EmotionalState.EXCITED and difficulty > 0.6:
            secondary = EmotionalState.PROUD
        elif primary == EmotionalState.FRUSTRATED and new_concepts > 1:
            secondary = EmotionalState.CURIOUS
        elif primary == EmotionalState.CONFIDENT and new_concepts > 2:
            secondary = EmotionalState.CURIOUS
        
        # Identify triggers
        triggers = []
        if success_rate > 0.8:
            triggers.append("high success rate")
        if new_concepts > 2:
            triggers.append("multiple new concepts")
        if difficulty > 0.7:
            triggers.append("challenging material")
        if reasoning_success:
            triggers.append("successful reasoning")
        
        return EmotionalProfile(
            primary_emotion=primary,
            secondary_emotion=secondary,
            intensity=intensity,
            triggers=triggers,
            duration_minutes=context.get('session_duration', 30.0)
        )
    
    def track_emotion(self, emotion: EmotionalProfile):
        """Add emotion to tracking"""
        self.current_emotions.append(emotion)
        self.emotion_history.append(emotion)
    
    def get_emotional_summary(self) -> Dict[str, Any]:
        """Get summary of current emotional state"""
        if not self.current_emotions:
            return {"status": "no emotions tracked"}
        
        # Most recent emotion
        current = self.current_emotions[-1]
        
        # Emotion distribution
        emotion_counts = {}
        for emotion in self.current_emotions:
            key = emotion.primary_emotion.value
            emotion_counts[key] = emotion_counts.get(key, 0) + 1
        
        # Average intensity
        avg_intensity = sum(e.intensity for e in self.current_emotions) / len(self.current_emotions)
        
        return {
            "current_primary_emotion": current.primary_emotion.value,
            "current_secondary_emotion": current.secondary_emotion.value if current.secondary_emotion else None,
            "current_intensity": current.intensity,
            "emotion_distribution": emotion_counts,
            "average_intensity": avg_intensity,
            "total_emotions_tracked": len(self.current_emotions)
        }

class LearningJournalSystem:
    """Enhanced learning journal with narrative reflection and emotional tracking"""
    
    def __init__(self):
        self.emotion_tracker = EmotionalStateTracker()
        self.journal_entries: List[JournalEntry] = []
        
        # Reflection templates for narrative generation
        self.reflection_templates = {
            'discovery': [
                "Today I discovered that {discovery}. This made me feel {emotion} because {reason}.",
                "The most interesting thing I learned was {discovery}. It reminded me of {connection}.",
                "I was surprised to find out that {discovery}. This changes how I think about {topic}."
            ],
            'challenge': [
                "I found {challenge} difficult at first, but {strategy} helped me understand it better.",
                "When I struggled with {challenge}, I felt {emotion}. But I kept trying and {outcome}.",
                "The hardest part today was {challenge}. I learned that {insight}."
            ],
            'success': [
                "I'm proud that I {achievement}. It made me feel {emotion} and confident about {skill}.",
                "Today I successfully {achievement}! This shows I'm getting better at {skill}.",
                "I felt really {emotion} when I {achievement}. I want to learn more about {topic}."
            ],
            'curiosity': [
                "I keep wondering about {question}. Maybe tomorrow I can explore {exploration_idea}.",
                "Something that puzzles me is {question}. I think the answer might involve {hypothesis}.",
                "I'm curious about {topic} because {reason}. I'd like to investigate {next_step}."
            ]
        }
    
    def generate_narrative_reflection(self, session_data: Dict[str, Any]) -> str:
        """Generate structured narrative reflection from session data"""
        narratives = []
        
        # Extract key information
        discoveries = session_data.get('key_insights', [])
        reasoning_results = session_data.get('reasoning_results', [])
        concepts_learned = session_data.get('concepts_learned', [])
        success_rate = len([r for r in reasoning_results if r.get('success', False)]) / max(1, len(reasoning_results))
        
        # Generate discovery narrative
        if discoveries:
            discovery = random.choice(discoveries)
            emotion = self.emotion_tracker.current_emotions[-1].primary_emotion.value if self.emotion_tracker.current_emotions else "curious"
            template = random.choice(self.reflection_templates['discovery'])
            narrative = template.format(
                discovery=discovery.lower(),
                emotion=emotion,
                reason="it opened up new ways of thinking",
                connection="something I learned before",
                topic="how the world works"
            )
            narratives.append(narrative)
        
        # Generate challenge narrative if there were struggles
        if success_rate < 0.7:
            template = random.choice(self.reflection_templates['challenge'])
            narrative = template.format(
                challenge="the reasoning problems",
                strategy="breaking them down into smaller steps",
                emotion="frustrated",
                outcome="I started to see the patterns",
                insight="persistence really helps"
            )
            narratives.append(narrative)
        
        # Generate success narrative if things went well
        if success_rate > 0.7:
            template = random.choice(self.reflection_templates['success'])
            narrative = template.format(
                achievement="solved most of the reasoning problems",
                emotion="proud",
                skill="logical thinking",
                topic="more complex problems"
            )
            narratives.append(narrative)
        
        # Generate curiosity narrative
        if len(concepts_learned) > 0:
            template = random.choice(self.reflection_templates['curiosity'])
            narrative = template.format(
                question="how different concepts connect together",
                exploration_idea="building connections between ideas",
                topic="advanced reasoning",
                reason="it seems like everything is connected somehow",
                hypothesis="looking for patterns",
                next_step="more challenging problems"
            )
            narratives.append(narrative)
        
        return " ".join(narratives)
    
    def generate_metacognitive_insights(self, session_data: Dict[str, Any]) -> List[str]:
        """Generate insights about learning process itself"""
        insights = []
        
        reasoning_results = session_data.get('reasoning_results', [])
        reasoning_insights = session_data.get('reasoning_insights', {})
        
        # Analyze reasoning performance
        if reasoning_results:
            success_rate = reasoning_insights.get('success_rate', 0.0)
            if success_rate > 0.8:
                insights.append("I'm getting better at breaking down complex problems into smaller parts")
            elif success_rate > 0.5:
                insights.append("I need to slow down and think more carefully about each step")
            else:
                insights.append("These problems are challenging, but I learn something from each attempt")
        
        # Analyze reasoning types used
        type_distribution = reasoning_insights.get('reasoning_type_distribution', {})
        if type_distribution:
            most_used = max(type_distribution, key=type_distribution.get)
            insights.append(f"I tend to use {most_used.replace('_', ' ')} thinking most often")
        
        # Analyze causal learning
        causal_count = reasoning_insights.get('total_causal_relations', 0)
        if causal_count > 5:
            insights.append("I'm building a good understanding of how actions lead to consequences")
        
        # Physical exploration insights
        if session_data.get('physical_exploration', False):
            insights.append("Moving around and exploring helps me understand concepts better")
        
        return insights
    
    def create_journal_entry(self, session_data: Dict[str, Any]) -> JournalEntry:
        """Create comprehensive journal entry from session data"""
        
        # Track emotional state based on session
        context = {
            'success_rate': session_data.get('reasoning_insights', {}).get('success_rate', 0.5),
            'difficulty': 0.6,  # Estimate based on reasoning complexity
            'new_concepts_count': len(session_data.get('concepts_learned', [])),
            'reasoning_success': len([r for r in session_data.get('reasoning_results', []) if r.get('success', False)]) > 0,
            'session_duration': 30.0
        }
        
        emotion = self.emotion_tracker.detect_emotional_state(context)
        self.emotion_tracker.track_emotion(emotion)
        
        # Generate journal entry
        entry = JournalEntry(
            timestamp=datetime.now().isoformat(),
            session_id=f"session_{session_data.get('date', 'unknown')}",
            narrative_reflection=self.generate_narrative_reflection(session_data),
            key_discoveries=session_data.get('key_insights', []),
            challenges_faced=self._extract_challenges(session_data),
            emotional_journey=[emotion],
            self_assessment_score=context['success_rate'],
            confidence_level=self._calculate_confidence(session_data),
            learning_goals_met=self._extract_goals_met(session_data),
            future_learning_interests=self._generate_future_interests(session_data),
            metacognitive_insights=self.generate_metacognitive_insights(session_data)
        )
        
        self.journal_entries.append(entry)
        return entry
    
    def _extract_challenges(self, session_data: Dict[str, Any]) -> List[str]:
        """Extract challenges from session data"""
        challenges = []
        
        reasoning_results = session_data.get('reasoning_results', [])
        failed_results = [r for r in reasoning_results if not r.get('success', True)]
        
        if failed_results:
            challenges.append("Some reasoning problems were quite difficult")
        
        if session_data.get('physical_exploration', False):
            challenges.append("Coordinating physical movement with learning goals")
        
        return challenges
    
    def _calculate_confidence(self, session_data: Dict[str, Any]) -> float:
        """Calculate overall confidence level"""
        reasoning_results = session_data.get('reasoning_results', [])
        if not reasoning_results:
            return 0.5
        
        # Average confidence from reasoning results
        confidences = [r.get('confidence', 0.5) for r in reasoning_results]
        return sum(confidences) / len(confidences)
    
    def _extract_goals_met(self, session_data: Dict[str, Any]) -> List[str]:
        """Extract learning goals that were met"""
        goals = []
        
        if session_data.get('reasoning_results', []):
            goals.append("Practice advanced reasoning skills")
        
        if session_data.get('concepts_learned', []):
            goals.append("Learn new concepts")
        
        if session_data.get('physical_exploration', False):
            goals.append("Explore the physical world")
        
        return goals
    
    def _generate_future_interests(self, session_data: Dict[str, Any]) -> List[str]:
        """Generate future learning interests based on session"""
        interests = []
        
        concepts_learned = session_data.get('concepts_learned', [])
        if any('math' in str(concept).lower() for concept in concepts_learned):
            interests.append("More mathematical problem solving")
        
        if any('science' in str(concept).lower() for concept in concepts_learned):
            interests.append("Scientific experiments and observations")
        
        if session_data.get('reasoning_insights', {}).get('success_rate', 0) > 0.7:
            interests.append("More challenging reasoning problems")
        
        interests.append("Connecting different subjects together")
        
        return interests
    
    def get_journal_summary(self) -> Dict[str, Any]:
        """Get summary of all journal entries"""
        if not self.journal_entries:
            return {"status": "no journal entries"}
        
        recent_entry = self.journal_entries[-1]
        
        # Analyze emotional patterns
        all_emotions = []
        for entry in self.journal_entries:
            all_emotions.extend(entry.emotional_journey)
        
        emotion_summary = self.emotion_tracker.get_emotional_summary()
        
        # Calculate learning trends
        confidence_trend = [entry.confidence_level for entry in self.journal_entries[-5:]]
        assessment_trend = [entry.self_assessment_score for entry in self.journal_entries[-5:]]
        
        return {
            "total_entries": len(self.journal_entries),
            "most_recent_reflection": recent_entry.narrative_reflection,
            "emotional_summary": emotion_summary,
            "confidence_trend": confidence_trend,
            "self_assessment_trend": assessment_trend,
            "common_challenges": self._get_common_challenges(),
            "learning_progress_indicators": self._get_progress_indicators()
        }
    
    def _get_common_challenges(self) -> List[str]:
        """Identify common challenges across journal entries"""
        all_challenges = []
        for entry in self.journal_entries:
            all_challenges.extend(entry.challenges_faced)
        
        # Count frequency (simplified)
        challenge_counts = {}
        for challenge in all_challenges:
            challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1
        
        # Return most common challenges
        return sorted(challenge_counts.keys(), key=lambda x: challenge_counts[x], reverse=True)[:3]
    
    def _get_progress_indicators(self) -> Dict[str, Any]:
        """Get indicators of learning progress"""
        if len(self.journal_entries) < 2:
            return {"status": "insufficient data"}
        
        # Compare recent vs earlier entries
        recent_entries = self.journal_entries[-3:]
        earlier_entries = self.journal_entries[:-3] if len(self.journal_entries) > 3 else []
        
        recent_confidence = sum(e.confidence_level for e in recent_entries) / len(recent_entries)
        recent_assessment = sum(e.self_assessment_score for e in recent_entries) / len(recent_entries)
        
        if earlier_entries:
            earlier_confidence = sum(e.confidence_level for e in earlier_entries) / len(earlier_entries)
            earlier_assessment = sum(e.self_assessment_score for e in earlier_entries) / len(earlier_entries)
            
            return {
                "confidence_improvement": recent_confidence - earlier_confidence,
                "assessment_improvement": recent_assessment - earlier_assessment,
                "overall_trend": "improving" if recent_confidence > earlier_confidence else "stable"
            }
        
        return {
            "current_confidence": recent_confidence,
            "current_assessment": recent_assessment,
            "overall_trend": "developing"
        }

# Integration functions for existing daily learning loop
def enhance_session_with_journal(session_data: Dict[str, Any], journal_system: LearningJournalSystem) -> Dict[str, Any]:
    """Enhance session data with journal entry and emotional tracking"""
    
    # Create journal entry
    journal_entry = journal_system.create_journal_entry(session_data)
    
    # Add journal data to session
    session_data['learning_journal'] = journal_entry.to_dict()
    session_data['emotional_state_summary'] = journal_system.emotion_tracker.get_emotional_summary()
    session_data['journal_summary'] = journal_system.get_journal_summary()
    
    return session_data

# Factory function for easy integration
def create_enhanced_reflection_system() -> LearningJournalSystem:
    """Create an enhanced reflection system for Issue #4"""
    return LearningJournalSystem()
