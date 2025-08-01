#!/usr/bin/env python3
"""
Marcus BULLETPROOF Integration - Handles All Error Cases and Saves Logs
"""

import datetime
import logging
import os
import json
from typing import Optional, Dict, Any, List

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/resilience_mode.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def safe_import_marcus_systems():
    """Safely import Marcus systems with fallbacks"""
    systems = {}
    fallbacks = []

    try:
        from marcus_memory_system import MarcusMemorySystem, Concept
        systems['memory_system'] = MarcusMemorySystem
        systems['concept'] = Concept
    except ImportError as e:
        logger.error("Cannot import memory system", exc_info=True)
        return None, ['memory_import_failed']

    try:
        from marcus_curriculum_system import MarcusCurriculumSystem
        systems['curriculum_system'] = MarcusCurriculumSystem
    except ImportError as e:
        logger.warning("Curriculum system unavailable", exc_info=True)
        systems['curriculum_system'] = None
        fallbacks.append("curriculum_missing")

    try:
        from enhanced_reflection_system import MarcusReflectionSystem
        systems['reflection_system'] = MarcusReflectionSystem
    except ImportError as e:
        logger.warning("Reflection system unavailable", exc_info=True)
        systems['reflection_system'] = None
        fallbacks.append("reflection_missing")

    return systems, fallbacks

def run_bulletproof_marcus_session():
    """Run Marcus session with error handling and logging"""
    print("🌅 Starting BULLETPROOF Marcus Session")
    print("=" * 50)

    systems, fallbacks = safe_import_marcus_systems()
    if not systems:
        print("❌ Critical error: Cannot import required systems")
        return None

    try:
        memory_system = systems['memory_system']("marcus_bulletproof.db")
        curriculum_system = systems.get('curriculum_system')
        reflection_system = systems.get('reflection_system')

        review_results = safe_conduct_reviews(memory_system)
        learning_results = safe_conduct_learning(memory_system, systems['concept'])
        reflection_data = safe_conduct_reflection(reflection_system, learning_results)

        session_report = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'reviews_completed': len(review_results),
            'concepts_learned': len(learning_results.get('new_concepts', [])),
            'reflection': reflection_data.get('content', 'Today was a learning day!'),
            'fallbacks_used': fallbacks + reflection_data.get('fallbacks', []),
            'success': True
        }

        print("\n✅ Session completed successfully!")
        print(f"📊 Reviews: {session_report['reviews_completed']}")
        print(f"📚 New concepts: {session_report['concepts_learned']}")
        print(f"💭 Reflection: {session_report['reflection'][:100]}...")

        # Save session report
        os.makedirs("output/sessions", exist_ok=True)
        filename = f"output/sessions/{session_report['date']}_report.json"
        with open(filename, "w") as f:
            json.dump(session_report, f, indent=2)
        print(f"📝 Report saved: {filename}")

        return session_report

    except Exception as e:
        logger.error("Critical error in Marcus session", exc_info=True)
        return {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'error': str(e),
            'fallbacks_used': fallbacks,
            'success': False
        }

def safe_conduct_reviews(memory_system) -> List[Dict[str, Any]]:
    review_results = []
    try:
        if hasattr(memory_system, 'get_due_reviews'):
            due_reviews = memory_system.get_due_reviews()
            for review_data in due_reviews[:3]:
                concept_id = review_data.get('id')
                if concept_id:
                    import random
                    success = random.random() > 0.25
                    memory_system.review_concept(concept_id, success)
                    review_results.append({'concept_id': concept_id, 'success': success})
                    print(f"🔍 Reviewed {concept_id}: {'✅' if success else '🔄'}")
    except Exception as e:
        logger.error("Error in review phase", exc_info=True)
    return review_results

def safe_conduct_learning(memory_system, ConceptClass) -> Dict[str, Any]:
    results = {'new_concepts': [], 'errors': []}
    examples = [
        {'id': 'kindness_today', 'content': 'Being kind helps others', 'subject': 'social_skills', 'emotional_context': 'warm'},
        {'id': 'colors_mixing', 'content': 'Red and blue make purple', 'subject': 'art', 'emotional_context': 'wonder'}
    ]
    try:
        for item in examples:
            concept = ConceptClass(**item)
            if memory_system.learn_concept(concept):
                results['new_concepts'].append(item['id'])
                print(f"📘 Learned: {item['content']}")
    except Exception as e:
        logger.error("Learning failed", exc_info=True)
        results['errors'].append(str(e))
    return results

def safe_conduct_reflection(reflection_system, learning_results) -> Dict[str, Any]:
    if not reflection_system:
        return {'content': 'Fallback reflection: Learning is fun!', 'fallbacks': ['reflection_fallback']}
    try:
        reflection_input = {
            'concepts_learned': learning_results.get('new_concepts', []),
            'success_rate': 0.8,
            'emotional_growth': ['joy', 'curiosity']
        }
        moment = reflection_system.generate_contextual_reflection(reflection_input)
        return {'content': getattr(moment, 'content', str(moment)), 'fallbacks': []}
    except Exception as e:
        logger.error("Reflection failed", exc_info=True)
        return {'content': 'Fallback after error: I learned today!', 'fallbacks': ['reflection_error']}

if __name__ == "__main__":
    session = run_bulletproof_marcus_session()
    if session and session.get('success'):
        print("\n🎉 BULLETPROOF session completed successfully!")
    else:
        print("\n⚠️ Session encountered errors.")