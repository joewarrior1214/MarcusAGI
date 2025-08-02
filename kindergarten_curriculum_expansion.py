#!/usr/bin/env python3
"""
Issue #5: Kindergarten Curriculum Expansion for Marcus AGI

This module implements comprehensive kindergarten curriculum expansion with:
1. Research-based developmental milestones for 5-6 year olds
2. Learning objectives mapped to Mr. Rogers episodes
3. Assessment rubrics for each skill area
4. Prerequisite relationship mapping
5. Multi-sensory learning activities
6. Differentiated instruction paths

Builds on existing curriculum system and integrates with daily learning loop.
"""

import json
import random
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# Developmental milestone categories based on research
class DevelopmentalDomain(Enum):
    """Developmental domains for kindergarten (5-6 years old)"""
    PHYSICAL_MOTOR = "physical_motor"
    COGNITIVE_ACADEMIC = "cognitive_academic" 
    SOCIAL_EMOTIONAL = "social_emotional"
    LANGUAGE_COMMUNICATION = "language_communication"
    CREATIVE_ARTISTIC = "creative_artistic"
    MORAL_CHARACTER = "moral_character"

class SkillLevel(Enum):
    """Skill mastery levels for assessment"""
    EMERGING = "emerging"          # 1 - Just beginning to show skill
    DEVELOPING = "developing"      # 2 - Skill is progressing with support
    PROFICIENT = "proficient"      # 3 - Demonstrates skill independently
    ADVANCED = "advanced"          # 4 - Exceeds grade-level expectations

class InstructionMode(Enum):
    """Different instruction delivery modes"""
    VISUAL = "visual"              # Charts, pictures, demonstrations
    AUDITORY = "auditory"          # Songs, stories, verbal instructions
    KINESTHETIC = "kinesthetic"    # Movement, hands-on activities
    TACTILE = "tactile"            # Touch, textures, manipulatives
    SOCIAL = "social"              # Group work, peer learning
    INDEPENDENT = "independent"    # Self-directed exploration
    CREATIVE = "creative"          # Art, imagination, expression

@dataclass
class DevelopmentalMilestone:
    """Research-based developmental milestone for 5-6 year olds"""
    id: str
    domain: DevelopmentalDomain
    milestone_text: str
    age_range: Tuple[int, int]  # months (60-72 for kindergarten)
    typical_behaviors: List[str]
    red_flags: List[str] = field(default_factory=list)
    supporting_activities: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'domain': self.domain.value,
            'milestone_text': self.milestone_text,
            'age_range': self.age_range,
            'typical_behaviors': self.typical_behaviors,
            'red_flags': self.red_flags,
            'supporting_activities': self.supporting_activities
        }

@dataclass
class AssessmentRubric:
    """Assessment rubric for skill evaluation"""
    skill_id: str
    skill_name: str
    domain: DevelopmentalDomain
    rubric_levels: Dict[SkillLevel, str]  # Level -> description
    assessment_methods: List[str]
    observable_behaviors: Dict[SkillLevel, List[str]]
    
    def evaluate_skill(self, observed_behaviors: List[str]) -> SkillLevel:
        """Evaluate skill level based on observed behaviors"""
        for level in [SkillLevel.ADVANCED, SkillLevel.PROFICIENT, SkillLevel.DEVELOPING, SkillLevel.EMERGING]:
            level_behaviors = self.observable_behaviors.get(level, [])
            matches = sum(1 for behavior in observed_behaviors if any(b.lower() in behavior.lower() for b in level_behaviors))
            if matches >= len(level_behaviors) * 0.6:  # 60% match threshold
                return level
        return SkillLevel.EMERGING

@dataclass 
class LearningObjective:
    """Enhanced learning objective with comprehensive metadata"""
    id: str
    title: str
    description: str
    domain: DevelopmentalDomain
    subject: str
    grade_level: str = "kindergarten"
    skill_level: SkillLevel = SkillLevel.DEVELOPING
    
    # Prerequisite and progression mapping
    prerequisites: List[str] = field(default_factory=list)
    leads_to: List[str] = field(default_factory=list)
    
    # Multi-sensory and differentiation
    instruction_modes: List[InstructionMode] = field(default_factory=list)
    accommodations: List[str] = field(default_factory=list)
    
    # Mr. Rogers integration
    mr_rogers_episode: Optional[str] = None
    emotional_component: str = "neutral"
    
    # Assessment
    assessment_rubric: Optional[str] = None
    success_criteria: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'domain': self.domain.value,
            'subject': self.subject,
            'grade_level': self.grade_level,
            'skill_level': self.skill_level.value,
            'prerequisites': self.prerequisites,
            'leads_to': self.leads_to,
            'instruction_modes': [mode.value for mode in self.instruction_modes],
            'accommodations': self.accommodations,
            'mr_rogers_episode': self.mr_rogers_episode,
            'emotional_component': self.emotional_component,
            'assessment_rubric': self.assessment_rubric,
            'success_criteria': self.success_criteria
        }

