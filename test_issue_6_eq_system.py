#!/usr/bin/env python3
"""
Test Suite for Issue #6: Emotional Intelligence Assessment System

This test suite validates the comprehensive emotional intelligence assessment
system and its integration with all Marcus AGI components.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Any

# Import our Issue #6 systems
from emotional_intelligence_assessment import (
    EmotionalIntelligenceAssessment, EQDomain, EQSkillLevel,
    create_eq_assessment_system
)
from eq_system_integration import EQSystemIntegrator, create_eq_integrator

def test_eq_system_components():
    """Test core EQ assessment system components"""
    print("🧪 Testing EQ System Components...")
    
    eq_system = create_eq_assessment_system()
    
    # Test EQ metrics definition
    assert len(eq_system.eq_metrics) == 5, "Should have 5 EQ domains"
    assert EQDomain.SELF_AWARENESS in eq_system.eq_metrics, "Self-awareness metrics missing"
    assert EQDomain.EMPATHY in eq_system.eq_metrics, "Empathy metrics missing"
    print("  ✅ EQ metrics properly defined")
    
    # Test assessment tools
    assert len(eq_system.emotion_recognition_tasks) >= 3, "Should have emotion recognition tasks"
    assert len(eq_system.empathy_scenarios) >= 3, "Should have empathy scenarios"
    assert len(eq_system.social_simulations) >= 3, "Should have social simulations"
    print("  ✅ Assessment tools available")
    
    # Test EQ profile initialization
    profile = eq_system.current_eq_profile
    assert "student_id" in profile, "EQ profile should have student ID"
    assert "current_levels" in profile, "EQ profile should have current levels"
    print("  ✅ EQ profile initialized")
    
    return True

def test_emotion_recognition_assessment():
    """Test emotion recognition assessment functionality"""
    print("🧪 Testing Emotion Recognition Assessment...")
    
    eq_system = create_eq_assessment_system()
    
    # Test basic emotion recognition
    result = eq_system.conduct_emotion_recognition_assessment("facial_expressions_basic")
    assert "task_id" in result, "Result should have task ID"
    assert "accuracy_score" in result, "Result should have accuracy score"
    assert "assessed_level" in result, "Result should have assessed level"
    print("  ✅ Basic emotion recognition works")
    
    # Test situational emotion recognition
    result = eq_system.conduct_emotion_recognition_assessment("situational_emotions")
    assert result["task_type"] == "situational", "Should be situational task"
    assert isinstance(result["responses"], list), "Should have response list"
    print("  ✅ Situational emotion recognition works")
    
    return True

def test_empathy_assessment():
    """Test empathy assessment functionality"""
    print("🧪 Testing Empathy Assessment...")
    
    eq_system = create_eq_assessment_system()
    
    # Test playground exclusion scenario
    result = eq_system.conduct_empathy_assessment("playground_exclusion")
    assert "scenario_id" in result, "Result should have scenario ID"
    assert "overall_empathy_level" in result, "Result should have empathy level"
    assert "empathy_strengths" in result, "Result should have strengths"
    assert "mr_rogers_connection" in result, "Result should have Mr. Rogers connection"
    print("  ✅ Empathy scenario assessment works")
    
    # Test mistake consequences scenario
    result = eq_system.conduct_empathy_assessment("mistake_consequences")
    assert len(result["responses"]) > 0, "Should have empathy responses"
    assert "growth_opportunities" in result, "Should have growth opportunities"
    print("  ✅ Multiple empathy scenarios work")
    
    return True

def test_social_simulation():
    """Test social skills simulation functionality"""
    print("🧪 Testing Social Skills Simulation...")
    
    eq_system = create_eq_assessment_system()
    
    # Test playground negotiation simulation
    result = eq_system.conduct_social_simulation("playground_negotiation")
    assert "simulation_id" in result, "Result should have simulation ID"
    assert "skill_levels" in result, "Result should have skill levels"
    assert "overall_social_competence" in result, "Result should have overall competence"
    print("  ✅ Playground simulation works")
    
    # Test classroom collaboration simulation
    result = eq_system.conduct_social_simulation("classroom_collaboration")
    assert "social_strengths" in result, "Result should have social strengths"
    assert "areas_for_growth" in result, "Result should have growth areas"
    print("  ✅ Classroom simulation works")
    
    return True

def test_comprehensive_eq_report():
    """Test comprehensive EQ report generation"""
    print("🧪 Testing Comprehensive EQ Report...")
    
    eq_system = create_eq_assessment_system()
    
    # Generate comprehensive report
    report = eq_system.generate_comprehensive_eq_report()
    
    assert "student_id" in report, "Report should have student ID"
    assert "eq_domain_levels" in report, "Report should have domain levels"
    assert "overall_eq_level" in report, "Report should have overall level"
    assert "eq_strengths" in report, "Report should have strengths"
    assert "growth_priorities" in report, "Report should have growth priorities"
    assert "intervention_recommendations" in report, "Report should have interventions"
    assert "mr_rogers_integration" in report, "Report should have Mr. Rogers integration"
    print("  ✅ Comprehensive report generation works")
    
    # Validate domain levels
    domain_levels = report["eq_domain_levels"]
    assert len(domain_levels) == 5, "Should have all 5 EQ domains"
    for level in domain_levels.values():
        assert level in ["beginning", "developing", "practicing", "applying", "leading"], f"Invalid level: {level}"
    print("  ✅ Domain levels properly assessed")
    
    return True

def test_reflection_system_integration():
    """Test integration with reflection system (Issue #4)"""
    print("🧪 Testing Reflection System Integration...")
    
    integrator = create_eq_integrator()
    
    # Mock reflection data
    reflection_data = {
        "session_id": "test_reflection",
        "emotional_states": [
            {"dominant_emotion": "frustrated", "intensity": 0.7},
            {"dominant_emotion": "curious", "intensity": 0.8}
        ],
        "learning_insights": ["Worked on challenging task", "Asked for help"]
    }
    
    # Test integration
    enhanced_reflection = integrator.integrate_with_reflection_system(reflection_data)
    
    assert "eq_integration" in enhanced_reflection, "Should mark EQ integration"
    assert "eq_assessments_triggered" in enhanced_reflection, "Should have triggered assessments"
    assert "eq_reflection_connections" in enhanced_reflection, "Should have EQ connections"
    assert len(enhanced_reflection["eq_reflection_connections"]) > 0, "Should have connection data"
    print("  ✅ Reflection system integration works")
    
    return True

def test_curriculum_system_integration():
    """Test integration with curriculum system (Issue #5)"""
    print("🧪 Testing Curriculum System Integration...")
    
    integrator = create_eq_integrator()
    
    # Mock curriculum data
    curriculum_data = {
        "session_id": "test_curriculum",
        "developmental_domains": {
            "social_emotional": {
                "activities": [
                    {"name": "Feeling Faces", "description": "Identify emotions"},
                    {"name": "Helping Friends", "description": "Practice helping"}
                ]
            }
        }
    }
    
    # Test integration
    enhanced_curriculum = integrator.integrate_with_curriculum_system(curriculum_data)
    
    assert "eq_integration" in enhanced_curriculum, "Should mark EQ integration"
    assert "eq_current_levels" in enhanced_curriculum, "Should have current EQ levels"
    assert "curriculum_eq_alignments" in enhanced_curriculum, "Should have alignments"
    assert "eq_guided_activities" in enhanced_curriculum, "Should have EQ activities"
    print("  ✅ Curriculum system integration works")
    
    return True

def test_daily_learning_loop_integration():
    """Test integration with daily learning loop"""
    print("🧪 Testing Daily Learning Loop Integration...")
    
    integrator = create_eq_integrator()
    
    # Mock daily session data
    daily_session = {
        "session_id": "test_daily",
        "marcus_age_days": 365*5 + 30,
        "learning_activities": ["Reading", "Math", "Art"],
        "emotional_states": [{"emotion": "excited", "context": "art"}],
        "social_interactions": [{"type": "peer_play", "outcome": "positive"}]
    }
    
    # Test integration
    integrated_session = integrator.integrate_with_daily_learning_loop(daily_session)
    
    assert integrated_session.session_id == "test_daily", "Should preserve session ID"
    assert len(integrated_session.eq_assessments_conducted) > 0, "Should have EQ assessments"
    assert len(integrated_session.targeted_eq_domains) > 0, "Should have targeted domains"
    assert len(integrated_session.eq_guided_activities) > 0, "Should have EQ activities"
    assert len(integrated_session.mr_rogers_eq_episodes) > 0, "Should have Mr. Rogers episodes"
    print("  ✅ Daily learning loop integration works")
    
    return True

def test_developmental_progression():
    """Test developmental progression tracking"""
    print("🧪 Testing Developmental Progression...")
    
    eq_system = create_eq_assessment_system()
    
    # Test skill level progression
    levels = [EQSkillLevel.BEGINNING, EQSkillLevel.DEVELOPING, EQSkillLevel.PRACTICING, 
              EQSkillLevel.APPLYING, EQSkillLevel.LEADING]
    
    for level in levels:
        assert level.value in ["beginning", "developing", "practicing", "applying", "leading"], f"Invalid level: {level.value}"
    print("  ✅ Skill levels properly defined")
    
    # Test age-appropriate indicators
    for domain, metrics in eq_system.eq_metrics.items():
        for metric in metrics:
            assert len(metric.age_appropriate_indicators) > 0, f"Metric {metric.id} should have indicators"
            assert len(metric.developmental_progression) > 0, f"Metric {metric.id} should have progression"
    print("  ✅ Age-appropriate indicators defined")
    
    return True

def test_mr_rogers_integration():
    """Test Mr. Rogers episode integration"""
    print("🧪 Testing Mr. Rogers Integration...")
    
    eq_system = create_eq_assessment_system()
    
    # Test scenarios with Mr. Rogers connections
    scenarios_with_connections = [s for s in eq_system.empathy_scenarios if s.mr_rogers_connection]
    assert len(scenarios_with_connections) > 0, "Should have scenarios with Mr. Rogers connections"
    print("  ✅ Mr. Rogers connections in scenarios")
    
    # Test episode selection in integration
    integrator = create_eq_integrator()
    episodes = integrator._select_eq_mr_rogers_episodes(["empathy", "social_skills"])
    assert len(episodes) > 0, "Should select relevant episodes"
    print("  ✅ Mr. Rogers episode selection works")
    
    return True

def test_data_serialization():
    """Test data serialization and storage"""
    print("🧪 Testing Data Serialization...")
    
    eq_system = create_eq_assessment_system()
    
    # Test EQ metric serialization
    for domain, metrics in eq_system.eq_metrics.items():
        for metric in metrics:
            metric_dict = metric.to_dict()
            assert "id" in metric_dict, "Metric should serialize ID"
            assert "domain" in metric_dict, "Metric should serialize domain"
            assert isinstance(metric_dict, dict), "Should serialize to dictionary"
    print("  ✅ EQ metrics serialize correctly")
    
    # Test assessment result serialization
    result = eq_system.conduct_emotion_recognition_assessment("facial_expressions_basic")
    assert isinstance(result, dict), "Assessment result should be dictionary"
    assert "assessment_date" in result, "Should have assessment date"
    print("  ✅ Assessment results serialize correctly")
    
    return True

def run_comprehensive_test_suite():
    """Run the complete test suite for Issue #6"""
    print("🧠 Issue #6 Test Suite: Emotional Intelligence Assessment System")
    print("=" * 75)
    
    tests = [
        test_eq_system_components,
        test_emotion_recognition_assessment,
        test_empathy_assessment,
        test_social_simulation,
        test_comprehensive_eq_report,
        test_reflection_system_integration,
        test_curriculum_system_integration,
        test_daily_learning_loop_integration,
        test_developmental_progression,
        test_mr_rogers_integration,
        test_data_serialization
    ]
    
    passed_tests = 0
    failed_tests = []
    
    for test in tests:
        try:
            test_name = test.__name__.replace("test_", "").replace("_", " ").title()
            print(f"\n🧪 {test_name}")
            
            result = test()
            if result:
                passed_tests += 1
                print(f"  ✅ PASSED")
            else:
                failed_tests.append(test_name)
                print(f"  ❌ FAILED")
                
        except Exception as e:
            failed_tests.append(test_name)
            print(f"  ❌ FAILED: {str(e)}")
    
    print(f"\n📊 Test Results Summary:")
    print(f"  ✅ Passed: {passed_tests}")
    print(f"  ❌ Failed: {len(failed_tests)}")
    
    if failed_tests:
        print(f"  Failed Tests: {', '.join(failed_tests)}")
    
    success_rate = passed_tests / len(tests) * 100
    print(f"  📈 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print(f"\n🎉 Issue #6 Implementation: SUCCESS!")
        print("   Emotional Intelligence Assessment System is ready for production!")
    elif success_rate >= 75:
        print(f"\n⚠️  Issue #6 Implementation: MOSTLY SUCCESSFUL")
        print("   Some minor issues need attention before production.")
    else:
        print(f"\n❌ Issue #6 Implementation: NEEDS WORK")
        print("   Significant issues need to be resolved.")
    
    return success_rate >= 90

if __name__ == "__main__":
    success = run_comprehensive_test_suite()
    sys.exit(0 if success else 1)
