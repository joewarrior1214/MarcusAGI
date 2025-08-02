#!/usr/bin/env python3
"""
Test Suite for Marcus AGI Embodied Social Learning Integration System

This test suite validates the integration of Marcus's virtual simple body world
with social learning capabilities for comprehensive multi-sensory development.
"""

import unittest
import sys
import os
import json
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the MarcusAGI directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the system under test
from marcus_embodied_social_integration import (
    MarcusEmbodiedSocialIntegration,
    EmbodiedSocialWorld,
    SensoryLearningExperience,
    EmbodiedSocialSkill,
    SensoryModalType,
    PhysicalSocialContext
)


class TestEmbodiedSocialWorld(unittest.TestCase):
    """Test the embodied social world functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.world = EmbodiedSocialWorld(size=10)
    
    def test_world_initialization(self):
        """Test that the embodied social world initializes correctly"""
        self.assertEqual(self.world.size, 10)
        self.assertIsNotNone(self.world.base_world)
        self.assertIn("Alice", self.world.peer_positions)
        self.assertIn("playground_ball", self.world.social_objects)
        self.assertIn("circle_time", self.world.interaction_zones)
    
    def test_social_look_functionality(self):
        """Test enhanced looking with social awareness"""
        result = self.world.social_look()
        
        # Check that result contains both base vision and social elements
        self.assertIn('visible_objects', result)
        self.assertIn('social_observations', result)
        self.assertIn('social_objects', result)
        self.assertIn('interaction_zones', result)
        
        # Social observations should contain peer information
        if result['social_observations']:
            for obs in result['social_observations']:
                self.assertIn('peer', obs)
                self.assertIn('distance', obs)
                self.assertIn('activity', obs)
                self.assertIn('body_language', obs)
    
    def test_social_movement_awareness(self):
        """Test movement with social proximity detection"""
        # Move Marcus and check for social encounters
        result = self.world.move_marcus_with_social_awareness('north')
        
        # Should contain basic movement result
        self.assertIn('success', result)
        
        # May contain social encounters if peers are nearby
        if 'social_encounters' in result:
            for encounter in result['social_encounters']:
                self.assertIn('peer', encounter)
                self.assertIn('distance', encounter)
                self.assertIn('social_signal', encounter)
    
    def test_social_interaction_initiation(self):
        """Test initiating social interactions with peers"""
        # Try to interact with Alice
        result = self.world.initiate_social_interaction("Alice", "greeting")
        
        # Should return interaction result
        self.assertIn('success', result)
        
        if result['success']:
            self.assertIn('peer', result)
            self.assertIn('interaction_type', result)
            self.assertIn('success_rate', result)
            self.assertIn('peer_response', result)
            self.assertEqual(result['peer'], "Alice")
            self.assertEqual(result['interaction_type'], "greeting")
    
    def test_peer_proximity_detection(self):
        """Test peer proximity detection system"""
        encounters = self.world._check_social_proximity()
        
        # Should return list of encounters
        self.assertIsInstance(encounters, list)
        
        for encounter in encounters:
            self.assertIn('peer', encounter)
            self.assertIn('distance', encounter)
            self.assertIn('interaction_possible', encounter)
            self.assertIn('social_signal', encounter)


class TestEmbodiedSocialSkill(unittest.TestCase):
    """Test embodied social skill development"""
    
    def setUp(self):
        """Set up test skill"""
        self.skill = EmbodiedSocialSkill(
            name="Test Skill",
            description="A test embodied social skill",
            physical_components=["movement", "touch"],
            social_components=["communication", "cooperation"],
            sensory_requirements=[SensoryModalType.VISUAL, SensoryModalType.SOCIAL],
            practice_contexts=[PhysicalSocialContext.FREE_PLAY]
        )
    
    def test_skill_initialization(self):
        """Test skill initialization"""
        self.assertEqual(self.skill.name, "Test Skill")
        self.assertEqual(self.skill.mastery_level, 0.0)
        self.assertEqual(self.skill.practice_sessions, 0)
    
    def test_skill_practice_improvement(self):
        """Test that skill improves with successful practice"""
        initial_mastery = self.skill.mastery_level
        initial_sessions = self.skill.practice_sessions
        
        # Practice with high success rate
        self.skill.practice(0.9)
        
        self.assertGreater(self.skill.mastery_level, initial_mastery)
        self.assertEqual(self.skill.practice_sessions, initial_sessions + 1)
    
    def test_skill_mastery_bounds(self):
        """Test that mastery level stays within bounds [0, 1]"""
        # Practice many times with perfect success
        for _ in range(20):
            self.skill.practice(1.0)
        
        self.assertLessEqual(self.skill.mastery_level, 1.0)
        self.assertGreaterEqual(self.skill.mastery_level, 0.0)


class TestSensoryLearningExperience(unittest.TestCase):
    """Test sensory learning experience data structure"""
    
    def setUp(self):
        """Set up test experience"""
        self.experience = SensoryLearningExperience(
            session_id="test_session_1",
            timestamp=datetime.now(),
            sensory_modalities=[SensoryModalType.VISUAL, SensoryModalType.SOCIAL],
            physical_context=PhysicalSocialContext.FREE_PLAY,
            social_participants=["Alice", "Bob"],
            marcus_position=(5, 5),
            objects_interacted=["ball"],
            movements_made=["north", "east"],
            touch_experiences=[{"object": "ball", "texture": "smooth"}],
            visual_observations=[{"objects": 2, "peers": 2}],
            social_exchanges=[{"type": "greeting", "peer": "Alice", "success_rate": 0.8}],
            peer_proximities={"Alice": 2.0, "Bob": 4.0},
            collaborative_actions=["shared_ball"],
            physical_skills_practiced=["movement", "touch"],
            social_skills_practiced=["greeting"],
            concepts_discovered=["cooperation is fun"],
            emotional_responses=["happy"],
            sensory_integration_score=0.75,
            social_physical_coherence=0.85,
            learning_engagement_level=0.70
        )
    
    def test_experience_initialization(self):
        """Test experience initialization"""
        self.assertEqual(self.experience.session_id, "test_session_1")
        self.assertEqual(len(self.experience.social_participants), 2)
        self.assertIn(SensoryModalType.VISUAL, self.experience.sensory_modalities)
    
    def test_experience_to_dict(self):
        """Test experience serialization to dictionary"""
        result = self.experience.to_dict()
        
        self.assertIn('session_id', result)
        self.assertIn('timestamp', result)
        self.assertIn('sensory_modalities', result)
        self.assertIn('physical_context', result)
        self.assertIn('social_participants', result)
        
        # Check that enums are converted to values
        self.assertEqual(result['physical_context'], 'free_play')
        self.assertIn('visual', result['sensory_modalities'])


class TestMarcusEmbodiedSocialIntegration(unittest.TestCase):
    """Test the main embodied social integration system"""
    
    def setUp(self):
        """Set up test integration system"""
        self.integration = MarcusEmbodiedSocialIntegration(world_size=8)
    
    def test_integration_initialization(self):
        """Test integration system initialization"""
        self.assertIsNotNone(self.integration.embodied_world)
        self.assertIsNotNone(self.integration.peer_simulator)
        self.assertIsNotNone(self.integration.embodied_social_skills)
        
        # Check that embodied social skills are initialized
        self.assertIn("personal_space_awareness", self.integration.embodied_social_skills)
        self.assertIn("collaborative_movement", self.integration.embodied_social_skills)
        self.assertIn("touch_social_communication", self.integration.embodied_social_skills)
        self.assertIn("visual_social_tracking", self.integration.embodied_social_skills)
        self.assertIn("shared_object_play", self.integration.embodied_social_skills)
    
    def test_embodied_social_session_creation(self):
        """Test running a complete embodied social learning session"""
        # Run a short session
        experience = self.integration.run_embodied_social_session(
            duration_minutes=10,
            context=PhysicalSocialContext.FREE_PLAY
        )
        
        # Verify experience was created
        self.assertIsInstance(experience, SensoryLearningExperience)
        self.assertEqual(experience.physical_context, PhysicalSocialContext.FREE_PLAY)
        self.assertIsInstance(experience.sensory_modalities, list)
        self.assertIsInstance(experience.social_participants, list)
        
        # Check that experience was stored
        self.assertEqual(len(self.integration.sensory_experiences), 1)
        self.assertEqual(self.integration.sensory_experiences[0], experience)
    
    def test_progress_report_generation(self):
        """Test progress report generation"""
        # Run a session first to generate data
        self.integration.run_embodied_social_session(
            duration_minutes=5,
            context=PhysicalSocialContext.CLASSROOM_CIRCLE
        )
        
        # Generate progress report
        report = self.integration.get_embodied_social_progress_report()
        
        # Verify report structure
        self.assertIn('total_sessions', report)
        self.assertIn('overall_metrics', report)
        self.assertIn('skill_development', report)
        self.assertIn('sensory_modality_usage', report)
        self.assertIn('social_interaction_metrics', report)
        self.assertIn('learning_diversity', report)
        self.assertIn('development_trends', report)
        self.assertIn('embodied_social_readiness', report)
        self.assertIn('recommendations', report)
        
        # Check overall metrics
        metrics = report['overall_metrics']
        self.assertIn('sensory_integration_score', metrics)
        self.assertIn('social_physical_coherence', metrics)
        self.assertIn('learning_engagement_level', metrics)
        self.assertIn('social_interaction_success_rate', metrics)
        
        # Check readiness assessment
        readiness = report['embodied_social_readiness']
        self.assertIn('readiness_level', readiness)
        self.assertIn('readiness_score', readiness)
        self.assertIn('component_scores', readiness)
    
    def test_skill_readiness_assessment(self):
        """Test skill readiness assessment"""
        skill = self.integration.embodied_social_skills["personal_space_awareness"]
        
        # Test different readiness levels
        skill.mastery_level = 0.9
        readiness = self.integration._assess_skill_readiness(skill)
        self.assertEqual(readiness, "Advanced")
        
        skill.mastery_level = 0.7
        readiness = self.integration._assess_skill_readiness(skill)
        self.assertEqual(readiness, "Proficient")
        
        skill.mastery_level = 0.5
        readiness = self.integration._assess_skill_readiness(skill)
        self.assertEqual(readiness, "Developing")
        
        skill.mastery_level = 0.3
        readiness = self.integration._assess_skill_readiness(skill)
        self.assertEqual(readiness, "Beginning")
        
        skill.mastery_level = 0.1
        readiness = self.integration._assess_skill_readiness(skill)
        self.assertEqual(readiness, "Emerging")
    
    def test_learning_recommendations_generation(self):
        """Test learning recommendations generation"""
        # Run a session to generate data
        self.integration.run_embodied_social_session(
            duration_minutes=5,
            context=PhysicalSocialContext.FREE_PLAY
        )
        
        recommendations = self.integration._generate_learning_recommendations()
        
        # Should return a list of recommendations
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        
        # Each recommendation should be a string
        for rec in recommendations:
            self.assertIsInstance(rec, str)
            self.assertGreater(len(rec), 0)
    
    def test_embodied_social_readiness_calculation(self):
        """Test overall embodied social readiness calculation"""
        # Run multiple sessions to generate data
        for context in [PhysicalSocialContext.FREE_PLAY, PhysicalSocialContext.PLAYGROUND]:
            self.integration.run_embodied_social_session(
                duration_minutes=5,
                context=context
            )
        
        readiness = self.integration._calculate_embodied_social_readiness()
        
        # Check readiness structure
        self.assertIn('readiness_level', readiness)
        self.assertIn('readiness_score', readiness)
        self.assertIn('component_scores', readiness)
        
        # Check score bounds
        self.assertGreaterEqual(readiness['readiness_score'], 0.0)
        self.assertLessEqual(readiness['readiness_score'], 1.0)
        
        # Check component scores
        components = readiness['component_scores']
        for component in ['sensory_integration', 'social_physical_coherence', 'skill_mastery', 'learning_engagement']:
            self.assertIn(component, components)
            self.assertGreaterEqual(components[component], 0.0)
            self.assertLessEqual(components[component], 1.0)
    
    def test_data_persistence(self):
        """Test saving and loading of embodied social learning data"""
        # Run a session to generate data
        self.integration.run_embodied_social_session(
            duration_minutes=5,
            context=PhysicalSocialContext.SHARED_WORKSPACE
        )
        
        # Save data to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        try:
            self.integration.save_embodied_social_data(temp_filename)
            
            # Verify file was created and contains valid JSON
            self.assertTrue(os.path.exists(temp_filename))
            
            with open(temp_filename, 'r') as f:
                data = json.load(f)
            
            # Check data structure
            self.assertIn('system_info', data)
            self.assertIn('embodied_social_skills', data)
            self.assertIn('learning_experiences', data)
            self.assertIn('progress_report', data)
            
            # Check that experiences are properly serialized
            self.assertEqual(len(data['learning_experiences']), 1)
            experience_data = data['learning_experiences'][0]
            self.assertIn('session_id', experience_data)
            self.assertIn('sensory_modalities', experience_data)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_multiple_context_learning(self):
        """Test learning across multiple physical contexts"""
        contexts = [
            PhysicalSocialContext.FREE_PLAY,
            PhysicalSocialContext.CLASSROOM_CIRCLE,
            PhysicalSocialContext.PLAYGROUND
        ]
        
        # Run sessions in different contexts
        for context in contexts:
            self.integration.run_embodied_social_session(
                duration_minutes=5,
                context=context
            )
        
        # Check that all contexts were used
        used_contexts = [exp.physical_context for exp in self.integration.sensory_experiences]
        self.assertEqual(len(set(used_contexts)), len(contexts))
        
        # Generate report and check context diversity
        report = self.integration.get_embodied_social_progress_report()
        diversity = report['learning_diversity']
        self.assertEqual(diversity['physical_contexts_explored'], len(contexts))
        self.assertGreater(diversity['context_diversity_score'], 0.4)  # Should be relatively high


class TestSensoryModalTypes(unittest.TestCase):
    """Test sensory modal type enumeration"""
    
    def test_sensory_modal_types(self):
        """Test that all required sensory modalities are defined"""
        expected_modalities = [
            'VISUAL', 'TACTILE', 'SPATIAL', 'SOCIAL', 'KINESTHETIC', 'MULTI_MODAL'
        ]
        
        for modality in expected_modalities:
            self.assertTrue(hasattr(SensoryModalType, modality))
    
    def test_sensory_modal_values(self):
        """Test sensory modality enum values"""
        self.assertEqual(SensoryModalType.VISUAL.value, "visual")
        self.assertEqual(SensoryModalType.TACTILE.value, "tactile")
        self.assertEqual(SensoryModalType.SOCIAL.value, "social")


class TestPhysicalSocialContexts(unittest.TestCase):
    """Test physical social context enumeration"""
    
    def test_physical_social_contexts(self):
        """Test that all required contexts are defined"""
        expected_contexts = [
            'PLAYGROUND', 'CLASSROOM_CIRCLE', 'SHARED_WORKSPACE', 
            'OUTDOOR_EXPLORATION', 'GROUP_ACTIVITY', 'FREE_PLAY'
        ]
        
        for context in expected_contexts:
            self.assertTrue(hasattr(PhysicalSocialContext, context))
    
    def test_context_values(self):
        """Test context enum values"""
        self.assertEqual(PhysicalSocialContext.PLAYGROUND.value, "playground")
        self.assertEqual(PhysicalSocialContext.FREE_PLAY.value, "free_play")
        self.assertEqual(PhysicalSocialContext.CLASSROOM_CIRCLE.value, "classroom_circle")


def run_all_tests():
    """Run all embodied social integration tests"""
    print("🧪 Running Marcus AGI Embodied Social Integration Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestEmbodiedSocialWorld,
        TestEmbodiedSocialSkill,
        TestSensoryLearningExperience,
        TestMarcusEmbodiedSocialIntegration,
        TestSensoryModalTypes,
        TestPhysicalSocialContexts
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"🎯 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n🚫 ERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error.split('Exception:')[-1].strip()}")
    
    if not result.failures and not result.errors:
        print(f"\n✅ All tests passed! Embodied Social Integration System is fully validated.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
