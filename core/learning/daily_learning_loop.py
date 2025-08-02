#!/usr/bin/env python3
"""
Marcus AGI Daily Learning Loop - Complete Implementation (Issue #3)

This module implements the core daily learning loop that drives Marcus's 
educational progression. It includes:

- Automated lesson generation
- Spaced repetition (SM-2 algorithm)
- Progress tracking and analytics
- Curriculum progression logic
- Parent-friendly reporting
- AGI-specific enhancements

The system adapts difficulty based on performance and maintains comprehensive
metrics for monitoring learning progress.
"""

import logging
import pathlib
import sys
from typing import List, Dict, Any, Tuple, Optional, NewType
from dataclasses import dataclass, field, asdict
from collections import defaultdict

# Type definitions
Graph = NewType('Graph', Dict[str, List[str]])
import json
import random
import os
from datetime import date, datetime, timedelta
from math import ceil

# Add logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('marcus_agi.log'),
        logging.StreamHandler()
    ]
)

# Add proper path handling:
BASE_DIR = pathlib.Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output" / "sessions"
ANALYTICS_DIR = BASE_DIR / "output" / "analytics"
SUMMARIES_DIR = BASE_DIR / "output" / "summaries"

# Import your existing systems
from reflection_system import generate_reflection  # This import might fail
from concept_graph_system import learn_new_concepts, review_previous_concepts  # This import might fail

# Import enhanced reflection system for Issue #4 completion
try:
    from reflection_journal_system import create_enhanced_reflection_system, enhance_session_with_journal
    ENHANCED_REFLECTION_AVAILABLE = True
except ImportError:
    ENHANCED_REFLECTION_AVAILABLE = False
    print("Enhanced reflection system not available - using basic reflection")

def get_due_reviews(session_history: List[Dict], today: str) -> List[Dict]:
    """
    Pulls concepts that are due for review based on 'next_review' date.
    """
    due_reviews = []

    for session in session_history:
        for review in session.get('review_results', []):
            next_review_str = review.get('next_review', '')
            try:
                next_review_date = datetime.strptime(next_review_str, "%Y-%m-%d").date()
                if next_review_date <= datetime.strptime(today, "%Y-%m-%d").date():
                    due_reviews.append({
                        'id': review.get('concept_id'),
                        'content': review.get('content'),
                        'interval_days': review.get('interval_days', 1),
                        'ease_factor': review.get('ease_factor', 2.5),
                        'repetitions': review.get('repetitions', 0)
                    })
            except Exception:
                continue  # Ignore malformed dates

    return due_reviews

# Configuration for Issue #3 requirements
LEARNING_CONFIG = {
    'max_new_concepts': 5,
    'max_reviews': 10,
    'mastery_threshold': 0.85,  # 85% for curriculum progression
    'difficulty_adjustment_rate': 0.1,
    'sm2_initial_interval': 1,
    'sm2_easy_bonus': 1.3,
    'sm2_min_ease': 1.3
}

# Default concept pool for testing
DEFAULT_CONCEPT_POOL = [
    {'subject': 'math', 'content': 'counting to 10', 'difficulty': 0.2},
    {'subject': 'reading', 'content': 'letter sounds', 'difficulty': 0.3},
    {'subject': 'science', 'content': 'colors', 'difficulty': 0.2},
    {'subject': 'social', 'content': 'sharing', 'difficulty': 0.3},
    {'subject': 'art', 'content': 'drawing shapes', 'difficulty': 0.2}
]

# Initialize concept pool
concept_pool = DEFAULT_CONCEPT_POOL.copy()

@dataclass
class ConceptReview:
    """Track review data for SM-2 algorithm"""
    concept_id: str
    content: str
    interval_days: float = 1.0
    ease_factor: float = 2.5
    repetitions: int = 0
    last_review: str = ""
    next_review: str = ""
    quality: int = 0  # 0-5 scale
    success: bool = False

@dataclass
class LearningMetrics:
    """Comprehensive learning metrics for Issue #3"""
    subject_mastery: Dict[str, float]
    review_success_rate: float
    concept_acquisition_rate: float
    adaptive_difficulty: float
    
    def calculate_learning_velocity(self) -> float:
        """Calculate rate of learning progress"""
        return (self.review_success_rate * 0.6 + 
                self.concept_acquisition_rate * 0.4) * self.adaptive_difficulty

    def get_optimal_difficulty(self) -> float:
        """Determine optimal challenge level"""
        return min(1.0, self.subject_mastery.get(
            max(self.subject_mastery, key=self.subject_mastery.get), 0
        ) + 0.2)

