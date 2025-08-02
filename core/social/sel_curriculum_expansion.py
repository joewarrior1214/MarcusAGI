#!/usr/bin/env python3
"""
SEL Curriculum Expansion for Marcus AGI - Strategic Option A Implementation

This module creates a comprehensive Social Emotional Learning curriculum expansion
that builds on existing foundations:
- Kindergarten Curriculum Expansion (issue #5)
- Emotional Intelligence Assessment (issue #6) 
- Mr. Rogers Episode Integration
- Daily Learning Loop Integration

Features:
1. Structured SEL lessons with progressive skill building
2. Emotion regulation practice modules
3. Conflict resolution drill scenarios  
4. Empathy development exercises
5. Daily SEL integration with existing curriculum
6. Assessment and progress tracking
7. Mr. Rogers wisdom integration
"""

import json
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SELSkillArea(Enum):
    """Core Social Emotional Learning skill areas"""
    EMOTION_IDENTIFICATION = "emotion_identification"
    EMOTION_REGULATION = "emotion_regulation"
    CONFLICT_RESOLUTION = "conflict_resolution"
    EMPATHY_DEVELOPMENT = "empathy_development"
    SOCIAL_AWARENESS = "social_awareness"
    RELATIONSHIP_SKILLS = "relationship_skills"
    RESPONSIBLE_DECISION_MAKING = "responsible_decision_making"
    STRESS_MANAGEMENT = "stress_management"

class SELDifficultyLevel(Enum):
    """SEL lesson difficulty progression"""
    FOUNDATION = "foundation"      # Basic concepts, simple scenarios
    BUILDING = "building"          # Multi-step processes, complex emotions
    PRACTICING = "practicing"      # Real-world application, peer interactions
    MASTERING = "mastering"        # Leadership, teaching others, complex situations

class SELLessonType(Enum):
    """Types of SEL lessons"""
    DIRECT_INSTRUCTION = "direct_instruction"    # Explicit teaching
    GUIDED_PRACTICE = "guided_practice"          # Structured activities
    ROLE_PLAY = "role_play"                     # Acting out scenarios
    REFLECTION = "reflection"                    # Journaling, discussion
    PROBLEM_SOLVING = "problem_solving"          # Case studies, dilemmas
    MINDFULNESS = "mindfulness"                  # Calming, awareness exercises
    CREATIVE_EXPRESSION = "creative_expression"  # Art, music, storytelling

@dataclass
class SELLesson:
    """Comprehensive SEL lesson structure"""
    id: str
    title: str
    skill_area: SELSkillArea
    difficulty_level: SELDifficultyLevel
    lesson_type: SELLessonType
    duration_minutes: int
    age_range: Tuple[int, int]  # months
    
    # Lesson content
    learning_objectives: List[str]
    mr_rogers_connection: Optional[str]
    materials_needed: List[str]
    warm_up_activity: str
    main_activities: List[Dict[str, Any]]
    closing_reflection: str
    
    # Assessment
    success_indicators: List[str]
    assessment_questions: List[str]
    extension_activities: List[str]
    
    # Integration
    prerequisite_skills: List[str] = field(default_factory=list)
    follow_up_lessons: List[str] = field(default_factory=list)
    cross_curricular_connections: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'skill_area': self.skill_area.value,
            'difficulty_level': self.difficulty_level.value,
            'lesson_type': self.lesson_type.value,
            'duration_minutes': self.duration_minutes,
            'age_range': self.age_range,
            'learning_objectives': self.learning_objectives,
            'mr_rogers_connection': self.mr_rogers_connection,
            'materials_needed': self.materials_needed,
            'warm_up_activity': self.warm_up_activity,
            'main_activities': self.main_activities,
            'closing_reflection': self.closing_reflection,
            'success_indicators': self.success_indicators,
            'assessment_questions': self.assessment_questions,
            'extension_activities': self.extension_activities,
            'prerequisite_skills': self.prerequisite_skills,
            'follow_up_lessons': self.follow_up_lessons,
            'cross_curricular_connections': self.cross_curricular_connections
        }

@dataclass
class EmotionRegulationDrill:
    """Structured emotion regulation practice activity"""
    id: str
    name: str
    target_emotion: str
    regulation_strategy: str
    scenario: str
    practice_steps: List[str]
    coaching_prompts: List[str]
    success_criteria: List[str]
    difficulty_level: SELDifficultyLevel
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'target_emotion': self.target_emotion,
            'regulation_strategy': self.regulation_strategy,
            'scenario': self.scenario,
            'practice_steps': self.practice_steps,
            'coaching_prompts': self.coaching_prompts,
            'success_criteria': self.success_criteria,
            'difficulty_level': self.difficulty_level.value
        }

@dataclass
class ConflictResolutionScenario:
    """Structured conflict resolution practice scenario"""
    id: str
    scenario_name: str
    conflict_type: str
    characters_involved: List[str]
    conflict_description: str
    resolution_steps: List[str]
    coaching_questions: List[str]
    possible_outcomes: List[str]
    key_skills_practiced: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'scenario_name': self.scenario_name,
            'conflict_type': self.conflict_type,
            'characters_involved': self.characters_involved,
            'conflict_description': self.conflict_description,
            'resolution_steps': self.resolution_steps,
            'coaching_questions': self.coaching_questions,
            'possible_outcomes': self.possible_outcomes,
            'key_skills_practiced': self.key_skills_practiced
        }

