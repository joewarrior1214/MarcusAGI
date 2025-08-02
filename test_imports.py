#!/usr/bin/env python3
"""
Test script to verify that all import paths are working correctly 
after the directory reorganization.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, '/workspaces/MarcusAGI')

def test_import(module_path, item_name=""):
    """Test importing a module or specific item from a module."""
    try:
        if item_name:
            exec(f"from {module_path} import {item_name}")
            print(f"✅ Successfully imported {item_name} from {module_path}")
        else:
            exec(f"import {module_path}")
            print(f"✅ Successfully imported {module_path}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {item_name or module_path}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Error importing {item_name or module_path}: {e}")
        return False

def main():
    print("🔍 Testing Import Paths After Reorganization")
    print("=" * 60)
    
    # Test core memory imports
    print("\n📁 Testing Memory System Imports:")
    test_import("core.memory.memory_system", "MarcusMemorySystem")
    test_import("core.memory.memory_manager", "MemoryManager")
    test_import("core.memory.autobiographical_memory_system", "AutobiographicalMemorySystem")
    
    # Test core learning imports
    print("\n📚 Testing Learning System Imports:")
    test_import("core.learning.daily_learning_loop", "run_daily_learning_loop")
    test_import("core.learning.daily_learning_loop", "LEARNING_CONFIG")
    test_import("core.learning.curriculum_integration")
    test_import("core.learning.marcus_simple_body", "MarcusGridWorld")
    
    # Test core social imports
    print("\n👥 Testing Social System Imports:")
    test_import("core.social.emotional_intelligence_assessment", "EmotionalIntelligenceAssessment")
    test_import("core.social.peer_interaction_simulation")
    test_import("core.social.marcus_social_integration")
    
    # Test core reasoning imports
    print("\n🧠 Testing Reasoning System Imports:")
    test_import("core.reasoning.advanced_reasoning_engine", "AdvancedReasoningEngine")
    test_import("core.reasoning.reflection_system", "generate_reflection")
    test_import("core.reasoning.reflection_journal_system")
    
    # Test core consciousness imports
    print("\n🌟 Testing Consciousness System Imports:")
    test_import("core.consciousness.consciousness_integration_framework", "ConsciousnessIntegrationFramework")
    test_import("core.consciousness.personal_narrative_constructor", "PersonalNarrativeConstructor")
    test_import("core.consciousness.intrinsic_motivation_engine", "IntrinsicMotivationEngine")
    test_import("core.consciousness.value_learning_system", "ValueLearningSystem")
    
    print("\n" + "=" * 60)
    print("✨ Import testing completed!")

if __name__ == "__main__":
    main()