@dataclass
class ConceptNode:
    """Minimal ConceptNode for AGILearningMetrics network metrics calculation"""
    relationships: List[str] = field(default_factory=list)

@dataclass
class AGILearningMetrics:
    """Enhanced metrics for AGI learning performance"""
    # Core metrics
    concept_retention: Dict[str, float] = field(default_factory=dict)
    knowledge_graph_density: float = 0.0
    learning_velocity: float = 0.0
    
    # Meta-learning metrics
    adaptation_rate: float = 0.0
    transfer_efficiency: float = 0.0
    concept_integration: float = 0.0
    
    # Network metrics
    semantic_connectivity: float = 0.0
    knowledge_entropy: float = 0.0
    
    def calculate_network_metrics(self, concept_graph: Dict[str, 'ConceptNode']) -> None:
        """Calculate knowledge graph metrics"""
        total_connections = sum(len(node.relationships) for node in concept_graph.values())
        possible_connections = len(concept_graph) * (len(concept_graph) - 1)
        self.knowledge_graph_density = total_connections / possible_connections if possible_connections > 0 else 0

def calculate_sm2_quality(performance: Dict[str, float]) -> int:
    """
    Calculate SM-2 quality rating (0-5) from performance metrics
    This is a core requirement for Issue #3
    """
    # Performance should include: recall_speed, accuracy, confidence
    weights = {
        'recall_speed': 0.2,
        'accuracy': 0.5,
        'confidence': 0.3
    }
    
    # Calculate weighted score
    score = 0.0
    for metric, weight in weights.items():
        score += performance.get(metric, 0.5) * weight
    
    # Convert to 0-5 scale
    if score >= 0.9:
        return 5  # Perfect
    elif score >= 0.8:
        return 4  # Good
    elif score >= 0.7:
        return 3  # Satisfactory
    elif score >= 0.6:
        return 2  # Difficult
    elif score >= 0.4:
        return 1  # Very difficult
    else:
        return 0  # Failed

def calculate_sm2_interval(review: ConceptReview, quality: int) -> Tuple[float, float]:
    """
    SM-2 (SuperMemo 2) algorithm implementation
    Required by Issue #3 for spaced repetition
    
    Returns: (next_interval_days, new_ease_factor)
    """
    # Update ease factor
    new_ease = review.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ease = max(LEARNING_CONFIG['sm2_min_ease'], new_ease)
    
    # Calculate next interval
    if quality < 3:
        # Failed - reset
        next_interval = 1
        repetitions = 0
    else:
        repetitions = review.repetitions + 1
        if repetitions == 1:
            next_interval = 1
        elif repetitions == 2:
            next_interval = 6
        else:
            next_interval = review.interval_days * new_ease
            
            # Apply quality-based multiplier
            if quality == 3:
                next_interval *= 0.6
            elif quality == 4:
                next_interval *= 1.0
            else:  # quality == 5
                next_interval *= LEARNING_CONFIG['sm2_easy_bonus']
    
    return round(next_interval), round(new_ease, 2)

def generate_adaptive_lessons(session_history: List[Dict], mastery_levels: Dict[str, float]) -> List[Dict]:
    """
    Generate personalized lessons based on progress
    Required by Issue #3 for adaptive learning
    """
    lessons = []
    
    # Calculate adaptive difficulty for each subject
    subjects = ['math', 'reading', 'science', 'social', 'art']
    subject_priorities = []
    
    for subject in subjects:
        mastery = mastery_levels.get(subject, 0.0)
        # Lower mastery = higher priority
        priority = 1.0 - mastery
        
        # Boost core subjects
        if subject in ['math', 'reading']:
            priority *= 1.2
            
        # Calculate appropriate difficulty
        difficulty = mastery + LEARNING_CONFIG['difficulty_adjustment_rate']
        difficulty = min(difficulty, 1.0)  # Cap at 1.0
        
        subject_priorities.append({
            'subject': subject,
            'priority': priority,
            'difficulty': difficulty,
            'mastery': mastery
        })
    
    # Sort by priority and select top subjects
    subject_priorities.sort(key=lambda x: x['priority'], reverse=True)
    
    # Generate lessons for top priority subjects
    max_lessons = LEARNING_CONFIG['max_new_concepts']
    for i, subject_data in enumerate(subject_priorities[:max_lessons]):
        lesson = {
            'id': f"{subject_data['subject']}_{datetime.now().timestamp()}_{i}",
            'subject': subject_data['subject'],
            'difficulty': subject_data['difficulty'],
            'content': f"Advanced {subject_data['subject']} concept (difficulty: {subject_data['difficulty']:.2f})",
            'priority_score': subject_data['priority'],
            'adaptive': True
        }
        lessons.append(lesson)
    
    return lessons