@dataclass
class EmpathyExercise:
    """Structured empathy development exercise"""
    id: str
    exercise_name: str
    exercise_type: str  # "perspective_taking", "emotion_recognition", "caring_response"
    scenario: str
    character_emotions: Dict[str, str]
    empathy_questions: List[str]
    reflection_prompts: List[str]
    action_suggestions: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'exercise_name': self.exercise_name,
            'exercise_type': self.exercise_type,
            'scenario': self.scenario,
            'character_emotions': self.character_emotions,
            'empathy_questions': self.empathy_questions,
            'reflection_prompts': self.reflection_prompts,
            'action_suggestions': self.action_suggestions
        }

@dataclass
class SELProgressTracker:
    """Track SEL skill development over time"""
    student_id: str
    skill_area: SELSkillArea
    current_level: SELDifficultyLevel
    lessons_completed: List[str]
    strengths: List[str]
    growth_areas: List[str]
    recent_successes: List[str]
    next_goals: List[str]
    last_updated: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'student_id': self.student_id,
            'skill_area': self.skill_area.value,
            'current_level': self.current_level.value,
            'lessons_completed': self.lessons_completed,
            'strengths': self.strengths,
            'growth_areas': self.growth_areas,
            'recent_successes': self.recent_successes,
            'next_goals': self.next_goals,
            'last_updated': self.last_updated.isoformat()
        }

