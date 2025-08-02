"""
Marcus AGI Core Systems

This package contains all core functionality for Marcus AGI including:
- Memory systems
- Consciousness integration
- Learning loops
- Social interaction
- Advanced reasoning
"""

__version__ = "2.0.0"
__author__ = "Marcus AGI Development Team"

# Core system availability flags
MEMORY_AVAILABLE = True
CONSCIOUSNESS_AVAILABLE = True
LEARNING_AVAILABLE = True
SOCIAL_AVAILABLE = True
REASONING_AVAILABLE = True

def get_system_status():
    """Get status of all core systems"""
    return {
        "memory": MEMORY_AVAILABLE,
        "consciousness": CONSCIOUSNESS_AVAILABLE, 
        "learning": LEARNING_AVAILABLE,
        "social": SOCIAL_AVAILABLE,
        "reasoning": REASONING_AVAILABLE,
        "version": __version__
    }