def conduct_sm2_reviews(concepts_to_review: List[Dict], session_history: List[Dict], today: str) -> List[ConceptReview]:
    reviews = []

    for concept_data in concepts_to_review:
        review = ConceptReview(
            concept_id=concept_data.get('id', f"concept_{len(reviews)}"),
            content=concept_data.get('content', 'Unknown concept'),
            interval_days=concept_data.get('interval_days', 1),
            ease_factor=concept_data.get('ease_factor', 2.5),
            repetitions=concept_data.get('repetitions', 0)
        )

        # Ensure content is not None
        if not review.content:
            review.content = f"Review concept {review.concept_id}"

        performance = {
            'recall_speed': random.uniform(0.6, 1.0),
            'accuracy': random.uniform(0.5, 1.0),
            'confidence': random.uniform(0.6, 0.95)
        }

        quality = calculate_sm2_quality(performance)
        review.quality = quality
        review.success = quality >= 3

        next_interval, new_ease = calculate_sm2_interval(review, quality)
        review.interval_days = next_interval
        review.ease_factor = new_ease
        review.last_review = today
        review.next_review = str(date.today() + timedelta(days=next_interval))

        reviews.append(review)
        content_preview = str(review.content)[:50] if review.content else "Unknown concept"
        print(f"  📖 Reviewed: {content_preview}... Quality: {quality}/5")

    return reviews


def calculate_mastery_levels(session_history: List[Dict]) -> Dict[str, float]:
    """
    Calculate current mastery level for each subject
    Required for curriculum progression (Issue #3)
    """
    if not session_history:
        return {subj: 0.2 for subj in ['math', 'reading', 'science', 'social', 'art']}
    
    subject_scores = {'math': [], 'reading': [], 'science': [], 'social': [], 'art': []}
    
    # Analyze recent sessions
    recent_sessions = session_history[-10:]  # Last 10 sessions
    
    for session in recent_sessions:
        # Check review performance
        for review in session.get('review_results', []):
            # Extract subject from concept
            for subject in subject_scores.keys():
                if subject in str(review.get('concept_id', '')).lower():
                    if review.get('success', False):
                        subject_scores[subject].append(1.0)
                    else:
                        subject_scores[subject].append(0.5)
        
        # Check new concepts learned
        for concept in session.get('concepts_learned', []):
            for subject in subject_scores.keys():
                if subject in concept.lower():
                    subject_scores[subject].append(0.1)  # Small boost for learning
    
    # Calculate mastery as average score
    mastery_levels = {}
    for subject, scores in subject_scores.items():
        if scores:
            mastery = sum(scores) / len(scores)
            # Add time-based progression
            mastery += len(session_history) * 0.01
            mastery = min(mastery, 1.0)  # Cap at 100%
        else:
            mastery = 0.2  # Base level
        mastery_levels[subject] = mastery
    
    return mastery_levels

def check_curriculum_progression(mastery_levels: Dict[str, float], current_unit: str = "Kindergarten Basics") -> Dict[str, Any]:
    """
    Check if learner is ready to advance to next curriculum unit
    Required by Issue #3
    """
    # Calculate overall mastery
    avg_mastery = sum(mastery_levels.values()) / len(mastery_levels) if mastery_levels else 0
    
    threshold = LEARNING_CONFIG['mastery_threshold']
    
    if avg_mastery >= threshold:
        # Ready to advance!
        return {
            'advanced': True,
            'previous_unit': current_unit,
            'new_unit': "Kindergarten Advanced" if "Basics" in current_unit else "First Grade Preparation",
            'mastery_achieved': avg_mastery,
            'subject_mastery': mastery_levels
        }
    else:
        # Not ready yet
        concepts_needed = int((threshold - avg_mastery) * 50)
        
        return {
            'advanced': False,
            'current_unit': current_unit,
            'current_mastery': avg_mastery,
            'target_mastery': threshold,
            'estimated_concepts_needed': concepts_needed,
            'subject_mastery': mastery_levels,
            'weakest_subject': min(mastery_levels, key=mastery_levels.get)
        }

