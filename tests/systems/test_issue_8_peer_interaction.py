#!/usr/bin/env python3
"""
Test Suite for Issue #8: Peer Interaction Simulation System

This test suite validates all components of the Peer Interaction Simulation System:
1. Virtual peer personality models with distinct characteristics
2. Conversation simulation engines with natural dialogue
3. Conflict resolution scenarios with guided practice
4. Collaborative learning activities across subjects
5. Social dynamics modeling with relationship tracking

Tests ensure proper integration with existing Marcus systems.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime, date
from unittest.mock import Mock, patch

# Import the system under test
from peer_interaction_simulation import (
    PeerInteractionSimulator, PeerPersonalityType, InteractionContext,
    ConversationTopic, SocialSkillArea, PeerPersonality, ConversationTurn,
    PeerInteractionSession, CollaborativeLearningActivity,
    ConversationEngine, SocialDynamicsModel,
    create_peer_interaction_system
)

class TestPeerInteractionSimulation(unittest.TestCase):
    """Test cases for Peer Interaction Simulation System"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create test system
        self.peer_system = PeerInteractionSimulator(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_system_initialization(self):
        """Test system initializes correctly"""
        print("🧪 Testing System Initialization...")
        
        self.assertIsInstance(self.peer_system, PeerInteractionSimulator)
        self.assertIsNotNone(self.peer_system.peers)
        self.assertIsNotNone(self.peer_system.collaborative_activities)
        self.assertIsNotNone(self.peer_system.conversation_engine)
        self.assertIsNotNone(self.peer_system.social_dynamics_model)
        
        # Test database tables were created
        import sqlite3
        with sqlite3.connect(self.peer_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'peer_interaction_sessions', 
                'peer_relationships', 
                'social_skills_progress'
            ]
            for table in expected_tables:
                self.assertIn(table, tables, f"Missing table: {table}")
        
        # Test peer personalities were created
        self.assertGreater(len(self.peer_system.peers), 0)
        
        # Test collaborative activities were created
        self.assertGreater(len(self.peer_system.collaborative_activities), 0)
        
        print("  ✅ System initialization successful")
    
    def test_peer_personality_creation(self):
        """Test peer personalities are properly created"""
        print("🧪 Testing Peer Personality Creation...")
        
        # Test that we have diverse personality types
        personality_types = set()
        for peer in self.peer_system.peers.values():
            personality_types.add(peer.personality_type)
        
        self.assertGreaterEqual(len(personality_types), 3, "Should have diverse personality types")
        
        # Test specific peer characteristics
        for peer_id, peer in self.peer_system.peers.items():
            self.assertIsInstance(peer, PeerPersonality)
            self.assertEqual(peer.id, peer_id)
            self.assertIsNotNone(peer.name)
            self.assertIn(peer.personality_type, list(PeerPersonalityType))
            self.assertGreater(peer.age_months, 60)  # Kindergarten age
            self.assertLess(peer.age_months, 72)
            self.assertIsInstance(peer.communication_style, dict)
            self.assertIsInstance(peer.interests, list)
            self.assertGreater(len(peer.interests), 0)
            self.assertIsInstance(peer.typical_responses, dict)
            
        print(f"  ✅ Created {len(self.peer_system.peers)} diverse peer personalities")
    
    def test_collaborative_activities_creation(self):
        """Test collaborative activities are properly created"""
        print("🧪 Testing Collaborative Activities Creation...")
        
        # Test that we have activities for different subjects
        subjects = set()
        for activity in self.peer_system.collaborative_activities.values():
            subjects.add(activity.subject_area)
        
        self.assertGreaterEqual(len(subjects), 2, "Should have activities for multiple subjects")
        
        # Test specific activity characteristics
        for activity_id, activity in self.peer_system.collaborative_activities.items():
            self.assertIsInstance(activity, CollaborativeLearningActivity)
            self.assertEqual(activity.activity_id, activity_id)
            self.assertIsNotNone(activity.name)
            self.assertIn(activity.grade_level, ["kindergarten", "first_grade"])
            self.assertGreater(activity.duration_minutes, 0)
            self.assertGreater(len(activity.learning_objectives), 0)
            self.assertGreater(len(activity.roles), 0)
            self.assertGreater(len(activity.social_skills_focus), 0)
            self.assertIsInstance(activity.assessment_rubric, dict)
            
        print(f"  ✅ Created {len(self.peer_system.collaborative_activities)} collaborative activities")
    
    def test_peer_interaction_simulation(self):
        """Test peer interaction simulation"""
        print("🧪 Testing Peer Interaction Simulation...")
        
        # Get available peer IDs
        available_peers = list(self.peer_system.peers.keys())[:2]
        
        # Simulate interaction
        session = self.peer_system.simulate_peer_interaction(
            peers_to_include=available_peers,
            context=InteractionContext.CLASSROOM,
            topic=ConversationTopic.ACADEMIC_HELP,
            duration_minutes=10
        )
        
        # Validate session structure
        self.assertIsInstance(session, PeerInteractionSession)
        self.assertIsNotNone(session.session_id)
        self.assertEqual(session.marcus_id, "marcus")
        self.assertEqual(len(session.peers_involved), len(available_peers))
        self.assertEqual(session.context, InteractionContext.CLASSROOM)
        self.assertEqual(session.topic, ConversationTopic.ACADEMIC_HELP)
        self.assertEqual(session.duration_minutes, 10)
        
        # Validate conversation turns
        self.assertGreater(len(session.conversation_turns), 0)
        self.assertIsInstance(session.conversation_turns[0], ConversationTurn)
        
        # Check for Marcus's participation
        marcus_turns = [turn for turn in session.conversation_turns if turn.speaker == "marcus"]
        self.assertGreater(len(marcus_turns), 0, "Marcus should participate in conversation")
        
        # Validate social skills tracking
        self.assertIsInstance(session.social_skills_practiced, list)
        self.assertGreater(len(session.social_skills_practiced), 0)
        
        # Validate success metrics
        self.assertGreaterEqual(session.overall_success_rating, 0.0)
        self.assertLessEqual(session.overall_success_rating, 1.0)
        self.assertGreaterEqual(session.conflicts_resolved, 0)
        self.assertGreaterEqual(session.collaboration_successes, 0)
        
        # Validate feedback
        self.assertIsInstance(session.peer_feedback, dict)
        self.assertEqual(len(session.peer_feedback), len(available_peers))
        
        print(f"  ✅ Simulated interaction with {len(available_peers)} peers")
        print(f"    💬 Conversation turns: {len(session.conversation_turns)}")
        print(f"    🎯 Skills practiced: {len(session.social_skills_practiced)}")
        print(f"    ⭐ Success rating: {session.overall_success_rating:.1%}")
    
    def test_collaborative_activity_execution(self):
        """Test collaborative activity execution"""
        print("🧪 Testing Collaborative Activity Execution...")
        
        # Get available activity and peers
        activity_id = list(self.peer_system.collaborative_activities.keys())[0]
        activity = self.peer_system.collaborative_activities[activity_id]
        participants = ["marcus"] + list(self.peer_system.peers.keys())[:activity.max_participants-1]
        
        # Conduct activity
        result = self.peer_system.conduct_collaborative_activity(
            activity_id=activity_id,
            participants=participants
        )
        
        # Validate result structure
        self.assertIsInstance(result, dict)
        self.assertIn("activity_id", result)
        self.assertIn("activity_name", result)
        self.assertIn("participants", result)
        self.assertIn("role_assignments", result)
        self.assertIn("learning_objectives_met", result)
        self.assertIn("social_skills_demonstrated", result)
        self.assertIn("success_rating", result)
        self.assertIn("recommendations", result)
        
        # Validate content
        self.assertEqual(result["activity_id"], activity_id)
        self.assertEqual(len(result["participants"]), len(participants))
        self.assertIn("marcus", result["role_assignments"])
        self.assertIsInstance(result["learning_objectives_met"], list)
        self.assertIsInstance(result["social_skills_demonstrated"], list)
        self.assertGreaterEqual(result["success_rating"], 0.0)
        self.assertLessEqual(result["success_rating"], 1.0)
        self.assertIsInstance(result["recommendations"], list)
        
        print(f"  ✅ Conducted activity: {result['activity_name']}")
        print(f"    👥 Participants: {len(result['participants'])}")
        print(f"    🎯 Objectives met: {len(result['learning_objectives_met'])}")
        print(f"    ⭐ Success rating: {result['success_rating']:.1%}")
    
    def test_conversation_engine(self):
        """Test conversation generation engine"""
        print("🧪 Testing Conversation Engine...")
        
        engine = ConversationEngine()
        peers = list(self.peer_system.peers.values())[:2]
        
        # Generate conversation
        conversation = engine.generate_conversation(
            peers=peers,
            context=InteractionContext.PLAYGROUND,
            topic=ConversationTopic.SHARING_INTERESTS,
            duration_minutes=5
        )
        
        # Validate conversation structure
        self.assertIsInstance(conversation, list)
        self.assertGreater(len(conversation), 0)
        
        # Check conversation turns
        for turn in conversation:
            self.assertIsInstance(turn, ConversationTurn)
            self.assertIsNotNone(turn.speaker)
            self.assertIsNotNone(turn.message)
            self.assertIsNotNone(turn.emotion)
            self.assertIsInstance(turn.social_skills_demonstrated, list)
            self.assertGreaterEqual(turn.response_quality, 0.0)
            self.assertLessEqual(turn.response_quality, 1.0)
        
        # Check for Marcus participation
        marcus_turns = [turn for turn in conversation if turn.speaker == "marcus"]
        self.assertGreater(len(marcus_turns), 0, "Marcus should participate")
        
        print(f"  ✅ Generated conversation with {len(conversation)} turns")
        print(f"    👤 Marcus turns: {len(marcus_turns)}")
    
    def test_social_dynamics_model(self):
        """Test social dynamics modeling"""
        print("🧪 Testing Social Dynamics Model...")
        
        model = SocialDynamicsModel()
        
        # Create test profiles
        marcus_profile = {
            "personality_type": "developing_learner",
            "interests": ["books", "building", "art"]
        }
        
        peer_profiles = [
            {
                "personality_type": "confident_leader",
                "interests": ["organizing", "books", "helping"]
            },
            {
                "personality_type": "shy_thoughtful", 
                "interests": ["reading", "art", "quiet games"]
            }
        ]
        
        # Test interaction success prediction
        success_prediction = model.predict_interaction_success(
            marcus_profile=marcus_profile,
            peer_profiles=peer_profiles,
            context=InteractionContext.LIBRARY
        )
        
        self.assertIsInstance(success_prediction, float)
        self.assertGreaterEqual(success_prediction, 0.0)
        self.assertLessEqual(success_prediction, 1.0)
        
        print(f"  ✅ Social dynamics prediction: {success_prediction:.1%}")
    
    def test_peer_relationship_tracking(self):
        """Test peer relationship tracking"""
        print("🧪 Testing Peer Relationship Tracking...")
        
        # Simulate some interactions to create relationship data
        peer_id = list(self.peer_system.peers.keys())[0]
        
        session = self.peer_system.simulate_peer_interaction(
            peers_to_include=[peer_id],
            context=InteractionContext.PLAYGROUND,
            topic=ConversationTopic.FRIENDSHIP_BUILDING,
            duration_minutes=5
        )
        
        # Get relationship status
        relationship = self.peer_system.get_peer_relationship_status(peer_id)
        
        # Validate relationship data
        self.assertIsInstance(relationship, dict)
        self.assertIn("peer_id", relationship)
        self.assertIn("relationship_strength", relationship)
        self.assertIn("interaction_count", relationship)
        self.assertIn("status", relationship)
        
        self.assertEqual(relationship["peer_id"], peer_id)
        self.assertGreaterEqual(relationship["relationship_strength"], 0.0)
        self.assertLessEqual(relationship["relationship_strength"], 1.0)
        self.assertGreater(relationship["interaction_count"], 0)
        
        print(f"  ✅ Relationship tracking for peer: {peer_id}")
        print(f"    💪 Strength: {relationship['relationship_strength']:.1%}")
        print(f"    🔢 Interactions: {relationship['interaction_count']}")
        print(f"    📊 Status: {relationship['status']}")
    
    def test_social_skills_progress_tracking(self):
        """Test social skills progress tracking"""
        print("🧪 Testing Social Skills Progress Tracking...")
        
        # Simulate interaction to generate progress data
        peer_ids = list(self.peer_system.peers.keys())[:2]
        
        session = self.peer_system.simulate_peer_interaction(
            peers_to_include=peer_ids,
            context=InteractionContext.CLASSROOM,
            topic=ConversationTopic.SOLVING_PROBLEMS,
            duration_minutes=8
        )
        
        # Get progress data
        progress = self.peer_system.get_social_skills_progress()
        
        # Validate progress structure
        self.assertIsInstance(progress, dict)
        self.assertIn("individual_skills", progress)
        self.assertIn("overall_social_level", progress)
        self.assertIn("development_stage", progress)
        self.assertIn("next_focus_areas", progress)
        
        # Validate metrics
        self.assertGreaterEqual(progress["overall_social_level"], 0.0)
        self.assertLessEqual(progress["overall_social_level"], 1.0)
        self.assertIsInstance(progress["development_stage"], str)
        self.assertIsInstance(progress["next_focus_areas"], list)
        
        print(f"  ✅ Social skills progress tracked")
        print(f"    📈 Overall level: {progress['overall_social_level']:.1%}")
        print(f"    🎯 Development stage: {progress['development_stage']}")
        print(f"    📚 Focus areas: {len(progress['next_focus_areas'])}")
    
    def test_interaction_recommendations(self):
        """Test interaction recommendations generation"""
        print("🧪 Testing Interaction Recommendations...")
        
        # Generate some interaction history first
        peer_ids = list(self.peer_system.peers.keys())[:2]
        
        for i in range(2):
            session = self.peer_system.simulate_peer_interaction(
                peers_to_include=[peer_ids[i % len(peer_ids)]],
                context=InteractionContext.PLAYGROUND,
                topic=ConversationTopic.FRIENDSHIP_BUILDING,
                duration_minutes=5
            )
        
        # Get recommendations
        recommendations = self.peer_system.generate_interaction_recommendations()
        
        # Validate recommendations structure
        self.assertIsInstance(recommendations, dict)
        self.assertIn("focus_skills", recommendations)
        self.assertIn("recommended_peers", recommendations)
        self.assertIn("recommended_activities", recommendations)
        self.assertIn("recommended_contexts", recommendations)
        self.assertIn("priority_interactions", recommendations)
        
        # Validate content
        self.assertIsInstance(recommendations["focus_skills"], list)
        self.assertIsInstance(recommendations["recommended_peers"], dict)
        self.assertIsInstance(recommendations["recommended_activities"], list)
        self.assertIsInstance(recommendations["recommended_contexts"], list)
        self.assertIsInstance(recommendations["priority_interactions"], list)
        
        print(f"  ✅ Generated interaction recommendations")
        print(f"    🎯 Focus skills: {len(recommendations['focus_skills'])}")
        print(f"    👥 Recommended peers: {len(recommendations['recommended_peers'])}")
        print(f"    🎪 Priority interactions: {len(recommendations['priority_interactions'])}")
    
    def test_database_operations(self):
        """Test database storage and retrieval"""
        print("🧪 Testing Database Operations...")
        
        # Simulate interaction to generate database records
        peer_id = list(self.peer_system.peers.keys())[0]
        
        session = self.peer_system.simulate_peer_interaction(
            peers_to_include=[peer_id],
            context=InteractionContext.LIBRARY,
            topic=ConversationTopic.SHARING_INTERESTS,
            duration_minutes=7
        )
        
        # Verify data was stored
        import sqlite3
        with sqlite3.connect(self.peer_system.db_path) as conn:
            cursor = conn.cursor()
            
            # Check interaction sessions table
            cursor.execute("SELECT COUNT(*) FROM peer_interaction_sessions")
            session_count = cursor.fetchone()[0]
            self.assertGreater(session_count, 0, "Interaction sessions should be stored")
            
            # Check peer relationships table
            cursor.execute("SELECT COUNT(*) FROM peer_relationships")
            relationship_count = cursor.fetchone()[0]
            self.assertGreater(relationship_count, 0, "Peer relationships should be tracked")
            
            # Check social skills progress table
            cursor.execute("SELECT COUNT(*) FROM social_skills_progress")
            skills_count = cursor.fetchone()[0]
            self.assertGreater(skills_count, 0, "Social skills progress should be tracked")
        
        print("  ✅ Database operations working correctly")
        print(f"    📊 Sessions stored: {session_count}")
        print(f"    👥 Relationships tracked: {relationship_count}") 
        print(f"    🎯 Skills tracked: {skills_count}")
    
    def test_factory_function(self):
        """Test factory function"""
        print("🧪 Testing Factory Function...")
        
        system = create_peer_interaction_system()
        self.assertIsInstance(system, PeerInteractionSimulator)
        
        print("  ✅ Factory function working correctly")
    
    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        print("🧪 Testing Error Handling...")
        
        # Test invalid peer IDs
        with self.assertRaises(ValueError):
            self.peer_system.simulate_peer_interaction(
                peers_to_include=["nonexistent_peer"],
                context=InteractionContext.PLAYGROUND,
                topic=ConversationTopic.SHARING_INTERESTS
            )
        
        # Test invalid activity ID
        with self.assertRaises(ValueError):
            self.peer_system.conduct_collaborative_activity(
                activity_id="nonexistent_activity",
                participants=["marcus", "emma"]
            )
        
        # Test invalid participant count
        activity_id = list(self.peer_system.collaborative_activities.keys())[0]
        activity = self.peer_system.collaborative_activities[activity_id]
        
        with self.assertRaises(ValueError):
            self.peer_system.conduct_collaborative_activity(
                activity_id=activity_id,
                participants=["marcus"]  # Too few participants
            )
        
        print("  ✅ Error handling working correctly")

def run_comprehensive_tests():
    """Run all tests for the Peer Interaction Simulation System"""
    print("🤝 Running Comprehensive Peer Interaction System Tests")
    print("=" * 65)
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPeerInteractionSimulation)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w'))
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n📊 Test Results Summary:")
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
        print(f"\n✅ All tests passed successfully!")
        return True
    else:
        print(f"\n❌ Some tests failed.")
        return False

