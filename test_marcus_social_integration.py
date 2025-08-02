#!/usr/bin/env python3
"""
Test Suite for Marcus AGI Social Learning Integration System

This test suite validates the integration of the Peer Interaction System with:
1. Daily Learning Loop integration
2. EQ System coaching integration  
3. Grade Progression social readiness assessment
4. Kindergarten deployment readiness

Tests ensure all systems work together seamlessly for Marcus's development.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime, date
from unittest.mock import Mock, patch, MagicMock

# Import the system under test
from marcus_social_integration import (
    MarcusSocialLearningIntegration, SocialLearningPhase, SocialReadinessLevel,
    IntegratedLearningSession, create_marcus_social_integration
)

class TestMarcusSocialIntegration(unittest.TestCase):
    """Test cases for Marcus Social Learning Integration System"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create test integration system
        self.integration = MarcusSocialLearningIntegration(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_integration_system_initialization(self):
        """Test integration system initializes correctly"""
        print("🧪 Testing Integration System Initialization...")
        
        self.assertIsInstance(self.integration, MarcusSocialLearningIntegration)
        self.assertIsNotNone(self.integration.peer_system)
        self.assertIsNotNone(self.integration.social_learning_config)
        
        # Check configuration values
        config = self.integration.social_learning_config
        self.assertGreater(config["daily_social_minutes"], 0)
        self.assertGreater(config["peer_interactions_per_day"], 0)
        self.assertGreater(config["social_readiness_threshold"], 0)
        
        print("  ✅ Integration system initialization successful")
    
    def test_morning_warmup_interaction(self):
        """Test morning social warmup functionality"""
        print("🧪 Testing Morning Warmup Interaction...")
        
        morning_interaction = self.integration._conduct_morning_warmup()
        
        # Validate morning interaction structure
        self.assertIsInstance(morning_interaction, dict)
        self.assertEqual(morning_interaction["type"], "morning_warmup")
        self.assertIn("peer", morning_interaction)
        self.assertIn("session", morning_interaction)
        self.assertIn("success_rating", morning_interaction)
        self.assertIn("skills_practiced", morning_interaction)
        
        # Validate success metrics
        self.assertGreaterEqual(morning_interaction["success_rating"], 0.0)
        self.assertLessEqual(morning_interaction["success_rating"], 1.0)
        self.assertIsInstance(morning_interaction["skills_practiced"], list)
        
        print(f"  ✅ Morning warmup with peer: {morning_interaction['peer']}")
        print(f"    Success rating: {morning_interaction['success_rating']:.1%}")
    
    def test_social_practice_session(self):
        """Test dedicated social practice functionality"""
        print("🧪 Testing Social Practice Session...")
        
        social_practice = self.integration._conduct_social_practice_session()
        
        # Validate social practice structure
        self.assertIsInstance(social_practice, dict)
        self.assertEqual(social_practice["type"], "social_practice")
        self.assertIn("focus_skills", social_practice)
        self.assertIn("peers", social_practice)
        self.assertIn("session", social_practice)
        self.assertIn("success_rating", social_practice)
        
        # Validate practice session content
        self.assertIsInstance(social_practice["focus_skills"], list)
        self.assertIsInstance(social_practice["peers"], list)
        self.assertGreater(len(social_practice["peers"]), 0)
        
        print(f"  ✅ Social practice with {len(social_practice['peers'])} peers")
        print(f"    Focus skills: {len(social_practice['focus_skills'])}")
        print(f"    Success rating: {social_practice['success_rating']:.1%}")
    
    def test_collaborative_activity_selection(self):
        """Test collaborative activity selection based on academic content"""
        print("🧪 Testing Collaborative Activity Selection...")
        
        # Test with math subjects
        math_subjects = ["counting to 10", "number recognition"]
        math_activity = self.integration._select_collaborative_activity(math_subjects)
        
        self.assertIsInstance(math_activity, dict)
        self.assertIn("activity_id", math_activity)
        self.assertIn("participants", math_activity)
        self.assertIn("reason", math_activity)
        self.assertIn("marcus", math_activity["participants"])
        
        # Test with reading subjects
        reading_subjects = ["letter sounds", "phonics"]
        reading_activity = self.integration._select_collaborative_activity(reading_subjects)
        
        self.assertIsInstance(reading_activity, dict)
        self.assertIn("activity_id", reading_activity)
        
        print(f"  ✅ Math activity selected: {math_activity['activity_id']}")
        print(f"  ✅ Reading activity selected: {reading_activity['activity_id']}")
    
    def test_eq_coaching_integration(self):
        """Test EQ coaching integration"""
        print("🧪 Testing EQ Coaching Integration...")
        
        # Create mock interactions with varying success rates
        morning_interaction = {
            "success_rating": 0.6,
            "skills_practiced": ["cooperation"]
        }
        
        social_practice = {
            "success_rating": 0.5,
            "conflicts_resolved": 1
        }
        
        eq_coaching = self.integration._integrate_eq_coaching(morning_interaction, social_practice)
        
        # Validate EQ coaching suggestions
        self.assertIsInstance(eq_coaching, list)
        
        if eq_coaching:  # May be empty if EQ system not available
            for coaching_moment in eq_coaching:
                self.assertIn("moment", coaching_moment)
                self.assertIn("domain", coaching_moment)
                self.assertIn("coaching_focus", coaching_moment)
                self.assertIn("suggested_activity", coaching_moment)
        
        print(f"  ✅ EQ coaching moments generated: {len(eq_coaching)}")
    
    def test_social_readiness_assessment(self):
        """Test social readiness assessment"""
        print("🧪 Testing Social Readiness Assessment...")
        
        readiness = self.integration._assess_social_readiness()
        
        # Validate readiness assessment structure
        self.assertIsInstance(readiness, dict)
        self.assertIn("overall_level", readiness)
        self.assertIn("readiness_level", readiness)
        self.assertIn("strengths", readiness)
        self.assertIn("growth_areas", readiness)
        self.assertIn("grade_advancement_ready", readiness)
        
        # Validate readiness values
        self.assertGreaterEqual(readiness["overall_level"], 0.0)
        self.assertLessEqual(readiness["overall_level"], 1.0)
        self.assertIn(readiness["readiness_level"], [level.value for level in SocialReadinessLevel])
        self.assertIsInstance(readiness["grade_advancement_ready"], bool)
        
        print(f"  ✅ Social readiness assessed")
        print(f"    Overall level: {readiness['overall_level']:.1%}")
        print(f"    Readiness level: {readiness['readiness_level']}")
        print(f"    Grade advancement ready: {readiness['grade_advancement_ready']}")
    
    def test_integration_metrics_calculation(self):
        """Test integration metrics calculation"""
        print("🧪 Testing Integration Metrics Calculation...")
        
        # Create mock interaction data
        morning_interaction = {"success_rating": 0.8}
        academic_session = {
            "collaborative_activities": [
                {"success_rating": 0.7},
                {"success_rating": 0.9}
            ]
        }
        social_practice = {
            "success_rating": 0.85,
            "conflicts_resolved": 1,
            "session": {"duration_minutes": 10}
        }
        eq_coaching = [{"moment": "test1"}, {"moment": "test2"}]
        
        metrics = self.integration._calculate_integration_metrics(
            morning_interaction, academic_session, social_practice, eq_coaching
        )
        
        # Validate metrics structure
        self.assertIsInstance(metrics, dict)
        self.assertIn("social_engagement", metrics)
        self.assertIn("academic_collaboration", metrics)
        self.assertIn("eq_coaching_integration", metrics)
        self.assertIn("overall_integration_success", metrics)
        
        # Validate metric values
        for key, value in metrics.items():
            if isinstance(value, float):
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)
        
        print(f"  ✅ Integration metrics calculated")
        print(f"    Overall integration success: {metrics['overall_integration_success']:.1%}")
    
    def test_grade_readiness_assessment(self):
        """Test grade advancement readiness assessment"""
        print("🧪 Testing Grade Advancement Readiness...")
        
        grade_readiness = self.integration.get_social_readiness_for_grade_advancement()
        
        # Validate grade readiness structure
        self.assertIsInstance(grade_readiness, dict)
        
        if "error" not in grade_readiness:  # If grade system is available
            self.assertIn("overall_social_level", grade_readiness)
            self.assertIn("grade_advancement_ready", grade_readiness)
            self.assertIn("criteria_met", grade_readiness)
            self.assertIn("peer_relationship_summary", grade_readiness)
            
            # Validate criteria
            criteria = grade_readiness["criteria_met"]
            self.assertIn("social_level", criteria)
            self.assertIn("required_skills", criteria)
            self.assertIn("peer_relationships", criteria)
        
        print(f"  ✅ Grade readiness assessment completed")
        if "overall_social_level" in grade_readiness:
            print(f"    Social level: {grade_readiness['overall_social_level']:.1%}")
            print(f"    Grade ready: {grade_readiness['grade_advancement_ready']}")
    
    def test_integrated_daily_session(self):
        """Test complete integrated daily learning session"""
        print("🧪 Testing Integrated Daily Learning Session...")
        
        session = self.integration.run_integrated_daily_session()
        
        # Validate integrated session structure
        self.assertIsInstance(session, IntegratedLearningSession)
        self.assertIsNotNone(session.session_id)
        self.assertIsInstance(session.date, datetime)
        self.assertIsInstance(session.academic_focus, list)
        self.assertIsInstance(session.social_focus, list)
        self.assertIsInstance(session.peer_interactions, list)
        self.assertIsInstance(session.recommendations, list)
        
        # Validate session content
        self.assertGreater(len(session.peer_interactions), 0)
        self.assertIsInstance(session.integration_success_metrics, dict)
        self.assertIn("overall_integration_success", session.integration_success_metrics)
        
        print(f"  ✅ Integrated session completed: {session.session_id}")
        print(f"    Academic focus areas: {len(session.academic_focus)}")
        print(f"    Social skills practiced: {len(session.social_focus)}")
        print(f"    Peer interactions: {len(session.peer_interactions)}")
        print(f"    Recommendations: {len(session.recommendations)}")
    
    def test_kindergarten_deployment_report(self):
        """Test kindergarten deployment readiness report"""
        print("🧪 Testing Kindergarten Deployment Report...")
        
        deployment_report = self.integration.generate_kindergarten_deployment_report()
        
        # Validate deployment report structure
        self.assertIsInstance(deployment_report, dict)
        self.assertIn("deployment_date", deployment_report)
        self.assertIn("marcus_social_profile", deployment_report)
        self.assertIn("peer_relationship_status", deployment_report)
        self.assertIn("deployment_readiness", deployment_report)
        self.assertIn("overall_deployment_ready", deployment_report)
        
        # Validate social profile
        social_profile = deployment_report["marcus_social_profile"]
        self.assertIn("overall_social_level", social_profile)
        self.assertIn("development_stage", social_profile)
        self.assertIsInstance(social_profile["strongest_skills"], list)
        self.assertIsInstance(social_profile["growth_areas"], list)
        
        # Validate deployment readiness
        readiness = deployment_report["deployment_readiness"]
        self.assertIsInstance(readiness["social_skills_ready"], bool)
        self.assertIsInstance(readiness["peer_interaction_ready"], bool)
        self.assertIsInstance(readiness["collaboration_ready"], bool)
        
        # Validate recommendations
        self.assertIn("recommended_classroom_activities", deployment_report)
        self.assertIn("teacher_guidance", deployment_report)
        self.assertIn("parent_communication_highlights", deployment_report)
        
        print(f"  ✅ Deployment report generated")
        print(f"    Overall deployment ready: {deployment_report['overall_deployment_ready']}")
        print(f"    Social level: {social_profile['overall_social_level']:.1%}")
        print(f"    Classroom activities: {len(deployment_report['recommended_classroom_activities'])}")
    
    def test_session_storage(self):
        """Test integrated session storage"""
        print("🧪 Testing Session Storage...")
        
        # Run a session to generate data
        session = self.integration.run_integrated_daily_session()
        
        # Check if session file was created
        expected_file = f"output/integrated_sessions/{session.session_id}.json"
        self.assertTrue(os.path.exists(expected_file), f"Session file should be created: {expected_file}")
        
        # Validate stored data
        with open(expected_file, 'r') as f:
            stored_data = json.load(f)
        
        self.assertIn("session_id", stored_data)
        self.assertIn("integration_success_metrics", stored_data)
        self.assertEqual(stored_data["session_id"], session.session_id)
        
        print(f"  ✅ Session storage working correctly")
        print(f"    File created: {expected_file}")
    
    def test_factory_function(self):
        """Test factory function"""
        print("🧪 Testing Factory Function...")
        
        integration = create_marcus_social_integration()
        self.assertIsInstance(integration, MarcusSocialLearningIntegration)
        
        print("  ✅ Factory function working correctly")
    
    def test_recommendations_generation(self):
        """Test personalized recommendations generation"""
        print("🧪 Testing Recommendations Generation...")
        
        # Mock integration metrics and social readiness
        integration_metrics = {
            "social_engagement": 0.6,
            "academic_collaboration": 0.5,
            "eq_coaching_integration": 0.3
        }
        
        social_readiness = {
            "readiness_level": "developing",
            "growth_areas": ["leadership", "empathy"]
        }
        
        recommendations = self.integration._generate_daily_recommendations(
            integration_metrics, social_readiness
        )
        
        # Validate recommendations
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        for recommendation in recommendations:
            self.assertIsInstance(recommendation, str)
            self.assertGreater(len(recommendation), 10)  # Substantial recommendations
        
        print(f"  ✅ Recommendations generated: {len(recommendations)}")
        for i, rec in enumerate(recommendations[:2], 1):
            print(f"    {i}. {rec[:60]}...")

def run_integration_tests():
    """Run all integration tests"""
    print("🔗 Running Marcus Social Learning Integration Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMarcusSocialIntegration)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w'))
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n📊 Integration Test Results:")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, failure in result.failures:
            print(f"  {test}: {failure}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, error in result.errors:
            print(f"  {test}: {error}")
    
    if result.wasSuccessful():
        print(f"\n✅ All integration tests passed!")
        return True
    else:
        print(f"\n❌ Some integration tests failed.")
        return False

if __name__ == "__main__":
    try:
        # Run integration tests
        tests_passed = run_integration_tests()
        
        if tests_passed:
            print("\n🎉 Integration system validated and ready for deployment!")
        else:
            print("\n⚠️  Integration system needs fixes before deployment.")
        
    except Exception as e:
        import traceback
        print(f"\n❌ Integration testing failed: {e}")
        print(f"📝 Traceback: {traceback.format_exc()}")
