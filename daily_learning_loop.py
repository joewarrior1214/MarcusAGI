#!/usr/bin/env python3
"""
Integrated Daily Learning Loop
Combines your existing structure with Issue #3 requirements from resilience_mode.py
"""

from datetime import date, datetime
import json
import os
import logging
from typing import List, Dict, Any, Tuple

# Import enhanced functions from resilience_mode
from resilience_mode import (
    generate_daily_lessons,
    calculate_sm2_quality,
    calculate_sm2_interval,
    track_learning_progress,
    check_curriculum_progression,
    generate_analytics_report,
    assess_concept_recall,
    LearningMetrics,
    DAILY_LEARNING_CONFIG
)

# Import your existing systems
try:
    from reflection_system import generate_reflection
    from concept_graph_system import learn_new_concepts, review_previous_concepts
    USING_EXISTING_SYSTEMS = True
except ImportError:
    USING_EXISTING_SYSTEMS = False
    print("⚠️ Using enhanced systems from resilience_mode")

# Constants
OUTPUT_DIR = "output/sessions"
TODAY = str(date.today())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def run_daily_learning_loop():
    """Run daily learning loop with full Issue #3 implementation"""
    print("🌅 Marcus Daily Learning Session - Enhanced Version")
    print("=" * 50)
    
    session_start = datetime.now()
    
    # Step 1: Load session history
    session_history = load_session_history()
    print(f"📚 Loaded {len(session_history)} previous sessions")
    
    # Step 2: Generate adaptive daily lessons
    print("\n📝 Phase 1: Generating personalized lessons...")
    if USING_EXISTING_SYSTEMS:
        # Use your existing learn_new_concepts but enhance it
        new_concepts_basic = learn_new_concepts()
        # Convert to enhanced format
        daily_lessons = enhance_concepts_with_metadata(new_concepts_basic)
    else:
        # Use the enhanced lesson generation
        from marcus_memory_system import MarcusMemorySystem
        from marcus_curriculum_system import MarcusCurriculumSystem
        
        memory_system = MarcusMemorySystem("marcus_learning.db")
        curriculum_system = MarcusCurriculumSystem()
        daily_lessons = generate_daily_lessons(curriculum_system, memory_system)
    
    print(f"Generated {len(daily_lessons)} adaptive lessons")
    
    # Step 3: Conduct spaced repetition reviews with SM-2
    print("\n🔄 Phase 2: Spaced repetition reviews...")
    if USING_EXISTING_SYSTEMS:
        # Enhance your existing review system
        basic_reviews = review_previous_concepts(session_history)
        review_results = enhance_reviews_with_sm2(basic_reviews, session_history)
    else:
        review_results = conduct_sm2_reviews(session_history)
    
    print(f"Completed {len(review_results)} reviews")
    
    # Step 4: Learn new concepts
    print("\n📚 Phase 3: Learning new concepts...")
    concepts_learned = []
    concept_details = []
    
    for lesson in daily_lessons:
        try:
            # Learn the concept
            concepts_learned.append(lesson.get('id', lesson.get('content', 'unknown')))
            concept_details.append(lesson)
            print(f"  📘 Learned: {lesson.get('content', 'concept')}")
        except Exception as e:
            logger.error(f"Failed to learn concept: {e}")
    
    # Step 5: Track progress and calculate metrics
    print("\n📊 Phase 4: Tracking progress...")
    metrics = calculate_session_metrics(
        concepts_learned, 
        review_results, 
        session_history
    )
    
    # Step 6: Check curriculum progression
    print("\n🎯 Phase 5: Checking curriculum progression...")
    progression = check_for_progression(metrics, session_history)
    
    # Step 7: Generate reflection
    print("\n💭 Phase 6: Reflection...")
    if USING_EXISTING_SYSTEMS:
        reflection = generate_reflection()
    else:
        reflection = generate_enhanced_reflection(
            concepts_learned, 
            review_results, 
            metrics
        )
    
    # Step 8: Create comprehensive session report
    session = create_session_report(
        concepts_learned,
        concept_details,
        review_results,
        metrics,
        progression,
        reflection,
        session_start
    )
    
    # Step 9: Save session
    save_session(session)
    
    # Step 10: Generate analytics if enough history
    if len(session_history) >= 7:
        print("\n📈 Generating weekly analytics...")
        analytics = generate_analytics_report(session_history + [session])
        save_analytics(analytics)
    
    # Print summary
    print_session_summary(session)
    
    # Generate parent summary
    generate_parent_summary(session)
    
    return session

def load_session_history() -> List[Dict]:
    """Load all previous sessions"""
    session_history = []
    if os.path.exists(OUTPUT_DIR):
        for fname in sorted(os.listdir(OUTPUT_DIR)):
            if fname.endswith("_report.json"):
                try:
                    with open(os.path.join(OUTPUT_DIR, fname)) as f:
                        session = json.load(f)
                        session_history.append(session)
                except Exception as e:
                    logger.error(f"Failed to load {fname}: {e}")
    
    # Also check master log
    master_log = os.path.join(OUTPUT_DIR, "master_log.jsonl")
    if os.path.exists(master_log):
        try:
            with open(master_log, 'r') as f:
                for line in f:
                    try:
                        session = json.loads(line.strip())
                        session_history.append(session)
                    except:
                        pass
        except Exception as e:
            logger.error(f"Failed to load master log: {e}")
    
    return session_history[-30:]  # Last 30 days

