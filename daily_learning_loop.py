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
    retention_rate: float = 0.0
    learning_velocity: int = 0
    difficulty_progression: float = 0.0
    mastery_by_subject: Dict[str, float] = None
    review_performance: Dict[str, float] = None
    
    def __post_init__(self):
        if self.mastery_by_subject is None:
            self.mastery_by_subject = {}
        if self.review_performance is None:
            self.review_performance = {}

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
        print(f"  📖 Reviewed: {review.content[:50]}... Quality: {quality}/5")

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

def calculate_learning_metrics(session: Dict, session_history: List[Dict]) -> LearningMetrics:
    """
    Calculate comprehensive learning metrics
    Required by Issue #3 for progress tracking
    """
    metrics = LearningMetrics()
    
    # Retention rate from reviews
    reviews = session.get('review_results', [])
    if reviews:
        successful = sum(1 for r in reviews if r.get('success', False))
        metrics.retention_rate = successful / len(reviews)
    else:
        metrics.retention_rate = 1.0
    
    # Learning velocity
    metrics.learning_velocity = len(session.get('concepts_learned', []))
    
    # Difficulty progression
    if session_history:
        recent_avg = sum(len(s.get('concepts_learned', [])) for s in session_history[-5:]) / 5
        metrics.difficulty_progression = 0.1 if metrics.learning_velocity > recent_avg else 0.05
    else:
        metrics.difficulty_progression = 0.1
    
    # Mastery by subject
    metrics.mastery_by_subject = calculate_mastery_levels(session_history)
    
    # Review performance
    if reviews:
        avg_quality = sum(r.get('quality', 0) for r in reviews) / len(reviews)
        metrics.review_performance = {
            'average_quality': avg_quality,
            'success_rate': metrics.retention_rate,
            'reviews_completed': len(reviews)
        }
    
    return metrics

def generate_analytics_report(session_history: List[Dict]) -> Dict[str, Any]:
    """
    Generate comprehensive analytics report
    Required by Issue #3
    """
    if not session_history:
        return {'error': 'No session history available'}
    
    # Calculate metrics
    total_concepts = sum(len(s.get('concepts_learned', [])) for s in session_history)
    total_reviews = sum(s.get('reviews_completed', 0) for s in session_history)
    
    # Retention trend
    retention_rates = [s.get('metrics', {}).get('retention_rate', 0) for s in session_history if 'metrics' in s]
    avg_retention = sum(retention_rates) / len(retention_rates) if retention_rates else 0
    
    # Learning velocity trend
    velocities = [len(s.get('concepts_learned', [])) for s in session_history]
    avg_velocity = sum(velocities) / len(velocities) if velocities else 0
    
    # Subject performance
    subject_performance = {}
    for subject in ['math', 'reading', 'science', 'social', 'art']:
        subject_concepts = 0
        for session in session_history:
            for concept in session.get('concepts_learned', []):
                if subject in concept.lower():
                    subject_concepts += 1
        subject_performance[subject] = subject_concepts
    
    # Generate recommendations
    recommendations = []
    if avg_retention < 0.7:
        recommendations.append("Focus on review sessions to improve retention")
    if avg_velocity < 3:
        recommendations.append("Try to learn at least 3 new concepts per session")
    if avg_velocity > 7:
        recommendations.append("Consider reducing concepts per session for deeper learning")
    
    weakest_subject = min(subject_performance, key=subject_performance.get)
    recommendations.append(f"Spend more time on {weakest_subject} concepts")
    
    return {
        'summary': {
            'total_sessions': len(session_history),
            'total_concepts_learned': total_concepts,
            'total_reviews_completed': total_reviews,
            'average_retention_rate': round(avg_retention, 3),
            'average_learning_velocity': round(avg_velocity, 1)
        },
        'trends': {
            'retention_trend': 'improving' if len(retention_rates) > 1 and retention_rates[-1] > retention_rates[0] else 'stable',
            'velocity_trend': 'increasing' if len(velocities) > 1 and velocities[-1] > velocities[0] else 'stable'
        },
        'subject_performance': subject_performance,
        'recommendations': recommendations,
        'generated_date': TODAY
    }