@dataclass
class MultiSensoryActivity:
    """Multi-sensory learning activity"""
    id: str
    name: str
    objective_ids: List[str]
    primary_modes: List[InstructionMode]
    materials_needed: List[str]
    instructions: List[str]
    adaptations: Dict[str, List[str]]  # difficulty_level -> modifications
    estimated_duration: int  # minutes
    group_size: str  # "individual", "small_group", "whole_class"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DifferentiatedPath:
    """Differentiated instruction path for different learner needs"""
    id: str
    name: str
    target_learners: List[str]  # "visual", "kinesthetic", "advanced", "struggling", etc.
    objective_sequence: List[str]  # Ordered list of objective IDs
    pacing_guide: Dict[str, int]  # objective_id -> estimated_days
    assessment_frequency: str  # "daily", "weekly", "bi-weekly"
    support_strategies: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class KindergartenCurriculumExpansion:
    """Comprehensive kindergarten curriculum with research-based milestones"""
    
    def __init__(self):
        self.developmental_milestones = self._load_developmental_milestones()
        self.learning_objectives = self._create_expanded_objectives()
        self.assessment_rubrics = self._create_assessment_rubrics()
        self.multi_sensory_activities = self._create_multi_sensory_activities()
        self.differentiated_paths = self._create_differentiated_paths()
        self.mr_rogers_mapping = self._map_mr_rogers_episodes()
        
    def _load_developmental_milestones(self) -> Dict[DevelopmentalDomain, List[DevelopmentalMilestone]]:
        """Load research-based developmental milestones for 5-6 year olds"""
        milestones = {
            DevelopmentalDomain.PHYSICAL_MOTOR: [
                DevelopmentalMilestone(
                    id="gross_motor_coordination",
                    domain=DevelopmentalDomain.PHYSICAL_MOTOR,
                    milestone_text="Demonstrates coordinated gross motor skills",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Runs smoothly with changes in direction and speed",
                        "Hops on one foot for 3-5 steps",
                        "Skips with alternating feet",
                        "Catches a ball thrown from 6 feet away",
                        "Rides a bicycle with training wheels"
                    ],
                    supporting_activities=[
                        "Playground games", "Dance and movement", "Obstacle courses"
                    ]
                ),
                DevelopmentalMilestone(
                    id="fine_motor_control",
                    domain=DevelopmentalDomain.PHYSICAL_MOTOR,
                    milestone_text="Shows refined fine motor control and hand-eye coordination",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Uses scissors to cut on curved and straight lines",
                        "Ties shoes independently",
                        "Draws recognizable people with 6+ body parts",
                        "Copies complex shapes and patterns",
                        "Uses proper pencil grip"
                    ],
                    supporting_activities=[
                        "Art projects", "Manipulative toys", "Writing practice"
                    ]
                )
            ],
            
            DevelopmentalDomain.COGNITIVE_ACADEMIC: [
                DevelopmentalMilestone(
                    id="mathematical_thinking",
                    domain=DevelopmentalDomain.COGNITIVE_ACADEMIC,
                    milestone_text="Demonstrates foundational mathematical reasoning",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Counts to 100 by 1s, 2s, 5s, and 10s",
                        "Recognizes and writes numbers 0-20",
                        "Understands concepts of addition and subtraction to 10",
                        "Identifies and creates patterns",
                        "Compares quantities using more/less/equal"
                    ],
                    supporting_activities=[
                        "Math manipulatives", "Number games", "Pattern activities"
                    ]
                ),
                DevelopmentalMilestone(
                    id="literacy_foundations",
                    domain=DevelopmentalDomain.COGNITIVE_ACADEMIC,
                    milestone_text="Shows emerging literacy skills and phonemic awareness",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Recognizes and names all 26 letters",
                        "Knows letter sounds for most consonants and short vowels",
                        "Reads simple CVC words (cat, dog, run)",
                        "Writes first name and some familiar words",
                        "Retells stories in sequence"
                    ],
                    supporting_activities=[
                        "Phonics games", "Shared reading", "Writing centers"
                    ]
                ),
                DevelopmentalMilestone(
                    id="scientific_inquiry",
                    domain=DevelopmentalDomain.COGNITIVE_ACADEMIC,
                    milestone_text="Engages in scientific thinking and exploration",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Makes predictions about outcomes",
                        "Observes and describes changes in nature",
                        "Sorts and classifies objects by multiple attributes",
                        "Asks questions about how things work",
                        "Uses simple tools for investigation"
                    ],
                    supporting_activities=[
                        "Science experiments", "Nature walks", "Investigation stations"
                    ]
                )
            ],
            
            DevelopmentalDomain.SOCIAL_EMOTIONAL: [
                DevelopmentalMilestone(
                    id="emotional_regulation",
                    domain=DevelopmentalDomain.SOCIAL_EMOTIONAL,
                    milestone_text="Develops emotional self-regulation and awareness",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Identifies and names basic emotions in self and others",
                        "Uses words to express feelings instead of acting out",
                        "Shows empathy and concern for others",
                        "Manages transitions with minimal support",
                        "Recovers from disappointment within reasonable time"
                    ],
                    supporting_activities=[
                        "Emotion identification games", "Mindfulness activities", "Social stories"
                    ]
                ),
                DevelopmentalMilestone(
                    id="social_interaction",
                    domain=DevelopmentalDomain.SOCIAL_EMOTIONAL,
                    milestone_text="Demonstrates positive social interaction skills",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Plays cooperatively with others for extended periods",
                        "Resolves conflicts using words and compromise",
                        "Shows respect for diversity and differences",
                        "Follows classroom rules and routines",
                        "Demonstrates leadership and followership"
                    ],
                    supporting_activities=[
                        "Cooperative games", "Peer problem-solving", "Group projects"
                    ]
                )
            ],
            
            DevelopmentalDomain.LANGUAGE_COMMUNICATION: [
                DevelopmentalMilestone(
                    id="oral_language",
                    domain=DevelopmentalDomain.LANGUAGE_COMMUNICATION,
                    milestone_text="Uses complex oral language for communication",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Speaks in complete sentences of 6+ words",
                        "Uses proper grammar most of the time",
                        "Tells detailed stories with beginning, middle, end",
                        "Asks and answers questions appropriately",
                        "Follows multi-step oral directions"
                    ],
                    supporting_activities=[
                        "Storytelling", "Show and tell", "Dramatic play"
                    ]
                ),
                DevelopmentalMilestone(
                    id="listening_comprehension",
                    domain=DevelopmentalDomain.LANGUAGE_COMMUNICATION,
                    milestone_text="Demonstrates active listening and comprehension",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Listens attentively to stories for 15-20 minutes",
                        "Answers questions about story details",
                        "Follows classroom discussions and contributes",
                        "Repeats instructions accurately",
                        "Shows understanding through appropriate responses"
                    ],
                    supporting_activities=[
                        "Read-alouds", "Audio stories", "Listening games"
                    ]
                )
            ],
            
            DevelopmentalDomain.CREATIVE_ARTISTIC: [
                DevelopmentalMilestone(
                    id="creative_expression",
                    domain=DevelopmentalDomain.CREATIVE_ARTISTIC,
                    milestone_text="Expresses creativity through various art forms",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Creates original artwork with details and planning",
                        "Uses variety of art materials appropriately",
                        "Sings songs and remembers lyrics",
                        "Moves rhythmically to music",
                        "Engages in dramatic play with complex scenarios"
                    ],
                    supporting_activities=[
                        "Art centers", "Music and movement", "Drama activities"
                    ]
                ),
                DevelopmentalMilestone(
                    id="aesthetic_appreciation",
                    domain=DevelopmentalDomain.CREATIVE_ARTISTIC,
                    milestone_text="Shows appreciation for beauty and artistic works",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Comments on colors, shapes, and patterns in art",
                        "Expresses preferences about music and art",
                        "Notices beauty in nature and environment",
                        "Discusses feelings evoked by artistic works",
                        "Shows respect for others' creative efforts"
                    ],
                    supporting_activities=[
                        "Art appreciation", "Museum visits", "Nature observation"
                    ]
                )
            ],
            
            DevelopmentalDomain.MORAL_CHARACTER: [
                DevelopmentalMilestone(
                    id="moral_reasoning",
                    domain=DevelopmentalDomain.MORAL_CHARACTER,
                    milestone_text="Develops basic moral reasoning and character",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Understands difference between right and wrong",
                        "Shows honesty in most situations",
                        "Demonstrates kindness and helpfulness",
                        "Takes responsibility for own actions",
                        "Shows respect for authority and rules"
                    ],
                    supporting_activities=[
                        "Character education stories", "Community service", "Moral discussions"
                    ]
                ),
                DevelopmentalMilestone(
                    id="citizenship_awareness",
                    domain=DevelopmentalDomain.MORAL_CHARACTER,
                    milestone_text="Shows awareness of community and citizenship",
                    age_range=(60, 72),
                    typical_behaviors=[
                        "Understands roles of community helpers",
                        "Shows care for classroom and school environment",
                        "Participates in group decisions and voting",
                        "Demonstrates respect for diversity",
                        "Shows concern for fairness and justice"
                    ],
                    supporting_activities=[
                        "Community helper studies", "Classroom government", "Service projects"
                    ]
                )
            ]
        }
        
        return milestones
    
    def _create_expanded_objectives(self) -> Dict[DevelopmentalDomain, List[LearningObjective]]:
        """Create comprehensive learning objectives mapped to developmental milestones"""
        objectives = {
            DevelopmentalDomain.PHYSICAL_MOTOR: [
                LearningObjective(
                    id="gross_motor_skills",
                    title="Gross Motor Coordination",
                    description="I can run, jump, hop, skip, and catch with coordination",
                    domain=DevelopmentalDomain.PHYSICAL_MOTOR,
                    subject="physical_education",
                    instruction_modes=[InstructionMode.KINESTHETIC, InstructionMode.VISUAL],
                    success_criteria=["Runs without falling", "Hops on one foot 5 times", "Catches large ball"],
                    mr_rogers_episode="Episode 1234: Moving and Playing",
                    emotional_component="confidence"
                ),
                LearningObjective(
                    id="fine_motor_precision",
                    title="Fine Motor Control",
                    description="I can use scissors, pencils, and small objects with precision",
                    domain=DevelopmentalDomain.PHYSICAL_MOTOR,
                    subject="handwriting",
                    instruction_modes=[InstructionMode.TACTILE, InstructionMode.VISUAL],
                    success_criteria=["Cuts on lines", "Draws recognizable shapes", "Proper pencil grip"],
                    accommodations=["Larger pencil grips", "Different scissors", "Extra practice time"]
                )
            ],
            
            DevelopmentalDomain.COGNITIVE_ACADEMIC: [
                LearningObjective(
                    id="number_sense_20",
                    title="Number Sense to 20",
                    description="I understand numbers, counting, and basic operations to 20",
                    domain=DevelopmentalDomain.COGNITIVE_ACADEMIC,
                    subject="mathematics",
                    prerequisites=["counting_1to10"],
                    leads_to=["addition_subtraction_10"],
                    instruction_modes=[InstructionMode.VISUAL, InstructionMode.KINESTHETIC, InstructionMode.TACTILE],
                    success_criteria=["Counts to 20", "Recognizes numerals 1-20", "Compares quantities"],
                    accommodations=["Number lines", "Manipulatives", "Visual aids"]
                ),
                LearningObjective(
                    id="phonemic_awareness",
                    title="Sound Awareness", 
                    description="I can hear and work with sounds in spoken words",
                    domain=DevelopmentalDomain.COGNITIVE_ACADEMIC,
                    subject="reading",
                    leads_to=["letter_sound_correspondence"],
                    instruction_modes=[InstructionMode.AUDITORY, InstructionMode.KINESTHETIC],
                    success_criteria=["Identifies rhyming words", "Segments words into sounds", "Blends sounds"],
                    mr_rogers_episode="Episode 1456: Language and Words"
                ),
                LearningObjective(
                    id="scientific_observation",
                    title="Scientific Observation",
                    description="I can observe, describe, and ask questions about the natural world",
                    domain=DevelopmentalDomain.COGNITIVE_ACADEMIC,
                    subject="science",
                    instruction_modes=[InstructionMode.KINESTHETIC, InstructionMode.VISUAL, InstructionMode.TACTILE],
                    success_criteria=["Makes detailed observations", "Asks relevant questions", "Records findings"],
                    accommodations=["Picture observation sheets", "Magnifying tools", "Partner support"]
                )
            ],
            
            DevelopmentalDomain.SOCIAL_EMOTIONAL: [
                LearningObjective(
                    id="emotion_identification",
                    title="Feeling Words",
                    description="I can identify and name emotions in myself and others",
                    domain=DevelopmentalDomain.SOCIAL_EMOTIONAL,
                    subject="social_emotional_learning",
                    leads_to=["emotion_regulation", "empathy_development"],
                    instruction_modes=[InstructionMode.VISUAL, InstructionMode.SOCIAL, InstructionMode.AUDITORY],
                    success_criteria=["Names 5+ emotions", "Identifies emotions in pictures", "Describes own feelings"],
                    mr_rogers_episode="Episode 1478: Angry Feelings",
                    emotional_component="self_awareness"
                ),
                LearningObjective(
                    id="conflict_resolution",
                    title="Problem Solving with Friends",
                    description="I can solve problems with friends using words and compromise",
                    domain=DevelopmentalDomain.SOCIAL_EMOTIONAL,
                    subject="social_skills",
                    prerequisites=["emotion_identification"],
                    instruction_modes=[InstructionMode.SOCIAL, InstructionMode.AUDITORY],
                    success_criteria=["Uses words not actions", "Takes turns speaking", "Finds compromises"],
                    mr_rogers_episode="Episode 1479: Making Friends"
                )
            ],
            
            DevelopmentalDomain.LANGUAGE_COMMUNICATION: [
                LearningObjective(
                    id="storytelling_skills",
                    title="Telling Stories",
                    description="I can tell stories with a beginning, middle, and end",
                    domain=DevelopmentalDomain.LANGUAGE_COMMUNICATION,
                    subject="oral_language",
                    instruction_modes=[InstructionMode.AUDITORY, InstructionMode.VISUAL, InstructionMode.SOCIAL],
                    success_criteria=["Includes story elements", "Uses descriptive words", "Maintains sequence"],
                    accommodations=["Story maps", "Picture prompts", "Recording devices"],
                    mr_rogers_episode="Episode 1567: Stories and Imagination"
                ),
                LearningObjective(
                    id="listening_comprehension",
                    title="Active Listening",
                    description="I can listen carefully and understand what others are saying",
                    domain=DevelopmentalDomain.LANGUAGE_COMMUNICATION,
                    subject="listening_skills",
                    instruction_modes=[InstructionMode.AUDITORY, InstructionMode.VISUAL],
                    success_criteria=["Follows 3-step directions", "Answers story questions", "Shows attention behaviors"],
                    accommodations=["Visual supports", "Reduced distractions", "Movement breaks"]
                )
            ],
            
            DevelopmentalDomain.CREATIVE_ARTISTIC: [
                LearningObjective(
                    id="artistic_expression",
                    title="Creating Art",
                    description="I can create original artwork using various materials and techniques",
                    domain=DevelopmentalDomain.CREATIVE_ARTISTIC,
                    subject="visual_arts",
                    instruction_modes=[InstructionMode.VISUAL, InstructionMode.TACTILE, InstructionMode.KINESTHETIC],
                    success_criteria=["Uses multiple materials", "Shows creativity", "Explains artwork"],
                    accommodations=["Adaptive tools", "Alternative materials", "Extra time"]
                ),
                LearningObjective(
                    id="musical_participation",
                    title="Music and Movement",
                    description="I can sing songs, keep rhythm, and move to music",
                    domain=DevelopmentalDomain.CREATIVE_ARTISTIC,
                    subject="music",
                    instruction_modes=[InstructionMode.AUDITORY, InstructionMode.KINESTHETIC],
                    success_criteria=["Sings simple songs", "Keeps steady beat", "Moves rhythmically"],
                    mr_rogers_episode="Episode 1345: Music and Feelings"
                )
            ],
            
            DevelopmentalDomain.MORAL_CHARACTER: [
                LearningObjective(
                    id="honesty_practice",
                    title="Being Truthful",
                    description="I understand the importance of honesty and telling the truth",
                    domain=DevelopmentalDomain.MORAL_CHARACTER,
                    subject="character_education",
                    instruction_modes=[InstructionMode.SOCIAL, InstructionMode.AUDITORY],
                    success_criteria=["Tells truth even when difficult", "Admits mistakes", "Understands consequences"],
                    mr_rogers_episode="Episode 1640: Making Mistakes"
                ),
                LearningObjective(
                    id="community_helpers",
                    title="People Who Help Us",
                    description="I know about different jobs and how people help our community",
                    domain=DevelopmentalDomain.MORAL_CHARACTER,
                    subject="social_studies",
                    instruction_modes=[InstructionMode.VISUAL, InstructionMode.SOCIAL, InstructionMode.AUDITORY],
                    success_criteria=["Names 5+ community helpers", "Describes their jobs", "Shows appreciation"],
                    accommodations=["Picture books", "Field trips", "Guest speakers"]
                )
            ]
        }
        
        return objectives
    
    def _create_assessment_rubrics(self) -> Dict[str, AssessmentRubric]:
        """Create detailed assessment rubrics for each skill area"""
        rubrics = {}
        
        # Example rubric for number sense
        rubrics["number_sense_20"] = AssessmentRubric(
            skill_id="number_sense_20",
            skill_name="Number Sense to 20",
            domain=DevelopmentalDomain.COGNITIVE_ACADEMIC,
            rubric_levels={
                SkillLevel.EMERGING: "Counts to 10 with support, recognizes some numerals",
                SkillLevel.DEVELOPING: "Counts to 15 independently, recognizes numerals 1-10",
                SkillLevel.PROFICIENT: "Counts to 20 accurately, recognizes all numerals 1-20, compares quantities",
                SkillLevel.ADVANCED: "Counts beyond 20, understands place value concepts, mental math strategies"
            },
            assessment_methods=["Observation", "One-on-one assessment", "Portfolio work", "Performance tasks"],
            observable_behaviors={
                SkillLevel.EMERGING: ["Points to numbers while counting", "Skips numbers occasionally", "Needs prompts"],
                SkillLevel.DEVELOPING: ["Counts accurately to 15", "Recognizes most single-digit numbers", "Uses fingers for support"],
                SkillLevel.PROFICIENT: ["Counts fluently to 20", "Identifies all numerals quickly", "Compares groups accurately"],
                SkillLevel.ADVANCED: ["Counts by 2s, 5s, 10s", "Understands teen numbers", "Solves simple word problems"]
            }
        )
        
        # Example rubric for emotional regulation
        rubrics["emotion_identification"] = AssessmentRubric(
            skill_id="emotion_identification",
            skill_name="Emotion Identification",
            domain=DevelopmentalDomain.SOCIAL_EMOTIONAL,
            rubric_levels={
                SkillLevel.EMERGING: "Names happy and sad, shows basic emotion recognition",
                SkillLevel.DEVELOPING: "Names 3-4 emotions, identifies emotions in pictures sometimes",
                SkillLevel.PROFICIENT: "Names 5+ emotions consistently, identifies emotions in self and others",
                SkillLevel.ADVANCED: "Names complex emotions, understands emotion triggers, helps others identify feelings"
            },
            assessment_methods=["Observation during social interactions", "Emotion picture tasks", "Anecdotal records"],
            observable_behaviors={
                SkillLevel.EMERGING: ["Points to happy/sad faces", "Uses basic emotion words", "Shows some awareness"],
                SkillLevel.DEVELOPING: ["Names mad, scared, excited", "Identifies emotions in books", "Describes own feelings sometimes"],
                SkillLevel.PROFICIENT: ["Consistently names emotions", "Identifies emotions in peers", "Uses emotion words appropriately"],
                SkillLevel.ADVANCED: ["Discusses emotion intensity", "Explains emotion causes", "Supports others emotionally"]
            }
        )
        
        # Add more rubrics for other key objectives...
        # (In a full implementation, we'd create rubrics for all objectives)
        
        return rubrics
    
    def _create_multi_sensory_activities(self) -> List[MultiSensoryActivity]:
        """Create multi-sensory learning activities"""
        activities = [
            MultiSensoryActivity(
                id="number_hunt_adventure",
                name="Number Hunt Adventure",
                objective_ids=["number_sense_20"],
                primary_modes=[InstructionMode.KINESTHETIC, InstructionMode.VISUAL, InstructionMode.TACTILE],
                materials_needed=["Number cards", "Clipboards", "Pencils", "Small manipulatives"],
                instructions=[
                    "Hide number cards around the classroom",
                    "Students hunt for numbers in sequence",
                    "When found, they trace the number with finger",
                    "Count out that many manipulatives",
                    "Record findings on clipboard"
                ],
                adaptations={
                    "struggling": ["Use numbers 1-10 only", "Provide number line reference", "Work with buddy"],
                    "advanced": ["Use numbers to 50", "Include number word cards", "Create number sentences"],
                    "visual": ["Use color-coded numbers", "Include picture representations"],
                    "kinesthetic": ["Add movement between stations", "Include jumping/clapping counting"]
                },
                estimated_duration=25,
                group_size="small_group"
            ),
            
            MultiSensoryActivity(
                id="emotion_body_mapping",
                name="Feelings in My Body",
                objective_ids=["emotion_identification"],
                primary_modes=[InstructionMode.VISUAL, InstructionMode.KINESTHETIC, InstructionMode.TACTILE],
                materials_needed=["Body outline sheets", "Colored pencils", "Emotion cards", "Mirrors"],
                instructions=[
                    "Look at emotion cards and discuss feelings",
                    "Use mirrors to practice emotion faces",
                    "Color body outline to show where you feel emotions",
                    "Share and discuss with classmates"
                ],
                adaptations={
                    "struggling": ["Start with 3 basic emotions", "Use photos of real children", "One-on-one support"],
                    "advanced": ["Include complex emotions", "Discuss emotion intensity", "Create emotion stories"],
                    "visual": ["Use picture emotion cards", "Color-coded feeling zones"],
                    "tactile": ["Use textured materials", "Add sensory bottles for emotions"]
                },
                estimated_duration=30,
                group_size="individual"
            ),
            
            MultiSensoryActivity(
                id="sound_story_creation",
                name="Make-Your-Own Sound Story",
                objective_ids=["phonemic_awareness", "storytelling_skills"],
                primary_modes=[InstructionMode.AUDITORY, InstructionMode.KINESTHETIC, InstructionMode.CREATIVE],
                materials_needed=["Simple instruments", "Sound makers", "Story picture cards", "Recording device"],
                instructions=[
                    "Choose picture cards for story sequence",
                    "Add sound effects for each story part",
                    "Practice telling story with sounds",
                    "Record final performance"
                ],
                adaptations={
                    "struggling": ["Use 3-part stories", "Provide sound suggestions", "Partner support"],
                    "advanced": ["Create original stories", "Add multiple sound layers", "Teach story to others"],
                    "auditory": ["Focus on sound patterns", "Include rhyming elements"],
                    "kinesthetic": ["Add movement to sounds", "Use whole body instruments"]
                },
                estimated_duration=35,
                group_size="small_group"
            )
        ]
        
        return activities
    
    def _create_differentiated_paths(self) -> List[DifferentiatedPath]:
        """Create differentiated instruction paths for different learner needs"""
        paths = [
            DifferentiatedPath(
                id="visual_learner_path",
                name="Visual Learning Journey",
                target_learners=["visual", "processing_differences", "English_language_learners"],
                objective_sequence=[
                    "emotion_identification", "number_sense_20", "phonemic_awareness", 
                    "artistic_expression", "scientific_observation"
                ],
                pacing_guide={
                    "emotion_identification": 5,
                    "number_sense_20": 10,
                    "phonemic_awareness": 8,
                    "artistic_expression": 6,
                    "scientific_observation": 7
                },
                assessment_frequency="weekly",
                support_strategies=[
                    "Visual schedules and cues",
                    "Graphic organizers",
                    "Picture-supported instructions",
                    "Color-coding systems",
                    "Mind mapping techniques"
                ]
            ),
            
            DifferentiatedPath(
                id="kinesthetic_learner_path", 
                name="Movement-Based Learning",
                target_learners=["kinesthetic", "attention_differences", "high_energy"],
                objective_sequence=[
                    "gross_motor_skills", "number_sense_20", "conflict_resolution",
                    "musical_participation", "scientific_observation"
                ],
                pacing_guide={
                    "gross_motor_skills": 4,
                    "number_sense_20": 12,
                    "conflict_resolution": 8,
                    "musical_participation": 5,
                    "scientific_observation": 8
                },
                assessment_frequency="bi-weekly",
                support_strategies=[
                    "Movement breaks every 15 minutes",
                    "Standing/flexible seating options",
                    "Hands-on manipulatives",
                    "Learning through games",
                    "Physical demonstration opportunities"
                ]
            ),
            
            DifferentiatedPath(
                id="advanced_learner_path",
                name="Enrichment and Extension",
                target_learners=["advanced", "gifted", "early_achievers"],
                objective_sequence=[
                    "number_sense_20", "storytelling_skills", "scientific_observation",
                    "artistic_expression", "honesty_practice"
                ],
                pacing_guide={
                    "number_sense_20": 6,
                    "storytelling_skills": 8,
                    "scientific_observation": 10,
                    "artistic_expression": 7,
                    "honesty_practice": 5
                },
                assessment_frequency="daily",
                support_strategies=[
                    "Independent projects",
                    "Peer teaching opportunities",
                    "Complex problem-solving tasks",
                    "Choice in learning topics",
                    "Accelerated pacing when appropriate"
                ]
            ),
            
            DifferentiatedPath(
                id="support_intensive_path",
                name="Foundational Skills Building",
                target_learners=["struggling", "developmental_delays", "intensive_support"],
                objective_sequence=[
                    "gross_motor_skills", "emotion_identification", "fine_motor_precision",
                    "listening_comprehension", "community_helpers"
                ],
                pacing_guide={
                    "gross_motor_skills": 8,
                    "emotion_identification": 10,
                    "fine_motor_precision": 12,
                    "listening_comprehension": 10,
                    "community_helpers": 8
                },
                assessment_frequency="daily",
                support_strategies=[
                    "Task analysis and small steps",
                    "Frequent positive reinforcement",
                    "Multi-sensory approaches",
                    "Peer buddy system",
                    "Extended practice time"
                ]
            )
        ]
        
        return paths
    
    def _map_mr_rogers_episodes(self) -> Dict[str, List[str]]:
        """Map Mr. Rogers episodes to learning objectives"""
        mapping = {
            "Episode 1478: Angry Feelings": ["emotion_identification", "conflict_resolution"],
            "Episode 1479: Making Friends": ["conflict_resolution", "community_helpers"],
            "Episode 1456: Language and Words": ["phonemic_awareness", "storytelling_skills"],
            "Episode 1567: Stories and Imagination": ["storytelling_skills", "artistic_expression"],
            "Episode 1345: Music and Feelings": ["musical_participation", "emotion_identification"],
            "Episode 1640: Making Mistakes": ["honesty_practice"],
            "Episode 1234: Moving and Playing": ["gross_motor_skills"],
            "Episode 1065: What Makes You Special": ["artistic_expression", "honesty_practice"]
        }
        
        return mapping
    
    def get_developmental_milestone_report(self, domain: Optional[DevelopmentalDomain] = None) -> Dict[str, Any]:
        """Generate developmental milestone report"""
        if domain:
            milestones = self.developmental_milestones.get(domain, [])
            return {
                "domain": domain.value,
                "milestones": [milestone.to_dict() for milestone in milestones],
                "total_milestones": len(milestones)
            }
        else:
            all_milestones = {}
            total = 0
            for dom, miles in self.developmental_milestones.items():
                all_milestones[dom.value] = [m.to_dict() for m in miles]
                total += len(miles)
            
            return {
                "all_domains": all_milestones,
                "total_milestones": total,
                "domains_covered": len(self.developmental_milestones)
            }
    
    def get_objective_progression_map(self, objective_id: str) -> Dict[str, Any]:
        """Get prerequisite and progression mapping for an objective"""
        # Find the objective across all domains
        target_objective = None
        for domain_objectives in self.learning_objectives.values():
            for obj in domain_objectives:
                if obj.id == objective_id:
                    target_objective = obj
                    break
            if target_objective:
                break
        
        if not target_objective:
            return {"error": f"Objective {objective_id} not found"}
        
        return {
            "objective": target_objective.to_dict(),
            "prerequisites": target_objective.prerequisites,
            "leads_to": target_objective.leads_to,
            "suggested_activities": [
                activity.name for activity in self.multi_sensory_activities 
                if objective_id in activity.objective_ids
            ],
            "assessment_rubric": self.assessment_rubrics.get(objective_id)
        }
    
    def generate_differentiated_lesson_plan(self, learner_profile: List[str], objectives: List[str]) -> Dict[str, Any]:
        """Generate a differentiated lesson plan based on learner profile"""
        # Find the best matching differentiated path
        best_path = None
        max_matches = 0
        
        for path in self.differentiated_paths:
            matches = len(set(learner_profile) & set(path.target_learners))
            if matches > max_matches:
                max_matches = matches
                best_path = path
        
        if not best_path:
            best_path = self.differentiated_paths[0]  # Default to first path
        
        # Select activities that match the objectives and path
        relevant_activities = [
            activity for activity in self.multi_sensory_activities
            if any(obj_id in activity.objective_ids for obj_id in objectives)
        ]
        
        # Apply adaptations based on learner profile
        adapted_activities = []
        for activity in relevant_activities:
            adapted_activity = activity.to_dict()
            for profile_type in learner_profile:
                if profile_type in activity.adaptations:
                    adapted_activity["adaptations_applied"] = activity.adaptations[profile_type]
            adapted_activities.append(adapted_activity)
        
        return {
            "learner_profile": learner_profile,
            "differentiated_path": best_path.to_dict(),
            "lesson_objectives": objectives,
            "recommended_activities": adapted_activities,
            "support_strategies": best_path.support_strategies,
            "assessment_frequency": best_path.assessment_frequency,
            "estimated_duration": sum(activity["estimated_duration"] for activity in adapted_activities)
        }
    
    def assess_student_progress(self, objective_id: str, observed_behaviors: List[str]) -> Dict[str, Any]:
        """Assess student progress using rubrics"""
        rubric = self.assessment_rubrics.get(objective_id)
        if not rubric:
            return {"error": f"No rubric found for objective {objective_id}"}
        
        assessed_level = rubric.evaluate_skill(observed_behaviors)
        
        return {
            "objective_id": objective_id,
            "assessed_level": assessed_level.value,
            "rubric_description": rubric.rubric_levels[assessed_level],
            "observed_behaviors": observed_behaviors,
            "next_steps": self._get_next_steps(objective_id, assessed_level),
            "assessment_date": datetime.now().isoformat()
        }
    
    def _get_next_steps(self, objective_id: str, current_level: SkillLevel) -> List[str]:
        """Get suggested next steps based on current skill level"""
        next_steps = {
            SkillLevel.EMERGING: [
                "Provide additional scaffolding and support",
                "Break skills into smaller components",
                "Increase practice opportunities",
                "Use multi-sensory approaches"
            ],
            SkillLevel.DEVELOPING: [
                "Continue regular practice with support",
                "Gradually reduce scaffolding",
                "Provide peer learning opportunities",
                "Celebrate progress made"
            ],
            SkillLevel.PROFICIENT: [
                "Provide opportunities for application",
                "Introduce extension activities",
                "Encourage peer teaching",
                "Consider advancing to next objective"
            ],
            SkillLevel.ADVANCED: [
                "Provide enrichment opportunities",
                "Increase complexity and challenge",
                "Leadership and mentoring roles",
                "Independent project work"
            ]
        }
        
        return next_steps.get(current_level, ["Continue current instructional approach"])