def calculate_learning_metrics(session: Dict[str, Any], session_history: List[Dict]) -> Dict[str, Any]:
    """Calculate comprehensive learning metrics with AGI enhancements"""
    
    # Calculate basic metrics
    reviews_completed = session.get('reviews_completed', 0)
    concepts_learned = len(session.get('concepts_learned', []))
    review_results = session.get('review_results', [])
    
    # Calculate success rates
    if review_results:
        successful_reviews = sum(1 for r in review_results if r.get('quality', 0) >= 3)
        review_success_rate = successful_reviews / len(review_results)
    else:
        review_success_rate = 0.0
    
    # Calculate subject mastery (use the mastery levels from session)
    subject_mastery = session.get('mastery_levels', {
        'math': 0.8, 'reading': 0.4, 'science': 0.3, 'social': 0.6, 'art': 0.2
    })
    
    # Calculate adaptive difficulty
    avg_mastery = sum(subject_mastery.values()) / len(subject_mastery) if subject_mastery else 0.5
    adaptive_difficulty = min(0.9, max(0.1, avg_mastery + 0.1))
    
    # Create metrics object with proper initialization
    metrics = LearningMetrics(
        subject_mastery=subject_mastery,
        review_success_rate=review_success_rate,
        concept_acquisition_rate=concepts_learned,
        adaptive_difficulty=adaptive_difficulty
    )
    
    # Add derived metrics
    metrics.retention_rate = review_success_rate
    metrics.learning_velocity = concepts_learned
    metrics.engagement_score = min(1.0, (review_success_rate + (concepts_learned / 10)) / 2)
    
    # Add session history analysis
    if len(session_history) > 1:
        recent_sessions = session_history[-5:]  # Last 5 sessions
        recent_concepts = sum(len(s.get('concepts_learned', [])) for s in recent_sessions)
        metrics.learning_trend = recent_concepts / len(recent_sessions)
    else:
        metrics.learning_trend = concepts_learned
    
    # Add embodied social exploration metrics if available
    if session.get('physical_exploration'):
        embodied_concepts = len(session.get('embodied_concepts', []))
        metrics.embodied_learning_rate = embodied_concepts
        metrics.grounded_concept_ratio = embodied_concepts / max(1, concepts_learned)
        
        # Add enhanced embodied social metrics
        if session.get('embodied_social_exploration'):
            metrics.social_interactions = session.get('social_interactions', 0)
            metrics.sensory_integration_score = session.get('sensory_integration_score', 0)
            metrics.social_physical_coherence = session.get('social_physical_coherence', 0)
            metrics.learning_engagement = session.get('learning_engagement', 0)
            metrics.skills_practiced = session.get('skills_practiced', 0)
            metrics.sensory_modalities_used = session.get('sensory_modalities_used', 0)
        else:
            # Basic embodied learning metrics
            metrics.social_interactions = 0
            metrics.sensory_integration_score = 0
            metrics.social_physical_coherence = 0
            metrics.learning_engagement = 0
            metrics.skills_practiced = 0
            metrics.sensory_modalities_used = 0
    else:
        metrics.embodied_learning_rate = 0
        metrics.grounded_concept_ratio = 0
        metrics.social_interactions = 0
        metrics.sensory_integration_score = 0
        metrics.social_physical_coherence = 0
        metrics.learning_engagement = 0
        metrics.skills_practiced = 0
        metrics.sensory_modalities_used = 0
    
    # Convert to dictionary for compatibility
    metrics_dict = {
        'subject_mastery': metrics.subject_mastery,
        'review_success_rate': metrics.review_success_rate,
        'concept_acquisition_rate': metrics.concept_acquisition_rate,
        'adaptive_difficulty': metrics.adaptive_difficulty,
        'retention_rate': metrics.retention_rate,
        'learning_velocity': metrics.learning_velocity,
        'engagement_score': metrics.engagement_score,
        'learning_trend': metrics.learning_trend,
        'embodied_learning_rate': getattr(metrics, 'embodied_learning_rate', 0),
        'grounded_concept_ratio': getattr(metrics, 'grounded_concept_ratio', 0),
        # Enhanced embodied social metrics
        'social_interactions': getattr(metrics, 'social_interactions', 0),
        'sensory_integration_score': getattr(metrics, 'sensory_integration_score', 0),
        'social_physical_coherence': getattr(metrics, 'social_physical_coherence', 0),
        'learning_engagement': getattr(metrics, 'learning_engagement', 0),
        'skills_practiced': getattr(metrics, 'skills_practiced', 0),
        'sensory_modalities_used': getattr(metrics, 'sensory_modalities_used', 0),
        'transfer_learning': measure_transfer_learning(),
        'meta_learning': {
            'adaptation_rate': calculate_adaptation_rate(session),
            'concept_integration': analyze_concept_integration()
        }
    }
    
    return metrics_dict

