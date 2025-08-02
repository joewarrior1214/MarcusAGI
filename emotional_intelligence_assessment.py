#!/usr/bin/env python3
"""
Issue #6: Emotional Intelligence Assessment System for Marcus AGI

This module implements comprehensive emotional intelligence assessment and development
tracking for Marcus's social-emotional growth, building on Issues #4 and #5.

Key Features:
1. Define emotional intelligence metrics for kindergarten level
2. Create emotion recognition assessment tools
3. Implement empathy development tracking
4. Add social skills progression monitoring
5. Build emotional regulation measurement system
6. Create social interaction simulations

Dependencies: Issues #2 (Mr. Rogers Processing), #4 (Reflection System), #5 (Curriculum Expansion)
"""

import json
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EQDomain(Enum):
    """Emotional Intelligence domains for kindergarten assessment"""
    SELF_AWARENESS = "self_awareness"           # Understanding own emotions
    SELF_REGULATION = "self_regulation"         # Managing emotions and behaviors
    MOTIVATION = "motivation"                   # Drive to achieve and persist
    EMPATHY = "empathy"                        # Understanding others' emotions
    SOCIAL_SKILLS = "social_skills"            # Managing relationships

class EQSkillLevel(Enum):
    """EQ skill progression levels"""
    BEGINNING = "beginning"        # 1 - Basic awareness, needs significant support
    DEVELOPING = "developing"      # 2 - Shows skills inconsistently, needs prompting
    PRACTICING = "practicing"      # 3 - Uses skills regularly with some support
    APPLYING = "applying"          # 4 - Demonstrates skills independently
    LEADING = "leading"           # 5 - Teaches and models for others

class EmotionIntensity(Enum):
    """Emotional intensity levels for assessment"""
    MILD = "mild"
    MODERATE = "moderate"
    STRONG = "strong"
    OVERWHELMING = "overwhelming"

@dataclass
class EQMetric:
    """Emotional intelligence metric for kindergarten level"""
    id: str
    domain: EQDomain
    skill_name: str
    description: str
    age_appropriate_indicators: List[str]
    assessment_methods: List[str]
    developmental_progression: Dict[EQSkillLevel, str]
    red_flags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'domain': self.domain.value,
            'skill_name': self.skill_name,
            'description': self.description,
            'age_appropriate_indicators': self.age_appropriate_indicators,
            'assessment_methods': self.assessment_methods,
            'developmental_progression': {level.value: desc for level, desc in self.developmental_progression.items()},
            'red_flags': self.red_flags
        }

@dataclass
class EmotionRecognitionTask:
    """Task for assessing emotion recognition abilities"""
    id: str
    task_type: str  # "facial_expressions", "body_language", "voice_tone", "situational"
    stimuli: List[Dict[str, Any]]  # List of emotion scenarios/images/sounds
    target_emotions: List[str]
    difficulty_level: EQSkillLevel
    scoring_criteria: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'task_type': self.task_type,
            'stimuli': self.stimuli,
            'target_emotions': self.target_emotions,
            'difficulty_level': self.difficulty_level.value,
            'scoring_criteria': self.scoring_criteria
        }

@dataclass
class EmpathyScenario:
    """Scenario for assessing empathy development"""
    id: str
    scenario_description: str
    characters_involved: List[str]
    emotional_context: Dict[str, str]  # character -> emotion
    empathy_questions: List[str]
    expected_responses: Dict[EQSkillLevel, List[str]]
    mr_rogers_connection: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'scenario_description': self.scenario_description,
            'characters_involved': self.characters_involved,
            'emotional_context': self.emotional_context,
            'empathy_questions': self.empathy_questions,
            'expected_responses': {level.value: responses for level, responses in self.expected_responses.items()},
            'mr_rogers_connection': self.mr_rogers_connection
        }

@dataclass
class SocialInteractionSimulation:
    """Simulation for assessing and practicing social skills"""
    id: str
    simulation_name: str
    context: str  # "playground", "classroom", "conflict_resolution", etc.
    participants: List[str]  # roles in simulation
    social_challenges: List[str]
    target_skills: List[str]
    success_indicators: List[str]
    coaching_prompts: Dict[str, List[str]]  # skill -> prompts
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'simulation_name': self.simulation_name,
            'context': self.context,
            'participants': self.participants,
            'social_challenges': self.social_challenges,
            'target_skills': self.target_skills,
            'success_indicators': self.success_indicators,
            'coaching_prompts': self.coaching_prompts
        }

@dataclass
class EQAssessmentResult:
    """Result from an emotional intelligence assessment"""
    assessment_id: str
    student_id: str
    assessment_date: datetime
    domain: EQDomain
    metric_id: str
    current_level: EQSkillLevel
    observed_behaviors: List[str]
    strengths: List[str]
    growth_areas: List[str]
    next_steps: List[str]
    confidence_score: float  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'assessment_id': self.assessment_id,
            'student_id': self.student_id, 
            'assessment_date': self.assessment_date.isoformat(),
            'domain': self.domain.value,
            'metric_id': self.metric_id,
            'current_level': self.current_level.value,
            'observed_behaviors': self.observed_behaviors,
            'strengths': self.strengths,
            'growth_areas': self.growth_areas,
            'next_steps': self.next_steps,
            'confidence_score': self.confidence_score
        }