# Factory function for integration with existing systems
def create_expanded_kindergarten_curriculum() -> KindergartenCurriculumExpansion:
    """Create the expanded kindergarten curriculum system"""
    return KindergartenCurriculumExpansion()

# Demo and testing functions
def demo_curriculum_expansion():
    """Demonstrate the expanded curriculum capabilities"""
    print("🎓 Issue #5 Demo: Kindergarten Curriculum Expansion")
    print("=" * 60)
    
    curriculum = create_expanded_kindergarten_curriculum()
    
    # Show developmental milestones
    print("\n📊 Developmental Milestones Summary:")
    report = curriculum.get_developmental_milestone_report()
    for domain, milestones in report["all_domains"].items():
        print(f"  {domain}: {len(milestones)} milestones")
    
    # Show objective progression
    print("\n🎯 Objective Progression Example (Number Sense):")
    progression = curriculum.get_objective_progression_map("number_sense_20")
    if "objective" in progression:
        obj = progression["objective"]
        print(f"  Title: {obj['title']}")
        print(f"  Prerequisites: {obj['prerequisites']}")
        print(f"  Leads to: {obj['leads_to']}")
        print(f"  Instruction modes: {obj['instruction_modes']}")
    
    # Show differentiated lesson plan
    print("\n🎨 Differentiated Lesson Plan Example:")
    lesson = curriculum.generate_differentiated_lesson_plan(
        learner_profile=["visual", "English_language_learners"],
        objectives=["emotion_identification", "number_sense_20"]
    )
    print(f"  Path: {lesson['differentiated_path']['name']}")
    print(f"  Activities: {len(lesson['recommended_activities'])}")
    print(f"  Duration: {lesson['estimated_duration']} minutes")
    
    # Show assessment example
    print("\n📋 Assessment Example:")
    assessment = curriculum.assess_student_progress(
        "emotion_identification",
        ["Names happy, sad, mad", "Points to emotions in pictures", "Describes own feelings sometimes"]
    )
    if "assessed_level" in assessment:
        print(f"  Level: {assessment['assessed_level']}")
        print(f"  Description: {assessment['rubric_description']}")
        print(f"  Next steps: {assessment['next_steps'][0]}")
    
    print(f"\n✅ Curriculum Expansion Complete!")
    print(f"   📚 {report['total_milestones']} developmental milestones")
    print(f"   🎯 {sum(len(objs) for objs in curriculum.learning_objectives.values())} learning objectives")
    print(f"   🎨 {len(curriculum.multi_sensory_activities)} multi-sensory activities")
    print(f"   🛤️  {len(curriculum.differentiated_paths)} differentiated paths")
    print(f"   📺 {len(curriculum.mr_rogers_mapping)} Mr. Rogers episodes mapped")

if __name__ == "__main__":
    demo_curriculum_expansion()
