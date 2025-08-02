#!/usr/bin/env python3
"""Test script to check if all imports work"""

import sys
import os

# Test basic imports
try:
    import json
    import random
    from datetime import date, datetime, timedelta
    from math import ceil
    print("✅ Basic imports work")
except ImportError as e:
    print(f"❌ Basic import failed: {e}")

# Test physical world import
try:
    sys.path.append('/workspaces')
    from marcus_simple_body import MarcusGridWorld, EmbodiedLearning
    print("✅ Physical world imports work")
    
    # Test basic functionality
    world = MarcusGridWorld()
    embodied = EmbodiedLearning(world)
    print("✅ Physical world objects created successfully")
    
except ImportError as e:
    print(f"❌ Physical world import failed: {e}")
except Exception as e:
    print(f"❌ Physical world creation failed: {e}")

# Test memory system import
try:
    from MarcusAGI.memory_system import MarcusMemorySystem, Concept
    print("✅ Memory system imports work")
except ImportError as e:
    print(f"⚠️  Memory system import failed (will use stubs): {e}")

print("\nReady to test daily_learning_loop.py!")