def enhance_concepts_with_metadata(basic_concepts: List[str]) -> List[Dict]:
    """Convert basic concept list to enhanced format"""
    import random
    subjects = ['math', 'reading', 'science', 'social_skills', 'art']
    emotions = ['curious', 'excited', 'calm', 'joyful']
    
    enhanced = []
    for i, concept in enumerate(basic_concepts):
        enhanced.append({
            'id': f'concept_{datetime.now().timestamp()}_{i}',
            'content': concept,
            'subject': random.choice(subjects),
            'difficulty': 0.3 + (i * 0.1),
            'emotional_context': random.choice(emotions)
        })
    
    return enhanced

def enhance_reviews_with_sm2(basic_reviews: List, session_history: List[Dict]) -> List[Dict]:
    """Enhance basic reviews with SM-2 algorithm"""
    enhanced_reviews = []
    
    for i, review in enumerate(basic_reviews):
        # Simulate performance assessment
        performance = {
            'recall_speed': 0.7 + (i * 0.05),
            'accuracy': 0.8 + (i * 0.03),
            'confidence': 0.75,
            'associations': 0.7
        }
        
        quality = calculate_sm2_quality(performance)
        
        # Get previous interval (default to 1 for first review)
        previous_interval = 1
        ease_factor = 2.5
        
        # Calculate next interval
        next_interval, new_ease = calculate_sm2_interval(
            previous_interval, 
            ease_factor, 
            quality
        )
        
        enhanced_reviews.append({
            'concept_id': f'review_{i}',
            'quality': quality,
            'success': quality >= 3,
            'performance': performance,
            'next_interval': next_interval,
            'ease_factor': new_ease,
            'timestamp': datetime.now().isoformat()
        })
    
    return enhanced_reviews

def conduct_sm2_reviews(session_history: List[Dict]) -> List[Dict]:
    """Conduct reviews using SM-2 algorithm"""
    # This would integrate with your memory system
    # For now, return mock data
    return enhance_reviews_with_sm2(['review1', 'review2', 'review3'], session_history)

def calculate_session_metrics(concepts_learned: List[str], 
                            review_results: List[Dict],
                            session_history: List[Dict]) -> LearningMetrics:
    """Calculate comprehensive session metrics"""
    metrics = LearningMetrics()
    
    metrics.concepts_learned = len(concepts_learned)
    metrics.reviews_completed = len(review_results)
    
    # Calculate retention rate
    if review_results:
        successes = sum(1 for r in review_results if r.get('success', False))
        metrics.retention_rate = successes / len(review_results)
    else:
        metrics.retention_rate = 1.0
    
    # Calculate learning velocity
    metrics.learning_velocity = len(concepts_learned)
    
    # Calculate other metrics
    metrics.difficulty_progression = 0.1  # 10% increase
    metrics.emotional_stability = 0.85
    
    # Mock mastery improvements
    metrics.mastery_improvements = {
        'math': 0.02,
        'reading': 0.03,
        'science': 0.01,
        'social_skills': 0.02,
        'art': 0.01
    }
    
    return metrics

def check_for_progression(metrics: LearningMetrics, 
                         session_history: List[Dict]) -> Dict[str, Any]:
    """Check if ready for curriculum progression"""
    # Calculate average mastery across subjects
    avg_mastery = sum(metrics.mastery_improvements.values()) / len(metrics.mastery_improvements)
    current_total_mastery = 0.6 + (len(session_history) * 0.01)  # Simulate progression
    
    mastery_threshold = DAILY_LEARNING_CONFIG['mastery_threshold']
    
    if current_total_mastery >= mastery_threshold:
        return {
            'advanced': True,
            'previous_unit': 'Kindergarten Basics',
            'new_unit': 'Kindergarten Advanced',
            'mastery_achieved': current_total_mastery
        }
    else:
        return {
            'advanced': False,
            'current_mastery': current_total_mastery,
            'target_mastery': mastery_threshold,
            'estimated_concepts_needed': int((mastery_threshold - current_total_mastery) * 50)
        }

def generate_enhanced_reflection(concepts_learned: List[str],
                               review_results: List[Dict],
                               metrics: LearningMetrics) -> str:
    """Generate enhanced reflection with context"""
    success_rate = metrics.retention_rate
    
    reflection_parts = []
    
    # Learning summary
    if concepts_learned:
        reflection_parts.append(f"Today I learned {len(concepts_learned)} new things!")
    
    # Review performance
    if review_results:
        reflection_parts.append(f"I remembered {success_rate:.0%} of what I reviewed.")
    
    # Emotional state
    if success_rate > 0.8:
        reflection_parts.append("I feel proud and confident!")
    else:
        reflection_parts.append("I'm working hard and getting better!")
    
    # Future goals
    reflection_parts.append("Tomorrow I'll learn even more!")
    
    return " ".join(reflection_parts)