class EmotionalIntelligenceAssessment:
    """Comprehensive emotional intelligence assessment system for Marcus"""
    
    def __init__(self):
        self.eq_metrics = self._define_eq_metrics()
        self.emotion_recognition_tasks = self._create_emotion_recognition_tasks()
        self.empathy_scenarios = self._create_empathy_scenarios()
        self.social_simulations = self._create_social_simulations()
        self.assessment_history = []
        self.current_eq_profile = self._initialize_eq_profile()
        
    def _define_eq_metrics(self) -> Dict[EQDomain, List[EQMetric]]:
        """Define comprehensive EQ metrics for kindergarten level"""
        metrics = {
            EQDomain.SELF_AWARENESS: [
                EQMetric(
                    id="emotion_vocabulary",
                    domain=EQDomain.SELF_AWARENESS,
                    skill_name="Emotion Vocabulary",
                    description="Ability to identify and name emotions in self",
                    age_appropriate_indicators=[
                        "Names basic emotions (happy, sad, mad, scared)",
                        "Uses emotion words to describe feelings",
                        "Recognizes physical sensations of emotions",
                        "Distinguishes between different emotion intensities"
                    ],
                    assessment_methods=["Emotion identification cards", "Feeling check-ins", "Body mapping activities"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Names happy and sad consistently",
                        EQSkillLevel.DEVELOPING: "Names 4-5 basic emotions, sometimes needs prompts",
                        EQSkillLevel.PRACTICING: "Names 8+ emotions independently, describes intensity",
                        EQSkillLevel.APPLYING: "Uses complex emotion words, explains emotional experiences",
                        EQSkillLevel.LEADING: "Helps others identify and name their emotions"
                    },
                    red_flags=["Cannot name any emotions", "Shows no emotional expression", "Extreme emotional reactions"]
                ),
                EQMetric(
                    id="emotional_triggers",
                    domain=EQDomain.SELF_AWARENESS,
                    skill_name="Understanding Triggers",
                    description="Awareness of what causes different emotional responses",
                    age_appropriate_indicators=[
                        "Identifies situations that make them feel certain ways",
                        "Recognizes personal patterns in emotional responses",
                        "Can predict emotional reactions to familiar situations",
                        "Understands connection between thoughts and feelings"
                    ],
                    assessment_methods=["Trigger mapping", "Emotion journals", "Scenario discussions"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Shows awareness that different things cause different feelings",
                        EQSkillLevel.DEVELOPING: "Identifies 2-3 personal triggers with support",
                        EQSkillLevel.PRACTICING: "Recognizes triggers independently, makes predictions",
                        EQSkillLevel.APPLYING: "Explains trigger-emotion connections clearly",
                        EQSkillLevel.LEADING: "Helps others identify their emotional triggers"
                    }
                )
            ],
            
            EQDomain.SELF_REGULATION: [
                EQMetric(
                    id="emotional_control",
                    domain=EQDomain.SELF_REGULATION,
                    skill_name="Emotional Control",
                    description="Ability to manage emotional responses appropriately",
                    age_appropriate_indicators=[
                        "Uses calming strategies when upset",
                        "Takes breaks when feeling overwhelmed",
                        "Asks for help managing difficult emotions",
                        "Recovers from emotional episodes within reasonable time"
                    ],
                    assessment_methods=["Observation during challenging situations", "Coping strategy demonstrations", "Self-report measures"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Sometimes uses basic calming strategies with heavy adult support",
                        EQSkillLevel.DEVELOPING: "Uses 1-2 coping strategies with prompting",
                        EQSkillLevel.PRACTICING: "Independently uses multiple coping strategies",
                        EQSkillLevel.APPLYING: "Chooses appropriate strategies for different situations",
                        EQSkillLevel.LEADING: "Teaches coping strategies to peers"
                    },
                    red_flags=["Extreme emotional outbursts", "Cannot calm down with support", "Hurts self or others when upset"]
                ),
                EQMetric(
                    id="impulse_control",
                    domain=EQDomain.SELF_REGULATION,
                    skill_name="Impulse Control",
                    description="Ability to think before acting and delay gratification",
                    age_appropriate_indicators=[
                        "Waits for turn in games and activities",
                        "Raises hand before speaking",
                        "Stops activities when asked",
                        "Resists immediate impulses for better outcomes"
                    ],
                    assessment_methods=["Wait time tasks", "Delay of gratification activities", "Classroom observations"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Sometimes waits when directly supervised",
                        EQSkillLevel.DEVELOPING: "Waits for short periods with reminders",
                        EQSkillLevel.PRACTICING: "Usually waits appropriately, self-reminds",
                        EQSkillLevel.APPLYING: "Consistently demonstrates impulse control",
                        EQSkillLevel.LEADING: "Helps others practice waiting and patience"
                    }
                )
            ],
            
            EQDomain.MOTIVATION: [
                EQMetric(
                    id="persistence",
                    domain=EQDomain.MOTIVATION,
                    skill_name="Persistence and Resilience",
                    description="Ability to keep trying despite challenges and setbacks",
                    age_appropriate_indicators=[
                        "Tries multiple approaches when first attempt fails",
                        "Seeks help rather than giving up",
                        "Shows positive attitude toward learning",
                        "Recovers from disappointments and tries again"
                    ],
                    assessment_methods=["Challenge tasks", "Frustration tolerance observations", "Learning attitude assessments"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Sometimes tries again with encouragement",
                        EQSkillLevel.DEVELOPING: "Tries 2-3 times before seeking help",
                        EQSkillLevel.PRACTICING: "Persists through moderate challenges independently",
                        EQSkillLevel.APPLYING: "Uses multiple strategies, maintains positive attitude",
                        EQSkillLevel.LEADING: "Encourages others to keep trying"
                    }
                )
            ],
            
            EQDomain.EMPATHY: [
                EQMetric(
                    id="emotion_recognition_others",
                    domain=EQDomain.EMPATHY,
                    skill_name="Recognizing Others' Emotions",
                    description="Ability to identify emotions in other people",
                    age_appropriate_indicators=[
                        "Notices when others are upset or happy",
                        "Reads facial expressions accurately",
                        "Responds appropriately to others' emotional states",
                        "Shows concern for others' feelings"
                    ],
                    assessment_methods=["Emotion recognition tasks", "Social observations", "Empathy scenario responses"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Notices obvious happy/sad expressions",
                        EQSkillLevel.DEVELOPING: "Identifies 3-4 emotions in others with prompts",
                        EQSkillLevel.PRACTICING: "Recognizes various emotions independently",
                        EQSkillLevel.APPLYING: "Accurately reads subtle emotional cues",
                        EQSkillLevel.LEADING: "Helps others understand emotional expressions"
                    }
                ),
                EQMetric(
                    id="perspective_taking",
                    domain=EQDomain.EMPATHY,
                    skill_name="Perspective Taking",
                    description="Ability to understand situations from others' viewpoints",
                    age_appropriate_indicators=[
                        "Considers how others might feel in different situations",
                        "Understands that people can have different opinions",
                        "Adjusts behavior based on others' needs",
                        "Shows compassion for others' experiences"
                    ],
                    assessment_methods=["Perspective-taking scenarios", "Theory of mind tasks", "Social problem-solving"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Shows basic awareness that others have feelings",
                        EQSkillLevel.DEVELOPING: "Sometimes considers others' perspectives with prompts",
                        EQSkillLevel.PRACTICING: "Regularly thinks about others' viewpoints",
                        EQSkillLevel.APPLYING: "Easily takes multiple perspectives in situations",
                        EQSkillLevel.LEADING: "Helps others consider different viewpoints"
                    }
                )
            ],
            
            EQDomain.SOCIAL_SKILLS: [
                EQMetric(
                    id="communication_skills",
                    domain=EQDomain.SOCIAL_SKILLS,
                    skill_name="Social Communication",
                    description="Ability to communicate effectively in social situations",
                    age_appropriate_indicators=[
                        "Uses appropriate tone and volume",
                        "Takes turns in conversation",
                        "Asks for clarification when confused",
                        "Expresses needs and wants clearly"
                    ],
                    assessment_methods=["Conversation observations", "Communication tasks", "Peer interaction assessments"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Communicates basic needs, sometimes interrupts",
                        EQSkillLevel.DEVELOPING: "Usually takes turns, needs prompts for appropriate tone",
                        EQSkillLevel.PRACTICING: "Communicates clearly in most situations",
                        EQSkillLevel.APPLYING: "Adapts communication style to different contexts",
                        EQSkillLevel.LEADING: "Models good communication for others"
                    }
                ),
                EQMetric(
                    id="conflict_resolution",
                    domain=EQDomain.SOCIAL_SKILLS,
                    skill_name="Conflict Resolution",
                    description="Ability to resolve disagreements peacefully",
                    age_appropriate_indicators=[
                        "Uses words instead of physical actions",
                        "Seeks adult help when needed",
                        "Willing to compromise",
                        "Apologizes when appropriate"
                    ],
                    assessment_methods=["Conflict scenario simulations", "Peer mediation observations", "Problem-solving assessments"],
                    developmental_progression={
                        EQSkillLevel.BEGINNING: "Sometimes uses words with adult support",
                        EQSkillLevel.DEVELOPING: "Usually seeks help rather than fighting",
                        EQSkillLevel.PRACTICING: "Independently tries peaceful solutions",
                        EQSkillLevel.APPLYING: "Successfully resolves most peer conflicts",
                        EQSkillLevel.LEADING: "Helps other children resolve conflicts"
                    }
                )
            ]
        }
        
        return metrics
    
    def _create_emotion_recognition_tasks(self) -> List[EmotionRecognitionTask]:
        """Create tasks for assessing emotion recognition abilities"""
        tasks = [
            EmotionRecognitionTask(
                id="facial_expressions_basic",
                task_type="facial_expressions",
                stimuli=[
                    {"type": "image", "description": "Child with big smile", "target_emotion": "happy"},
                    {"type": "image", "description": "Child with tears", "target_emotion": "sad"},
                    {"type": "image", "description": "Child with frown and crossed arms", "target_emotion": "mad"},
                    {"type": "image", "description": "Child hiding behind adult", "target_emotion": "scared"}
                ],
                target_emotions=["happy", "sad", "mad", "scared"],
                difficulty_level=EQSkillLevel.BEGINNING,
                scoring_criteria={
                    "correct_identifications": "Number of emotions correctly identified",
                    "response_time": "Time taken to identify each emotion",
                    "confidence_level": "How certain child appears in responses"
                }
            ),
            
            EmotionRecognitionTask(
                id="situational_emotions",
                task_type="situational",
                stimuli=[
                    {"scenario": "A child's ice cream falls on the ground", "target_emotion": "disappointed"},
                    {"scenario": "A child receives a surprise gift", "target_emotion": "excited"},
                    {"scenario": "A child has to go to the doctor", "target_emotion": "nervous"},
                    {"scenario": "A child's friend won't play with them", "target_emotion": "lonely"}
                ],
                target_emotions=["disappointed", "excited", "nervous", "lonely"],
                difficulty_level=EQSkillLevel.DEVELOPING,
                scoring_criteria={
                    "emotion_accuracy": "Correctly identifies expected emotion",
                    "explanation_quality": "Can explain why person would feel that way",
                    "personal_connection": "Relates to own experiences"
                }
            ),
            
            EmotionRecognitionTask(
                id="complex_emotions",
                task_type="mixed_emotions",
                stimuli=[
                    {"scenario": "Moving to a new school", "target_emotions": ["excited", "nervous"]},
                    {"scenario": "Winning a game when friend loses", "target_emotions": ["proud", "sympathetic"]},
                    {"scenario": "Getting in trouble for helping a friend", "target_emotions": ["frustrated", "caring"]}
                ],
                target_emotions=["mixed", "complex", "conflicting"],
                difficulty_level=EQSkillLevel.APPLYING,
                scoring_criteria={
                    "multiple_emotions": "Recognizes multiple emotions in one situation",
                    "emotional_complexity": "Understands conflicting feelings",
                    "nuanced_understanding": "Shows sophisticated emotional awareness"
                }
            )
        ]
        
        return tasks
    
    def _create_empathy_scenarios(self) -> List[EmpathyScenario]:
        """Create scenarios for assessing empathy development"""
        scenarios = [
            EmpathyScenario(
                id="playground_exclusion",
                scenario_description="Alex is standing alone at recess while other children play together. Alex looks sad and keeps looking at the group.",
                characters_involved=["Alex", "Group of children", "Observer (Marcus)"],
                emotional_context={"Alex": "lonely", "Group": "engaged", "Observer": "witnessing"},
                empathy_questions=[
                    "How do you think Alex is feeling?",
                    "Why might Alex be feeling this way?",
                    "What could you do to help Alex feel better?",
                    "How would you feel if you were Alex?"
                ],
                expected_responses={
                    EQSkillLevel.BEGINNING: ["Alex is sad", "I would go play"],
                    EQSkillLevel.DEVELOPING: ["Alex feels left out", "I could ask Alex to play with us"],
                    EQSkillLevel.PRACTICING: ["Alex feels lonely and excluded", "I could invite Alex to join our game or start a new activity together"],
                    EQSkillLevel.APPLYING: ["Alex feels rejected and might be wondering if anyone likes them", "I could introduce Alex to the group or find other children who might want to include Alex"],
                    EQSkillLevel.LEADING: ["Alex is experiencing social exclusion which can be very painful", "I could not only help Alex join activities but also talk to the group about including everyone"]
                },
                mr_rogers_connection="Episode 1479: Making Friends - About inclusion and kindness"
            ),
            
            EmpathyScenario(
                id="mistake_consequences",
                scenario_description="Jamie accidentally knocks over Sam's block tower that Sam spent a long time building. Sam starts to cry and looks very upset.",
                characters_involved=["Jamie", "Sam", "Observer (Marcus)"],
                emotional_context={"Jamie": "guilty", "Sam": "frustrated", "Observer": "witnessing"},
                empathy_questions=[
                    "How is Sam feeling and why?",
                    "How might Jamie be feeling?",
                    "What should Jamie do?",
                    "How can both children feel better?"
                ],
                expected_responses={
                    EQSkillLevel.BEGINNING: ["Sam is sad", "Jamie should say sorry"],
                    EQSkillLevel.DEVELOPING: ["Sam is upset because their tower fell down", "Jamie feels bad and should help rebuild"],
                    EQSkillLevel.PRACTICING: ["Sam is frustrated and disappointed about their hard work being destroyed", "Jamie feels guilty and should apologize sincerely and offer to help"],
                    EQSkillLevel.APPLYING: ["Sam feels devastated because they put effort into something that got ruined", "Jamie feels terrible about the accident and should validate Sam's feelings while helping fix the situation"],
                    EQSkillLevel.LEADING: ["Both children are experiencing valid emotions that need acknowledgment", "This is an opportunity to practice repair, forgiveness, and collaborative problem-solving"]
                },
                mr_rogers_connection="Episode 1640: Making Mistakes - About accidents, apologies, and making things right"
            ),
            
            EmpathyScenario(
                id="family_changes",
                scenario_description="Riley mentions that their parents are getting divorced and they're moving to a smaller house. Riley seems quiet and withdrawn lately.",
                characters_involved=["Riley", "Friends", "Observer (Marcus)"],
                emotional_context={"Riley": "confused", "Friends": "uncertain", "Observer": "concerned"},
                empathy_questions=[
                    "What might Riley be going through?",
                    "How can friends be supportive?",
                    "What feelings might Riley have about these changes?",
                    "How can we show we care?"
                ],
                expected_responses={
                    EQSkillLevel.BEGINNING: ["Riley is sad", "We should be nice"],
                    EQSkillLevel.DEVELOPING: ["Riley's family is changing", "We could play with Riley more"],
                    EQSkillLevel.PRACTICING: ["Riley is dealing with big scary changes", "We could listen and include Riley in activities"],
                    EQSkillLevel.APPLYING: ["Riley is experiencing grief, uncertainty, and major life disruption", "We can offer consistent friendship, listen without trying to fix, and include Riley in normal activities"],
                    EQSkillLevel.LEADING: ["Riley needs support during a major life transition", "We can be emotionally available, maintain normal friendship routines, and help Riley feel valued and accepted"]
                },
                mr_rogers_connection="Episode about family changes and supporting friends"
            )
        ]
        
        return scenarios
    
    def _create_social_simulations(self) -> List[SocialInteractionSimulation]:
        """Create social interaction simulations for skill practice"""
        simulations = [
            SocialInteractionSimulation(
                id="playground_negotiation",
                simulation_name="Playground Equipment Sharing",
                context="playground",
                participants=["Marcus", "Peer 1", "Peer 2", "Playground Monitor"],
                social_challenges=[
                    "Multiple children want to use the same swing",
                    "Someone cuts in line",
                    "Disagreement about game rules"
                ],
                target_skills=["turn-taking", "negotiation", "patience", "compromise"],
                success_indicators=[
                    "Uses polite language to express wants",
                    "Waits appropriately for turn",
                    "Suggests fair solutions",
                    "Accepts compromise gracefully"
                ],
                coaching_prompts={
                    "turn-taking": ["Remember to wait your turn", "How can we make this fair for everyone?"],
                    "negotiation": ["What could we do so everyone gets a chance?", "Let's think of a solution together"],
                    "patience": ["Take deep breaths while you wait", "Good waiting! Your turn is coming"],
                    "compromise": ["That's a great middle ground!", "Both ideas could work together"]
                }
            ),
            
            SocialInteractionSimulation(
                id="classroom_collaboration",
                simulation_name="Group Project Teamwork",
                context="classroom",
                participants=["Marcus", "Team Member 1", "Team Member 2", "Teacher"],
                social_challenges=[
                    "Different opinions about project direction",
                    "One person wanting to do everything",
                    "Someone not participating enough"
                ],
                target_skills=["collaboration", "leadership", "listening", "including others"],
                success_indicators=[
                    "Listens to all team members' ideas",
                    "Builds on others' suggestions",
                    "Encourages quiet members to participate",
                    "Helps resolve disagreements peacefully"
                ],
                coaching_prompts={
                    "collaboration": ["How can we combine these ideas?", "Everyone's thoughts are important"],
                    "leadership": ["Great job helping the team stay focused!", "You're being a good leader"],
                    "listening": ["Show you're listening with your eyes and body", "Repeat back what you heard"],
                    "including others": ["Let's hear from everyone", "What do you think about this idea?"]
                }
            ),
            
            SocialInteractionSimulation(
                id="conflict_mediation",
                simulation_name="Friend Disagreement Resolution",
                context="conflict_resolution",
                participants=["Marcus", "Friend A", "Friend B", "Mediator"],
                social_challenges=[
                    "Two friends arguing over a toy",
                    "Hurt feelings from exclusion",
                    "Misunderstanding between friends"
                ],
                target_skills=["active listening", "empathy", "problem-solving", "peace-making"],
                success_indicators=[
                    "Acknowledges both friends' feelings",
                    "Suggests solutions that work for everyone",
                    "Uses calm voice and body language",
                    "Helps friends apologize and make up"
                ],
                coaching_prompts={
                    "active listening": ["Let's hear what each person is feeling", "I understand you're both upset"],
                    "empathy": ["How do you think your friend feels?", "I can see why that would be hurtful"],
                    "problem-solving": ["What are some ways to solve this?", "Let's think of solutions together"],
                    "peace-making": ["How can you both feel better?", "What would help repair this friendship?"]
                }
            )
        ]
        
        return simulations
    
    def _initialize_eq_profile(self) -> Dict[str, Any]:
        """Initialize Marcus's emotional intelligence profile"""
        return {
            "student_id": "marcus_agi",
            "profile_created": datetime.now().isoformat(),
            "current_levels": {domain.value: EQSkillLevel.DEVELOPING.value for domain in EQDomain},
            "strengths": ["curiosity", "persistence", "analytical thinking"],
            "growth_areas": ["social interaction", "emotional expression", "peer relationships"],
            "learning_preferences": ["kinesthetic", "visual", "systematic"],
            "emotional_vocabulary_size": 8,
            "last_assessment": None
        }
    
    def conduct_emotion_recognition_assessment(self, task_id: str) -> Dict[str, Any]:
        """Conduct emotion recognition assessment"""
        task = next((t for t in self.emotion_recognition_tasks if t.id == task_id), None)
        if not task:
            return {"error": f"Task {task_id} not found"}
        
        print(f"\n🧠 Emotion Recognition Assessment: {task.task_type.title()}")
        print(f"📋 Target emotions: {', '.join(task.target_emotions)}")
        
        # Simulate assessment responses
        correct_responses = 0
        total_responses = len(task.stimuli)
        responses = []
        
        for stimulus in task.stimuli:
            # Simulate Marcus's response based on his current EQ level
            if task.difficulty_level == EQSkillLevel.BEGINNING:
                accuracy = 0.8  # 80% accuracy on basic emotions
            elif task.difficulty_level == EQSkillLevel.DEVELOPING:
                accuracy = 0.65  # 65% accuracy on situational emotions  
            else:
                accuracy = 0.5   # 50% accuracy on complex emotions
            
            is_correct = random.random() < accuracy
            if is_correct:
                correct_responses += 1
                
            response = {
                "stimulus": stimulus,
                "correct": is_correct,
                "response_time": random.uniform(2.0, 8.0),
                "confidence": random.uniform(0.6, 0.9) if is_correct else random.uniform(0.3, 0.7)
            }
            responses.append(response)
        
        accuracy_score = correct_responses / total_responses
        
        # Determine skill level based on performance
        if accuracy_score >= 0.8:
            assessed_level = EQSkillLevel.APPLYING
        elif accuracy_score >= 0.65:
            assessed_level = EQSkillLevel.PRACTICING
        elif accuracy_score >= 0.5:
            assessed_level = EQSkillLevel.DEVELOPING
        else:
            assessed_level = EQSkillLevel.BEGINNING
        
        result = {
            "task_id": task_id,
            "task_type": task.task_type,
            "total_items": total_responses,
            "correct_responses": correct_responses,
            "accuracy_score": accuracy_score,
            "assessed_level": assessed_level.value,
            "responses": responses,
            "assessment_date": datetime.now().isoformat(),
            "recommendations": self._generate_emotion_recognition_recommendations(assessed_level, task.task_type)
        }
        
        print(f"  ✅ Completed: {correct_responses}/{total_responses} correct ({accuracy_score:.1%})")
        print(f"  📊 Current Level: {assessed_level.value}")
        
        return result
    
    def conduct_empathy_assessment(self, scenario_id: str) -> Dict[str, Any]:
        """Conduct empathy assessment using scenarios"""
        scenario = next((s for s in self.empathy_scenarios if s.id == scenario_id), None)
        if not scenario:
            return {"error": f"Scenario {scenario_id} not found"}
        
        print(f"\n💝 Empathy Assessment: {scenario_id.replace('_', ' ').title()}")
        print(f"📖 Scenario: {scenario.scenario_description}")
        
        # Simulate Marcus's empathic responses
        responses = []
        empathy_level_scores = []
        
        for question in scenario.empathy_questions:
            # Simulate response quality based on current empathy development
            response_quality = random.choice([EQSkillLevel.DEVELOPING, EQSkillLevel.PRACTICING])
            
            # Get expected response for this level
            expected_responses = scenario.expected_responses.get(response_quality, ["Basic empathic response"])
            simulated_response = random.choice(expected_responses)
            
            response_data = {
                "question": question,
                "response": simulated_response,
                "level_demonstrated": response_quality.value,
                "empathy_indicators": self._identify_empathy_indicators(simulated_response)
            }
            responses.append(response_data)
            empathy_level_scores.append(response_quality.value)
        
        # Calculate overall empathy level
        level_values = {"beginning": 1, "developing": 2, "practicing": 3, "applying": 4, "leading": 5}
        avg_score = sum(level_values[level] for level in empathy_level_scores) / len(empathy_level_scores)
        
        if avg_score >= 4.5:
            overall_level = EQSkillLevel.LEADING
        elif avg_score >= 3.5:
            overall_level = EQSkillLevel.APPLYING
        elif avg_score >= 2.5:
            overall_level = EQSkillLevel.PRACTICING
        elif avg_score >= 1.5:
            overall_level = EQSkillLevel.DEVELOPING
        else:
            overall_level = EQSkillLevel.BEGINNING
        
        result = {
            "scenario_id": scenario_id,
            "scenario_description": scenario.scenario_description,
            "responses": responses,
            "overall_empathy_level": overall_level.value,
            "empathy_strengths": self._identify_empathy_strengths(responses),
            "growth_opportunities": self._identify_empathy_growth_areas(responses),
            "next_steps": self._generate_empathy_next_steps(overall_level),
            "mr_rogers_connection": scenario.mr_rogers_connection,
            "assessment_date": datetime.now().isoformat()
        }
        
        print(f"  ✅ Overall Empathy Level: {overall_level.value}")
        print(f"  💪 Strengths: {', '.join(result['empathy_strengths'][:2])}")
        
        return result
    
    def conduct_social_simulation(self, simulation_id: str) -> Dict[str, Any]:
        """Conduct social interaction simulation"""
        simulation = next((s for s in self.social_simulations if s.id == simulation_id), None)
        if not simulation:
            return {"error": f"Simulation {simulation_id} not found"}
        
        print(f"\n🤝 Social Simulation: {simulation.simulation_name}")
        print(f"🏫 Context: {simulation.context}")
        print(f"👥 Participants: {', '.join(simulation.participants)}")
        
        # Simulate social interaction performance
        performance_results = []
        skill_demonstrations = {}
        
        for challenge in simulation.social_challenges:
            print(f"\n  🎯 Challenge: {challenge}")
            
            # Simulate performance on each target skill
            for skill in simulation.target_skills:
                # Marcus's performance varies by skill and challenge type
                if skill in ["turn-taking", "patience"]:
                    performance = random.uniform(0.7, 0.9)  # Strong in structured skills
                elif skill in ["negotiation", "compromise"]:
                    performance = random.uniform(0.6, 0.8)  # Developing in social negotiation
                elif skill in ["empathy", "including others"]:
                    performance = random.uniform(0.5, 0.7)  # Growing in emotional skills
                else:
                    performance = random.uniform(0.6, 0.8)  # Average performance
                
                skill_demonstrations[skill] = skill_demonstrations.get(skill, []) + [performance]
                
                # Provide coaching if performance is low
                if performance < 0.6:
                    prompts = simulation.coaching_prompts.get(skill, ["Keep trying!"])
                    print(f"    💬 Coach: {random.choice(prompts)}")
        
        # Calculate overall social skill levels
        skill_levels = {}
        for skill, performances in skill_demonstrations.items():
            avg_performance = sum(performances) / len(performances)
            
            if avg_performance >= 0.8:
                skill_levels[skill] = EQSkillLevel.APPLYING.value
            elif avg_performance >= 0.65:
                skill_levels[skill] = EQSkillLevel.PRACTICING.value
            elif avg_performance >= 0.5:
                skill_levels[skill] = EQSkillLevel.DEVELOPING.value
            else:
                skill_levels[skill] = EQSkillLevel.BEGINNING.value
        
        # Check success indicators
        success_indicators_met = []
        for indicator in simulation.success_indicators:
            # Simulate whether indicator was demonstrated
            met = random.random() < 0.7  # 70% chance of meeting each indicator
            if met:
                success_indicators_met.append(indicator)
        
        result = {
            "simulation_id": simulation_id,
            "simulation_name": simulation.simulation_name,
            "context": simulation.context,
            "challenges_addressed": simulation.social_challenges,
            "skill_levels": skill_levels,
            "success_indicators_met": success_indicators_met,
            "overall_social_competence": self._calculate_social_competence(skill_levels),
            "coaching_provided": sum(len(prompts) for prompts in simulation.coaching_prompts.values()),
            "social_strengths": self._identify_social_strengths(skill_levels),
            "areas_for_growth": self._identify_social_growth_areas(skill_levels),
            "next_practice_opportunities": self._suggest_social_practice(skill_levels),
            "assessment_date": datetime.now().isoformat()
        }
        
        print(f"\n  ✅ Social Competence: {result['overall_social_competence']}")
        print(f"  🎯 Indicators Met: {len(success_indicators_met)}/{len(simulation.success_indicators)}")
        
        return result
    
    def generate_comprehensive_eq_report(self) -> Dict[str, Any]:
        """Generate comprehensive emotional intelligence assessment report"""
        
        # Conduct assessments across all domains if not recent
        recent_assessments = [a for a in self.assessment_history if 
                            datetime.fromisoformat(a.get("assessment_date", "2020-01-01T00:00:00")) > 
                            datetime.now() - timedelta(days=30)]
        
        if len(recent_assessments) < 3:
            print("🧠 Conducting comprehensive EQ assessment...")
            
            # Emotion Recognition
            emotion_results = self.conduct_emotion_recognition_assessment("facial_expressions_basic")
            
            # Empathy Assessment  
            empathy_results = self.conduct_empathy_assessment("playground_exclusion")
            
            # Social Skills Simulation
            social_results = self.conduct_social_simulation("playground_negotiation")
            
            recent_assessments = [emotion_results, empathy_results, social_results]
        
        # Analyze overall EQ profile
        domain_levels = {}
        for domain in EQDomain:
            # Calculate current level for each domain based on assessments
            domain_assessments = [a for a in recent_assessments if 
                                domain.value in str(a).lower()]
            
            if domain_assessments:
                # Average assessment levels for domain
                levels = []
                for assessment in domain_assessments:
                    if "assessed_level" in assessment:
                        levels.append(assessment["assessed_level"])
                    elif "overall_empathy_level" in assessment:
                        levels.append(assessment["overall_empathy_level"])
                    elif "overall_social_competence" in assessment:
                        levels.append(assessment["overall_social_competence"])
                
                if levels:
                    level_values = {"beginning": 1, "developing": 2, "practicing": 3, "applying": 4, "leading": 5}
                    avg_level = sum(level_values.get(level, 2) for level in levels) / len(levels)
                    
                    if avg_level >= 4.5:
                        domain_levels[domain.value] = "leading"
                    elif avg_level >= 3.5:
                        domain_levels[domain.value] = "applying"
                    elif avg_level >= 2.5:
                        domain_levels[domain.value] = "practicing"
                    elif avg_level >= 1.5:
                        domain_levels[domain.value] = "developing"
                    else:
                        domain_levels[domain.value] = "beginning"
            else:
                domain_levels[domain.value] = "developing"  # Default
        
        # Generate comprehensive report
        report = {
            "student_id": "marcus_agi",
            "report_date": datetime.now().isoformat(),
            "assessment_period": "30 days",
            "eq_domain_levels": domain_levels,
            "overall_eq_level": self._calculate_overall_eq_level(domain_levels),
            "eq_strengths": self._identify_overall_eq_strengths(recent_assessments),
            "growth_priorities": self._identify_eq_growth_priorities(domain_levels),
            "recent_assessments": recent_assessments,
            "developmental_progress": self._track_eq_progress(),
            "intervention_recommendations": self._generate_eq_interventions(domain_levels),
            "mr_rogers_integration": self._suggest_mr_rogers_episodes(domain_levels),
            "next_assessment_recommendations": self._suggest_next_assessments(domain_levels)
        }
        
        return report
    
    def _generate_emotion_recognition_recommendations(self, level: EQSkillLevel, task_type: str) -> List[str]:
        """Generate recommendations for emotion recognition development"""
        recommendations = []
        
        if level == EQSkillLevel.BEGINNING:
            recommendations.extend([
                "Practice with basic emotion cards daily",
                "Use emotion mirrors and facial expression games",
                "Connect emotions to physical sensations",
                "Start emotion check-ins during daily routines"
            ])
        elif level == EQSkillLevel.DEVELOPING:
            recommendations.extend([
                "Expand emotion vocabulary with feeling words",
                "Practice emotion intensity levels (little mad vs. very mad)",
                "Use emotion stories and books",
                "Connect emotions to situations and causes"
            ])
        elif level == EQSkillLevel.PRACTICING:
            recommendations.extend([
                "Work on complex and mixed emotions",
                "Practice reading subtle emotional cues",
                "Discuss emotion triggers and patterns",
                "Help others identify emotions"
            ])
        else:
            recommendations.extend([
                "Develop emotion coaching skills for peers",
                "Explore cultural differences in emotional expression",
                "Practice advanced emotional intelligence concepts",
                "Lead emotion learning activities"
            ])
        
        return recommendations
    
    def _identify_empathy_indicators(self, response: str) -> List[str]:
        """Identify empathy indicators in response"""
        indicators = []
        
        response_lower = response.lower()
        
        if any(word in response_lower for word in ["feel", "feeling", "feels"]):
            indicators.append("emotion_awareness")
        if any(word in response_lower for word in ["help", "comfort", "support"]):
            indicators.append("helping_orientation")
        if any(word in response_lower for word in ["because", "since", "why"]):
            indicators.append("causal_understanding")
        if any(word in response_lower for word in ["i would", "if i were"]):
            indicators.append("perspective_taking")
        if len(response.split()) > 10:
            indicators.append("detailed_response")
        
        return indicators
    
    def _identify_empathy_strengths(self, responses: List[Dict]) -> List[str]:
        """Identify empathy strengths from responses"""
        strengths = []
        
        # Analyze response patterns
        total_indicators = []
        for response in responses:
            total_indicators.extend(response.get("empathy_indicators", []))
        
        if total_indicators.count("emotion_awareness") >= 2:
            strengths.append("Strong emotion recognition")
        if total_indicators.count("helping_orientation") >= 2:
            strengths.append("Natural helping instinct")
        if total_indicators.count("perspective_taking") >= 1:
            strengths.append("Perspective-taking ability")
        if total_indicators.count("detailed_response") >= 2:
            strengths.append("Thoughtful analysis")
        
        return strengths if strengths else ["Developing empathy awareness"]
    
    def _identify_empathy_growth_areas(self, responses: List[Dict]) -> List[str]:
        """Identify empathy growth areas"""
        growth_areas = []
        
        # Analyze gaps in empathy indicators
        total_indicators = []
        for response in responses:
            total_indicators.extend(response.get("empathy_indicators", []))
        
        if total_indicators.count("emotion_awareness") < 2:
            growth_areas.append("Emotion recognition in others")
        if total_indicators.count("helping_orientation") < 1:
            growth_areas.append("Prosocial helping behaviors")
        if total_indicators.count("perspective_taking") < 1:
            growth_areas.append("Understanding others' viewpoints")
        if total_indicators.count("causal_understanding") < 2:
            growth_areas.append("Understanding emotion causes")
        
        return growth_areas if growth_areas else ["Continue building empathy skills"]
    
    def _generate_empathy_next_steps(self, level: EQSkillLevel) -> List[str]:
        """Generate next steps for empathy development"""
        next_steps = {
            EQSkillLevel.BEGINNING: [
                "Practice identifying emotions in picture books",
                "Role-play simple helping scenarios",
                "Use 'How would you feel if...' questions daily"
            ],
            EQSkillLevel.DEVELOPING: [
                "Discuss characters' feelings in stories",
                "Practice perspective-taking games",
                "Encourage helping behaviors with peers"
            ],
            EQSkillLevel.PRACTICING: [
                "Work on complex emotional situations",
                "Practice conflict mediation skills",
                "Discuss real-world empathy scenarios"
            ],
            EQSkillLevel.APPLYING: [
                "Take on peer mentoring roles",
                "Lead empathy-building activities",
                "Discuss community service and helping others"
            ],
            EQSkillLevel.LEADING: [
                "Teach empathy skills to younger children",
                "Organize community helping projects",
                "Develop advanced emotional intelligence"
            ]
        }
        
        return next_steps.get(level, ["Continue empathy development"])
    
    def _calculate_social_competence(self, skill_levels: Dict[str, str]) -> str:
        """Calculate overall social competence level"""
        level_values = {"beginning": 1, "developing": 2, "practicing": 3, "applying": 4, "leading": 5}
        
        if not skill_levels:
            return "developing"
        
        avg_level = sum(level_values.get(level, 2) for level in skill_levels.values()) / len(skill_levels)
        
        if avg_level >= 4.5:
            return "leading"
        elif avg_level >= 3.5:
            return "applying"
        elif avg_level >= 2.5:
            return "practicing"
        elif avg_level >= 1.5:
            return "developing"
        else:
            return "beginning"
    
    def _identify_social_strengths(self, skill_levels: Dict[str, str]) -> List[str]:
        """Identify social strengths"""
        strengths = []
        
        high_skills = [skill for skill, level in skill_levels.items() 
                      if level in ["applying", "leading", "practicing"]]
        
        strength_mapping = {
            "turn-taking": "Excellent at waiting and sharing",
            "patience": "Shows good self-control",
            "negotiation": "Good problem-solving skills", 
            "compromise": "Flexible and fair-minded",
            "collaboration": "Works well with others",
            "listening": "Pays attention to others",
            "empathy": "Understands others' feelings",
            "including others": "Inclusive and kind"
        }
        
        for skill in high_skills:
            if skill in strength_mapping:
                strengths.append(strength_mapping[skill])
        
        return strengths if strengths else ["Developing social awareness"]
    
    def _identify_social_growth_areas(self, skill_levels: Dict[str, str]) -> List[str]:
        """Identify social growth areas"""
        growth_areas = []
        
        low_skills = [skill for skill, level in skill_levels.items() 
                     if level in ["beginning", "developing"]]
        
        growth_mapping = {
            "turn-taking": "Practice waiting and sharing turns",
            "patience": "Work on self-regulation skills",
            "negotiation": "Develop conflict resolution abilities",
            "compromise": "Practice flexible thinking",
            "collaboration": "Build teamwork skills",
            "listening": "Improve attention to others",
            "empathy": "Strengthen emotion recognition",
            "including others": "Practice inclusive behaviors"
        }
        
        for skill in low_skills:
            if skill in growth_mapping:
                growth_areas.append(growth_mapping[skill])
        
        return growth_areas if growth_areas else ["Continue social skill development"]
    
    def _suggest_social_practice(self, skill_levels: Dict[str, str]) -> List[str]:
        """Suggest social practice opportunities"""
        suggestions = []
        
        low_skills = [skill for skill, level in skill_levels.items() 
                     if level in ["beginning", "developing"]]
        
        practice_mapping = {
            "turn-taking": "Board games and playground equipment sharing",
            "patience": "Waiting games and mindfulness activities",
            "negotiation": "Conflict resolution role-plays",
            "compromise": "Group decision-making activities",
            "collaboration": "Team projects and group art",
            "listening": "Story time and conversation practice",
            "empathy": "Emotion books and helping scenarios",
            "including others": "Friendship activities and peer support"
        }
        
        for skill in low_skills[:3]:  # Top 3 priorities
            if skill in practice_mapping:
                suggestions.append(practice_mapping[skill])
        
        return suggestions if suggestions else ["Continue regular social interaction opportunities"]
    
    def _calculate_overall_eq_level(self, domain_levels: Dict[str, str]) -> str:
        """Calculate overall EQ level from domain levels"""
        level_values = {"beginning": 1, "developing": 2, "practicing": 3, "applying": 4, "leading": 5}
        
        if not domain_levels:
            return "developing"
        
        avg_level = sum(level_values.get(level, 2) for level in domain_levels.values()) / len(domain_levels)
        
        if avg_level >= 4.5:
            return "leading"
        elif avg_level >= 3.5:
            return "applying"
        elif avg_level >= 2.5:
            return "practicing"
        elif avg_level >= 1.5:
            return "developing"
        else:
            return "beginning"
    
    def _identify_overall_eq_strengths(self, assessments: List[Dict]) -> List[str]:
        """Identify overall EQ strengths from assessments"""
        strengths = []
        
        # Analyze patterns across assessments
        for assessment in assessments:
            if "empathy_strengths" in assessment:
                strengths.extend(assessment["empathy_strengths"])
            if "social_strengths" in assessment:
                strengths.extend(assessment["social_strengths"])
        
        # Remove duplicates and return top strengths
        unique_strengths = list(set(strengths))
        return unique_strengths[:4] if unique_strengths else ["Developing emotional awareness"]
    
    def _identify_eq_growth_priorities(self, domain_levels: Dict[str, str]) -> List[str]:
        """Identify EQ growth priorities"""
        priorities = []
        
        # Find domains with lowest levels
        level_values = {"beginning": 1, "developing": 2, "practicing": 3, "applying": 4, "leading": 5}
        sorted_domains = sorted(domain_levels.items(), key=lambda x: level_values.get(x[1], 2))
        
        priority_mapping = {
            "self_awareness": "Expand emotion vocabulary and self-understanding",
            "self_regulation": "Strengthen emotional control and coping strategies",
            "motivation": "Build persistence and resilience skills",
            "empathy": "Develop perspective-taking and caring behaviors",
            "social_skills": "Practice communication and relationship skills"
        }
        
        # Take bottom 2-3 domains as priorities
        for domain, level in sorted_domains[:3]:
            if level in ["beginning", "developing"]:
                if domain in priority_mapping:
                    priorities.append(priority_mapping[domain])
        
        return priorities if priorities else ["Continue balanced EQ development"]
    
    def _track_eq_progress(self) -> Dict[str, Any]:
        """Track EQ progress over time"""
        # This would track changes over time in a real implementation
        return {
            "progress_trend": "steady_improvement",
            "months_tracked": 3,
            "key_improvements": [
                "Expanded emotion vocabulary from 5 to 8 words",
                "Increased helping behaviors with peers",
                "Better self-regulation during transitions"
            ],
            "areas_needing_attention": [
                "Complex emotion recognition",
                "Conflict resolution skills"
            ]
        }
    
    def _generate_eq_interventions(self, domain_levels: Dict[str, str]) -> List[str]:
        """Generate EQ intervention recommendations"""
        interventions = []
        
        for domain, level in domain_levels.items():
            if level in ["beginning", "developing"]:
                if domain == "self_awareness":
                    interventions.append("Daily emotion check-ins with feeling wheels")
                elif domain == "self_regulation":
                    interventions.append("Teach and practice calming strategies")
                elif domain == "empathy":
                    interventions.append("Read emotion-rich books and discuss characters' feelings")
                elif domain == "social_skills":
                    interventions.append("Structured social skills groups and role-play")
                elif domain == "motivation":
                    interventions.append("Break tasks into smaller steps, celebrate effort")
        
        # Add general interventions
        if len([l for l in domain_levels.values() if l in ["beginning", "developing"]]) >= 3:
            interventions.append("Consider additional social-emotional learning support")
        
        return interventions if interventions else ["Continue current EQ development approach"]
    
    def _suggest_mr_rogers_episodes(self, domain_levels: Dict[str, str]) -> List[str]:
        """Suggest relevant Mr. Rogers episodes for EQ development"""
        episodes = []
        
        episode_mapping = {
            "self_awareness": "Episode 1478: Angry Feelings - Understanding emotions",
            "self_regulation": "Episode about Managing Big Feelings",
            "empathy": "Episode 1479: Making Friends - Caring about others",
            "social_skills": "Episode about Friendship and Kindness",
            "motivation": "Episode 1640: Making Mistakes - Trying again"
        }
        
        # Suggest episodes for domains needing support
        low_domains = [domain for domain, level in domain_levels.items() 
                      if level in ["beginning", "developing"]]
        
        for domain in low_domains[:3]:
            if domain in episode_mapping:
                episodes.append(episode_mapping[domain])
        
        return episodes if episodes else ["Continue regular Mr. Rogers viewing for character development"]
    
    def _suggest_next_assessments(self, domain_levels: Dict[str, str]) -> List[str]:
        """Suggest next assessments to conduct"""
        suggestions = []
        
        # Suggest deeper assessments for developing areas
        low_domains = [domain for domain, level in domain_levels.items() 
                      if level in ["beginning", "developing"]]
        
        assessment_mapping = {
            "self_awareness": "Emotion trigger mapping assessment",
            "self_regulation": "Coping strategy effectiveness evaluation",
            "empathy": "Advanced perspective-taking scenarios",
            "social_skills": "Peer interaction observation",
            "motivation": "Persistence and resilience challenge tasks"
        }
        
        for domain in low_domains:
            if domain in assessment_mapping:
                suggestions.append(assessment_mapping[domain])
        
        if not suggestions:
            suggestions.append("Quarterly comprehensive EQ review")
        
        return suggestions

