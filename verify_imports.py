#!/usr/bin/env python3
"""
Comprehensive import verification before committing changes.
"""
import sys
import traceback

# Add the project root to Python path
sys.path.insert(0, '/workspaces/MarcusAGI')

def test_import(module_path, item_name="", description=""):
    """Test importing a module or specific item from a module."""
    try:
        if item_name:
            exec(f"from {module_path} import {item_name}")
            print(f"✅ {description or f'{item_name} from {module_path}'}")
        else:
            exec(f"import {module_path}")
            print(f"✅ {description or module_path}")
        return True
    except ImportError as e:
        print(f"❌ IMPORT ERROR - {description or f'{item_name or module_path}'}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  ERROR - {description or f'{item_name or module_path}'}: {e}")
        return False

def main():
    print("🔍 COMPREHENSIVE IMPORT VERIFICATION")
    print("=" * 70)
    
    failed_imports = []
    total_tests = 0
    
    # Test all core memory imports
    print("\n📁 MEMORY SYSTEM IMPORTS:")
    tests = [
        ("core.memory.memory_system", "MarcusMemorySystem", "Memory System Core"),
        ("core.memory.memory_manager", "MemoryManager", "Memory Manager"),
        ("core.memory.memory_utils", "", "Memory Utils"),
        ("core.memory.autobiographical_memory_system", "AutobiographicalMemorySystem", "Autobiographical Memory"),
    ]
    
    for module, item, desc in tests:
        total_tests += 1
        if not test_import(module, item, desc):
            failed_imports.append(f"{desc} ({module}.{item})")
    
    # Test all core learning imports
    print("\n📚 LEARNING SYSTEM IMPORTS:")
    tests = [
        ("core.learning.daily_learning_loop", "run_daily_learning_loop", "Daily Learning Loop"),
        ("core.learning.daily_learning_loop", "LEARNING_CONFIG", "Learning Config"),
        ("core.learning.curriculum_integration", "", "Curriculum Integration"),
        ("core.learning.kindergarten_curriculum_expansion", "", "Kindergarten Curriculum"),
        ("core.learning.marcus_simple_body", "MarcusGridWorld", "Marcus Simple Body"),
        ("core.learning.concept_graph_system", "", "Concept Graph System"),
        ("core.learning.grade_progression_system", "", "Grade Progression System"),
        ("core.learning.grade_progression_integration", "", "Grade Progression Integration"),
        ("core.learning.marcus_curriculum_system", "", "Marcus Curriculum System"),
    ]
    
    for module, item, desc in tests:
        total_tests += 1
        if not test_import(module, item, desc):
            failed_imports.append(f"{desc} ({module}.{item})")
    
    # Test all core social imports
    print("\n👥 SOCIAL SYSTEM IMPORTS:")
    tests = [
        ("core.social.emotional_intelligence_assessment", "EmotionalIntelligenceAssessment", "EQ Assessment"),
        ("core.social.peer_interaction_simulation", "", "Peer Interaction"),
        ("core.social.marcus_social_integration", "", "Marcus Social Integration"),
        ("core.social.marcus_embodied_social_integration", "", "Embodied Social Integration"),
        ("core.social.eq_system_integration", "", "EQ System Integration"),
        ("core.social.peer_personality_refinement", "", "Peer Personality Refinement"),
        ("core.social.daily_sel_integration", "", "Daily SEL Integration"),
        ("core.social.sel_curriculum_expansion", "", "SEL Curriculum"),
        ("core.social.sel_strategic_implementation", "", "SEL Strategic Implementation"),
    ]
    
    for module, item, desc in tests:
        total_tests += 1
        if not test_import(module, item, desc):
            failed_imports.append(f"{desc} ({module}.{item})")
    
    # Test all core reasoning imports
    print("\n🧠 REASONING SYSTEM IMPORTS:")
    tests = [
        ("core.reasoning.advanced_reasoning_engine", "AdvancedReasoningEngine", "Advanced Reasoning"),
        ("core.reasoning.reflection_system", "generate_reflection", "Reflection System"),
        ("core.reasoning.reflection_engine", "", "Reflection Engine"),
        ("core.reasoning.reflection_journal_system", "", "Reflection Journal"),
        ("core.reasoning.enhanced_reflection_system", "", "Enhanced Reflection"),
    ]
    
    for module, item, desc in tests:
        total_tests += 1
        if not test_import(module, item, desc):
            failed_imports.append(f"{desc} ({module}.{item})")
    
    # Test all core consciousness imports
    print("\n🌟 CONSCIOUSNESS SYSTEM IMPORTS:")
    tests = [
        ("core.consciousness.consciousness_integration_framework", "ConsciousnessIntegrationFramework", "Consciousness Framework"),
        ("core.consciousness.personal_narrative_constructor", "PersonalNarrativeConstructor", "Personal Narrative"),
        ("core.consciousness.intrinsic_motivation_engine", "IntrinsicMotivationEngine", "Intrinsic Motivation"),
        ("core.consciousness.value_learning_system", "ValueLearningSystem", "Value Learning"),
    ]
    
    for module, item, desc in tests:
        total_tests += 1
        if not test_import(module, item, desc):
            failed_imports.append(f"{desc} ({module}.{item})")
    
    # Test key script imports
    print("\n🔧 SCRIPT SYSTEM IMPORTS:")
    tests = [
        ("scripts.utilities.run_multiple_sessions", "", "Run Multiple Sessions"),
        ("scripts.utilities.simulate_multiple_days", "", "Simulate Multiple Days"),
        ("scripts.utilities.quick_test_learning_loop", "", "Quick Test Learning Loop"),
    ]
    
    for module, item, desc in tests:
        total_tests += 1
        if not test_import(module, item, desc):
            failed_imports.append(f"{desc} ({module}.{item})")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"📊 IMPORT VERIFICATION SUMMARY:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Successful: {total_tests - len(failed_imports)}")
    print(f"   Failed: {len(failed_imports)}")
    
    if failed_imports:
        print(f"\n❌ FAILED IMPORTS:")
        for failed in failed_imports:
            print(f"   - {failed}")
        print(f"\n⚠️  COMMIT BLOCKED - Fix import issues first!")
        return False
    else:
        print(f"\n✅ ALL IMPORTS SUCCESSFUL!")
        print(f"🎉 Ready to commit changes!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