def test_integration_with_existing_systems():
    """Test integration with existing Marcus systems"""
    print("\n🔗 Testing Integration with Existing Systems")
    print("=" * 50)
    
    try:
        # Test integration with EQ system
        from emotional_intelligence_assessment import EmotionalIntelligenceAssessment
        eq_system = EmotionalIntelligenceAssessment()
        print("  ✅ EQ system integration available")
        
        # Test integration with grade progression system
        try:
            from grade_progression_system import GradeProgressionSystem
            grade_system = GradeProgressionSystem()
            print("  ✅ Grade progression system integration available")
        except ImportError:
            print("  ⚠️  Grade progression system not available (optional)")
        
        # Test integration with curriculum system
        from kindergarten_curriculum_expansion import KindergartenCurriculumExpansion
        curriculum = KindergartenCurriculumExpansion()
        print("  ✅ Curriculum system integration available")
        
        # Test creating complete system
        peer_system = create_peer_interaction_system()
        print("  ✅ Peer interaction system creation successful")
        
        # Test basic functionality with integration
        available_peers = list(peer_system.peers.keys())[:2]
        session = peer_system.simulate_peer_interaction(
            peers_to_include=available_peers,
            context=InteractionContext.CLASSROOM,
            topic=ConversationTopic.ACADEMIC_HELP,
            duration_minutes=5
        )
        print(f"  ✅ Basic interaction simulation successful")
        print(f"    Success rating: {session.overall_success_rating:.1%}")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"  ❌ Integration test failed: {e}")
        print(f"  📝 Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    # Run comprehensive tests
    tests_passed = run_comprehensive_tests()
    
    # Run integration tests
    integration_passed = test_integration_with_existing_systems()
    
    # Final summary
    print(f"\n🎯 Final Test Summary")
    print("=" * 30)
    if tests_passed and integration_passed:
        print("✅ All tests passed! Peer Interaction System is ready for use.")
        exit(0)
    else:
        print("❌ Some tests failed. Please review and fix issues.")
        exit(1)
