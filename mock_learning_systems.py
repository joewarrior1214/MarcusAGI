#!/usr/bin/env python3
"""
Mock systems for testing daily_learning_loop.py
Creates reflection_system.py and concept_graph_system.py
"""

import os

# Create reflection_system.py
reflection_system_code = '''
"""Mock Reflection System"""
import random
from datetime import datetime

def generate_reflection():
    """Generate a reflection for the daily session"""
    reflections = [
        "Today I learned about colors and shapes! It was fun to discover new patterns.",
        "I practiced counting and remembered most of my numbers. Tomorrow I'll try harder!",
        "Learning makes me happy! I especially enjoyed the stories about kindness.",
        "My brain feels stronger after today's practice. I love learning new things!",
        "I helped my friend understand sharing today. Learning together is better!",
        f"On {datetime.now().strftime('%A')}, I grew smarter and kinder!",
        "Every day I learn something new. Today was special because I understood more!",
        "I'm getting better at remembering what I learned yesterday. Practice helps!"
    ]
    
    return random.choice(reflections)
'''

# Create concept_graph_system.py
concept_graph_code = '''
"""Mock Concept Graph System"""
import random
from typing import List, Dict, Any

# Kindergarten concept pool
CONCEPT_POOL = {
    'math': [
        'counting to 10',
        'basic shapes',
        'bigger and smaller',
        'patterns with colors',
        'adding with fingers',
        'counting objects',
        'number recognition 1-5',
        'simple sorting'
    ],
    'reading': [
        'letter A sounds',
        'letter B sounds', 
        'rhyming words',
        'story sequencing',
        'character feelings',
        'beginning sounds',
        'sight word: the',
        'sight word: and'
    ],
    'science': [
        'plants need water',
        'day and night',
        'weather types',
        'animal homes',
        'five senses',
        'hot and cold',
        'living things grow',
        'seasons change'
    ],
    'social': [
        'sharing toys',
        'using kind words',
        'taking turns',
        'helping friends',
        'following rules',
        'expressing feelings',
        'saying please',
        'saying thank you'
    ],
    'art': [
        'primary colors',
        'mixing colors',
        'drawing circles',
        'making patterns',
        'cutting with scissors',
        'gluing shapes',
        'finger painting',
        'clay shapes'
    ]
}

def learn_new_concepts() -> List[str]:
    """Select new concepts to learn today"""
    concepts = []
    
    # Select 3-5 concepts from different subjects
    num_concepts = random.randint(3, 5)
    subjects = list(CONCEPT_POOL.keys())
    
    for i in range(num_concepts):
        subject = random.choice(subjects)
        concept = random.choice(CONCEPT_POOL[subject])
        concepts.append(f"{concept} ({subject})")
    
    return concepts

def review_previous_concepts(session_history: List[Dict[str, Any]]) -> List[str]:
    """Select concepts for review based on previous sessions"""
    reviews = []
    
    # If we have history, review some old concepts
    if session_history:
        # Get concepts from recent sessions
        all_previous_concepts = []
        for session in session_history[-5:]:  # Last 5 sessions
            all_previous_concepts.extend(session.get('concepts_learned', []))
        
        # Select 2-4 for review
        if all_previous_concepts:
            num_reviews = min(len(all_previous_concepts), random.randint(2, 4))
            reviews = random.sample(all_previous_concepts, num_reviews)
    else:
        # No history, so review some basic concepts
        reviews = [
            'counting to 5 (math)',
            'primary colors (art)',
            'sharing toys (social)'
        ]
    
    return reviews
'''

# Write the files
print("📝 Creating mock systems...")

with open('reflection_system.py', 'w') as f:
    f.write(reflection_system_code)
print("✅ Created reflection_system.py")

with open('concept_graph_system.py', 'w') as f:
    f.write(concept_graph_code)
print("✅ Created concept_graph_system.py")

print("\n✨ Mock systems created successfully!")
print("\nYou can now run:")
print("  python quick_test_learning_loop.py")
print("\nOr test them individually:")
print("  python -c 'from reflection_system import generate_reflection; print(generate_reflection())'")
print("  python -c 'from concept_graph_system import learn_new_concepts; print(learn_new_concepts())'")

# Test the systems
print("\n🧪 Testing mock systems...")
try:
    from reflection_system import generate_reflection
    from concept_graph_system import learn_new_concepts, review_previous_concepts
    
    print(f"\n💭 Sample reflection: {generate_reflection()}")
    print(f"\n📚 Sample concepts: {learn_new_concepts()}")
    print(f"\n🔄 Sample reviews: {review_previous_concepts([])}")
    
    print("\n✅ All systems working correctly!")
except Exception as e:
    print(f"\n❌ Error testing systems: {e}")