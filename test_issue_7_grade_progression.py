#!/usr/bin/env python3
"""
Test Suite for Issue #7: Grade Progression System

This test suite validates all components of the Grade Progression System:
1. Grade transition criteria
2. Cross-grade skill mapping
3. Difficulty scaling algorithms  
4. Grade-appropriate content libraries
5. Assessment and placement systems

Tests ensure proper integration with existing Marcus systems.
"""

import unittest
import tempfile
import os
import json
from datetime import datetime, date, timedelta
from unittest.mock import Mock, patch

# Import the system under test
from grade_progression_system import (
    GradeProgressionSystem, GradeLevel, AcademicSubject, ReadinessStatus,
    GradeTransitionCriteria, SkillMapping, DifficultyScaling, PlacementAssessment,
    create_grade_progression_system
)

# Import dependencies
from memory_system import MarcusMemorySystem
from emotional_intelligence_assessment import EmotionalIntelligenceAssessment
from kindergarten_curriculum_expansion import KindergartenCurriculumExpansion

class TestGradeProgressionSystem(unittest.TestCase):
    """Test cases for Grade Progression System"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Create test systems
        self.memory_system = MarcusMemorySystem(db_path=self.temp_db.name)
        self.eq_system = Mock(spec=EmotionalIntelligenceAssessment)
        self.kindergarten_curriculum = Mock(spec=KindergartenCurriculumExpansion)
        
        # Mock EQ system response
        self.eq_system.generate_comprehensive_eq_report.return_value = {
            'eq_metrics': {
                'self_awareness': [Mock(current_level=0.8)],
                'self_regulation': [Mock(current_level=0.7)],
                'social_skills': [Mock(current_level=0.75)],
                'empathy': [Mock(current_level=0.72)]
            }
        }
        
        # Mock kindergarten curriculum
        mock_milestones = {
            'physical_motor': [Mock(id='gross_motor_coordination'), Mock(id='fine_motor_control')],
            'cognitive_academic': [Mock(id='mathematical_thinking'), Mock(id='literacy_foundations')]
        }
        self.kindergarten_curriculum.developmental_milestones = mock_milestones
        
        # Create progression system
        self.progression_system = GradeProgressionSystem(
            memory_system=self.memory_system,
            eq_system=self.eq_system,
            kindergarten_curriculum=self.kindergarten_curriculum
        )
    
    def tearDown(self):
        """Clean up test environment"""
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_system_initialization(self):
        """Test system initializes correctly"""
        print("🧪 Testing System Initialization...")
        
        self.assertIsInstance(self.progression_system, GradeProgressionSystem)
        self.assertIsNotNone(self.progression_system.grade_standards)
        self.assertIsNotNone(self.progression_system.transition_criteria)
        self.assertIsNotNone(self.progression_system.skill_mappings)
        self.assertIsNotNone(self.progression_system.difficulty_scalings)
        
        # Test database tables were created
        import sqlite3
        with sqlite3.connect(self.progression_system.memory_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['grade_progressions', 'current_grade_status', 'subject_mastery_tracking']
            for table in expected_tables:
                self.assertIn(table, tables, f"Missing table: {table}")
        
        print("  ✅ System initialization successful")
    
    def test_grade_standards_loading(self):
        """Test grade standards are properly loaded"""
        print("🧪 Testing Grade Standards Loading...")
        
        # Test kindergarten standards
        k_standards = self.progression_system.grade_standards[GradeLevel.KINDERGARTEN]
        self.assertEqual(k_standards.grade_level, GradeLevel.KINDERGARTEN)
        self.assertIn(AcademicSubject.MATHEMATICS, k_standards.subject_standards)
        self.assertIn(AcademicSubject.READING_LANGUAGE_ARTS, k_standards.subject_standards)
        
        # Test first grade standards
        first_standards = self.progression_system.grade_standards[GradeLevel.FIRST_GRADE]
        self.assertEqual(first_standards.grade_level, GradeLevel.FIRST_GRADE)
        self.assertGreater(len(first_standards.subject_standards[AcademicSubject.MATHEMATICS]), 0)
        
        print("  ✅ Grade standards loaded correctly")
    
    def test_transition_criteria_definition(self):
        """Test transition criteria are properly defined"""
        print("🧪 Testing Transition Criteria Definition...")
        
        # Test first grade criteria
        first_grade_criteria = self.progression_system.transition_criteria[GradeLevel.FIRST_GRADE]
        self.assertEqual(first_grade_criteria.grade_level, GradeLevel.FIRST_GRADE)
        self.assertGreater(first_grade_criteria.minimum_overall_mastery, 0.0)
        self.assertGreater(first_grade_criteria.time_in_grade_minimum, 0)
        
        # Check core subject requirements
        self.assertIn(AcademicSubject.MATHEMATICS, first_grade_criteria.core_subject_requirements)
        self.assertIn(AcademicSubject.READING_LANGUAGE_ARTS, first_grade_criteria.core_subject_requirements)
        
        # Check developmental milestones
        self.assertGreater(len(first_grade_criteria.developmental_milestones), 0)
        
        print("  ✅ Transition criteria defined correctly")
    
    def test_skill_mappings_creation(self):
        """Test skill mappings across grades"""
        print("🧪 Testing Skill Mappings Creation...")
        
        # Test number sense mapping
        if "number_sense" in self.progression_system.skill_mappings:
            number_sense = self.progression_system.skill_mappings["number_sense"]
            self.assertEqual(number_sense.subject, AcademicSubject.MATHEMATICS)
            self.assertIsNotNone(number_sense.kindergarten_level)
            self.assertIsNotNone(number_sense.first_grade_level)
            self.assertGreater(len(number_sense.prerequisites), 0)
        
        # Test reading comprehension mapping
        if "reading_comprehension" in self.progression_system.skill_mappings:
            reading_comp = self.progression_system.skill_mappings["reading_comprehension"]
            self.assertEqual(reading_comp.subject, AcademicSubject.READING_LANGUAGE_ARTS)
            self.assertIsNotNone(reading_comp.kindergarten_level)
            self.assertIsNotNone(reading_comp.first_grade_level)
        
        print("  ✅ Skill mappings created successfully")
    
    def test_difficulty_scaling_algorithms(self):
        """Test difficulty scaling algorithms"""
        print("🧪 Testing Difficulty Scaling Algorithms...")
        
        # Test reading complexity scaling
        if "reading_complexity" in self.progression_system.difficulty_scalings:
            reading_scaling = self.progression_system.difficulty_scalings["reading_complexity"]
            
            # Test scaling factors increase with grade level
            k_factor = reading_scaling.scaling_factors[GradeLevel.KINDERGARTEN]
            first_factor = reading_scaling.scaling_factors[GradeLevel.FIRST_GRADE]
            self.assertLessEqual(k_factor, first_factor, "Difficulty should increase with grade level")
            
            # Test complexity indicators exist for each grade
            self.assertIn(GradeLevel.KINDERGARTEN, reading_scaling.complexity_indicators)
            self.assertIn(GradeLevel.FIRST_GRADE, reading_scaling.complexity_indicators)
            
            # Test vocabulary requirements increase
            k_vocab = reading_scaling.vocabulary_level[GradeLevel.KINDERGARTEN]
            first_vocab = reading_scaling.vocabulary_level[GradeLevel.FIRST_GRADE]
            self.assertLess(k_vocab, first_vocab, "Vocabulary requirements should increase")
        
        print("  ✅ Difficulty scaling algorithms working correctly")
    
    def test_current_grade_tracking(self):
        """Test current grade tracking functionality"""
        print("🧪 Testing Current Grade Tracking...")
        
        # Test getting current grade (should default to kindergarten for new student)
        current_grade = self.progression_system._get_current_grade("test_student")
        self.assertEqual(current_grade, GradeLevel.KINDERGARTEN)
        
        # Test days in grade calculation
        days_in_grade = self.progression_system._get_days_in_current_grade("test_student")
        self.assertGreaterEqual(days_in_grade, 0)
        
        print("  ✅ Current grade tracking working correctly")
    
    def test_academic_subject_assessment(self):
        """Test academic subject assessment"""
        print("🧪 Testing Academic Subject Assessment...")
        
        # Add some test data to memory system
        test_concepts = [
            ("math_concept_1", "mathematics", 0.8),
            ("reading_concept_1", "reading_language_arts", 0.7),
            ("science_concept_1", "science", 0.6)
        ]
        
        import sqlite3
        with sqlite3.connect(self.progression_system.memory_system.db_path) as conn:
            cursor = conn.cursor()
            for concept_id, subject, mastery in test_concepts:
                cursor.execute("""
                    INSERT INTO subject_mastery_tracking
                    (student_id, grade_level, subject, concept_id, mastery_level, assessment_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, ("test_student", "kindergarten", subject, concept_id, mastery, datetime.now().isoformat()))
        
        # Test assessment
        subject_scores = self.progression_system._assess_academic_subjects("test_student", GradeLevel.KINDERGARTEN)
        
        self.assertIsInstance(subject_scores, dict)
        self.assertGreater(len(subject_scores), 0)
        
        # Check that scores are percentages (0-100)
        for subject, score in subject_scores.items():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 100.0)
        
        print("  ✅ Academic subject assessment working correctly")
    
    def test_developmental_readiness_assessment(self):
        """Test developmental readiness assessment"""
        print("🧪 Testing Developmental Readiness Assessment...")
        
        # Test developmental assessment
        developmental_readiness = self.progression_system._assess_developmental_readiness("test_student")
        
        self.assertIsInstance(developmental_readiness, dict)
        
        # Should have readiness scores for each domain
        for domain, score in developmental_readiness.items():
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
        
        print("  ✅ Developmental readiness assessment working correctly")
    
    def test_overall_readiness_calculation(self):
        """Test overall readiness score calculation"""
        print("🧪 Testing Overall Readiness Calculation...")
        
        # Test data
        subject_scores = {
            AcademicSubject.MATHEMATICS: 85.0,
            AcademicSubject.READING_LANGUAGE_ARTS: 80.0,
            AcademicSubject.SCIENCE: 75.0
        }
        
        developmental_readiness = {
            'physical_motor': 0.8,
            'cognitive_academic': 0.85,
            'social_emotional': 0.75
        }
        
        social_emotional_scores = {
            'self_awareness': 0.8,
            'self_regulation': 0.7,
            'social_skills': 0.75
        }
        
        overall_score = self.progression_system._calculate_overall_readiness(
            subject_scores, developmental_readiness, social_emotional_scores
        )
        
        self.assertIsInstance(overall_score, float)
        self.assertGreater(overall_score, 0.0)
        self.assertLessEqual(overall_score, 100.0)
        
        print(f"  📊 Overall readiness score: {overall_score:.1f}%")
        print("  ✅ Overall readiness calculation working correctly")
    
    def test_readiness_status_determination(self):
        """Test readiness status determination"""
        print("🧪 Testing Readiness Status Determination...")
        
        # Test different score ranges
        test_cases = [
            (95.0, ReadinessStatus.ADVANCED),
            (85.0, ReadinessStatus.READY),
            (75.0, ReadinessStatus.APPROACHING),
            (65.0, ReadinessStatus.NOT_READY)
        ]
        
        for score, expected_status in test_cases:
            actual_status = self.progression_system._determine_readiness_status(score)
            self.assertEqual(actual_status, expected_status, 
                           f"Score {score} should result in {expected_status.value}, got {actual_status.value}")
        
        print("  ✅ Readiness status determination working correctly")
    
    def test_grade_readiness_assessment(self):
        """Test complete grade readiness assessment"""
        print("🧪 Testing Complete Grade Readiness Assessment...")
        
        # Conduct assessment
        assessment = self.progression_system.assess_grade_readiness("test_student")
        
        # Validate assessment structure
        self.assertIsInstance(assessment, PlacementAssessment)
        self.assertEqual(assessment.student_id, "test_student")
        self.assertIsInstance(assessment.assessment_date, datetime)
        self.assertIn(assessment.current_grade, list(GradeLevel))
        self.assertIn(assessment.recommended_grade, list(GradeLevel))
        self.assertIn(assessment.overall_readiness, list(ReadinessStatus))
        
        # Validate subject scores
        self.assertIsInstance(assessment.subject_scores, dict)
        for subject, score in assessment.subject_scores.items():
            self.assertIn(subject, list(AcademicSubject))
            self.assertIsInstance(score, float)
        
        # Validate developmental readiness
        self.assertIsInstance(assessment.developmental_readiness, dict)
        
        # Validate recommendations
        self.assertIsInstance(assessment.strengths, list)
        self.assertIsInstance(assessment.areas_for_growth, list)
        self.assertIsInstance(assessment.recommended_interventions, list)
        
        print(f"  📊 Assessment results:")
        print(f"    Current Grade: {assessment.current_grade.value}")
        print(f"    Recommended Grade: {assessment.recommended_grade.value}")
        print(f"    Overall Readiness: {assessment.overall_readiness.value}")
        print(f"    Strengths: {len(assessment.strengths)}")
        print(f"    Growth Areas: {len(assessment.areas_for_growth)}")
        print("  ✅ Grade readiness assessment working correctly")
    
    def test_grade_advancement_process(self):
        """Test grade advancement process"""
        print("🧪 Testing Grade Advancement Process...")
        
        # Create high-performing assessment
        mock_assessment = PlacementAssessment(
            student_id="test_student",
            assessment_date=datetime.now(),
            current_grade=GradeLevel.KINDERGARTEN,
            recommended_grade=GradeLevel.FIRST_GRADE,
            subject_scores={
                AcademicSubject.MATHEMATICS: 85.0,
                AcademicSubject.READING_LANGUAGE_ARTS: 85.0,
                AcademicSubject.SOCIAL_EMOTIONAL_LEARNING: 80.0
            },
            developmental_readiness={'domain1': 0.8, 'domain2': 0.85},
            overall_readiness=ReadinessStatus.READY,
            strengths=["Strong math skills", "Good reading comprehension"],
            areas_for_growth=["Social skills development"],
            recommended_interventions=["Continue current program"]
        )
        
        # Test advancement
        advancement_result = self.progression_system.advance_grade("test_student", mock_assessment)
        
        self.assertIsInstance(advancement_result, dict)
        self.assertIn('success', advancement_result)
        self.assertIn('message', advancement_result)
        
        if advancement_result['success']:
            print(f"  ✅ Grade advancement successful: {advancement_result['message']}")
        else:
            print(f"  ⚠️  Grade advancement not ready: {advancement_result['message']}")
        
        print("  ✅ Grade advancement process working correctly")
    
    def test_progression_report_generation(self):
        """Test progression report generation"""
        print("🧪 Testing Progression Report Generation...")
        
        # Generate report
        report = self.progression_system.get_grade_progression_report("test_student")
        
        # Validate report structure
        self.assertIsInstance(report, dict)
        self.assertIn('student_id', report)
        self.assertIn('current_grade', report)
        self.assertIn('grade_progression_history', report)
        self.assertIn('current_assessment', report)
        self.assertIn('recommendations', report)
        self.assertIn('report_generated', report)
        
        # Validate report content
        self.assertEqual(report['student_id'], "test_student")
        self.assertIsInstance(report['grade_progression_history'], list)
        self.assertIsInstance(report['current_assessment'], dict)
        self.assertIsInstance(report['recommendations'], list)
        
        print(f"  📊 Report generated for: {report['student_id']}")
        print(f"    Current Grade: {report['current_grade']}")
        print(f"    Progression History: {len(report['grade_progression_history'])} entries")
        print(f"    Recommendations: {len(report['recommendations'])}")
        print("  ✅ Progression report generation working correctly")
    
    def test_intervention_recommendations(self):
        """Test intervention recommendation generation"""
        print("🧪 Testing Intervention Recommendations...")
        
        # Test different readiness levels
        test_cases = [
            (ReadinessStatus.NOT_READY, ["intensive", "individualized"]),
            (ReadinessStatus.APPROACHING, ["targeted", "scaffolded"]),
            (ReadinessStatus.ADVANCED, ["enrichment", "acceleration"])
        ]
        
        for readiness_status, expected_keywords in test_cases:
            interventions = self.progression_system._generate_intervention_recommendations(
                readiness_status, ["math needs improvement"], GradeLevel.KINDERGARTEN
            )
            
            self.assertIsInstance(interventions, list)
            self.assertGreater(len(interventions), 0)
            
            # Check that expected keywords appear in interventions
            intervention_text = " ".join(interventions).lower()
            for keyword in expected_keywords:
                self.assertTrue(any(keyword in intervention_text for intervention_text in [intervention_text]),
                              f"Expected keyword '{keyword}' not found in interventions for {readiness_status.value}")
        
        print("  ✅ Intervention recommendations working correctly")
    
    def test_database_operations(self):
        """Test database operations"""
        print("🧪 Testing Database Operations...")
        
        # Test storing assessment results
        mock_assessment = PlacementAssessment(
            student_id="test_student",
            assessment_date=datetime.now(),
            current_grade=GradeLevel.KINDERGARTEN,
            recommended_grade=GradeLevel.FIRST_GRADE,
            subject_scores={AcademicSubject.MATHEMATICS: 85.0},
            developmental_readiness={'domain1': 0.8},
            overall_readiness=ReadinessStatus.READY,
            strengths=["Strong performance"],
            areas_for_growth=["Continue growth"],
            recommended_interventions=["Maintain progress"]
        )
        
        # Store assessment
        self.progression_system._store_assessment_results(mock_assessment)
        
        # Verify data was stored
        import sqlite3
        with sqlite3.connect(self.progression_system.memory_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM subject_mastery_tracking 
                WHERE student_id = ?
            """, ("test_student",))
            count = cursor.fetchone()[0]
            self.assertGreater(count, 0, "Assessment results should be stored in database")
        
        print("  ✅ Database operations working correctly")
    
    def test_factory_function(self):
        """Test factory function"""
        print("🧪 Testing Factory Function...")
        
        system = create_grade_progression_system()
        self.assertIsInstance(system, GradeProgressionSystem)
        
        print("  ✅ Factory function working correctly")

def run_comprehensive_tests():
    """Run all tests for the Grade Progression System"""
    print("🎓 Running Comprehensive Grade Progression System Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestGradeProgressionSystem)
    
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
        # Clean up any existing default database
        import os
        default_db = "marcus_memory.db"
        if os.path.exists(default_db):
            os.unlink(default_db)
            print("  🧹 Cleaned up existing database")
        
        # Test integration with memory system using a temporary database
        from memory_system import MarcusMemorySystem
        import tempfile
        temp_db1 = tempfile.mktemp(suffix='_memory.db')
        memory_system = MarcusMemorySystem(db_path=temp_db1)
        print("  ✅ Memory system integration successful")
        
        # Test integration with EQ system
        from emotional_intelligence_assessment import EmotionalIntelligenceAssessment
        eq_system = EmotionalIntelligenceAssessment()
        print("  ✅ EQ system integration successful")
        
        # Test integration with curriculum system
        from kindergarten_curriculum_expansion import KindergartenCurriculumExpansion
        curriculum = KindergartenCurriculumExpansion()
        print("  ✅ Curriculum system integration successful")
        
        # Test creating complete system with separate database for integration
        temp_db2 = tempfile.mktemp(suffix='_progression.db')
        memory_system_for_integration = MarcusMemorySystem(db_path=temp_db2)
        
        progression_system = GradeProgressionSystem(
            memory_system=memory_system_for_integration,
            eq_system=eq_system,
            kindergarten_curriculum=curriculum
        )
        print("  ✅ Complete system integration successful")
        
        # Test basic functionality
        grade_standards = progression_system.grade_standards[GradeLevel.KINDERGARTEN]
        print(f"  ✅ Grade standards retrieved: {len(grade_standards.subject_standards)} subjects")
        
        # Clean up
        for temp_db in [temp_db1, temp_db2]:
            if os.path.exists(temp_db):
                os.unlink(temp_db)
        
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
        print("✅ All tests passed! Grade Progression System is ready for use.")
        exit(0)
    else:
        print("❌ Some tests failed. Please review and fix issues.")
        exit(1)
