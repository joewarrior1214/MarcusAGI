#!/usr/bin/env python3
"""
Issue #7: Grade Progression System for Marcus AGI

This module implements the comprehensive grade progression system that allows Marcus
to advance from kindergarten through elementary grades (K-5). The system includes:

1. Grade transition criteria and requirements
2. Cross-grade skill mapping and prerequisites  
3. Difficulty scaling algorithms
4. Grade-appropriate content libraries
5. Assessment and placement systems
6. Academic readiness evaluation
7. Developmental milestone tracking

Dependencies: Issues #1-6 (Memory, Mr. Rogers, Daily Learning, Reflection, Curriculum, EQ)
"""

import json
import sqlite3
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from enum import Enum
import logging
import math

# Import from existing systems
from kindergarten_curriculum_expansion import (
    DevelopmentalDomain, SkillLevel, KindergartenCurriculumExpansion,
    LearningObjective, DifferentiatedPath
)
from emotional_intelligence_assessment import EmotionalIntelligenceAssessment
from memory_system import MarcusMemorySystem, Concept

logger = logging.getLogger(__name__)

class GradeLevel(Enum):
    """Available grade levels in the system"""
    KINDERGARTEN = "kindergarten"
    FIRST_GRADE = "first_grade"
    SECOND_GRADE = "second_grade"
    THIRD_GRADE = "third_grade"
    FOURTH_GRADE = "fourth_grade"
    FIFTH_GRADE = "fifth_grade"

class AcademicSubject(Enum):
    """Core academic subjects across grades"""
    MATHEMATICS = "mathematics"
    READING_LANGUAGE_ARTS = "reading_language_arts"
    SCIENCE = "science"
    SOCIAL_STUDIES = "social_studies"
    PHYSICAL_EDUCATION = "physical_education"
    ART = "art"
    MUSIC = "music"
    SOCIAL_EMOTIONAL_LEARNING = "social_emotional_learning"

class ReadinessStatus(Enum):
    """Grade advancement readiness statuses"""
    NOT_READY = "not_ready"           # Below 70% - needs significant support
    APPROACHING = "approaching"        # 70-79% - making progress, needs time
    READY = "ready"                   # 80-89% - meets advancement criteria
    ADVANCED = "advanced"             # 90%+ - exceeds expectations, may skip

@dataclass
class GradeTransitionCriteria:
    """Criteria required for advancing to next grade"""
    grade_level: GradeLevel
    core_subject_requirements: Dict[AcademicSubject, float]  # subject -> minimum mastery %
    developmental_milestones: List[str]  # Required milestone IDs
    social_emotional_readiness: Dict[str, float]  # EQ domain -> minimum score
    minimum_overall_mastery: float  # Overall average required
    reading_level_requirement: str  # Reading level benchmark
    mathematical_concepts: List[str]  # Required math concepts
    time_in_grade_minimum: int  # Minimum days in current grade
    special_considerations: List[str]  # Additional factors to consider

@dataclass
class SkillMapping:
    """Maps skills across grade levels showing progression"""
    skill_id: str
    skill_name: str
    subject: AcademicSubject
    kindergarten_level: Optional[str] = None
    first_grade_level: Optional[str] = None
    second_grade_level: Optional[str] = None
    third_grade_level: Optional[str] = None
    fourth_grade_level: Optional[str] = None
    fifth_grade_level: Optional[str] = None
    prerequisites: List[str] = field(default_factory=list)
    leads_to: List[str] = field(default_factory=list)

@dataclass
class DifficultyScaling:
    """Defines how difficulty scales across grades for a concept"""
    concept_id: str
    base_difficulty: float  # Kindergarten baseline (1.0)
    scaling_factors: Dict[GradeLevel, float]  # Grade -> multiplier
    complexity_indicators: Dict[GradeLevel, List[str]]  # Grade -> complexity features
    vocabulary_level: Dict[GradeLevel, int]  # Grade -> reading level required
    prerequisite_depth: Dict[GradeLevel, int]  # Grade -> number of prerequisites

@dataclass
class GradeStandards:
    """Academic standards and expectations for each grade"""
    grade_level: GradeLevel
    subject_standards: Dict[AcademicSubject, List[str]]  # Subject -> learning standards
    assessment_benchmarks: Dict[str, Dict[str, Any]]  # Test_id -> benchmark data
    expected_time_allocation: Dict[AcademicSubject, int]  # Subject -> minutes per week
    developmental_expectations: List[str]  # Age-appropriate developmental goals
    social_expectations: List[str]  # Social behavior expectations

@dataclass
class PlacementAssessment:
    """Results of academic placement assessment"""
    student_id: str
    assessment_date: datetime
    current_grade: GradeLevel
    recommended_grade: GradeLevel
    subject_scores: Dict[AcademicSubject, float]  # Subject -> proficiency %
    developmental_readiness: Dict[str, float]  # Domain -> readiness score
    overall_readiness: ReadinessStatus
    strengths: List[str]
    areas_for_growth: List[str]
    recommended_interventions: List[str]
    timeline_for_reassessment: Optional[date] = None

