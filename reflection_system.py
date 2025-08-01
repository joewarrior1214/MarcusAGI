
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