def generate_parent_summary(session: Dict) -> str:
    """
    Generate parent-friendly summary
    Enhancement for Issue #3
    """
    summary = f"""📅 Marcus's Daily Learning Report - {session['date']}

🌟 Today's Achievements:
• Learned {len(session.get('concepts_learned', []))} new concepts
• Completed {session.get('reviews_completed', 0)} reviews
• Success rate: {session.get('metrics', {}).get('retention_rate', 0):.0%}

📚 What Marcus Learned Today:
"""
    
    # List concepts in friendly format
    for i, concept in enumerate(session.get('concepts_learned', []), 1):
        summary += f"{i}. {concept}\n"
    
    # Add progression status
    progression = session.get('curriculum_progression', {})
    if progression.get('advanced'):
        summary += f"\n🎉 Big Achievement: Marcus advanced to {progression['new_unit']}!\n"
    else:
        mastery = progression.get('current_mastery', 0)
        summary += f"\n📊 Progress: {mastery:.0%} toward next level"
        if progression.get('weakest_subject'):
            summary += f"\n💡 Focus area: {progression['weakest_subject']}"
    
    # Add reflection
    summary += f"\n\n💭 Marcus's Reflection:\n\"{session.get('reflection', 'Today was a good day for learning!')}\"\n"
    
    # Add metrics if available
    if 'metrics' in session:
        metrics = session['metrics']
        summary += f"\n📈 Learning Stats:\n"
        summary += f"• Retention rate: {metrics.get('retention_rate', 0):.0%}\n"
        summary += f"• Learning speed: {metrics.get('learning_velocity', 0)} concepts/session\n"
    
    return summary

@dataclass
class ConceptNode:
    """Enhanced concept representation for AGI learning"""
    id: str
    content: str
    relationships: Dict[str, float] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Learning parameters
    activation_threshold: float = 0.5
    learning_rate: float = 0.1
    plasticity: float = 0.5
    
    def update_relationships(self, related_concept: 'ConceptNode', strength: float) -> None:
        """Update semantic relationships between concepts"""
        self.relationships[related_concept.id] = strength
        
    def evaluate_readiness(self) -> float:
        """Check if prerequisites are met"""
        if not self.dependencies:
            return 1.0
        return sum(self.relationships.get(dep, 0.0) for dep in self.dependencies) / len(self.dependencies)

# Add config validation
def validate_config() -> None:
    required_keys = ['max_new_concepts', 'max_reviews', 'mastery_threshold']
    for key in required_keys:
        if key not in LEARNING_CONFIG:
            raise ValueError(f"Missing required config key: {key}")

def validate_session_data(session: Dict[str, Any]) -> bool:
    """Validate required session data fields"""
    if not isinstance(session, dict):
        return False
        
    required_fields = ['date', 'reviews_completed', 'concepts_learned']
    return all(
        field in session and session[field] is not None 
        for field in required_fields
    )

def measure_transfer_learning() -> float:
    """Currently returns dummy 0.0"""
    # Needs real implementation for:
    # - Cross-subject knowledge transfer
    # - Skill application in new contexts
    # - Learning efficiency metrics
    return 0.0

def calculate_adaptation_rate(session: Dict[str, Any]) -> float:
    """
    Stub for adaptation rate calculation.
    Returns a dummy value for now.
    """
    return 0.0

def analyze_concept_integration() -> float:
    """
    Stub for concept integration analysis.
    Returns a dummy value for now.
    """
    return 0.0

def analyze_concept_clusters() -> Dict[str, List[str]]:
    pass

def identify_central_concepts() -> List[str]:
    pass

def adjust_learning_parameters() -> dict:
    """
    Stub for learning rate adjustment logic.
    Returns a dummy value for now.
    """
    return {}

def adapt_learning_strategies() -> dict:
    """
    Stub for learning strategy adaptation logic.
    Returns a dummy value for now.
    """
    return {}

def propose_structural_changes() -> dict:
    """
    Stub for proposing structural changes.
    Returns a dummy value for now.
    """
    return {}