class GradeProgressionSystem:
    """Comprehensive grade progression system for Marcus AGI"""
    
    def __init__(self, memory_system: MarcusMemorySystem = None, 
                 eq_system: EmotionalIntelligenceAssessment = None,
                 kindergarten_curriculum: KindergartenCurriculumExpansion = None):
        self.memory_system = memory_system or MarcusMemorySystem()
        self.eq_system = eq_system or EmotionalIntelligenceAssessment()
        self.kindergarten_curriculum = kindergarten_curriculum or KindergartenCurriculumExpansion()
        
        # Initialize core components
        self.grade_standards = self._load_grade_standards()
        self.transition_criteria = self._define_transition_criteria()
        self.skill_mappings = self._create_skill_mappings()
        self.difficulty_scalings = self._create_difficulty_scalings()
        
        # Initialize database
        self._init_progression_database()
    
    def _init_progression_database(self):
        """Initialize database tables for grade progression tracking"""
        with sqlite3.connect(self.memory_system.db_path) as conn:
            cursor = conn.cursor()
            
            # Grade progression history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grade_progressions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL DEFAULT 'marcus',
                    from_grade TEXT NOT NULL,
                    to_grade TEXT NOT NULL,
                    progression_date TEXT NOT NULL,
                    readiness_score REAL NOT NULL,
                    assessment_data TEXT NOT NULL,
                    intervention_plan TEXT,
                    success_metrics TEXT
                )
            """)
            
            # Current grade status table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS current_grade_status (
                    student_id TEXT PRIMARY KEY DEFAULT 'marcus',
                    current_grade TEXT NOT NULL,
                    grade_entry_date TEXT NOT NULL,
                    days_in_grade INTEGER NOT NULL DEFAULT 0,
                    subject_mastery_levels TEXT NOT NULL DEFAULT '{}',
                    developmental_progress TEXT NOT NULL DEFAULT '{}',
                    last_assessment_date TEXT,
                    next_assessment_due TEXT
                )
            """)
            
            # Subject mastery tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subject_mastery_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL DEFAULT 'marcus',
                    grade_level TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    concept_id TEXT NOT NULL,
                    mastery_level REAL NOT NULL,
                    assessment_date TEXT NOT NULL,
                    growth_trajectory TEXT,
                    intervention_notes TEXT
                )
            """)
            
            conn.commit()
    
    def _load_grade_standards(self) -> Dict[GradeLevel, GradeStandards]:
        """Load academic standards for each grade level"""
        standards = {}
        
        # Kindergarten Standards
        standards[GradeLevel.KINDERGARTEN] = GradeStandards(
            grade_level=GradeLevel.KINDERGARTEN,
            subject_standards={
                AcademicSubject.MATHEMATICS: [
                    "Count to 100 by ones and by tens",
                    "Count forward beginning from a given number within 100",
                    "Write numbers from 0 to 20",
                    "Understand addition as putting together and subtraction as taking apart",
                    "Solve addition and subtraction word problems within 10"
                ],
                AcademicSubject.READING_LANGUAGE_ARTS: [
                    "Demonstrate understanding of print concepts",
                    "Demonstrate understanding of phonological awareness",
                    "Know and apply grade-level phonics and decoding skills",
                    "Read emergent-reader texts with purpose and understanding",
                    "Use a combination of drawing, dictating, and writing to compose informative texts"
                ],
                AcademicSubject.SCIENCE: [
                    "Use observations to describe patterns in natural world",
                    "Plan and conduct investigations to determine effect of pushing and pulling",
                    "Analyze data from tests to determine which materials have properties best suited for intended use",
                    "Construct an argument supported by evidence for how plants and animals can change environment"
                ],
                AcademicSubject.SOCIAL_STUDIES: [
                    "Understand family structures and roles",
                    "Identify basic needs of people",
                    "Recognize symbols, customs, and celebrations that represent American beliefs",
                    "Understand concept of time and sequence of events"
                ]
            },
            assessment_benchmarks={
                "dibels_kindergarten": {"fluency_target": 40, "accuracy_target": 0.90},
                "math_concepts_k": {"number_sense": 0.80, "operations": 0.75}
            },
            expected_time_allocation={
                AcademicSubject.READING_LANGUAGE_ARTS: 300,  # 5 hours per week
                AcademicSubject.MATHEMATICS: 180,            # 3 hours per week
                AcademicSubject.SCIENCE: 120,                # 2 hours per week
                AcademicSubject.SOCIAL_STUDIES: 120,         # 2 hours per week
                AcademicSubject.PHYSICAL_EDUCATION: 150,     # 2.5 hours per week
                AcademicSubject.ART: 90,                     # 1.5 hours per week
                AcademicSubject.MUSIC: 90                    # 1.5 hours per week
            },
            developmental_expectations=[
                "Follows classroom routines independently",
                "Manages personal belongings",
                "Works cooperatively in small groups",
                "Shows persistence in challenging tasks",
                "Demonstrates self-regulation skills"
            ],
            social_expectations=[
                "Uses words to solve conflicts",
                "Shows empathy for others",
                "Follows school rules and expectations",
                "Builds positive relationships with peers and adults"
            ]
        )
        
        # First Grade Standards
        standards[GradeLevel.FIRST_GRADE] = GradeStandards(
            grade_level=GradeLevel.FIRST_GRADE,
            subject_standards={
                AcademicSubject.MATHEMATICS: [
                    "Extend counting sequence to 120",
                    "Understand place value through 19",
                    "Use addition and subtraction within 20 to solve problems",
                    "Work with addition and subtraction equations",
                    "Reason with shapes and their attributes"
                ],
                AcademicSubject.READING_LANGUAGE_ARTS: [
                    "Ask and answer questions about key details in text",
                    "Retell stories including key details",
                    "Identify characters, settings, and major events in stories", 
                    "Know and apply grade-level phonics and word analysis skills",
                    "Read with sufficient accuracy and fluency to support comprehension"
                ],
                AcademicSubject.SCIENCE: [
                    "Use materials to design solutions to human problems",
                    "Read texts and use media to determine patterns in behavior of parents and offspring",
                    "Make observations to determine effect of sunlight on Earth's surface",
                    "Use observations of sun, moon, and stars to describe patterns"
                ],
                AcademicSubject.SOCIAL_STUDIES: [
                    "Understand concepts of past, present, and future",
                    "Identify examples of needs and wants",
                    "Explain how people make choices about wants and needs",
                    "Describe roles and responsibilities of people in authority"
                ]
            },
            assessment_benchmarks={
                "dibels_first_grade": {"fluency_target": 60, "accuracy_target": 0.92},
                "math_concepts_1": {"number_sense": 0.85, "operations": 0.80, "geometry": 0.75}
            },
            expected_time_allocation={
                AcademicSubject.READING_LANGUAGE_ARTS: 360,  # 6 hours per week
                AcademicSubject.MATHEMATICS: 240,            # 4 hours per week
                AcademicSubject.SCIENCE: 150,                # 2.5 hours per week
                AcademicSubject.SOCIAL_STUDIES: 150,         # 2.5 hours per week
                AcademicSubject.PHYSICAL_EDUCATION: 150,     # 2.5 hours per week
                AcademicSubject.ART: 90,                     # 1.5 hours per week
                AcademicSubject.MUSIC: 90                    # 1.5 hours per week
            },
            developmental_expectations=[
                "Demonstrates increased attention span (20-25 minutes)",
                "Shows more complex problem-solving abilities",
                "Begins to understand abstract concepts",
                "Develops greater fine motor control",
                "Shows improved memory and recall"
            ],
            social_expectations=[
                "Works collaboratively on extended projects",
                "Shows leadership skills in group settings",
                "Demonstrates fairness and justice concepts",
                "Develops stronger friendships",
                "Shows increased emotional regulation"
            ]
        )
        
        # Continue with other grades...
        # (For brevity, I'll implement the core structure and can expand other grades)
        
        return standards
    
    def _define_transition_criteria(self) -> Dict[GradeLevel, GradeTransitionCriteria]:
        """Define criteria for transitioning between grades"""
        criteria = {}
        
        # Kindergarten to First Grade
        criteria[GradeLevel.FIRST_GRADE] = GradeTransitionCriteria(
            grade_level=GradeLevel.FIRST_GRADE,
            core_subject_requirements={
                AcademicSubject.MATHEMATICS: 0.80,  # 80% mastery in math concepts
                AcademicSubject.READING_LANGUAGE_ARTS: 0.75,  # 75% mastery in literacy
                AcademicSubject.SOCIAL_EMOTIONAL_LEARNING: 0.70  # 70% social-emotional readiness
            },
            developmental_milestones=[
                "gross_motor_coordination", "fine_motor_control", "emotional_regulation",
                "social_interaction", "oral_language", "listening_comprehension"
            ],
            social_emotional_readiness={
                "self_awareness": 0.70,
                "self_regulation": 0.70,
                "social_skills": 0.65,
                "empathy": 0.65
            },
            minimum_overall_mastery=0.75,
            reading_level_requirement="Beginning Reader (Level D-F)",
            mathematical_concepts=[
                "number_sense_20", "counting_1to100", "basic_addition_subtraction",
                "shape_recognition", "pattern_recognition"
            ],
            time_in_grade_minimum=150,  # At least 150 days (about 30 weeks)
            special_considerations=[
                "Shows consistent attendance and engagement",
                "Demonstrates readiness for increased academic rigor",
                "Can follow multi-step directions",
                "Shows appropriate social interaction skills"
            ]
        )
        
        # First Grade to Second Grade
        criteria[GradeLevel.SECOND_GRADE] = GradeTransitionCriteria(
            grade_level=GradeLevel.SECOND_GRADE,
            core_subject_requirements={
                AcademicSubject.MATHEMATICS: 0.80,
                AcademicSubject.READING_LANGUAGE_ARTS: 0.80,
                AcademicSubject.SCIENCE: 0.70,
                AcademicSubject.SOCIAL_STUDIES: 0.70
            },
            developmental_milestones=[
                "advanced_literacy", "mathematical_reasoning", "scientific_inquiry",
                "collaborative_learning", "independent_work_skills"
            ],
            social_emotional_readiness={
                "self_awareness": 0.75,
                "self_regulation": 0.75,
                "social_skills": 0.70,
                "empathy": 0.70,
                "motivation": 0.70
            },
            minimum_overall_mastery=0.78,
            reading_level_requirement="Transitional Reader (Level G-I)",
            mathematical_concepts=[
                "place_value_100", "addition_subtraction_fluency", "measurement_concepts",
                "data_analysis_basics", "geometric_reasoning"
            ],
            time_in_grade_minimum=150,
            special_considerations=[
                "Demonstrates fluent reading at grade level",
                "Shows mathematical reasoning abilities",
                "Can work independently for extended periods",
                "Demonstrates problem-solving persistence"
            ]
        )
        
        # Additional grades would follow similar patterns...
        
        return criteria
    
    def _create_skill_mappings(self) -> Dict[str, SkillMapping]:
        """Create cross-grade skill progression mappings"""
        mappings = {}
        
        # Mathematics progression
        mappings["number_sense"] = SkillMapping(
            skill_id="number_sense",
            skill_name="Number Sense and Place Value",
            subject=AcademicSubject.MATHEMATICS,
            kindergarten_level="Count to 20, recognize numerals 1-10",
            first_grade_level="Count to 120, understand place value to 19", 
            second_grade_level="Understand place value to 1000, count by 2s, 5s, 10s",
            third_grade_level="Round to nearest 10 or 100, understand fractions",
            fourth_grade_level="Compare decimals, understand place value to millions",
            fifth_grade_level="Understand decimal place value, powers of 10",
            prerequisites=["counting_basics", "numeral_recognition"],
            leads_to=["algebraic_thinking", "proportional_reasoning"]
        )
        
        mappings["reading_comprehension"] = SkillMapping(
            skill_id="reading_comprehension",
            skill_name="Reading Comprehension",
            subject=AcademicSubject.READING_LANGUAGE_ARTS,
            kindergarten_level="Listen to stories, answer simple questions",
            first_grade_level="Read simple texts, identify main characters and events",
            second_grade_level="Read longer texts, make predictions and connections",
            third_grade_level="Read complex texts, identify themes and main ideas",
            fourth_grade_level="Analyze character development, compare texts",
            fifth_grade_level="Synthesize information across multiple texts",
            prerequisites=["phonemic_awareness", "decoding_skills"],
            leads_to=["critical_thinking", "literary_analysis"]
        )
        
        mappings["scientific_inquiry"] = SkillMapping(
            skill_id="scientific_inquiry",
            skill_name="Scientific Inquiry and Investigation",
            subject=AcademicSubject.SCIENCE,
            kindergarten_level="Make observations, ask questions about nature",
            first_grade_level="Plan simple investigations, record observations",
            second_grade_level="Design experiments, collect and analyze data",
            third_grade_level="Form hypotheses, draw conclusions from evidence",
            fourth_grade_level="Design controlled experiments, communicate findings",
            fifth_grade_level="Conduct independent research, evaluate scientific claims",
            prerequisites=["observation_skills", "questioning_strategies"],
            leads_to=["advanced_research_methods", "scientific_reasoning"]
        )
        
        # Continue with other key skills...
        
        return mappings
    
    def _create_difficulty_scalings(self) -> Dict[str, DifficultyScaling]:
        """Create difficulty scaling algorithms for concepts across grades"""
        scalings = {}
        
        scalings["reading_complexity"] = DifficultyScaling(
            concept_id="reading_complexity",
            base_difficulty=1.0,  # Kindergarten baseline
            scaling_factors={
                GradeLevel.KINDERGARTEN: 1.0,
                GradeLevel.FIRST_GRADE: 1.4,
                GradeLevel.SECOND_GRADE: 1.8,
                GradeLevel.THIRD_GRADE: 2.3,
                GradeLevel.FOURTH_GRADE: 2.8,
                GradeLevel.FIFTH_GRADE: 3.4
            },
            complexity_indicators={
                GradeLevel.KINDERGARTEN: ["Simple sentences", "Familiar vocabulary", "Picture support"],
                GradeLevel.FIRST_GRADE: ["Compound sentences", "Grade-level vocabulary", "Some inference"],
                GradeLevel.SECOND_GRADE: ["Complex sentences", "Academic vocabulary", "Multiple meanings"],
                GradeLevel.THIRD_GRADE: ["Paragraph structure", "Abstract concepts", "Cause and effect"],
                GradeLevel.FOURTH_GRADE: ["Multiple paragraphs", "Figurative language", "Text structure"],
                GradeLevel.FIFTH_GRADE: ["Extended texts", "Complex themes", "Author's purpose"]
            },
            vocabulary_level={
                GradeLevel.KINDERGARTEN: 300,   # 300 sight words
                GradeLevel.FIRST_GRADE: 500,    # 500 sight words
                GradeLevel.SECOND_GRADE: 800,   # 800 sight words
                GradeLevel.THIRD_GRADE: 1200,   # 1200 sight words
                GradeLevel.FOURTH_GRADE: 1800,  # 1800 sight words
                GradeLevel.FIFTH_GRADE: 2500    # 2500 sight words
            },
            prerequisite_depth={
                GradeLevel.KINDERGARTEN: 2,
                GradeLevel.FIRST_GRADE: 3,
                GradeLevel.SECOND_GRADE: 4,
                GradeLevel.THIRD_GRADE: 5,
                GradeLevel.FOURTH_GRADE: 6,
                GradeLevel.FIFTH_GRADE: 7
            }
        )
        
        scalings["mathematical_reasoning"] = DifficultyScaling(
            concept_id="mathematical_reasoning",
            base_difficulty=1.0,
            scaling_factors={
                GradeLevel.KINDERGARTEN: 1.0,
                GradeLevel.FIRST_GRADE: 1.5,
                GradeLevel.SECOND_GRADE: 2.0,
                GradeLevel.THIRD_GRADE: 2.8,
                GradeLevel.FOURTH_GRADE: 3.6,
                GradeLevel.FIFTH_GRADE: 4.5
            },
            complexity_indicators={
                GradeLevel.KINDERGARTEN: ["Concrete objects", "Visual representations", "Simple counting"],
                GradeLevel.FIRST_GRADE: ["Basic operations", "Number lines", "Word problems"],
                GradeLevel.SECOND_GRADE: ["Two-step problems", "Place value", "Measurement"],
                GradeLevel.THIRD_GRADE: ["Multi-step problems", "Fractions", "Area and perimeter"],
                GradeLevel.FOURTH_GRADE: ["Complex fractions", "Decimals", "Multi-digit operations"],
                GradeLevel.FIFTH_GRADE: ["Algebraic thinking", "Coordinate planes", "Volume"]
            },
            vocabulary_level={
                GradeLevel.KINDERGARTEN: 50,    # 50 math terms
                GradeLevel.FIRST_GRADE: 100,    # 100 math terms
                GradeLevel.SECOND_GRADE: 180,   # 180 math terms
                GradeLevel.THIRD_GRADE: 280,    # 280 math terms
                GradeLevel.FOURTH_GRADE: 400,   # 400 math terms
                GradeLevel.FIFTH_GRADE: 550     # 550 math terms
            },
            prerequisite_depth={
                GradeLevel.KINDERGARTEN: 1,
                GradeLevel.FIRST_GRADE: 2,
                GradeLevel.SECOND_GRADE: 3,
                GradeLevel.THIRD_GRADE: 4,
                GradeLevel.FOURTH_GRADE: 5,
                GradeLevel.FIFTH_GRADE: 6
            }
        )
        
        return scalings
    
    def assess_grade_readiness(self, student_id: str = "marcus") -> PlacementAssessment:
        """Conduct comprehensive grade readiness assessment"""
        logger.info(f"Conducting grade readiness assessment for {student_id}")
        
        # Get current grade status
        current_grade = self._get_current_grade(student_id)
        
        # Assess academic subjects
        subject_scores = self._assess_academic_subjects(student_id, current_grade)
        
        # Assess developmental readiness
        developmental_readiness = self._assess_developmental_readiness(student_id)
        
        # Assess social-emotional readiness using EQ system
        eq_results = self.eq_system.generate_comprehensive_eq_report()
        social_emotional_scores = {
            domain: metrics[0].current_level if metrics else 0.0
            for domain, metrics in eq_results.get('eq_metrics', {}).items()
        }
        
        # Calculate overall readiness
        overall_score = self._calculate_overall_readiness(subject_scores, developmental_readiness, social_emotional_scores)
        readiness_status = self._determine_readiness_status(overall_score)
        
        # Determine recommended grade
        recommended_grade = self._recommend_grade_placement(current_grade, readiness_status, subject_scores)
        
        # Generate strengths and areas for growth
        strengths, areas_for_growth = self._analyze_strengths_and_growth_areas(
            subject_scores, developmental_readiness, social_emotional_scores
        )
        
        # Generate intervention recommendations
        interventions = self._generate_intervention_recommendations(
            readiness_status, areas_for_growth, current_grade
        )
        
        # Create assessment result
        assessment = PlacementAssessment(
            student_id=student_id,
            assessment_date=datetime.now(),
            current_grade=current_grade,
            recommended_grade=recommended_grade,
            subject_scores=subject_scores,
            developmental_readiness=developmental_readiness,
            overall_readiness=readiness_status,
            strengths=strengths,
            areas_for_growth=areas_for_growth,
            recommended_interventions=interventions,
            timeline_for_reassessment=date.today() + timedelta(days=90) if readiness_status != ReadinessStatus.READY else None
        )
        
        # Store assessment in database
        self._store_assessment_results(assessment)
        
        return assessment
    
    def advance_grade(self, student_id: str = "marcus", assessment: PlacementAssessment = None) -> Dict[str, Any]:
        """Advance student to next grade if ready"""
        if not assessment:
            assessment = self.assess_grade_readiness(student_id)
        
        if assessment.overall_readiness not in [ReadinessStatus.READY, ReadinessStatus.ADVANCED]:
            return {
                'success': False,
                'message': f'Student not ready for advancement. Status: {assessment.overall_readiness.value}',
                'required_interventions': assessment.recommended_interventions,
                'timeline_for_reassessment': assessment.timeline_for_reassessment
            }
        
        # Check transition criteria
        next_grade = assessment.recommended_grade
        if next_grade == assessment.current_grade:
            return {
                'success': False,
                'message': 'Assessment recommends staying in current grade',
                'current_performance': assessment.subject_scores
            }
        
        # Verify transition criteria
        criteria = self.transition_criteria.get(next_grade)
        if not criteria:
            return {
                'success': False,
                'message': f'No transition criteria defined for {next_grade.value}'
            }
        
        meets_criteria, criteria_details = self._verify_transition_criteria(assessment, criteria)
        
        if not meets_criteria:
            return {
                'success': False,
                'message': 'Does not meet all transition criteria',
                'criteria_details': criteria_details,
                'recommended_interventions': assessment.recommended_interventions
            }
        
        # Execute grade advancement
        advancement_result = self._execute_grade_advancement(student_id, assessment.current_grade, next_grade, assessment)
        
        return advancement_result
    
    def _get_current_grade(self, student_id: str) -> GradeLevel:
        """Get student's current grade level"""
        with sqlite3.connect(self.memory_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT current_grade FROM current_grade_status 
                WHERE student_id = ?
            """, (student_id,))
            
            result = cursor.fetchone()
            if result:
                return GradeLevel(result[0])
            else:
                # Default to kindergarten for new students
                self._initialize_student_grade_status(student_id, GradeLevel.KINDERGARTEN)
                return GradeLevel.KINDERGARTEN
    
    def _initialize_student_grade_status(self, student_id: str, grade: GradeLevel):
        """Initialize student's grade status in database"""
        with sqlite3.connect(self.memory_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO current_grade_status
                (student_id, current_grade, grade_entry_date, days_in_grade,
                 subject_mastery_levels, developmental_progress)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (student_id, grade.value, datetime.now().isoformat(), 0, '{}', '{}'))
            conn.commit()
    
    def _assess_academic_subjects(self, student_id: str, current_grade: GradeLevel) -> Dict[AcademicSubject, float]:
        """Assess proficiency in core academic subjects"""
        subject_scores = {}
        
        # Get mastery levels from memory system for different subjects
        with sqlite3.connect(self.memory_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT subject, AVG(mastery_level) as avg_mastery
                FROM subject_mastery_tracking
                WHERE student_id = ? AND grade_level = ?
                GROUP BY subject
            """, (student_id, current_grade.value))
            
            results = cursor.fetchall()
            subject_data = {row[0]: row[1] for row in results}
        
        # Map subjects and calculate scores
        for subject in AcademicSubject:
            subject_key = subject.value.lower()
            
            # Get base score from database
            base_score = subject_data.get(subject_key, 0.0)
            
            # Apply grade-level scaling
            if current_grade in self.difficulty_scalings:
                scaling = self.difficulty_scalings.get(f"{subject_key}_complexity", None)
                if scaling and current_grade in scaling.scaling_factors:
                    # Adjust score based on grade-level expectations
                    expected_difficulty = scaling.scaling_factors[current_grade]
                    adjusted_score = base_score * (1.0 / expected_difficulty) if expected_difficulty > 0 else base_score
                    subject_scores[subject] = min(adjusted_score, 1.0) * 100  # Convert to percentage
                else:
                    subject_scores[subject] = base_score * 100
            else:
                subject_scores[subject] = base_score * 100
        
        return subject_scores
    
    def _assess_developmental_readiness(self, student_id: str) -> Dict[str, float]:
        """Assess developmental readiness across domains"""
        readiness_scores = {}
        
        # Use kindergarten curriculum system to assess developmental progress
        if hasattr(self.kindergarten_curriculum, 'developmental_milestones'):
            for domain, milestones in self.kindergarten_curriculum.developmental_milestones.items():
                domain_scores = []
                for milestone in milestones:
                    # Check if milestone is achieved based on memory system data
                    milestone_score = self._evaluate_milestone_achievement(student_id, milestone.id)
                    domain_scores.append(milestone_score)
                
                if domain_scores:
                    readiness_scores[str(domain)] = sum(domain_scores) / len(domain_scores)
                else:
                    readiness_scores[str(domain)] = 0.0
        
        return readiness_scores
    
    def _evaluate_milestone_achievement(self, student_id: str, milestone_id: str) -> float:
        """Evaluate achievement level for a specific developmental milestone"""
        try:
            # Get all concepts from memory and filter for relevant ones
            all_concepts = self.memory_system.fetch_all_concepts()
            concepts = [c for c in all_concepts if milestone_id.lower() in str(c.get('content', '')).lower()]
            
            if not concepts:
                return 0.0
            
            # Calculate average mastery level for related concepts
            mastery_levels = [concept.get('mastery_level', 0) for concept in concepts]
            if mastery_levels:
                return sum(mastery_levels) / len(mastery_levels) / 10.0  # Normalize to 0-1
            else:
                return 0.0
        except Exception as e:
            logger.warning(f"Error evaluating milestone {milestone_id}: {e}")
            return 0.0
    
    def _calculate_overall_readiness(self, subject_scores: Dict[AcademicSubject, float],
                                   developmental_readiness: Dict[str, float],
                                   social_emotional_scores: Dict[str, float]) -> float:
        """Calculate overall readiness score"""
        # Weight different components
        academic_weight = 0.50  # 50% academic subjects
        developmental_weight = 0.30  # 30% developmental readiness
        social_emotional_weight = 0.20  # 20% social-emotional readiness
        
        # Calculate weighted average of academic subjects
        academic_average = sum(subject_scores.values()) / len(subject_scores) if subject_scores else 0.0
        
        # Calculate weighted average of developmental domains
        developmental_average = sum(developmental_readiness.values()) / len(developmental_readiness) if developmental_readiness else 0.0
        developmental_average *= 100  # Convert to percentage
        
        # Calculate weighted average of social-emotional domains
        se_average = sum(social_emotional_scores.values()) / len(social_emotional_scores) if social_emotional_scores else 0.0
        se_average *= 100  # Convert to percentage
        
        # Calculate overall weighted score
        overall_score = (
            academic_average * academic_weight +
            developmental_average * developmental_weight +
            se_average * social_emotional_weight
        )
        
        return overall_score
    
    def _determine_readiness_status(self, overall_score: float) -> ReadinessStatus:
        """Determine readiness status based on overall score"""
        if overall_score >= 90.0:
            return ReadinessStatus.ADVANCED
        elif overall_score >= 80.0:
            return ReadinessStatus.READY
        elif overall_score >= 70.0:
            return ReadinessStatus.APPROACHING
        else:
            return ReadinessStatus.NOT_READY
    
    def _recommend_grade_placement(self, current_grade: GradeLevel, readiness_status: ReadinessStatus,
                                 subject_scores: Dict[AcademicSubject, float]) -> GradeLevel:
        """Recommend appropriate grade placement"""
        if readiness_status == ReadinessStatus.ADVANCED:
            # Consider grade acceleration for advanced students
            grade_order = list(GradeLevel)
            current_index = grade_order.index(current_grade)
            if current_index < len(grade_order) - 1:
                return grade_order[current_index + 1]
            else:
                return current_grade  # Already at highest grade
        
        elif readiness_status == ReadinessStatus.READY:
            # Ready for next grade
            grade_order = list(GradeLevel)
            current_index = grade_order.index(current_grade)
            if current_index < len(grade_order) - 1:
                return grade_order[current_index + 1]
            else:
                return current_grade
        
        else:
            # Not ready - stay in current grade
            return current_grade
    
    def _analyze_strengths_and_growth_areas(self, subject_scores: Dict[AcademicSubject, float],
                                          developmental_readiness: Dict[str, float],
                                          social_emotional_scores: Dict[str, float]) -> Tuple[List[str], List[str]]:
        """Analyze student strengths and areas needing growth"""
        strengths = []
        areas_for_growth = []
        
        # Analyze academic strengths and growth areas
        for subject, score in subject_scores.items():
            if score >= 85.0:
                strengths.append(f"Strong {subject.value.replace('_', ' ').title()} skills ({score:.1f}%)")
            elif score < 70.0:
                areas_for_growth.append(f"{subject.value.replace('_', ' ').title()} needs improvement ({score:.1f}%)")
        
        # Analyze developmental strengths and growth areas
        for domain, score in developmental_readiness.items():
            percentage = score * 100
            if percentage >= 85.0:
                strengths.append(f"Strong {domain.replace('_', ' ').title()} development ({percentage:.1f}%)")
            elif percentage < 70.0:
                areas_for_growth.append(f"{domain.replace('_', ' ').title()} development needs support ({percentage:.1f}%)")
        
        # Analyze social-emotional strengths and growth areas
        for domain, score in social_emotional_scores.items():
            percentage = score * 100
            if percentage >= 85.0:
                strengths.append(f"Strong {domain.replace('_', ' ').title()} skills ({percentage:.1f}%)")
            elif percentage < 70.0:
                areas_for_growth.append(f"{domain.replace('_', ' ').title()} skills need development ({percentage:.1f}%)")
        
        return strengths, areas_for_growth
    
    def _generate_intervention_recommendations(self, readiness_status: ReadinessStatus,
                                             areas_for_growth: List[str], 
                                             current_grade: GradeLevel) -> List[str]:
        """Generate targeted intervention recommendations"""
        interventions = []
        
        if readiness_status == ReadinessStatus.NOT_READY:
            interventions.extend([
                "Intensive individualized instruction in identified deficit areas",
                "Small group interventions with specialized curriculum",
                "Extended learning time through tutoring or extended day programs",
                "Multi-sensory instructional approaches",
                "Frequent progress monitoring and assessment",
                "Collaboration with specialists (reading, math, OT/PT as needed)"
            ])
        
        elif readiness_status == ReadinessStatus.APPROACHING:
            interventions.extend([
                "Targeted skill-building in specific academic areas",
                "Scaffolded instruction with gradual release of support",
                "Peer tutoring and cooperative learning opportunities",
                "Additional practice time in deficit skill areas",
                "Regular check-ins and progress monitoring"
            ])
        
        elif readiness_status == ReadinessStatus.ADVANCED:
            interventions.extend([
                "Enrichment activities and advanced curriculum materials",
                "Independent study projects and research opportunities",
                "Mentorship and leadership roles",
                "Acceleration in specific subject areas",
                "Gifted and talented program consideration"
            ])
        
        # Add specific interventions based on areas for growth
        for area in areas_for_growth:
            if "mathematics" in area.lower():
                interventions.append("Mathematics intervention program with manipulatives and visual supports")
            elif "reading" in area.lower() or "language" in area.lower():
                interventions.append("Phonics-based reading intervention with decodable texts")
            elif "social" in area.lower() or "emotional" in area.lower():
                interventions.append("Social-emotional learning curriculum and counseling support")
            elif "physical" in area.lower() or "motor" in area.lower():
                interventions.append("Occupational therapy consultation and fine/gross motor activities")
        
        return interventions
    
    def _verify_transition_criteria(self, assessment: PlacementAssessment, 
                                  criteria: GradeTransitionCriteria) -> Tuple[bool, Dict[str, Any]]:
        """Verify if student meets transition criteria for next grade"""
        criteria_met = {}
        overall_met = True
        
        # Check core subject requirements
        subject_requirements_met = True
        for subject, required_score in criteria.core_subject_requirements.items():
            actual_score = assessment.subject_scores.get(subject, 0.0)
            meets_requirement = actual_score >= (required_score * 100)
            criteria_met[f"{subject.value}_requirement"] = {
                'required': required_score * 100,
                'actual': actual_score,
                'met': meets_requirement
            }
            if not meets_requirement:
                subject_requirements_met = False
        
        overall_met = overall_met and subject_requirements_met
        
        # Check overall mastery requirement
        overall_readiness_score = self._calculate_overall_readiness(
            assessment.subject_scores, assessment.developmental_readiness, {}
        )
        meets_overall = overall_readiness_score >= (criteria.minimum_overall_mastery * 100)
        criteria_met['overall_mastery'] = {
            'required': criteria.minimum_overall_mastery * 100,
            'actual': overall_readiness_score,
            'met': meets_overall
        }
        overall_met = overall_met and meets_overall
        
        # Check time in grade requirement
        days_in_grade = self._get_days_in_current_grade(assessment.student_id)
        meets_time_requirement = days_in_grade >= criteria.time_in_grade_minimum
        criteria_met['time_in_grade'] = {
            'required': criteria.time_in_grade_minimum,
            'actual': days_in_grade,
            'met': meets_time_requirement
        }
        overall_met = overall_met and meets_time_requirement
        
        # Check developmental milestones
        milestone_progress = self._check_developmental_milestones(assessment.student_id, criteria.developmental_milestones)
        milestones_met = all(progress >= 0.75 for progress in milestone_progress.values())  # 75% threshold
        criteria_met['developmental_milestones'] = {
            'required': criteria.developmental_milestones,
            'progress': milestone_progress,
            'met': milestones_met
        }
        overall_met = overall_met and milestones_met
        
        return overall_met, criteria_met
    
    def _get_days_in_current_grade(self, student_id: str) -> int:
        """Get number of days student has been in current grade"""
        with sqlite3.connect(self.memory_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT grade_entry_date FROM current_grade_status 
                WHERE student_id = ?
            """, (student_id,))
            
            result = cursor.fetchone()
            if result:
                entry_date = datetime.fromisoformat(result[0])
                days_in_grade = (datetime.now() - entry_date).days
                return days_in_grade
            else:
                return 0
    
    def _check_developmental_milestones(self, student_id: str, milestone_ids: List[str]) -> Dict[str, float]:
        """Check progress on required developmental milestones"""
        milestone_progress = {}
        
        for milestone_id in milestone_ids:
            progress = self._evaluate_milestone_achievement(student_id, milestone_id)
            milestone_progress[milestone_id] = progress
        
        return milestone_progress
    
    def _execute_grade_advancement(self, student_id: str, from_grade: GradeLevel, 
                                 to_grade: GradeLevel, assessment: PlacementAssessment) -> Dict[str, Any]:
        """Execute the grade advancement process"""
        try:
            with sqlite3.connect(self.memory_system.db_path) as conn:
                cursor = conn.cursor()
                
                # Record the progression
                cursor.execute("""
                    INSERT INTO grade_progressions
                    (student_id, from_grade, to_grade, progression_date, 
                     readiness_score, assessment_data, intervention_plan)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    student_id, from_grade.value, to_grade.value, 
                    datetime.now().isoformat(),
                    assessment.overall_readiness.value,
                    json.dumps(asdict(assessment), default=str),
                    json.dumps(assessment.recommended_interventions)
                ))
                
                # Update current grade status
                cursor.execute("""
                    UPDATE current_grade_status
                    SET current_grade = ?, grade_entry_date = ?, days_in_grade = 0,
                        last_assessment_date = ?, next_assessment_due = ?
                    WHERE student_id = ?
                """, (
                    to_grade.value, datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    (date.today() + timedelta(days=45)).isoformat(),  # Next assessment in 45 days
                    student_id
                ))
                
                conn.commit()
            
            logger.info(f"Successfully advanced {student_id} from {from_grade.value} to {to_grade.value}")
            
            return {
                'success': True,
                'message': f'Successfully advanced from {from_grade.value} to {to_grade.value}',
                'new_grade': to_grade.value,
                'advancement_date': datetime.now().isoformat(),
                'assessment_summary': {
                    'overall_readiness': assessment.overall_readiness.value,
                    'subject_scores': assessment.subject_scores,
                    'strengths': assessment.strengths,
                    'growth_areas': assessment.areas_for_growth
                },
                'next_steps': self._generate_next_steps_for_new_grade(to_grade)
            }
            
        except Exception as e:
            logger.error(f"Error executing grade advancement: {e}")
            return {
                'success': False,
                'message': f'Error during grade advancement: {str(e)}',
                'recommendation': 'Contact system administrator'
            }
    
    def _generate_next_steps_for_new_grade(self, grade: GradeLevel) -> List[str]:
        """Generate next steps and recommendations for new grade level"""
        next_steps = [
            f"Begin {grade.value.replace('_', ' ').title()} curriculum and learning objectives",
            "Establish new learning routines and expectations",
            "Assess baseline performance in new grade-level standards",
            "Create individualized learning plan based on strengths and growth areas"
        ]
        
        # Add grade-specific recommendations
        if grade == GradeLevel.FIRST_GRADE:
            next_steps.extend([
                "Focus on building reading fluency and comprehension",
                "Strengthen number sense and basic addition/subtraction facts",
                "Develop independent work habits and longer attention span",
                "Build more complex social interaction skills"
            ])
        elif grade == GradeLevel.SECOND_GRADE:
            next_steps.extend([
                "Advance to more complex reading texts and genres",
                "Master place value concepts and multi-digit operations",
                "Develop scientific observation and inquiry skills",
                "Strengthen collaborative learning and communication"
            ])
        
        return next_steps
    
    def _store_assessment_results(self, assessment: PlacementAssessment):
        """Store assessment results in database for tracking"""
        with sqlite3.connect(self.memory_system.db_path) as conn:
            cursor = conn.cursor()
            
            # Store in subject mastery tracking
            for subject, score in assessment.subject_scores.items():
                cursor.execute("""
                    INSERT INTO subject_mastery_tracking
                    (student_id, grade_level, subject, concept_id, mastery_level, 
                     assessment_date, growth_trajectory)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    assessment.student_id,
                    assessment.current_grade.value,
                    subject.value,
                    f"grade_readiness_assessment_{subject.value}",
                    score / 100.0,  # Convert percentage back to decimal
                    assessment.assessment_date.isoformat(),
                    json.dumps({'readiness_status': assessment.overall_readiness.value})
                ))
            
            conn.commit()
    
    def get_grade_progression_report(self, student_id: str = "marcus") -> Dict[str, Any]:
        """Generate comprehensive grade progression report"""
        # Get current status
        current_grade = self._get_current_grade(student_id)
        
        # Get progression history
        with sqlite3.connect(self.memory_system.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT from_grade, to_grade, progression_date, readiness_score
                FROM grade_progressions
                WHERE student_id = ?
                ORDER BY progression_date
            """, (student_id,))
            
            progression_history = [
                {
                    'from_grade': row[0],
                    'to_grade': row[1],
                    'date': row[2],
                    'readiness_score': row[3]
                }
                for row in cursor.fetchall()
            ]
        
        # Get current performance
        latest_assessment = self.assess_grade_readiness(student_id)
        
        # Generate recommendations
        recommendations = self._generate_progression_recommendations(latest_assessment)
        
        return {
            'student_id': student_id,
            'current_grade': current_grade.value,
            'grade_progression_history': progression_history,
            'current_assessment': {
                'overall_readiness': latest_assessment.overall_readiness.value,
                'subject_scores': latest_assessment.subject_scores,
                'developmental_readiness': latest_assessment.developmental_readiness,
                'strengths': latest_assessment.strengths,
                'areas_for_growth': latest_assessment.areas_for_growth
            },
            'recommendations': recommendations,
            'next_assessment_date': latest_assessment.timeline_for_reassessment,
            'report_generated': datetime.now().isoformat()
        }
    
    def _generate_progression_recommendations(self, assessment: PlacementAssessment) -> List[str]:
        """Generate progression recommendations based on assessment"""
        recommendations = []
        
        if assessment.overall_readiness == ReadinessStatus.ADVANCED:
            recommendations.extend([
                "Consider acceleration or enrichment opportunities",
                "Provide advanced curriculum materials",
                "Explore independent study projects",
                "Consider grade advancement evaluation"
            ])
        elif assessment.overall_readiness == ReadinessStatus.READY:
            recommendations.extend([
                "Continue current grade progression",
                "Monitor progress regularly",
                "Provide appropriate challenges to maintain growth",
                "Prepare for next grade transition"
            ])
        elif assessment.overall_readiness == ReadinessStatus.APPROACHING:
            recommendations.extend([
                "Implement targeted interventions",
                "Increase practice time in deficit areas",
                "Provide additional scaffolding and support",
                "Monitor progress closely with frequent assessments"
            ])
        else:  # NOT_READY
            recommendations.extend([
                "Intensive intervention required",
                "Consider grade retention if patterns persist",
                "Implement comprehensive support plan",
                "Coordinate with specialists and support staff"
            ])
        
        return recommendations

# Factory function for easy integration
def create_grade_progression_system() -> GradeProgressionSystem:
    """Create and initialize the grade progression system"""
    # Create a memory system with a specific database path for the grade progression system
    memory_system = MarcusMemorySystem(db_path="grade_progression_memory.db")
    return GradeProgressionSystem(memory_system=memory_system)

# Demo function
def demo_grade_progression_system():
    """Demonstrate the grade progression system capabilities"""
    print("🎓 Grade Progression System Demo")
    print("=" * 50)
    
    # Create system
    progression_system = create_grade_progression_system()
    
    # Conduct readiness assessment
    print("\n📊 Conducting Grade Readiness Assessment...")
    assessment = progression_system.assess_grade_readiness()
    
    print(f"Current Grade: {assessment.current_grade.value}")
    print(f"Recommended Grade: {assessment.recommended_grade.value}")
    print(f"Overall Readiness: {assessment.overall_readiness.value}")
    
    print("\n📈 Subject Scores:")
    for subject, score in assessment.subject_scores.items():
        print(f"  {subject.value.replace('_', ' ').title()}: {score:.1f}%")
    
    print(f"\n💪 Strengths ({len(assessment.strengths)}):")
    for strength in assessment.strengths[:3]:  # Show first 3
        print(f"  • {strength}")
    
    print(f"\n📚 Areas for Growth ({len(assessment.areas_for_growth)}):")
    for area in assessment.areas_for_growth[:3]:  # Show first 3
        print(f"  • {area}")
    
    # Try grade advancement
    print(f"\n🚀 Attempting Grade Advancement...")
    advancement_result = progression_system.advance_grade(assessment=assessment)
    
    if advancement_result['success']:
        print(f"✅ {advancement_result['message']}")
        print(f"New Grade: {advancement_result['new_grade']}")
    else:
        print(f"❌ {advancement_result['message']}")
        if 'required_interventions' in advancement_result:
            print("Required Interventions:")
            for intervention in advancement_result['required_interventions'][:2]:
                print(f"  • {intervention}")
    
    # Generate progression report
    print(f"\n📋 Grade Progression Report...")
    report = progression_system.get_grade_progression_report()
    print(f"Student: {report['student_id']}")
    print(f"Current Grade: {report['current_grade']}")
    print(f"Progression History: {len(report['grade_progression_history'])} advancement(s)")
    print(f"Recommendations: {len(report['recommendations'])} recommendation(s)")
    
    print("\n✅ Grade Progression System Demo Complete!")

if __name__ == "__main__":
    demo_grade_progression_system()
