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
    
    # Add physical exploration metrics if available
    if session.get('physical_exploration'):
        embodied_concepts = len(session.get('embodied_concepts', []))
        metrics.embodied_learning_rate = embodied_concepts
        metrics.grounded_concept_ratio = embodied_concepts / max(1, concepts_learned)
    else:
        metrics.embodied_learning_rate = 0
        metrics.grounded_concept_ratio = 0
    
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
        'transfer_learning': measure_transfer_learning(),
        'meta_learning': {
            'adaptation_rate': calculate_adaptation_rate(session),
            'concept_integration': analyze_concept_integration()
        }
    }
    
    return metrics_dict

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
    
    # Add physical exploration metrics if available
    if session.get('physical_exploration'):
        embodied_concepts = len(session.get('embodied_concepts', []))
        metrics.embodied_learning_rate = embodied_concepts
        metrics.grounded_concept_ratio = embodied_concepts / max(1, concepts_learned)
    else:
        metrics.embodied_learning_rate = 0
        metrics.grounded_concept_ratio = 0
    
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
        'transfer_learning': measure_transfer_learning(),
        'meta_learning': {
            'adaptation_rate': calculate_adaptation_rate(session),
            'concept_integration': analyze_concept_integration()
        }
    }
    
    return metrics_dict

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
    
    # Add physical exploration metrics if available
    if session.get('physical_exploration'):
        embodied_concepts = len(session.get('embodied_concepts', []))
        metrics.embodied_learning_rate = embodied_concepts
        metrics.grounded_concept_ratio = embodied_concepts / max(1, concepts_learned)
    else:
        metrics.embodied_learning_rate = 0
        metrics.grounded_concept_ratio = 0
    
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
        'transfer_learning': measure_transfer_learning(),
        'meta_learning': {
            'adaptation_rate': calculate_adaptation_rate(session),
            'concept_integration': analyze_concept_integration()
        }
    }
    
    return metrics_dict

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
    
    # Add physical exploration metrics if available
    if session.get('physical_exploration'):
        embodied_concepts = len(session.get('embodied_concepts', []))
        metrics.embodied_learning_rate = embodied_concepts
        metrics.grounded_concept_ratio = embodied_concepts / max(1, concepts_learned)
    else:
        metrics.embodied_learning_rate = 0
        metrics.grounded_concept_ratio = 0
    
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
        'transfer_learning': measure_transfer_learning(),
        'meta_learning': {
            'adaptation_rate': calculate_adaptation_rate(session),
            'concept_integration': analyze_concept_integration()
        }
    }
    
    return metrics_dict

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
    
    # Add physical exploration metrics if available
    if session.get('physical_exploration'):
        embodied_concepts = len(session.get('embodied_concepts', []))
        metrics.embodied_learning_rate = embodied_concepts
        metrics.grounded_concept_ratio = embodied_concepts / max(1, concepts_learned)
    else:
        metrics.embodied_learning_rate = 0
        metrics.grounded_concept_ratio = 0
    
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
        'transfer_learning': measure_transfer_learning(),
        'meta_learning': {
            'adaptation_rate': calculate_adaptation_rate(session),
            'concept_integration': analyze_concept_integration()
        }
    }
    
    return metrics_dict

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
    
    # Add physical exploration metrics if available
    if session.get('physical_exploration'):
        embodied_concepts = len(session.get('embodied_concepts', []))
        metrics.embodied_learning_rate = embodied_concepts
        metrics.grounded_concept_ratio = embodied_concepts / max(1, concepts_learned)
    else:
        metrics.embodied_learning_rate = 0
        metrics.grounded_concept_ratio = 0
    
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
        'transfer_learning': measure_transfer_learning(),
        'meta_learning': {
            'adaptation_rate': calculate_adaptation_rate(session),
            'concept_integration': analyze_concept_integration()
        }
    }
    
    return metrics_dict

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
        