def enhance_daily_learning_loop(
    session: Dict[str, Any],
    enhancement_threshold: float = 0.5
) -> Dict[str, Any]:
    """Add AGI-specific enhancements to the learning loop"""
    try:
        # Add meta-learning capabilities
        session['meta_learning'] = {
            'adaptation_rate': calculate_adaptation_rate(session),
            'transfer_efficiency': measure_transfer_learning(),
            'concept_integration': analyze_concept_integration()
        }
        
        # Add knowledge graph analysis
        session['knowledge_graph'] = {
            'density': 0.0,  # Placeholder: implement calculate_graph_density if needed
            'clustering': analyze_concept_clusters(),
            'centrality': identify_central_concepts()
        }
        
        # Add self-modification capabilities
        session['self_modifications'] = {
            'learning_rate_adjustments': adjust_learning_parameters(),
            'strategy_adaptations': adapt_learning_strategies(),
            'architecture_changes': propose_structural_changes()
        }
    except Exception as e:
        logging.error(f"Failed to enhance learning loop: {e}")
        return session  # Return unmodified session on error
    
    return session

TODAY = str(date.today())

def run_daily_learning_loop(run_date: date = date.today()) -> Dict[str, Any]:
    """Enhanced daily learning loop with AGI capabilities"""
    print("🌸 Marcus Daily Learning Session - Complete Implementation")
    print("=" * 60)
    TODAY = str(run_date)  # Local override of global TODAY

    # Create output directories
    for directory in [OUTPUT_DIR, ANALYTICS_DIR, SUMMARIES_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Step 1: Load session history
    session_history = []
    if os.path.exists(OUTPUT_DIR):
        for fname in sorted(os.listdir(OUTPUT_DIR)):
            if fname.endswith("_report.json") or fname.endswith("_session.json"):
                try:
                    with open(os.path.join(OUTPUT_DIR, fname)) as f:
                        session_history.append(json.load(f))
                except Exception as e:
                    print(f"Warning: Could not load {fname}: {e}")
    
    print(f"📚 Loaded {len(session_history)} previous sessions")
    
    # Step 2: Calculate current mastery levels
    print("\n📊 Calculating mastery levels...")
    mastery_levels = calculate_mastery_levels(session_history)
    for subject, mastery in mastery_levels.items():
        print(f"  {subject}: {mastery:.0%}")
    
    # Step 3: Generate adaptive lessons
    print("\n📝 Generating adaptive lessons...")
    adaptive_lessons = generate_adaptive_lessons(session_history, mastery_levels)
    
    # Combine with your existing concept selection
    basic_concepts = learn_new_concepts()
    
    # Merge adaptive and basic concepts
    all_concepts = []
    for i, lesson in enumerate(adaptive_lessons[:3]):  # Take top 3 adaptive
        all_concepts.append(f"{basic_concepts[i] if i < len(basic_concepts) else lesson['content']}")
    
    # Step 4: Conduct SM-2 spaced repetition reviews
    print("\n🔄 Conducting spaced repetition reviews...")
    
    # Get concepts due for review
    concepts_to_review = []
    if session_history:
        for session in session_history[-5:]:
            for concept in session.get('concepts_learned', []):
                if random.random() < 0.3:
                    concepts_to_review.append({
                        'id': concept,
                        'content': concept,
                        'interval_days': random.randint(1, 7),
                        'ease_factor': 2.5,
                        'repetitions': random.randint(0, 5)
                    })
    
    # Limit reviews
    concepts_to_review = concepts_to_review[:LEARNING_CONFIG['max_reviews']]
    
    # If no concepts to review, use defaults
    if not concepts_to_review:
        default_reviews = review_previous_concepts(session_history)
        concepts_to_review = [{'id': r, 'content': r} for r in default_reviews]
    
    # Conduct reviews with SM-2
    review_results = conduct_sm2_reviews(concepts_to_review, session_history, TODAY)

    # Step 5: Learn new concepts
    print(f"\n📘 Learning {len(all_concepts)} new concepts...")
    for i, concept in enumerate(all_concepts, 1):
        print(f"  {i}. {concept}")
    
    # Step 6: Calculate metrics
    print("\n📈 Calculating learning metrics...")
    
    # Create session before metrics calculation
    session = {
        'date': TODAY,
        'timestamp': datetime.now().isoformat(),
        'reviews_completed': len(review_results),
        'review_results': [asdict(r) if hasattr(r, '__dict__') else r for r in review_results],
        'concepts_learned': all_concepts,
        'adaptive_lessons': adaptive_lessons,
        'reflection': generate_reflection()
    }
    
    metrics = calculate_learning_metrics(session, session_history)
    session['metrics'] = asdict(metrics)
    
    # Step 7: Check curriculum progression
    print("\n🎯 Checking curriculum progression...")
    current_unit = "Kindergarten Basics"  # In real implementation, load from state
    progression = check_curriculum_progression(mastery_levels, current_unit)
    session['curriculum_progression'] = progression
    
    if progression['advanced']:
        print(f"  🎉 ADVANCED to {progression['new_unit']}!")
    else:
        print(f"  📊 Progress: {progression['current_mastery']:.0%} (need {progression['target_mastery']:.0%})")
        print(f"  📚 Estimated concepts needed: {progression['estimated_concepts_needed']}")
    
    # Step 8: Save session
    print("\n💾 Saving session data...")
    session_file = os.path.join(OUTPUT_DIR, f"{TODAY}_complete_session.json")
    try:
        with open(session_file, "w") as f:
            json.dump(session, f, indent=2)
        logging.info(f"Session saved successfully to {session_file}")
    except Exception as e:
        logging.error(f"Failed to save session: {e}")
        raise
    
    # Step 9: Generate analytics if enough history
    if len(session_history) >= 5:
        print("\n📊 Generating analytics report...")
        analytics = generate_analytics_report(session_history + [session])
        analytics_file = os.path.join(ANALYTICS_DIR, f"{TODAY}_analytics.json")
        with open(analytics_file, "w") as f:
            json.dump(analytics, f, indent=2)
        print(f"  ✅ Analytics saved to {analytics_file}")
        
        # Display key analytics
        print("\n📈 Analytics Summary:")
        for key, value in analytics['summary'].items():
            print(f"  • {key}: {value}")
    
    # Step 10: Generate parent summary
    print("\n👪 Generating parent summary...")
    parent_summary = generate_parent_summary(session)
    summary_file = os.path.join(SUMMARIES_DIR, f"{TODAY}_parent_summary.txt")
    with open(summary_file, "w") as f:
        f.write(parent_summary)
    print(f"  ✅ Parent summary saved to {summary_file}")
    
    # Add AGI enhancements
    session = enhance_daily_learning_loop(session)
    
    # Add meta-learning metrics with initialized concept_graph
    agi_metrics = AGILearningMetrics()
    concept_graph = {concept: ConceptNode(id=concept, content=concept) 
                    for concept in session.get('concepts_learned', [])}
    agi_metrics.calculate_network_metrics(concept_graph)
    session['agi_metrics'] = asdict(agi_metrics)
    
    return session

def optimize_subject_distribution(current_mastery: Dict[str, float]) -> Dict[str, int]:
    """Optimize concept distribution with focus on science"""
    target_mastery = 0.85
    concept_allocation = {}
    
    # Prioritize science concepts
    science_weight = 1.5  # Increase science learning weight
    
    for subject, mastery in current_mastery.items():
        if mastery < target_mastery:
            gap = target_mastery - mastery
            weight = science_weight if subject == 'science' else 1.0
            concepts_needed = int(ceil(gap * 100 * weight / 15))
            concept_allocation[subject] = concepts_needed
        else:
            concept_allocation[subject] = 0
            
    return concept_allocation

def calculate_optimal_difficulty(
    subject: str,
    current_mastery: float,
    recent_performance: List[float]
) -> float:
    """Dynamic difficulty adjustment based on performance"""
    base_difficulty = current_mastery
    performance_modifier = sum(recent_performance) / len(recent_performance) if recent_performance else 0.5
    
    return min(0.95, base_difficulty * (1 + performance_modifier * 0.2))

@dataclass
class SubjectPriority:
    subject: str
    current_mastery: float
    days_since_practice: int
    recent_success_rate: float
    
    learning_style_adaptation: Dict[str, float] = field(default_factory=dict)
    difficulty_curve: List[float] = field(default_factory=list)
    concept_relationships: Graph = field(default_factory=lambda: Graph({}))
    
    def calculate_priority(self) -> float:
        mastery_weight = 1 - self.current_mastery
        recency_weight = min(1.0, self.days_since_practice / 7)
        performance_weight = 1 - self.recent_success_rate
        
        return (mastery_weight * 0.5 + 
                recency_weight * 0.3 + 
                performance_weight * 0.2)

def select_optimal_concepts(
    session: Dict[str, Any],
    concept_pool: List[Dict],
    target_concepts: int = 5
) -> List[Dict]:
    """Select concepts optimized for reaching 85% mastery"""
    priorities = {}
    mastery = session['metrics']['mastery_by_subject']
    
    for subject in mastery:
        if mastery[subject] < 0.85:
            priority = SubjectPriority(
                subject=subject,
                current_mastery=mastery[subject],
                days_since_practice=get_days_since_practice(session, subject),
                recent_success_rate=get_success_rate(session, subject)
            )
            priorities[subject] = priority.calculate_priority()
    
    selected_concepts = []
    for _ in range(target_concepts):
        subject = max(priorities.items(), key=lambda x: x[1])[0]
        concept = get_next_concept(concept_pool, subject)
        if concept:
            selected_concepts.append(concept)
            priorities[subject] *= 0.5  # Reduce priority after selection
    
    return selected_concepts

def track_mastery_progression(session_history: List[Dict]) -> Dict[str, List[float]]:
    """Track mastery progression over time for each subject"""
    progression = defaultdict(list)
    
    for session in session_history:
        mastery = session.get('metrics', {}).get('mastery_by_subject', {})
        for subject, level in mastery.items():
            progression[subject].append(level)
    
    return dict(progression)

def get_days_since_practice(session: Dict[str, Any], subject: str) -> int:
    """Calculate days since last practice for a subject"""
    if not session.get('session_history'):
        return 7  # Default to maximum priority if no history
    
    for past_session in reversed(session.get('session_history', [])):
        if any(subject.lower() in concept.lower() 
               for concept in past_session.get('concepts_learned', [])):
            last_date = datetime.strptime(past_session['date'], '%Y-%m-%d').date()
            return (date.today() - last_date).days
    return 7

def get_success_rate(session: Dict[str, Any], subject: str) -> float:
    """Calculate recent success rate for a subject"""
    if not session.get('review_results'):
        return 0.5  # Default to neutral if no review history
        
    subject_reviews = [
        review for review in session.get('review_results', [])
        if subject.lower() in review.get('concept_id', '').lower()
    ]
    
    if not subject_reviews:
        return 0.5
        
    return sum(review.get('quality', 0) >= 4 for review in subject_reviews) / len(subject_reviews)

def get_next_concept(concept_pool: List[Dict], subject: str) -> Optional[Dict]:
    """
    Get next available concept for a given subject from the concept pool.
    
    Args:
        concept_pool: List of available concepts
        subject: Target subject to find concept for
        
    Returns:
        Optional[Dict]: Next concept or None if no concepts available
    """
    available_concepts = [
        concept for concept in concept_pool 
        if concept.get('subject', '').lower() == subject.lower() 
        and not concept.get('learned', False)
    ]
    
    if not available_concepts:
        # If no exact match, try to generate a concept
        return {
            'subject': subject,
            'content': f"New {subject} concept",
            'difficulty': 0.5,
            'id': f"{subject}_{datetime.now().timestamp()}"
        }
    
    # Select concept with appropriate difficulty
    selected = random.choice(available_concepts)
    selected['learned'] = True  # Mark as learned
    
    return selected

Graph = NewType('Graph', Dict[str, List[str]])

# Test functions for validation
def test_learning_progression():
    """Test full learning cycle"""
    test_session = {
        'date': TODAY,
        'concepts_learned': ['test_concept'],
        'metrics': {'mastery_by_subject': {'math': 0.5}}
    }
    progression = track_mastery_progression([test_session])
    assert 'math' in progression
    assert len(progression['math']) == 1

def test_mastery_calculation():
    """Verify mastery algorithms"""
    test_mastery = {'math': 0.5, 'reading': 0.3}
    allocation = optimize_subject_distribution(test_mastery)
    assert allocation['math'] > 0
    assert allocation['reading'] > allocation['math']

def test_adaptation_mechanics():
    """Verify system adaptation"""
    difficulty = calculate_optimal_difficulty('math', 0.5, [0.7, 0.8, 0.9])
    assert 0 <= difficulty <= 1

if __name__ == "__main__":
    import sys
    from datetime import datetime

    # Run tests in debug mode
    if '--test' in sys.argv:
        test_learning_progression()
        test_mastery_calculation()
        test_adaptation_mechanics()
        print("✅ All tests passed!")
        sys.exit(0)

    # Normal execution
    if len(sys.argv) > 1 and sys.argv[1] != '--test':
        run_date = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    else:
        run_date = date.today()

    session = run_daily_learning_loop(run_date)
    print(f"\n🎉 Learning complete for {run_date}!")