class SELCurriculumExpansion:
    """Comprehensive SEL Curriculum System for Marcus AGI"""
    
    def __init__(self):
        self.lessons = self._create_sel_lessons()
        self.emotion_regulation_drills = self._create_emotion_regulation_drills()
        self.conflict_resolution_scenarios = self._create_conflict_resolution_scenarios()
        self.empathy_exercises = self._create_empathy_exercises()
        self.progress_trackers = {}
        self.daily_sel_schedule = self._create_daily_schedule()
        
    def _create_sel_lessons(self) -> Dict[str, SELLesson]:
        """Create comprehensive SEL lesson library"""
        lessons = {}
        
        # EMOTION IDENTIFICATION LESSONS
        lessons['emotions_basic'] = SELLesson(
            id="emotions_basic",
            title="Feeling Faces: Identifying Basic Emotions",
            skill_area=SELSkillArea.EMOTION_IDENTIFICATION,
            difficulty_level=SELDifficultyLevel.FOUNDATION,
            lesson_type=SELLessonType.DIRECT_INSTRUCTION,
            duration_minutes=20,
            age_range=(60, 72),
            learning_objectives=[
                "I can identify happy, sad, mad, and scared emotions",
                "I can match facial expressions to emotion words",
                "I can point to where I feel emotions in my body"
            ],
            mr_rogers_connection="Episode 1478 - Angry Feelings: How we can recognize different feelings",
            materials_needed=["Emotion face cards", "Body outline drawing", "Emotion mirror"],
            warm_up_activity="Look in the emotion mirror and make different feeling faces",
            main_activities=[
                {
                    "name": "Emotion Face Match",
                    "description": "Match emotion words to facial expression cards",
                    "duration": 8,
                    "interaction": "guided_practice"
                },
                {
                    "name": "Body Mapping",
                    "description": "Draw where you feel each emotion in your body",
                    "duration": 7,
                    "interaction": "individual_work"
                }
            ],
            closing_reflection="How are you feeling right now? Show me with your face and tell me where you feel it.",
            success_indicators=[
                "Correctly identifies 3/4 basic emotions",
                "Makes appropriate facial expressions",
                "Points to body locations for emotions"
            ],
            assessment_questions=[
                "Show me a happy face. Where do you feel happy in your body?",
                "What emotion do you think this person is feeling?",
                "When someone is sad, how can you tell?"
            ],
            extension_activities=[
                "Create an emotion book with drawings",
                "Play emotion charades with family",
                "Use emotion faces during daily check-ins"
            ]
        )
        
        lessons['emotions_complex'] = SELLesson(
            id="emotions_complex",
            title="More Than Mad: Understanding Complex Emotions",
            skill_area=SELSkillArea.EMOTION_IDENTIFICATION,
            difficulty_level=SELDifficultyLevel.BUILDING,
            lesson_type=SELLessonType.GUIDED_PRACTICE,
            duration_minutes=25,
            age_range=(64, 78),
            learning_objectives=[
                "I can identify frustrated, disappointed, excited, and worried emotions",
                "I can tell the difference between similar feelings",
                "I can use emotion words to describe my experiences"
            ],
            mr_rogers_connection="Episode 1495 - Making Mistakes: Understanding disappointment and growth",
            materials_needed=["Complex emotion cards", "Feeling thermometer", "Scenario pictures"],
            warm_up_activity="Share about a time you felt really excited about something",
            main_activities=[
                {
                    "name": "Emotion Sorting",
                    "description": "Sort emotions by intensity using feeling thermometer",
                    "duration": 10,
                    "interaction": "hands_on_sorting"
                },
                {
                    "name": "Scenario Discussions",
                    "description": "Discuss what emotions characters might feel in different situations",
                    "duration": 10,
                    "interaction": "group_discussion"
                }
            ],
            closing_reflection="What's one new emotion word you learned today? When might you feel that way?",
            success_indicators=[
                "Uses complex emotion vocabulary",
                "Distinguishes between similar emotions",
                "Relates emotions to personal experiences"
            ],
            assessment_questions=[
                "How is frustrated different from mad?",
                "What might make someone feel disappointed?",
                "Show me excited vs. happy on the feeling thermometer"
            ],
            extension_activities=[
                "Keep an emotion journal for a week",
                "Create emotion stories using new vocabulary",
                "Practice emotion check-ins with friends"
            ],
            prerequisite_skills=["emotions_basic"]
        )
        
        # EMOTION REGULATION LESSONS
        lessons['calm_down_strategies'] = SELLesson(
            id="calm_down_strategies",
            title="Calm Down Tools: Learning to Self-Regulate",
            skill_area=SELSkillArea.EMOTION_REGULATION,
            difficulty_level=SELDifficultyLevel.FOUNDATION,
            lesson_type=SELLessonType.GUIDED_PRACTICE,
            duration_minutes=30,
            age_range=(60, 72),
            learning_objectives=[
                "I can use deep breathing to calm down",
                "I can count to 10 when I feel upset",
                "I can ask for help when my emotions feel too big"
            ],
            mr_rogers_connection="Episode 1478 - Angry Feelings: Ways to handle angry feelings",
            materials_needed=["Breathing buddy (stuffed animal)", "Calm down cards", "Timer"],
            warm_up_activity="Practice belly breathing with your breathing buddy",
            main_activities=[
                {
                    "name": "Deep Breathing Practice",
                    "description": "Learn 4-7-8 breathing technique with breathing buddy",
                    "duration": 10,
                    "interaction": "mindfulness_practice"
                },
                {
                    "name": "Calm Down Menu",
                    "description": "Create personalized calm down strategy cards",
                    "duration": 15,
                    "interaction": "creative_activity"
                }
            ],
            closing_reflection="Which calm down strategy feels most helpful for you? When might you use it?",
            success_indicators=[
                "Demonstrates proper breathing technique",
                "Can count to 10 slowly when prompted",
                "Identifies personal calm down preferences"
            ],
            assessment_questions=[
                "Show me how to do belly breathing",
                "What can you do when you feel really mad?",
                "Who can you ask for help when emotions feel too big?"
            ],
            extension_activities=[
                "Practice breathing exercises at bedtime",
                "Create a calm down corner at home",
                "Teach breathing to a family member"
            ],
            prerequisite_skills=["emotions_basic"]
        )
        
        lessons['anger_management'] = SELLesson(
            id="anger_management",
            title="When I Feel Mad: Healthy Ways to Handle Anger",
            skill_area=SELSkillArea.EMOTION_REGULATION,
            difficulty_level=SELDifficultyLevel.BUILDING,
            lesson_type=SELLessonType.ROLE_PLAY,
            duration_minutes=35,
            age_range=(64, 78),
            learning_objectives=[
                "I can recognize anger warning signs in my body",
                "I can use appropriate strategies before anger gets too big",
                "I can express anger in ways that don't hurt others"
            ],
            mr_rogers_connection="Episode 1478 - Angry Feelings: It's okay to feel angry, but not okay to hurt",
            materials_needed=["Anger thermometer", "Stress balls", "Anger scenario cards"],
            warm_up_activity="Notice how your body feels when you're calm vs. starting to get upset",
            main_activities=[
                {
                    "name": "Anger Warning Signs",
                    "description": "Identify physical sensations that signal rising anger",
                    "duration": 12,
                    "interaction": "body_awareness"
                },
                {
                    "name": "Anger Scenarios",
                    "description": "Role-play appropriate responses to anger-triggering situations",
                    "duration": 18,
                    "interaction": "role_play_practice"
                }
            ],
            closing_reflection="What's your anger warning sign? What strategy will you try next time?",
            success_indicators=[
                "Identifies personal anger warning signs",
                "Demonstrates appropriate anger responses in role-play",
                "Uses strategies before anger escalates"
            ],
            assessment_questions=[
                "How does your body feel when you start to get mad?",
                "What can you do instead of yelling or hitting?",
                "How can you tell someone you're angry in a respectful way?"
            ],
            extension_activities=[
                "Keep an anger tracking chart",
                "Practice anger strategies during peer conflicts",
                "Create an anger management poster"
            ],
            prerequisite_skills=["emotions_basic", "calm_down_strategies"]
        )
        
        # CONFLICT RESOLUTION LESSONS
        lessons['problem_solving_steps'] = SELLesson(
            id="problem_solving_steps",
            title="Working It Out: Steps for Solving Problems with Friends",
            skill_area=SELSkillArea.CONFLICT_RESOLUTION,
            difficulty_level=SELDifficultyLevel.FOUNDATION,
            lesson_type=SELLessonType.DIRECT_INSTRUCTION,
            duration_minutes=25,
            age_range=(60, 72),
            learning_objectives=[
                "I can identify when there's a problem with a friend",
                "I can use words to tell someone how I feel",
                "I can listen to what others have to say"
            ],
            mr_rogers_connection="Episode 1640 - Making Mistakes: Learning to say sorry and forgive",
            materials_needed=["Problem-solving steps poster", "Role-play scenario cards"],
            warm_up_activity="Think of a time you had a problem with a friend. How did it feel?",
            main_activities=[
                {
                    "name": "Problem-Solving Steps",
                    "description": "Learn the 4-step process: Stop, Talk, Listen, Try Again",
                    "duration": 12,
                    "interaction": "direct_teaching"
                },
                {
                    "name": "Practice Scenarios",
                    "description": "Practice problem-solving steps with simple friend conflicts",
                    "duration": 10,
                    "interaction": "guided_practice"
                }
            ],
            closing_reflection="Which step do you think might be hardest for you? How can you remember to use these steps?",
            success_indicators=[
                "Can recite the 4 problem-solving steps",
                "Uses words to express feelings appropriately",
                "Shows listening behavior during practice"
            ],
            assessment_questions=[
                "What are the steps for solving problems?",
                "How can you tell someone you're upset without being mean?",
                "What does good listening look like?"
            ],
            extension_activities=[
                "Make a problem-solving poster for home",
                "Practice steps with family members",
                "Use steps during actual peer conflicts"
            ]
        )
        
        # EMPATHY DEVELOPMENT LESSONS
        lessons['perspective_taking'] = SELLesson(
            id="perspective_taking",
            title="In Their Shoes: Understanding How Others Feel",
            skill_area=SELSkillArea.EMPATHY_DEVELOPMENT,
            difficulty_level=SELDifficultyLevel.BUILDING,
            lesson_type=SELLessonType.CREATIVE_EXPRESSION,
            duration_minutes=30,
            age_range=(64, 78),
            learning_objectives=[
                "I can think about how other people might be feeling",
                "I can understand that others might feel differently than I do",
                "I can show caring when someone is upset"
            ],
            mr_rogers_connection="Episode 1479 - Making Friends: Understanding that everyone has feelings",
            materials_needed=["Story books", "Emotion perspective cards", "Art supplies"],
            warm_up_activity="Look at a picture and guess how each person in it might be feeling",
            main_activities=[
                {
                    "name": "Story Character Feelings",
                    "description": "Read stories and discuss character emotions and motivations",
                    "duration": 15,
                    "interaction": "literature_discussion"
                },
                {
                    "name": "Empathy Art",
                    "description": "Draw or create art showing how to help someone who's sad",
                    "duration": 12,
                    "interaction": "creative_expression"
                }
            ],
            closing_reflection="How can you show someone you care about their feelings?",
            success_indicators=[
                "Accurately identifies character emotions in stories",
                "Suggests appropriate helping behaviors",
                "Shows understanding that people can feel differently"
            ],
            assessment_questions=[
                "How do you think this character is feeling? Why?",
                "What would you do if you saw someone crying?",
                "How might someone feel different from you in this situation?"
            ],
            extension_activities=[
                "Keep a kindness journal",
                "Practice noticing friends' emotions",
                "Do acts of kindness for family members"
            ],
            prerequisite_skills=["emotions_basic", "emotions_complex"]
        )
        
        return lessons
    
    def _create_emotion_regulation_drills(self) -> List[EmotionRegulationDrill]:
        """Create structured emotion regulation practice drills"""
        drills = []
        
        # ANGER REGULATION DRILLS
        drills.append(EmotionRegulationDrill(
            id="anger_breathing_drill",
            name="Anger Breathing Challenge",
            target_emotion="anger",
            regulation_strategy="deep_breathing",
            scenario="Your friend accidentally knocked down your block tower that you worked hard on",
            practice_steps=[
                "Stop what you're doing and pause",
                "Notice anger rising in your body (tight fists, hot face)",
                "Take 5 slow, deep belly breaths",
                "Count each breath: 1... 2... 3... 4... 5...",
                "Check: How does your body feel now?",
                "Use words to tell your friend how you feel"
            ],
            coaching_prompts=[
                "I notice your hands are getting tight. Let's try some breathing.",
                "Good job stopping! Now let's breathe together.",
                "Put your hand on your belly and feel it rise and fall.",
                "You're doing great managing your anger!"
            ],
            success_criteria=[
                "Pauses before reacting",
                "Completes 5 breaths with coaching",
                "Shows physical signs of calming",
                "Uses words instead of physical actions"
            ],
            difficulty_level=SELDifficultyLevel.FOUNDATION
        ))
        
        drills.append(EmotionRegulationDrill(
            id="frustration_problem_solving",
            name="Frustration Problem-Solving Drill",
            target_emotion="frustration",
            regulation_strategy="problem_solving",
            scenario="You can't figure out how to complete a puzzle and feel like giving up",
            practice_steps=[
                "Recognize frustration signals (wanting to throw puzzle, saying 'I can't')",
                "Take 3 deep breaths",
                "Ask yourself: 'What's the real problem here?'",
                "Think of 3 different solutions",
                "Try one solution",
                "If it doesn't work, try another solution",
                "Ask for help if you need it"
            ],
            coaching_prompts=[
                "I can see you're getting frustrated. Let's pause and think.",
                "What exactly is making this hard for you?",
                "What are some different ways you could try this?",
                "It's okay to ask for help when you need it."
            ],
            success_criteria=[
                "Identifies frustration without being prompted",
                "Can name the specific problem",
                "Generates at least 2 solutions",
                "Tries solutions before giving up"
            ],
            difficulty_level=SELDifficultyLevel.BUILDING
        ))
        
        # SADNESS REGULATION DRILLS
        drills.append(EmotionRegulationDrill(
            id="sadness_comfort_drill",
            name="Sadness Comfort Strategies",
            target_emotion="sadness",
            regulation_strategy="self_comfort",
            scenario="You miss your parent who had to go to work, and you feel sad",
            practice_steps=[
                "Notice sadness in your body (heavy chest, want to cry)",
                "It's okay to feel sad - all feelings are okay",
                "Choose a comfort strategy: hug a stuffed animal, look at photos, draw a picture",
                "Practice the comfort strategy for 2 minutes",
                "Talk to someone you trust about your feelings",
                "Remember: the sad feeling will get smaller"
            ],
            coaching_prompts=[
                "I can see you're feeling sad. That's okay.",
                "What would help you feel a little better right now?",
                "Sometimes when we're sad, a hug can help.",
                "Would you like to tell me about your sad feelings?"
            ],
            success_criteria=[
                "Accepts sadness as a normal emotion",
                "Chooses appropriate comfort strategy",
                "Engages with comfort activity",
                "Shares feelings with trusted person"
            ],
            difficulty_level=SELDifficultyLevel.FOUNDATION
        ))
        
        # ANXIETY/WORRY REGULATION DRILLS
        drills.append(EmotionRegulationDrill(
            id="worry_thought_check",
            name="Worry Thought Checking",
            target_emotion="worry",
            regulation_strategy="cognitive_reframing",
            scenario="You're worried about trying something new and think you might fail",
            practice_steps=[
                "Notice worry thoughts ('What if I can't do it?')",
                "Take 3 slow breaths",
                "Ask: 'Is this worry thought helpful?'",
                "Think of a more helpful thought: 'I can try my best'",
                "Remember times you've succeeded at new things",
                "Make a plan: 'If it's hard, I can ask for help'"
            ],
            coaching_prompts=[
                "What thoughts are going through your mind?",
                "Is that worry thought helping you or making you feel worse?",
                "What would you tell a friend who had this worry?",
                "Remember when you learned to ride a bike? You tried your best then too."
            ],
            success_criteria=[
                "Identifies worry thoughts",
                "Challenges unhelpful thoughts",
                "Generates more balanced thoughts",
                "Makes coping plan"
            ],
            difficulty_level=SELDifficultyLevel.PRACTICING
        ))
        
        return drills
    
    def _create_conflict_resolution_scenarios(self) -> List[ConflictResolutionScenario]:
        """Create structured conflict resolution practice scenarios"""
        scenarios = []
        
        scenarios.append(ConflictResolutionScenario(
            id="toy_sharing_conflict",
            scenario_name="The Toy Sharing Disagreement",
            conflict_type="resource_sharing",
            characters_involved=["Marcus", "Emma"],
            conflict_description="Marcus and Emma both want to play with the same toy truck at the same time. Marcus had it first, but Emma says she was waiting for a turn.",
            resolution_steps=[
                "Stop and take a breath",
                "Each person shares their feelings using 'I' statements",
                "Listen to understand, not to argue",
                "Brainstorm solutions together",
                "Choose a solution that works for both",
                "Try the solution and check how it's working"
            ],
            coaching_questions=[
                "How is each person feeling right now?",
                "What does Marcus need? What does Emma need?",
                "What are some ways they could both be happy?",
                "How can they make sure this is fair for both of them?"
            ],
            possible_outcomes=[
                "Take turns with a timer",
                "Play with the truck together",
                "Find a different toy they both like",
                "One person chooses something else for now and gets first turn later"
            ],
            key_skills_practiced=["active_listening", "compromise", "empathy", "problem_solving"]
        ))
        
        scenarios.append(ConflictResolutionScenario(
            id="game_rules_conflict",
            scenario_name="The Game Rules Argument",
            conflict_type="rule_disagreement",
            characters_involved=["Marcus", "Oliver", "Zoe"],
            conflict_description="The children are playing a game, but they disagree about the rules. Oliver thinks they should play one way, Zoe thinks differently, and Marcus is confused about what to do.",
            resolution_steps=[
                "Pause the game",
                "Each person explains what they think the rule should be",
                "Ask: 'Why do you think that rule is important?'",
                "Look for common ground - what do we all agree on?",
                "Create a new rule together that everyone can accept",
                "Write down the rule so everyone remembers"
            ],
            coaching_questions=[
                "What rule does each person want?",
                "Why are rules important in games?",
                "How can we make this fair for everyone?",
                "What happens if we can't agree on rules?"
            ],
            possible_outcomes=[
                "Vote on which rule to use",
                "Combine ideas to make a new rule",
                "Take turns using different rule versions",
                "Choose a different game everyone knows"
            ],
            key_skills_practiced=["negotiation", "democracy", "flexibility", "collaboration"]
        ))
        
        scenarios.append(ConflictResolutionScenario(
            id="hurt_feelings_conflict",
            scenario_name="The Hurt Feelings Situation",
            conflict_type="emotional_harm",
            characters_involved=["Marcus", "Sofia"],
            conflict_description="Sofia made a comment about Marcus's drawing that hurt his feelings. She didn't mean to be hurtful, but Marcus feels sad and doesn't want to be around her.",
            resolution_steps=[
                "Recognize that someone's feelings are hurt",
                "The hurt person explains how they feel using 'I' statements",
                "The other person listens without defending",
                "The person who caused hurt acknowledges the impact",
                "Both people work on understanding each other",
                "Make a plan to prevent this in the future"
            ],
            coaching_questions=[
                "How do you think Marcus is feeling?",
                "What did Sofia intend vs. what was the impact?",
                "How can Sofia show she cares about Marcus's feelings?",
                "What could they do differently next time?"
            ],
            possible_outcomes=[
                "Sofia gives a genuine apology",
                "Marcus explains why the comment hurt",
                "They agree on kinder ways to give feedback",
                "They rebuild their friendship with understanding"
            ],
            key_skills_practiced=["empathy", "accountability", "forgiveness", "communication"]
        ))
        
        return scenarios
    
    def _create_empathy_exercises(self) -> List[EmpathyExercise]:
        """Create structured empathy development exercises"""
        exercises = []
        
        exercises.append(EmpathyExercise(
            id="emotion_detective",
            exercise_name="Emotion Detective",
            exercise_type="emotion_recognition",
            scenario="You notice your friend sitting alone at recess, looking down at the ground with their shoulders slumped.",
            character_emotions={"friend": "sad_lonely"},
            empathy_questions=[
                "What clues tell you how your friend might be feeling?",
                "What do you notice about their body language?",
                "How do you think they might be feeling inside?",
                "Why might they be feeling this way?"
            ],
            reflection_prompts=[
                "Think about a time when you felt lonely. What was that like?",
                "What would have helped you feel better in that situation?",
                "How does it feel when someone notices you're sad?"
            ],
            action_suggestions=[
                "Go sit with your friend",
                "Ask if they're okay",
                "Invite them to play with you",
                "Tell a trusted adult if you're worried"
            ]
        ))
        
        exercises.append(EmpathyExercise(
            id="perspective_glasses",
            exercise_name="Perspective-Taking Glasses",
            exercise_type="perspective_taking",
            scenario="A new student joins your class. They don't know anyone, don't know where things are, and seem nervous about joining activities.",
            character_emotions={"new_student": "nervous_uncertain"},
            empathy_questions=[
                "How do you think the new student is feeling?",
                "What might be hard about being new?",
                "What might they be thinking about?",
                "What would you want if you were the new student?"
            ],
            reflection_prompts=[
                "Remember your first day at school. How did you feel?",
                "What helped you feel welcome when you were new somewhere?",
                "How does it feel when others include you vs. leave you out?"
            ],
            action_suggestions=[
                "Introduce yourself and ask their name",
                "Show them around the classroom",
                "Invite them to sit with you at lunch",
                "Include them in games at recess"
            ]
        ))
        
        exercises.append(EmpathyExercise(
            id="caring_response",
            exercise_name="Caring Response Practice",
            exercise_type="caring_response",
            scenario="Your friend tells you they're upset because their pet goldfish died last night.",
            character_emotions={"friend": "grief_sadness"},
            empathy_questions=[
                "How is your friend feeling right now?",
                "What makes losing a pet special and sad?",
                "What do you think would help them feel supported?",
                "What would NOT be helpful to say right now?"
            ],
            reflection_prompts=[
                "Think about something important to you. How would you feel if you lost it?",
                "When you're sad, what do you want from friends?",
                "What makes you feel cared about when you're upset?"
            ],
            action_suggestions=[
                "Say 'I'm sorry your goldfish died. That must be really sad.'",
                "Give them a hug if they want one",
                "Listen if they want to tell you about their pet",
                "Ask if there's anything you can do to help"
            ]
        ))
        
        return exercises
    
    def _create_daily_schedule(self) -> Dict[str, List[str]]:
        """Create a daily SEL integration schedule"""
        return {
            "morning_check_in": [
                "How are you feeling this morning?",
                "What emotions do you notice in your body?",
                "What do you need to have a good day?"
            ],
            "transition_times": [
                "Take three deep breaths before starting new activity",
                "Use calm down strategy if feeling overwhelmed",
                "Check in with friends during transitions"
            ],
            "conflict_moments": [
                "Use problem-solving steps immediately",
                "Practice emotion regulation strategies",
                "Apply empathy and perspective-taking"
            ],
            "afternoon_reflection": [
                "What emotions did you experience today?",
                "How did you handle challenging moments?",
                "What are you proud of from today?"
            ],
            "bedtime_wind_down": [
                "Practice gratitude - what went well today?",
                "Do calming breathing exercises",
                "Set positive intentions for tomorrow"
            ]
        }
    
    def get_daily_sel_lesson(self, student_level: Dict[SELSkillArea, SELDifficultyLevel]) -> SELLesson:
        """Get appropriate SEL lesson based on student's current levels"""
        # Find skill area with lowest level for targeted instruction
        lowest_skill = min(student_level.items(), key=lambda x: list(SELDifficultyLevel).index(x[1]))
        skill_area, current_level = lowest_skill
        
        # Find appropriate lesson for that skill area and level
        appropriate_lessons = [
            lesson for lesson in self.lessons.values()
            if lesson.skill_area == skill_area and lesson.difficulty_level == current_level
        ]
        
        if appropriate_lessons:
            return random.choice(appropriate_lessons)
        else:
            # Fallback to foundation level emotion identification
            return self.lessons['emotions_basic']
    
    def get_emotion_regulation_drill(self, target_emotion: str, difficulty: SELDifficultyLevel) -> Optional[EmotionRegulationDrill]:
        """Get specific emotion regulation drill"""
        matching_drills = [
            drill for drill in self.emotion_regulation_drills
            if drill.target_emotion == target_emotion and drill.difficulty_level == difficulty
        ]
        
        return random.choice(matching_drills) if matching_drills else None
    
    def get_conflict_resolution_scenario(self, conflict_type: str) -> Optional[ConflictResolutionScenario]:
        """Get specific conflict resolution scenario"""
        matching_scenarios = [
            scenario for scenario in self.conflict_resolution_scenarios
            if scenario.conflict_type == conflict_type
        ]
        
        return random.choice(matching_scenarios) if matching_scenarios else None
    
    def integrate_with_daily_learning(self, daily_subjects: List[str]) -> Dict[str, List[str]]:
        """Suggest SEL integration opportunities with academic subjects"""
        integration_suggestions = {}
        
        for subject in daily_subjects:
            if subject.lower() == "reading":
                integration_suggestions[subject] = [
                    "Discuss character emotions in stories",
                    "Practice empathy by understanding character motivations",
                    "Use books to explore different perspectives"
                ]
            elif subject.lower() == "math":
                integration_suggestions[subject] = [
                    "Practice patience when problems are challenging",
                    "Use problem-solving steps for math word problems",
                    "Celebrate effort and growth, not just correct answers"
                ]
            elif subject.lower() == "science":
                integration_suggestions[subject] = [
                    "Practice curiosity and wonder",
                    "Develop persistence when experiments don't work",
                    "Collaborate respectfully during group investigations"
                ]
            elif subject.lower() == "art":
                integration_suggestions[subject] = [
                    "Express emotions through creative work",
                    "Practice accepting when art doesn't turn out as expected",
                    "Appreciate different styles and perspectives"
                ]
            else:
                integration_suggestions[subject] = [
                    "Practice deep breathing before starting",
                    "Use encouraging self-talk",
                    "Ask for help when needed"
                ]
        
        return integration_suggestions
    
    def assess_sel_progress(self, student_id: str, skill_area: SELSkillArea, observed_behaviors: List[str]) -> SELProgressTracker:
        """Assess and track SEL progress"""
        # Determine current level based on observed behaviors
        current_level = self._determine_skill_level(skill_area, observed_behaviors)
        
        # Get or create progress tracker
        tracker_key = f"{student_id}_{skill_area.value}"
        if tracker_key in self.progress_trackers:
            tracker = self.progress_trackers[tracker_key]
            tracker.current_level = current_level
            tracker.last_updated = datetime.now()
        else:
            tracker = SELProgressTracker(
                student_id=student_id,
                skill_area=skill_area,
                current_level=current_level,
                lessons_completed=[],
                strengths=[],
                growth_areas=[],
                recent_successes=observed_behaviors,
                next_goals=self._generate_next_goals(skill_area, current_level),
                last_updated=datetime.now()
            )
            self.progress_trackers[tracker_key] = tracker
        
        return tracker
    
    def _determine_skill_level(self, skill_area: SELSkillArea, observed_behaviors: List[str]) -> SELDifficultyLevel:
        """Determine skill level based on observed behaviors"""
        # Simple heuristic - in real implementation, would be more sophisticated
        behavior_count = len(observed_behaviors)
        positive_indicators = sum(1 for behavior in observed_behaviors if any(
            word in behavior.lower() for word in ['successfully', 'independently', 'appropriately', 'helped']
        ))
        
        success_rate = positive_indicators / behavior_count if behavior_count > 0 else 0
        
        if success_rate >= 0.8:
            return SELDifficultyLevel.MASTERING
        elif success_rate >= 0.6:
            return SELDifficultyLevel.PRACTICING
        elif success_rate >= 0.4:
            return SELDifficultyLevel.BUILDING
        else:
            return SELDifficultyLevel.FOUNDATION
    
    def _generate_next_goals(self, skill_area: SELSkillArea, current_level: SELDifficultyLevel) -> List[str]:
        """Generate next learning goals based on skill area and level"""
        goal_templates = {
            SELSkillArea.EMOTION_IDENTIFICATION: {
                SELDifficultyLevel.FOUNDATION: ["Learn to identify 2 more basic emotions", "Practice naming emotions daily"],
                SELDifficultyLevel.BUILDING: ["Distinguish between similar emotions", "Use emotion words in conversations"],
                SELDifficultyLevel.PRACTICING: ["Help friends identify their emotions", "Notice emotion changes throughout day"],
                SELDifficultyLevel.MASTERING: ["Teach emotion identification to younger children", "Create emotion stories"]
            },
            SELSkillArea.EMOTION_REGULATION: {
                SELDifficultyLevel.FOUNDATION: ["Practice deep breathing daily", "Use calm down strategies with help"],
                SELDifficultyLevel.BUILDING: ["Use regulation strategies independently", "Recognize early warning signs"],
                SELDifficultyLevel.PRACTICING: ["Help friends calm down", "Use advanced regulation techniques"],
                SELDifficultyLevel.MASTERING: ["Model emotional regulation for others", "Create personal regulation toolkit"]
            }
        }
        
        return goal_templates.get(skill_area, {}).get(current_level, ["Continue practicing current skills"])
    
    def generate_weekly_report(self, student_id: str) -> Dict[str, Any]:
        """Generate comprehensive weekly SEL progress report"""
        student_trackers = {
            key: tracker for key, tracker in self.progress_trackers.items() 
            if tracker.student_id == student_id
        }
        
        report = {
            "student_id": student_id,
            "report_date": datetime.now().isoformat(),
            "skill_areas": {},
            "overall_progress": "",
            "recommendations": [],
            "celebrations": []
        }
        
        for skill_area in SELSkillArea:
            tracker_key = f"{student_id}_{skill_area.value}"
            if tracker_key in student_trackers:
                tracker = student_trackers[tracker_key]
                report["skill_areas"][skill_area.value] = {
                    "current_level": tracker.current_level.value,
                    "strengths": tracker.strengths,
                    "growth_areas": tracker.growth_areas,
                    "next_goals": tracker.next_goals
                }
        
        # Generate overall assessment
        if student_trackers:
            avg_level = sum(list(SELDifficultyLevel).index(t.current_level) for t in student_trackers.values()) / len(student_trackers)
            level_names = [level.value for level in SELDifficultyLevel]
            report["overall_progress"] = level_names[int(avg_level)]
        
        return report
    
    def save_curriculum_data(self, output_dir: str = "output/sel_curriculum"):
        """Save all SEL curriculum data to JSON files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Save lessons
        lessons_data = {lesson_id: lesson.to_dict() for lesson_id, lesson in self.lessons.items()}
        with open(output_path / "sel_lessons.json", 'w') as f:
            json.dump(lessons_data, f, indent=2)
        
        # Save drills
        drills_data = [drill.to_dict() for drill in self.emotion_regulation_drills]
        with open(output_path / "emotion_regulation_drills.json", 'w') as f:
            json.dump(drills_data, f, indent=2)
        
        # Save scenarios
        scenarios_data = [scenario.to_dict() for scenario in self.conflict_resolution_scenarios]
        with open(output_path / "conflict_resolution_scenarios.json", 'w') as f:
            json.dump(scenarios_data, f, indent=2)
        
        # Save exercises
        exercises_data = [exercise.to_dict() for exercise in self.empathy_exercises]
        with open(output_path / "empathy_exercises.json", 'w') as f:
            json.dump(exercises_data, f, indent=2)
        
        # Save daily schedule
        with open(output_path / "daily_sel_schedule.json", 'w') as f:
            json.dump(self.daily_sel_schedule, f, indent=2)
        
        print(f"✅ SEL Curriculum data saved to {output_path}")

def main():
    """Demonstrate SEL Curriculum Expansion functionality"""
    print("🎯 SEL Curriculum Expansion - Strategic Option A")
    print("=" * 50)
    
    # Initialize the system
    sel_system = SELCurriculumExpansion()
    
    # Show available lessons
    print(f"\n📚 Available SEL Lessons: {len(sel_system.lessons)}")
    for lesson_id, lesson in sel_system.lessons.items():
        print(f"  • {lesson.title} ({lesson.skill_area.value} - {lesson.difficulty_level.value})")
    
    # Show emotion regulation drills
    print(f"\n💪 Emotion Regulation Drills: {len(sel_system.emotion_regulation_drills)}")
    for drill in sel_system.emotion_regulation_drills:
        print(f"  • {drill.name} (Target: {drill.target_emotion})")
    
    # Show conflict resolution scenarios
    print(f"\n🤝 Conflict Resolution Scenarios: {len(sel_system.conflict_resolution_scenarios)}")
    for scenario in sel_system.conflict_resolution_scenarios:
        print(f"  • {scenario.scenario_name} ({scenario.conflict_type})")
    
    # Show empathy exercises
    print(f"\n❤️ Empathy Exercises: {len(sel_system.empathy_exercises)}")
    for exercise in sel_system.empathy_exercises:
        print(f"  • {exercise.exercise_name} ({exercise.exercise_type})")
    
    # Demonstrate getting a daily lesson
    print(f"\n📅 Daily SEL Integration:")
    student_levels = {
        SELSkillArea.EMOTION_IDENTIFICATION: SELDifficultyLevel.FOUNDATION,
        SELSkillArea.EMOTION_REGULATION: SELDifficultyLevel.BUILDING,
        SELSkillArea.CONFLICT_RESOLUTION: SELDifficultyLevel.FOUNDATION,
        SELSkillArea.EMPATHY_DEVELOPMENT: SELDifficultyLevel.BUILDING
    }
    
    daily_lesson = sel_system.get_daily_sel_lesson(student_levels)
    print(f"  Today's Focus: {daily_lesson.title}")
    print(f"  Skill Area: {daily_lesson.skill_area.value}")
    print(f"  Duration: {daily_lesson.duration_minutes} minutes")
    print(f"  Mr. Rogers Connection: {daily_lesson.mr_rogers_connection}")
    
    # Demonstrate academic integration
    print(f"\n🔗 Academic Integration Suggestions:")
    daily_subjects = ["reading", "math", "science", "art"]
    integration = sel_system.integrate_with_daily_learning(daily_subjects)
    for subject, suggestions in integration.items():
        print(f"  {subject.title()}:")
        for suggestion in suggestions:
            print(f"    - {suggestion}")
    
    # Save curriculum data
    sel_system.save_curriculum_data()
    
    print(f"\n🎉 SEL Curriculum Expansion Complete!")
    print("Ready for integration with Marcus's daily learning loop!")

if __name__ == "__main__":
    main()