def measure_transfer_learning() -> float:
    """Measure how well concepts transfer between subjects"""
    return random.uniform(0.3, 0.8)  # Placeholder

def calculate_adaptation_rate(session: Dict[str, Any]) -> float:
    """Calculate how quickly Marcus adapts to new concepts"""
    concepts_learned = len(session.get('concepts_learned', []))
    return min(1.0, concepts_learned / 5)  # Placeholder

def generate_daily_reasoning_problems(current_session: Dict[str, Any], all_sessions: List[Dict]) -> List:
    """Generate reasoning problems based on Marcus's current learning state"""
    
    try:
        from advanced_reasoning_engine import ReasoningProblem
    except ImportError:
        return []
    
    problems = []
    
    # Problem 1: Based on physical exploration
    if current_session.get('physical_exploration'):
        key_insights = current_session.get('key_insights', [])
        if key_insights:
            problems.append(ReasoningProblem(
                id=f"physical_reasoning_{len(all_sessions)}",
                description=f"Apply physical insight: {key_insights[0]}",
                domain="physics",
                goal="use physical understanding to solve abstract problem",
                givens=key_insights,
                difficulty=0.6
            ))
    
    # Problem 2: Based on learning performance
    mastery_levels = current_session.get('mastery_levels', {})
    if mastery_levels:
        weakest_subject = min(mastery_levels, key=mastery_levels.get)
        problems.append(ReasoningProblem(
            id=f"learning_reasoning_{len(all_sessions)}",
            description=f"How to improve performance in {weakest_subject}",
            domain="learning",
            goal=f"increase {weakest_subject} mastery from {mastery_levels[weakest_subject]:.1%} to 80%",
            givens=[f"current {weakest_subject} mastery: {mastery_levels[weakest_subject]:.1%}"],
            difficulty=0.7
        ))
    
    # Problem 3: Meta-learning problem
    total_sessions = len(all_sessions)
    if total_sessions > 5:
        problems.append(ReasoningProblem(
            id=f"meta_reasoning_{len(all_sessions)}",
            description="How to optimize learning strategy based on past performance",
            domain="meta-learning",
            goal="design optimal learning approach",
            givens=[f"completed {total_sessions} learning sessions"],
            difficulty=0.8
        ))
    
    return problems

def analyze_concept_integration() -> float:
    """Analyze how well concepts integrate with existing knowledge"""
    return random.uniform(0.4, 0.9)  # Placeholder

def generate_reflection() -> str:
    """Generate learning reflection"""
    reflections = [
        "I learned about heavy objects today through physical exploration!",
        "Touching different textures helped me understand materials.",
        "Moving around the world taught me about boundaries and obstacles.",
        "I discovered that some things can't be moved or lifted."
    ]
    return random.choice(reflections)

def learn_new_concepts(concepts: List[str]) -> List[str]:
    """Stub for concept learning"""
    return concepts

def review_previous_concepts(num_reviews: int) -> List[Dict]:
    """Stub for concept review"""
    sample_concepts = [
        {'id': 'art_1', 'content': 'cutting with scissors'},
        {'id': 'social_1', 'content': 'using kind words'},
        {'id': 'science_1', 'content': 'weather types'},
        {'id': 'reading_1', 'content': 'beginning sounds'}
    ]
    return sample_concepts[:num_reviews]

def load_all_sessions() -> List[Dict]:
    """Load all previous sessions from files"""
    all_sessions = []
    
    if os.path.exists(OUTPUT_DIR):
        for fname in sorted(os.listdir(OUTPUT_DIR)):
            if fname.endswith(".json") and ("session" in fname or "marcus_session" in fname):
                try:
                    with open(os.path.join(OUTPUT_DIR, fname)) as f:
                        session_data = json.load(f)
                        # Handle both single session and list of sessions
                        if isinstance(session_data, list):
                            all_sessions.extend(session_data)
                        else:
                            all_sessions.append(session_data)
                except Exception as e:
                    print(f"Warning: Could not load {fname}: {e}")
    
    # Sort sessions by timestamp if available
    all_sessions.sort(key=lambda x: x.get('timestamp', x.get('date', '')))
    return all_sessions

