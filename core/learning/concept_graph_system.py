
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
