#!/usr/bin/env python3
"""
Demo script to showcase Issue #4 completion: Enhanced Reflection & Learning Journal System

This script demonstrates the new reflection and emotional tracking capabilities
that complete Issue #4's requirements for metacognitive awareness.
"""

import json
from reflection_journal_system import create_enhanced_reflection_system, enhance_session_with_journal

def demo_enhanced_reflection():
    """Demonstrate the enhanced reflection system capabilities"""
    
    print("🌟 Issue #4 Completion Demo: Enhanced Reflection & Learning Journal")
    print("=" * 70)
    
    # Create the enhanced reflection system
    journal_system = create_enhanced_reflection_system()
    
    # Simulate a diverse learning session with various scenarios
    sample_sessions = [
        {
            "date": "2025-08-02",
            "physical_exploration": True,
            "key_insights": ["Objects have weight", "Gravity affects movement", "Some materials are harder than others"],
            "reasoning_results": [
                {"problem_id": "physics_1", "success": True, "reasoning_type": "causal", "confidence": 0.85},
                {"problem_id": "logic_1", "success": False, "reasoning_type": "analogical", "confidence": 0.45}
            ],
            "reasoning_insights": {
                "success_rate": 0.5,
                "total_causal_relations": 8,
                "reasoning_type_distribution": {"causal": 1, "analogical": 1}
            },
            "concepts_learned": ["Advanced physics concepts", "Material properties"],
            "scenario": "Mixed success with some struggles"
        },
        {
            "date": "2025-08-02",
            "physical_exploration": True,
            "key_insights": ["Patterns repeat in nature", "Colors can indicate properties", "Shapes affect function"],
            "reasoning_results": [
                {"problem_id": "pattern_1", "success": True, "reasoning_type": "pattern_recognition", "confidence": 0.92},
                {"problem_id": "pattern_2", "success": True, "reasoning_type": "pattern_recognition", "confidence": 0.88},
                {"problem_id": "analogy_1", "success": True, "reasoning_type": "analogical", "confidence": 0.78}
            ],
            "reasoning_insights": {
                "success_rate": 1.0,
                "total_causal_relations": 12,
                "reasoning_type_distribution": {"pattern_recognition": 2, "analogical": 1}
            },
            "concepts_learned": ["Pattern recognition", "Visual analysis", "Mathematical relationships"],
            "scenario": "High success with pattern recognition"
        },
        {
            "date": "2025-08-02", 
            "physical_exploration": False,
            "key_insights": ["Abstract thinking is challenging", "Need more practice with symbols"],
            "reasoning_results": [
                {"problem_id": "abstract_1", "success": False, "reasoning_type": "goal_decomposition", "confidence": 0.3},
                {"problem_id": "abstract_2", "success": False, "reasoning_type": "causal", "confidence": 0.2}
            ],
            "reasoning_insights": {
                "success_rate": 0.0,
                "total_causal_relations": 5,
                "reasoning_type_distribution": {"goal_decomposition": 1, "causal": 1}
            },
            "concepts_learned": ["Abstract symbols", "Logical operations"],
            "scenario": "Challenging abstract concepts"
        }
    ]
    
    print("\n🎭 Demonstrating Emotional State Detection Across Different Scenarios:")
    print("-" * 70)
    
    for i, session in enumerate(sample_sessions, 1):
        print(f"\n📚 Scenario {i}: {session['scenario']}")
        
        # Process session through enhanced reflection system
        enhanced_session = enhance_session_with_journal(session, journal_system)
        
        # Extract and display key reflection features
        journal_entry = enhanced_session['learning_journal']
        emotion_summary = enhanced_session['emotional_state_summary']
        
        print(f"  🎯 Success Rate: {session['reasoning_insights']['success_rate']:.0%}")
        print(f"  😊 Primary Emotion: {emotion_summary['current_primary_emotion']}")
        print(f"  📊 Intensity: {emotion_summary['current_intensity']:.1f}/1.0")
        print(f"  🎪 Triggers: {', '.join(journal_entry['emotional_journey'][0]['triggers'])}")
        print(f"  📝 Narrative: {journal_entry['narrative_reflection'][:120]}...")
        
        # Show metacognitive insights
        insights = journal_entry['metacognitive_insights']
        if insights:
            print(f"  🧠 Meta-insight: {insights[0]}")
        
        # Show future interests
        interests = journal_entry['future_learning_interests']
        if interests:
            print(f"  🚀 Next interest: {interests[0]}")
    
    # Demonstrate journal summary capabilities
    print(f"\n📊 Learning Journal Summary After {len(sample_sessions)} Sessions:")
    print("-" * 70)
    
    journal_summary = journal_system.get_journal_summary()
    
    print(f"  📈 Total Journal Entries: {journal_summary['total_entries']}")
    print(f"  😊 Emotion Distribution: {journal_summary['emotional_summary']['emotion_distribution']}")
    print(f"  📊 Confidence Trend: {[f'{c:.2f}' for c in journal_summary['confidence_trend']]}")
    print(f"  🎯 Assessment Trend: {[f'{a:.2f}' for a in journal_summary['self_assessment_trend']]}")
    
    if 'learning_progress_indicators' in journal_summary:
        progress = journal_summary['learning_progress_indicators']
        if 'overall_trend' in progress:
            print(f"  📈 Overall Trend: {progress['overall_trend']}")
    
    # Show common challenges
    if 'common_challenges' in journal_summary:
        challenges = journal_summary['common_challenges']
        if challenges:
            print(f"  ⚠️  Common Challenge: {challenges[0]}")
    
    print(f"\n🎉 Issue #4 Feature Showcase Complete!")
    print("✅ All reflection and self-assessment requirements implemented:")
    print("   • Narrative reflection generation with emotional context")
    print("   • 10 different emotional states with intensity tracking")
    print("   • Metacognitive insights about learning process")
    print("   • Self-assessment scoring with confidence levels") 
    print("   • Learning journal with structured entries")
    print("   • Progress tracking and trend analysis")
    print("   • Challenge identification and future interest generation")

if __name__ == "__main__":
    demo_enhanced_reflection()