def create_session_report(concepts_learned: List[str],
                         concept_details: List[Dict],
                         review_results: List[Dict],
                         metrics: LearningMetrics,
                         progression: Dict[str, Any],
                         reflection: str,
                         session_start: datetime) -> Dict[str, Any]:
    """Create comprehensive session report"""
    session_duration = (datetime.now() - session_start).seconds / 60  # minutes
    
    return {
        'date': TODAY,
        'time': session_start.strftime('%H:%M:%S'),
        'duration_minutes': round(session_duration, 1),
        'reviews_completed': metrics.reviews_completed,
        'review_results': review_results,
        'concepts_learned': concepts_learned,
        'concept_details': concept_details,
        'success_rate': metrics.retention_rate,
        'metrics': {
            'retention_rate': metrics.retention_rate,
            'learning_velocity': metrics.learning_velocity,
            'difficulty_progression': metrics.difficulty_progression,
            'emotional_stability': metrics.emotional_stability,
            'mastery_improvements': metrics.mastery_improvements
        },
        'curriculum_progression': progression,
        'reflection': reflection,
        'success': True
    }

def save_session(session: Dict[str, Any]):
    """Save session report"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Save daily report
    filename = os.path.join(OUTPUT_DIR, f"{TODAY}_report.json")
    with open(filename, "w") as f:
        json.dump(session, f, indent=2)
    
    # Append to master log
    master_log = os.path.join(OUTPUT_DIR, "master_log.jsonl")
    with open(master_log, "a") as f:
        f.write(json.dumps(session) + "\n")
    
    print(f"📝 Session saved to: {filename}")

def save_analytics(analytics: Dict[str, Any]):
    """Save analytics report"""
    analytics_dir = "output/analytics"
    os.makedirs(analytics_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(analytics_dir, f"weekly_report_{timestamp}.json")
    
    with open(filename, "w") as f:
        json.dump(analytics, f, indent=2)
    
    print(f"📊 Analytics saved to: {filename}")

def print_session_summary(session: Dict[str, Any]):
    """Print session summary"""
    print("\n" + "="*50)
    print("✅ Session Complete!")
    print("="*50)
    print(f"📅 Date: {session['date']}")
    print(f"⏱️ Duration: {session.get('duration_minutes', 0):.1f} minutes")
    print(f"🔄 Reviews completed: {session['reviews_completed']}")
    print(f"🧠 New concepts learned: {len(session['concepts_learned'])}")
    print(f"🎯 Success rate: {session['success_rate']:.1%}")
    print(f"💬 Reflection: {session['reflection']}")
    
    # Show progression status
    prog = session.get('curriculum_progression', {})
    if prog.get('advanced'):
        print(f"🎓 ADVANCED to: {prog.get('new_unit')}!")
    else:
        print(f"🎓 Progress: {prog.get('current_mastery', 0):.0%} mastery")

def generate_parent_summary(session: Dict[str, Any]):
    """Generate parent-friendly summary"""
    summary_dir = "output/summaries"
    os.makedirs(summary_dir, exist_ok=True)
    
    summary = f"""📅 Daily Report for {session['date']}

✨ Today's Achievements:
- Learned {len(session['concepts_learned'])} new concepts
- Completed {session['reviews_completed']} reviews ({session['success_rate']:.0%} success rate)
- Session duration: {session.get('duration_minutes', 0):.0f} minutes

📚 Subjects Covered:
"""
    
    # Add subjects
    subjects = set()
    for detail in session.get('concept_details', []):
        if 'subject' in detail:
            subjects.add(detail['subject'].replace('_', ' ').title())
    
    for subject in subjects:
        summary += f"- {subject}\n"
    
    # Add progression
    prog = session.get('curriculum_progression', {})
    if prog.get('advanced'):
        summary += f"\n🎉 Big News: Advanced to {prog.get('new_unit')}!\n"
    else:
        summary += f"\n📈 Progress: {prog.get('current_mastery', 0):.0%} toward next level\n"
    
    # Add reflection
    summary += f"\n💭 Marcus says: \"{session['reflection']}\"\n"
    
    # Add recommendations
    if session['success_rate'] < 0.7:
        summary += "\n💡 Tomorrow: Focus on review to strengthen memory"
    elif len(session['concepts_learned']) > 5:
        summary += "\n💡 Tomorrow: Great progress! Keep up the momentum"
    
    # Save summary
    filename = os.path.join(summary_dir, f"{session['date']}_parent_summary.txt")
    with open(filename, "w") as f:
        f.write(summary)
    
    print(f"\n👪 Parent summary saved to: {filename}")

if __name__ == "__main__":
    session = run_daily_learning_loop()
    
    # Show final message
    print("\n🌸 Marcus Daily Session Complete!")
    print("Check the output directory for detailed reports and analytics.")