def save_current_session_only(current_session: Dict) -> None:
    """Save only the current session to a unique file with detailed timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")  # More detailed: YYYYMMDD_HHMMSS
    session_id = f"marcus_session_{timestamp}"
    filename = f"{session_id}.json"
    
    # Add session metadata
    current_session['session_id'] = session_id
    current_session['timestamp'] = datetime.now().isoformat()
    current_session['session_duration_minutes'] = random.randint(15, 45)  # Simulated duration
    
    try:
        with open(OUTPUT_DIR / filename, "w") as f:
            json.dump(current_session, f, indent=4, default=str)
        print(f"✅ Session saved: {session_id}")
    except Exception as e:
        print(f"🚨 Error saving session: {e}")

def run_daily_learning_loop(run_date: date = date.today()) -> Dict[str, Any]:
    """Enhanced daily learning loop with advanced reasoning capabilities"""
    print("🌸 Marcus AGI - Daily Learning Session")
    print("=" * 50)
    TODAY = str(run_date)

    # Create output directories
    for directory in [OUTPUT_DIR, ANALYTICS_DIR, SUMMARIES_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Step 1: Load ALL previous sessions (not overwriting)
    all_previous_sessions = load_all_sessions()
    print(f"📚 Loaded {len(all_previous_sessions)} previous sessions")
    
    # Step 2: Initialize Advanced Reasoning Engine
    try:
        from advanced_reasoning_engine import AdvancedReasoningEngine, ReasoningProblem
        reasoning_engine = AdvancedReasoningEngine()
        print("🧠 Advanced Reasoning Engine initialized")
    except ImportError:
        reasoning_engine = None
        print("⚠️  Advanced Reasoning Engine not available")
    
    # Step 3: Enhanced Embodied Social Exploration
    print("\n🎮🤝 Enhanced Embodied Social Exploration...")
    current_session = {'date': TODAY, 'physical_exploration': False, 'embodied_social_exploration': False}
    
    try:
        # Import the enhanced embodied social system
        import sys
        sys.path.append('/workspaces')
        
        # Try to use the new embodied social integration system first
        try:
            from marcus_embodied_social_integration import (
                MarcusEmbodiedSocialIntegration, PhysicalSocialContext
            )
            
            print("  🎯 Using Enhanced Embodied Social Learning System")
            
            # Initialize the comprehensive embodied social system
            integration = MarcusEmbodiedSocialIntegration(world_size=10)
            
            # Run an embodied social learning session
            learning_experience = integration.run_embodied_social_session(
                duration_minutes=20,
                context=PhysicalSocialContext.FREE_PLAY
            )
            
            # Extract comprehensive learning data
            concepts_discovered = len(learning_experience.concepts_discovered)
            social_interactions = len(learning_experience.social_exchanges)
            sensory_modalities = len(learning_experience.sensory_modalities)
            skills_practiced = len(set(learning_experience.physical_skills_practiced + 
                                     learning_experience.social_skills_practiced))
            
            print(f"  ✅ Embodied Social Learning Complete:")
            print(f"    • Concepts Discovered: {concepts_discovered}")
            print(f"    • Social Interactions: {social_interactions}")
            print(f"    • Sensory Modalities Used: {sensory_modalities}/6")
            print(f"    • Skills Practiced: {skills_practiced}")
            print(f"    • Integration Score: {learning_experience.sensory_integration_score:.3f}")
            print(f"    • Social-Physical Coherence: {learning_experience.social_physical_coherence:.3f}")
            
            # Extract key insights from embodied social learning
            key_insights = learning_experience.concepts_discovered[:3]  # Top 3 discoveries
            
            current_session.update({
                'physical_exploration': True,
                'embodied_social_exploration': True,
                'concepts_discovered': concepts_discovered,
                'social_interactions': social_interactions,
                'sensory_integration_score': learning_experience.sensory_integration_score,
                'social_physical_coherence': learning_experience.social_physical_coherence,
                'learning_engagement': learning_experience.learning_engagement_level,
                'key_insights': key_insights,
                'skills_practiced': skills_practiced,
                'sensory_modalities_used': sensory_modalities,
                'embodied_concepts': learning_experience.concepts_discovered
            })
            
        except ImportError:
            # Fallback to basic embodied learning system
            print("  🔄 Falling back to Basic Embodied Learning System")
            from marcus_simple_body import MarcusGridWorld, EmbodiedLearning
            from memory_system import MarcusMemorySystem, Concept
            
            # Initialize physical world
            world = MarcusGridWorld()
            embodied = EmbodiedLearning(world)
            memory_system = MarcusMemorySystem("marcus_embodied.db")
            
            # Conduct physical exploration - QUIET MODE
            physical_learnings = embodied.explore_and_learn(20)
            
            # Show summary instead of verbose output
            concepts_discovered = physical_learnings.get('concepts_discovered', 0)
            print(f"  ✅ Explored world: {concepts_discovered} new concepts discovered")
            
            # Extract key insights
            key_insights = []
            for category, learnings in physical_learnings.get('key_learnings', {}).items():
                if learnings:
                    key_insights.extend(learnings[:2])  # Top 2 per category
            
            if key_insights:
                print("  🧠 Key Discoveries:")
                for insight in key_insights[:3]:  # Show top 3 insights
                    print(f"    • {insight}")
            
            current_session.update({
                'physical_exploration': True,
                'concepts_discovered': concepts_discovered,
                'key_insights': key_insights[:3],
                'total_experiences': physical_learnings.get('total_experiences', 0),
                'embodied_concepts': key_insights[:3]
            })
        
        # Feed embodied insights to reasoning engine
        if reasoning_engine:
            reasoning_engine.extract_causal_relations_from_session(current_session)
        
    except Exception as e:
        print(f"  ⚠️ Embodied exploration error: {str(e)[:50]}...")
        current_session.update({
            'physical_exploration': False,
            'embodied_social_exploration': False
        })
    
    # Step 4: Advanced Reasoning Challenge
    reasoning_results = []
    if reasoning_engine:
        print("\n🎯 Advanced Reasoning Challenge...")
        
        # Generate reasoning problems based on current session
        daily_problems = generate_daily_reasoning_problems(current_session, all_previous_sessions)
        
        for problem in daily_problems[:2]:  # Solve 2 problems per session
            result = reasoning_engine.solve_problem_with_reasoning(problem)
            reasoning_results.append(result)
            
            print(f"  🧩 Problem: {problem.description}")
            print(f"     Solution: {result.solution[0] if result.solution else 'No solution'}")
            print(f"     Method: {result.reasoning_type} (confidence: {result.confidence:.2f})")
        
        # Get reasoning insights
        reasoning_insights = reasoning_engine.get_reasoning_insights()
        current_session['reasoning_results'] = [
            {
                'problem_id': r.problem_id,
                'success': r.success,
                'reasoning_type': r.reasoning_type,
                'confidence': r.confidence
            } for r in reasoning_results
        ]
        current_session['reasoning_insights'] = reasoning_insights
    
    # Step 5: Academic Learning (use all previous sessions for context)
    session_history_for_learning = all_previous_sessions + [current_session]
    learning_results = run_learning_session(session_history_for_learning, TODAY)
    
    # Update current session with learning results
    current_session.update(learning_results)
    
    # Step 6: Enhanced Reflection & Learning Journal (Issue #4 completion)
    if ENHANCED_REFLECTION_AVAILABLE:
        print("\n📖 Creating Learning Journal Entry...")
        try:
            # Initialize journal system (could be persistent in real implementation)
            journal_system = create_enhanced_reflection_system()
            
            # Enhance session with journal entry and emotional tracking
            current_session = enhance_session_with_journal(current_session, journal_system)
            
            # Show brief summary of journal entry
            if 'learning_journal' in current_session:
                journal_entry = current_session['learning_journal']
                print(f"  📝 Reflection: {journal_entry['narrative_reflection'][:100]}...")
                
                if 'emotional_state_summary' in current_session:
                    emotion_summary = current_session['emotional_state_summary']
                    if 'current_primary_emotion' in emotion_summary:
                        print(f"  😊 Primary emotion: {emotion_summary['current_primary_emotion']}")
                
                metacognitive_insights = journal_entry.get('metacognitive_insights', [])
                if metacognitive_insights:
                    print(f"  🧠 Meta-insight: {metacognitive_insights[0]}")
        
        except Exception as e:
            print(f"  ⚠️ Enhanced reflection error: {str(e)[:50]}...")
    
    # Step 7: Save ONLY current session (no overwriting)
    save_current_session_only(current_session)
    
    # Step 8: Generate report for current session
    generate_reports([current_session], TODAY)
    
    print("\n✅ Learning session complete!")
    return current_session

def run_learning_session(session_history: List[Dict], today: str) -> Dict[str, Any]:
    """
    Run the core learning session: generate lessons, conduct reviews, and update metrics
    """
    # 1. Calculate mastery levels
    mastery_levels = calculate_mastery_levels(session_history)
    
    # 2. Check curriculum progression
    progression_report = check_curriculum_progression(mastery_levels, session_history[-1].get('current_unit', "Kindergarten Basics"))
    
    # 3. Generate adaptive lessons
    new_lessons = generate_adaptive_lessons(session_history, mastery_levels)
    
    # 4. Conduct SM-2 reviews for spaced repetition
    due_reviews = get_due_reviews(session_history, today)
    review_results = conduct_sm2_reviews(due_reviews, session_history, today)
    
    # 5. Update session history
    session_history[-1].update({
        'date': today,
        'reviews_completed': len(review_results),
        'concepts_learned': [lesson.get('content') for lesson in new_lessons],
        'review_results': [asdict(result) for result in review_results],
        'mastery_levels': mastery_levels
    })
    
    # 6. Generate learning metrics - QUIET
    metrics = calculate_learning_metrics(session_history[-1], session_history)
    
    return {
        'reviews_completed': len(review_results),
        'concepts_learned': [lesson.get('content') for lesson in new_lessons],
        'review_results': [asdict(result) for result in review_results],
        'mastery_levels': mastery_levels,
        'metrics': metrics
    }

def save_session_history(session_history: List[Dict]) -> None:
    """Save the session history to files with unique timestamps"""
    if not session_history:
        return
    
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"session_{timestamp}.json"
    
    # Save as JSON
    try:
        with open(OUTPUT_DIR / filename, "w") as f:
            json.dump(session_history, f, indent=4, default=str)
        print(f"✅ Session history saved: {OUTPUT_DIR / filename}")
    except Exception as e:
        print(f"🚨 Error saving session history: {e}")

def generate_reports(session_history: List[Dict], today: str) -> None:
    """Generate and save progress reports with detailed timestamps"""
    if not session_history:
        return
    
    # Create detailed timestamp for reports
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_id = f"marcus_report_{timestamp}"
    report_filename = f"{report_id}.txt"
    
    # Aggregate data for reporting
    total_sessions = len(session_history)
    total_reviews = sum(len(s.get('review_results', [])) for s in session_history)
    total_concepts_learned = sum(len(s.get('concepts_learned', [])) for s in session_history)
    
    # Save detailed text report
    try:
        with open(SUMMARIES_DIR / report_filename, "w") as f:
            f.write("🌟 Marcus AGI Learning Report\n")
            f.write("=" * 40 + "\n")
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}\n")
            f.write(f"Session Date: {today}\n\n")
            f.write(f"📊 Session Summary:\n")
            f.write(f"  • Total Sessions: {total_sessions}\n")
            f.write(f"  • Reviews Conducted: {total_reviews}\n")
            f.write(f"  • Concepts Learned: {total_concepts_learned}\n\n")
            f.write("📈 Detailed Progress:\n")
            
            for i, session in enumerate(session_history, 1):
                session_id = session.get('session_id', f'session_{i}')
                concepts_count = len(session.get('concepts_learned', []))
                reviews_count = len(session.get('review_results', []))
                physical_exploration = "✅" if session.get('physical_exploration') else "❌"
                embodied_social = "✅" if session.get('embodied_social_exploration') else "❌"
                
                f.write(f"  {i}. {session_id}\n")
                f.write(f"     Date: {session.get('date')}\n")
                f.write(f"     Physical Exploration: {physical_exploration}\n")
                f.write(f"     Embodied Social Learning: {embodied_social}\n")
                
                # Add embodied social metrics if available
                if session.get('embodied_social_exploration'):
                    social_interactions = session.get('social_interactions', 0)
                    integration_score = session.get('sensory_integration_score', 0)
                    coherence_score = session.get('social_physical_coherence', 0)
                    skills_practiced = session.get('skills_practiced', 0)
                    f.write(f"     Social Interactions: {social_interactions} | Integration: {integration_score:.3f}\n")
                    f.write(f"     Social-Physical Coherence: {coherence_score:.3f} | Skills: {skills_practiced}\n")
                
                f.write(f"     Concepts: {concepts_count} | Reviews: {reviews_count}\n\n")
        
        print(f"📊 Report saved: {report_id}")
    except Exception as e:
        print(f"🚨 Error generating report: {e}")

# Example of running the daily learning loop
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            print("🧪 Running test mode...")
            # Run with today's date
            result = run_daily_learning_loop()
            print(f"✅ Test completed successfully!")
        else:
            # Parse date from command line
            try:
                test_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
                result = run_daily_learning_loop(test_date)
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD")
                sys.exit(1)
    else:
        # Run with today's date
        print("🚀 Running Marcus Daily Learning Loop...")
        result = run_daily_learning_loop()
        print("✅ Daily learning session completed!")