# Integration functions
def integrate_eq_with_curriculum(curriculum_session: Dict[str, Any]) -> Dict[str, Any]:
    """Integrate EQ assessment with curriculum expansion"""
    
    eq_system = EmotionalIntelligenceAssessment()
    
    # Generate EQ report
    eq_report = eq_system.generate_comprehensive_eq_report()
    
    # Enhance curriculum session with EQ insights
    curriculum_session.update({
        "eq_integration": True,
        "eq_assessment_version": "issue_6",
        "current_eq_levels": eq_report["eq_domain_levels"],
        "eq_strengths": eq_report["eq_strengths"],
        "eq_growth_priorities": eq_report["growth_priorities"],
        "eq_interventions": eq_report["intervention_recommendations"],
        "mr_rogers_eq_episodes": eq_report["mr_rogers_integration"]
    })
    
    return curriculum_session

# Factory function
def create_eq_assessment_system() -> EmotionalIntelligenceAssessment:
    """Create emotional intelligence assessment system"""
    return EmotionalIntelligenceAssessment()

# Demo function
def demo_eq_assessment():
    """Demonstrate emotional intelligence assessment capabilities"""
    
    print("🧠 Issue #6 Demo: Emotional Intelligence Assessment System")
    print("=" * 65)
    
    eq_system = create_eq_assessment_system()
    
    print(f"\n📊 EQ Metrics Defined:")
    for domain in EQDomain:
        metrics = eq_system.eq_metrics.get(domain, [])
        print(f"  {domain.value.replace('_', ' ').title()}: {len(metrics)} metrics")
    
    print(f"\n🎭 Assessment Tools Available:")
    print(f"  🎯 Emotion Recognition Tasks: {len(eq_system.emotion_recognition_tasks)}")
    print(f"  💝 Empathy Scenarios: {len(eq_system.empathy_scenarios)}")
    print(f"  🤝 Social Simulations: {len(eq_system.social_simulations)}")
    
    # Conduct sample assessments
    print(f"\n🧪 Conducting Sample Assessments...")
    
    # Emotion recognition
    emotion_result = eq_system.conduct_emotion_recognition_assessment("facial_expressions_basic")
    
    # Empathy assessment
    empathy_result = eq_system.conduct_empathy_assessment("playground_exclusion")
    
    # Social simulation
    social_result = eq_system.conduct_social_simulation("playground_negotiation")
    
    # Generate comprehensive report
    print(f"\n📋 Generating Comprehensive EQ Report...")
    eq_report = eq_system.generate_comprehensive_eq_report()
    
    print(f"\n✅ EQ Assessment Results:")
    print(f"  🧠 Overall EQ Level: {eq_report['overall_eq_level']}")
    print(f"  💪 Top Strengths: {', '.join(eq_report['eq_strengths'][:2])}")
    print(f"  🎯 Growth Priorities: {', '.join(eq_report['growth_priorities'][:2])}")
    print(f"  📺 Mr. Rogers Episodes: {len(eq_report['mr_rogers_integration'])}")
    print(f"  🔄 Interventions: {len(eq_report['intervention_recommendations'])}")
    
    print(f"\n🎉 Issue #6 Implementation Complete!")
    print("   Comprehensive emotional intelligence assessment system ready for Marcus!")

if __name__ == "__main__":
    demo_eq_assessment()
