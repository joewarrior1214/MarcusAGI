#!/usr/bin/env python3
"""
Issue #8: Peer Interaction Simulation System

This module implements comprehensive peer interaction simulations to help Marcus develop
social skills and collaborative learning abilities. It builds on the existing EQ system
to create realistic peer personalities and conversation engines.

Key Features:
1. Virtual peer personality models with distinct characteristics
2. Conversation simulation engines with natural dialogue
3. Conflict resolution scenarios with guided practice
4. Collaborative learning activities across subjects
5. Social dynamics modeling with relationship tracking

Integration Points:
- EQ Assessment System (Issue #6) - Leverages existing social skills framework
- Grade Progression System (Issue #7) - Adapts interactions to grade level
- Curriculum System (Issue #5) - Aligns activities with learning objectives
- Daily Learning Loop (Issue #3) - Integrates peer interactions into daily routine
"""

import random
import json
import sqlite3
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PeerPersonalityType(Enum):
    """Different peer personality types for diverse interactions"""
    CONFIDENT_LEADER = "confident_leader"
    SHY_THOUGHTFUL = "shy_thoughtful"
    ENERGETIC_FRIENDLY = "energetic_friendly"
    ANALYTICAL_PRECISE = "analytical_precise"
    CREATIVE_IMAGINATIVE = "creative_imaginative"
    COMPETITIVE_DRIVEN = "competitive_driven"
    SUPPORTIVE_HELPER = "supportive_helper"
    CURIOUS_QUESTIONER = "curious_questioner"

class InteractionContext(Enum):
    """Different contexts for peer interactions"""
    PLAYGROUND = "playground"
    CLASSROOM = "classroom"
    LUNCH_TABLE = "lunch_table"
    ART_CENTER = "art_center"
    LIBRARY = "library"
    GROUP_PROJECT = "group_project"
    FREE_PLAY = "free_play"
    CONFLICT_RESOLUTION = "conflict_resolution"

class ConversationTopic(Enum):
    """Topics for peer conversations"""
    ACADEMIC_HELP = "academic_help"
    SHARING_INTERESTS = "sharing_interests"
    MAKING_PLANS = "making_plans"
    SOLVING_PROBLEMS = "solving_problems"
    EXPRESSING_FEELINGS = "expressing_feelings"
    CREATIVE_COLLABORATION = "creative_collaboration"
    CONFLICT_DISCUSSION = "conflict_discussion"
    FRIENDSHIP_BUILDING = "friendship_building"

class SocialSkillArea(Enum):
    """Social skill areas to practice"""
    ACTIVE_LISTENING = "active_listening"
    TURN_TAKING = "turn_taking"
    EMPATHY = "empathy"
    ASSERTIVENESS = "assertiveness"
    COMPROMISE = "compromise"
    LEADERSHIP = "leadership"
    COOPERATION = "cooperation"
    CONFLICT_RESOLUTION = "conflict_resolution"
    INCLUSION = "inclusion"
    EMOTIONAL_REGULATION = "emotional_regulation"

@dataclass
class PeerPersonality:
    """Model of a virtual peer with distinct personality traits"""
    id: str
    name: str
    personality_type: PeerPersonalityType
    age_months: int  # Age in months for developmental appropriateness
    communication_style: Dict[str, float]  # verbal, non_verbal, assertive, etc.
    interests: List[str]
    strengths: List[str]
    challenges: List[str]
    friendship_style: str
    conflict_style: str
    learning_preferences: List[str]
    typical_responses: Dict[str, List[str]]  # situation -> possible responses
    emotional_tendencies: Dict[str, float]  # emotion -> frequency (0-1)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'personality_type': self.personality_type.value,
            'age_months': self.age_months,
            'communication_style': self.communication_style,
            'interests': self.interests,
            'strengths': self.strengths,
            'challenges': self.challenges,
            'friendship_style': self.friendship_style,
            'conflict_style': self.conflict_style,
            'learning_preferences': self.learning_preferences,
            'typical_responses': self.typical_responses,
            'emotional_tendencies': self.emotional_tendencies
        }

@dataclass
class ConversationTurn:
    """A single turn in a peer conversation"""
    speaker: str  # "marcus" or peer name
    message: str
    emotion: str
    social_skills_demonstrated: List[SocialSkillArea]
    response_quality: float  # 0-1 rating
    coaching_triggered: bool = False
    coaching_message: Optional[str] = None

@dataclass
class PeerInteractionSession:
    """A complete peer interaction session"""
    session_id: str
    marcus_id: str
    peers_involved: List[str]
    context: InteractionContext
    topic: ConversationTopic
    duration_minutes: int
    conversation_turns: List[ConversationTurn]
    social_skills_practiced: List[SocialSkillArea]
    learning_objectives_met: List[str]
    conflicts_resolved: int
    collaboration_successes: int
    overall_success_rating: float  # 0-1
    marcus_growth_areas: List[str]
    peer_feedback: Dict[str, str]  # peer_name -> feedback
    session_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'session_id': self.session_id,
            'marcus_id': self.marcus_id,
            'peers_involved': self.peers_involved,
            'context': self.context.value,
            'topic': self.topic.value,
            'duration_minutes': self.duration_minutes,
            'conversation_turns': [asdict(turn) for turn in self.conversation_turns],
            'social_skills_practiced': [skill.value for skill in self.social_skills_practiced],
            'learning_objectives_met': self.learning_objectives_met,
            'conflicts_resolved': self.conflicts_resolved,
            'collaboration_successes': self.collaboration_successes,
            'overall_success_rating': self.overall_success_rating,
            'marcus_growth_areas': self.marcus_growth_areas,
            'peer_feedback': self.peer_feedback,
            'session_timestamp': self.session_timestamp.isoformat()
        }

@dataclass
class CollaborativeLearningActivity:
    """A structured collaborative learning activity"""
    activity_id: str
    name: str
    subject_area: str
    grade_level: str
    duration_minutes: int
    min_participants: int
    max_participants: int
    learning_objectives: List[str]
    required_materials: List[str]
    roles: List[str]  # different roles participants can take
    success_criteria: List[str]
    social_skills_focus: List[SocialSkillArea]
    differentiation_strategies: Dict[str, List[str]]  # personality_type -> strategies
    assessment_rubric: Dict[str, List[str]]  # skill -> indicators

class PeerInteractionSimulator:
    """Core simulation engine for peer interactions"""
    
    def __init__(self, db_path: str = "peer_interactions.db"):
        self.db_path = db_path
        self.peers = {}  # peer_id -> PeerPersonality
        self.collaborative_activities = {}  # activity_id -> CollaborativeLearningActivity
        self.conversation_engine = ConversationEngine()
        self.social_dynamics_model = SocialDynamicsModel()
        
        # Initialize database
        self._init_database()
        
        # Load peer personalities and activities
        self._create_peer_personalities()
        self._create_collaborative_activities()
        
        logger.info("Peer Interaction Simulator initialized")
    
    def _init_database(self):
        """Initialize database for tracking peer interactions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Peer interaction sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS peer_interaction_sessions (
                    session_id TEXT PRIMARY KEY,
                    marcus_id TEXT NOT NULL DEFAULT 'marcus',
                    peers_involved TEXT NOT NULL,  -- JSON list
                    context TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    conversation_data TEXT NOT NULL,  -- JSON
                    social_skills_practiced TEXT NOT NULL,  -- JSON list
                    learning_objectives_met TEXT NOT NULL,  -- JSON list
                    conflicts_resolved INTEGER DEFAULT 0,
                    collaboration_successes INTEGER DEFAULT 0,
                    overall_success_rating REAL NOT NULL,
                    marcus_growth_areas TEXT NOT NULL,  -- JSON list
                    peer_feedback TEXT,  -- JSON
                    session_timestamp TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Peer relationships tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS peer_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    marcus_id TEXT NOT NULL DEFAULT 'marcus',
                    peer_id TEXT NOT NULL,
                    relationship_strength REAL DEFAULT 0.5,  -- 0-1 scale
                    interaction_count INTEGER DEFAULT 0,
                    positive_interactions INTEGER DEFAULT 0,
                    conflicts_resolved INTEGER DEFAULT 0,
                    collaboration_history TEXT,  -- JSON
                    last_interaction_date TEXT,
                    relationship_notes TEXT,
                    UNIQUE(marcus_id, peer_id)
                )
            """)
            
            # Social skills progress tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS social_skills_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    marcus_id TEXT NOT NULL DEFAULT 'marcus',
                    skill_area TEXT NOT NULL,
                    current_level REAL NOT NULL,  -- 0-1 scale
                    practice_count INTEGER DEFAULT 0,
                    successful_demonstrations INTEGER DEFAULT 0,
                    last_practiced DATE,
                    progress_notes TEXT,
                    UNIQUE(marcus_id, skill_area)
                )
            """)
            
            conn.commit()
    
    def _create_peer_personalities(self):
        """Create diverse peer personalities for interactions"""
        
        # Emma - Confident Leader
        self.peers["emma"] = PeerPersonality(
            id="emma",
            name="Emma",
            personality_type=PeerPersonalityType.CONFIDENT_LEADER,
            age_months=66,  # 5.5 years
            communication_style={
                "verbal": 0.9, "assertive": 0.8, "direct": 0.8, "encouraging": 0.7
            },
            interests=["organizing games", "helping others", "storytelling", "art projects"],
            strengths=["natural leadership", "problem-solving", "including others"],
            challenges=["can be bossy", "struggles with being wrong"],
            friendship_style="inclusive_organizer",
            conflict_style="direct_problem_solver",
            learning_preferences=["group activities", "verbal instructions", "hands-on projects"],
            typical_responses={
                "greeting": ["Hi! Want to play with us?", "Come join our game!", "Let's all play together!"],
                "conflict": ["Let's figure this out", "What if we try this way?", "How can we make everyone happy?"],
                "collaboration": ["I have an idea!", "Let's work together", "Everyone should get a turn"]
            },
            emotional_tendencies={
                "confident": 0.8, "enthusiastic": 0.9, "frustrated": 0.3, "patient": 0.6
            }
        )
        
        # Oliver - Shy Thoughtful
        self.peers["oliver"] = PeerPersonality(
            id="oliver",
            name="Oliver",
            personality_type=PeerPersonalityType.SHY_THOUGHTFUL,
            age_months=64,  # 5.3 years
            communication_style={
                "verbal": 0.5, "assertive": 0.3, "observant": 0.9, "thoughtful": 0.9
            },
            interests=["books", "quiet games", "drawing", "nature observation"],
            strengths=["careful listening", "creative ideas", "gentle nature"],
            challenges=["difficulty speaking up", "needs encouragement to participate"],
            friendship_style="loyal_supporter",
            conflict_style="conflict_avoider",
            learning_preferences=["quiet spaces", "visual instructions", "one-on-one help"],
            typical_responses={
                "greeting": ["Hi", "Hello", "*waves shyly*"],
                "conflict": ["I don't like fighting", "Maybe we could...", "*looks uncomfortable*"],
                "collaboration": ["That's a good idea", "I could help with that", "What should I do?"]
            },
            emotional_tendencies={
                "anxious": 0.6, "calm": 0.8, "thoughtful": 0.9, "hesitant": 0.7
            }
        )
        
        # Zoe - Energetic Friendly
        self.peers["zoe"] = PeerPersonality(
            id="zoe",
            name="Zoe",
            personality_type=PeerPersonalityType.ENERGETIC_FRIENDLY,
            age_months=67,  # 5.6 years
            communication_style={
                "verbal": 0.9, "enthusiastic": 0.9, "quick": 0.8, "friendly": 0.9
            },
            interests=["running games", "music", "dancing", "making friends"],
            strengths=["infectious enthusiasm", "making others feel welcome", "high energy"],
            challenges=["difficulty waiting turns", "can overwhelm quieter peers"],
            friendship_style="enthusiastic_includer",
            conflict_style="emotional_expresser",
            learning_preferences=["movement activities", "group work", "hands-on learning"],
            typical_responses={
                "greeting": ["Hi! Hi! Want to be friends?", "Come play! This is so fun!", "I'm Zoe! What's your name?"],
                "conflict": ["That's not fair!", "I'm really upset!", "Can we please fix this?"],
                "collaboration": ["Ooh! I know!", "Let's do it together!", "This is going to be amazing!"]
            },
            emotional_tendencies={
                "excited": 0.9, "happy": 0.8, "impatient": 0.7, "friendly": 0.9
            }
        )
        
        # Alex - Analytical Precise
        self.peers["alex"] = PeerPersonality(
            id="alex",
            name="Alex",
            personality_type=PeerPersonalityType.ANALYTICAL_PRECISE,
            age_months=68,  # 5.7 years
            communication_style={
                "verbal": 0.7, "precise": 0.9, "logical": 0.8, "questioning": 0.8
            },
            interests=["puzzles", "building blocks", "science experiments", "math games"],
            strengths=["logical thinking", "attention to detail", "problem-solving"],
            challenges=["can be inflexible", "frustrated by imprecision"],
            friendship_style="intellectual_companion",
            conflict_style="logical_negotiator",
            learning_preferences=["step-by-step instructions", "visual aids", "logical sequences"],
            typical_responses={
                "greeting": ["Hello", "Would you like to work on this puzzle?", "I'm building something interesting"],
                "conflict": ["That doesn't make sense", "Let's think about this logically", "Here's what I observed"],
                "collaboration": ["First we need to plan", "Let's organize our materials", "I think the pattern is..."]
            },
            emotional_tendencies={
                "curious": 0.8, "focused": 0.9, "analytical": 0.9, "patient": 0.7
            }
        )
        
        # Sofia - Creative Imaginative
        self.peers["sofia"] = PeerPersonality(
            id="sofia",
            name="Sofia",
            personality_type=PeerPersonalityType.CREATIVE_IMAGINATIVE,
            age_months=65,  # 5.4 years
            communication_style={
                "verbal": 0.8, "creative": 0.9, "expressive": 0.9, "storytelling": 0.9
            },
            interests=["art", "pretend play", "stories", "music"],
            strengths=["creative problem-solving", "imaginative play", "artistic expression"],
            challenges=["difficulty with rigid rules", "gets lost in imagination"],
            friendship_style="creative_collaborator",
            conflict_style="creative_solution_finder",
            learning_preferences=["creative activities", "storytelling", "artistic expression"],
            typical_responses={
                "greeting": ["Hi! Want to create something magical?", "I'm pretending to be a...", "Look what I made!"],
                "conflict": ["What if we pretended...", "Maybe we could make up a story", "I have a creative idea!"],
                "collaboration": ["Let's make it beautiful!", "We could add some magic", "What if our project could..."]
            },
            emotional_tendencies={
                "imaginative": 0.9, "expressive": 0.8, "dreamy": 0.7, "artistic": 0.9
            }
        )
        
        logger.info(f"Created {len(self.peers)} peer personalities")
    
    def _create_collaborative_activities(self):
        """Create structured collaborative learning activities"""
        
        # Science Exploration Activity
        self.collaborative_activities["science_exploration"] = CollaborativeLearningActivity(
            activity_id="science_exploration",
            name="Weather Station Collaboration",
            subject_area="science",
            grade_level="kindergarten",
            duration_minutes=20,
            min_participants=2,
            max_participants=4,
            learning_objectives=[
                "Observe and record weather patterns",
                "Practice measurement skills",
                "Learn weather vocabulary",
                "Develop scientific inquiry skills"
            ],
            required_materials=["thermometer", "rain gauge", "weather chart", "crayons"],
            roles=["Weather Observer", "Data Recorder", "Chart Manager", "Reporter"],
            success_criteria=[
                "All team members participate in observations",
                "Data is recorded accurately",
                "Team communicates findings clearly",
                "Weather vocabulary is used correctly"
            ],
            social_skills_focus=[
                SocialSkillArea.COOPERATION,
                SocialSkillArea.TURN_TAKING,
                SocialSkillArea.ACTIVE_LISTENING
            ],
            differentiation_strategies={
                "confident_leader": ["Assign leadership role", "Encourage peer support"],
                "shy_thoughtful": ["Provide specific role", "Use visual supports"],
                "energetic_friendly": ["Include movement", "Provide clear boundaries"],
                "analytical_precise": ["Emphasize measurement accuracy", "Provide detailed instructions"]
            },
            assessment_rubric={
                "cooperation": ["Takes turns", "Shares materials", "Helps teammates"],
                "communication": ["Uses weather words", "Asks questions", "Listens to others"],
                "participation": ["Contributes ideas", "Stays engaged", "Follows directions"]
            }
        )
        
        # Math Problem Solving Activity
        self.collaborative_activities["math_problem_solving"] = CollaborativeLearningActivity(
            activity_id="math_problem_solving",
            name="Classroom Store Shopping",
            subject_area="mathematics",
            grade_level="kindergarten",
            duration_minutes=25,
            min_participants=2,
            max_participants=3,
            learning_objectives=[
                "Practice counting and number recognition",
                "Understand money concepts",
                "Solve simple word problems",
                "Develop estimation skills"
            ],
            required_materials=["play money", "toy items with prices", "shopping lists", "calculator"],
            roles=["Shopper", "Store Clerk", "Money Counter"],
            success_criteria=[
                "Uses counting strategies correctly",
                "Makes appropriate purchases within budget",
                "Communicates clearly about quantities",
                "Shows good sportsmanship"
            ],
            social_skills_focus=[
                SocialSkillArea.TURN_TAKING,
                SocialSkillArea.COOPERATION,
                SocialSkillArea.COMPROMISE
            ],
            differentiation_strategies={
                "confident_leader": ["Let them guide problem-solving", "Encourage peer teaching"],
                "competitive_driven": ["Add challenge elements", "Set clear goals"],
                "supportive_helper": ["Give them the helper role", "Encourage assistance"],
                "analytical_precise": ["Focus on accuracy", "Provide systematic approaches"]
            },
            assessment_rubric={
                "math_skills": ["Counts accurately", "Recognizes numbers", "Solves problems"],
                "collaboration": ["Works well with partner", "Shares materials", "Takes turns"],
                "communication": ["Uses math vocabulary", "Explains thinking", "Asks for help"]
            }
        )
        
        # Language Arts Storytelling Activity
        self.collaborative_activities["storytelling_collaboration"] = CollaborativeLearningActivity(
            activity_id="storytelling_collaboration",
            name="Create Our Class Adventure",
            subject_area="language_arts",
            grade_level="kindergarten",
            duration_minutes=30,
            min_participants=3,
            max_participants=5,
            learning_objectives=[
                "Develop oral storytelling skills",
                "Practice sequencing events",
                "Build vocabulary",
                "Encourage creative expression"
            ],
            required_materials=["story cards", "props", "drawing paper", "crayons"],
            roles=["Story Starter", "Character Creator", "Problem Solver", "Ending Maker", "Illustrator"],
            success_criteria=[
                "Story has clear beginning, middle, end",
                "All members contribute ideas",
                "Characters are well-developed",
                "Story makes sense and is creative"
            ],
            social_skills_focus=[
                SocialSkillArea.ACTIVE_LISTENING,
                SocialSkillArea.COOPERATION,
                SocialSkillArea.LEADERSHIP,
                SocialSkillArea.INCLUSION
            ],
            differentiation_strategies={
                "creative_imaginative": ["Give them character creation role", "Encourage wild ideas"],
                "shy_thoughtful": ["Provide story starter prompts", "Pair with supportive peer"],
                "energetic_friendly": ["Include action elements", "Give them active role"],
                "curious_questioner": ["Let them develop the problem", "Encourage questions"]
            },
            assessment_rubric={
                "creativity": ["Contributes unique ideas", "Builds on others' ideas", "Uses imagination"],
                "storytelling": ["Uses descriptive words", "Sequences events", "Develops characters"],
                "collaboration": ["Listens to others", "Includes everyone's ideas", "Works cooperatively"]
            }
        )
        
        logger.info(f"Created {len(self.collaborative_activities)} collaborative activities")
    
    def simulate_peer_interaction(self, peers_to_include: List[str], 
                                context: InteractionContext,
                                topic: ConversationTopic,
                                duration_minutes: int = 15) -> PeerInteractionSession:
        """Simulate a complete peer interaction session"""
        
        session_id = str(uuid.uuid4())
        logger.info(f"Starting peer interaction simulation: {session_id}")
        
        # Select peers for interaction
        selected_peers = []
        for peer_id in peers_to_include:
            if peer_id in self.peers:
                selected_peers.append(self.peers[peer_id])
        
        if not selected_peers:
            raise ValueError("No valid peers found for interaction")
        
        # Generate conversation based on context and topic
        conversation_turns = self.conversation_engine.generate_conversation(
            selected_peers, context, topic, duration_minutes
        )
        
        # Analyze social skills demonstrated
        social_skills_practiced = self._analyze_social_skills(conversation_turns)
        
        # Determine learning objectives met
        learning_objectives_met = self._identify_learning_objectives(
            context, topic, conversation_turns
        )
        
        # Count collaboration successes and conflicts resolved
        collaboration_successes = self._count_collaboration_successes(conversation_turns)
        conflicts_resolved = self._count_conflicts_resolved(conversation_turns)
        
        # Calculate overall success rating
        overall_success_rating = self._calculate_success_rating(
            conversation_turns, social_skills_practiced, collaboration_successes
        )
        
        # Identify Marcus's growth areas
        marcus_growth_areas = self._identify_growth_areas(conversation_turns)
        
        # Generate peer feedback
        peer_feedback = self._generate_peer_feedback(selected_peers, conversation_turns)
        
        # Create session object
        session = PeerInteractionSession(
            session_id=session_id,
            marcus_id="marcus",
            peers_involved=[peer.id for peer in selected_peers],
            context=context,
            topic=topic,
            duration_minutes=duration_minutes,
            conversation_turns=conversation_turns,
            social_skills_practiced=social_skills_practiced,
            learning_objectives_met=learning_objectives_met,
            conflicts_resolved=conflicts_resolved,
            collaboration_successes=collaboration_successes,
            overall_success_rating=overall_success_rating,
            marcus_growth_areas=marcus_growth_areas,
            peer_feedback=peer_feedback,
            session_timestamp=datetime.now()
        )
        
        # Store session in database
        self._store_interaction_session(session)
        
        # Update peer relationships
        self._update_peer_relationships(selected_peers, overall_success_rating)
        
        # Update social skills progress
        self._update_skills_progress(social_skills_practiced, overall_success_rating)
        
        logger.info(f"Completed peer interaction simulation: {session_id}")
        return session
    
    def conduct_collaborative_activity(self, activity_id: str, 
                                     participants: List[str]) -> Dict[str, Any]:
        """Conduct a structured collaborative learning activity"""
        
        if activity_id not in self.collaborative_activities:
            raise ValueError(f"Activity {activity_id} not found")
        
        activity = self.collaborative_activities[activity_id]
        
        # Validate participant count
        if len(participants) < activity.min_participants or len(participants) > activity.max_participants:
            raise ValueError(f"Activity requires {activity.min_participants}-{activity.max_participants} participants")
        
        logger.info(f"Starting collaborative activity: {activity.name}")
        
        # Assign roles based on personalities
        role_assignments = self._assign_activity_roles(activity, participants)
        
        # Simulate activity execution
        activity_results = self._simulate_activity_execution(activity, participants, role_assignments)
        
        # Assess learning outcomes
        learning_assessment = self._assess_learning_outcomes(activity, activity_results)
        
        # Generate recommendations for next steps
        recommendations = self._generate_activity_recommendations(activity, learning_assessment)
        
        result = {
            "activity_id": activity_id,
            "activity_name": activity.name,
            "participants": participants,
            "role_assignments": role_assignments,
            "duration_minutes": activity.duration_minutes,
            "learning_objectives_met": learning_assessment["objectives_met"],
            "social_skills_demonstrated": learning_assessment["social_skills"],
            "individual_performance": learning_assessment["individual_performance"],
            "group_dynamics": activity_results["group_dynamics"],
            "success_rating": learning_assessment["overall_success"],
            "growth_opportunities": learning_assessment["growth_areas"],
            "recommendations": recommendations,
            "activity_timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Completed collaborative activity: {activity.name}")
        return result
    
    def get_peer_relationship_status(self, peer_id: str) -> Dict[str, Any]:
        """Get current relationship status with a specific peer"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT relationship_strength, interaction_count, positive_interactions,
                       conflicts_resolved, collaboration_history, last_interaction_date,
                       relationship_notes
                FROM peer_relationships
                WHERE marcus_id = ? AND peer_id = ?
            """, ("marcus", peer_id))
            
            row = cursor.fetchone()
            if not row:
                return {
                    "peer_id": peer_id,
                    "relationship_strength": 0.5,
                    "interaction_count": 0,
                    "status": "new_relationship"
                }
            
            return {
                "peer_id": peer_id,
                "relationship_strength": row[0],
                "interaction_count": row[1],
                "positive_interactions": row[2],
                "conflicts_resolved": row[3],
                "collaboration_history": json.loads(row[4]) if row[4] else [],
                "last_interaction_date": row[5],
                "relationship_notes": row[6],
                "status": self._categorize_relationship_strength(row[0])
            }
    
    def get_social_skills_progress(self) -> Dict[str, Any]:
        """Get Marcus's current social skills progress"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT skill_area, current_level, practice_count,
                       successful_demonstrations, last_practiced, progress_notes
                FROM social_skills_progress
                WHERE marcus_id = ?
            """, ("marcus",))
            
            skills_data = {}
            for row in cursor.fetchall():
                skill_area = row[0]
                skills_data[skill_area] = {
                    "current_level": row[1],
                    "practice_count": row[2],
                    "successful_demonstrations": row[3],
                    "success_rate": row[3] / row[2] if row[2] > 0 else 0,
                    "last_practiced": row[4],
                    "progress_notes": row[5],
                    "level_description": self._get_skill_level_description(row[1])
                }
            
            # Calculate overall social development
            if skills_data:
                overall_level = sum(data["current_level"] for data in skills_data.values()) / len(skills_data)
                total_practice = sum(data["practice_count"] for data in skills_data.values())
                total_successes = sum(data["successful_demonstrations"] for data in skills_data.values())
            else:
                overall_level = 0.5
                total_practice = 0
                total_successes = 0
            
            return {
                "individual_skills": skills_data,
                "overall_social_level": overall_level,
                "total_practice_sessions": total_practice,
                "total_successful_demonstrations": total_successes,
                "overall_success_rate": total_successes / total_practice if total_practice > 0 else 0,
                "development_stage": self._get_social_development_stage(overall_level),
                "next_focus_areas": self._identify_next_focus_areas(skills_data)
            }
    
    def generate_interaction_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for Marcus's next peer interactions"""
        
        # Get current social skills status
        skills_progress = self.get_social_skills_progress()
        
        # Get peer relationship statuses
        peer_relationships = {}
        for peer_id in self.peers.keys():
            peer_relationships[peer_id] = self.get_peer_relationship_status(peer_id)
        
        # Identify focus areas
        focus_skills = skills_progress.get("next_focus_areas", [])
        
        # Recommend specific peers for different skill development
        peer_recommendations = self._recommend_peers_for_skills(focus_skills, peer_relationships)
        
        # Recommend activities
        activity_recommendations = self._recommend_activities_for_skills(focus_skills)
        
        # Recommend contexts
        context_recommendations = self._recommend_contexts_for_skills(focus_skills)
        
        return {
            "focus_skills": focus_skills,
            "recommended_peers": peer_recommendations,
            "recommended_activities": activity_recommendations,
            "recommended_contexts": context_recommendations,
            "current_social_level": skills_progress.get("overall_social_level", 0.5),
            "development_stage": skills_progress.get("development_stage", "beginning"),
            "priority_interactions": self._prioritize_next_interactions(
                focus_skills, peer_recommendations, activity_recommendations
            )
        }
    
    # Helper methods for internal processing
    def _analyze_social_skills(self, conversation_turns: List[ConversationTurn]) -> List[SocialSkillArea]:
        """Analyze which social skills were demonstrated in conversation"""
        skills_demonstrated = set()
        
        for turn in conversation_turns:
            if turn.speaker == "marcus":
                skills_demonstrated.update(turn.social_skills_demonstrated)
        
        return list(skills_demonstrated)
    
    def _identify_learning_objectives(self, context: InteractionContext, 
                                    topic: ConversationTopic,
                                    conversation_turns: List[ConversationTurn]) -> List[str]:
        """Identify which learning objectives were met during interaction"""
        objectives_met = []
        
        # Context-based objectives
        context_objectives = {
            InteractionContext.CLASSROOM: ["academic collaboration", "following classroom rules"],
            InteractionContext.PLAYGROUND: ["physical play skills", "conflict resolution"],
            InteractionContext.GROUP_PROJECT: ["teamwork", "shared responsibility"],
            InteractionContext.CONFLICT_RESOLUTION: ["problem-solving", "emotional regulation"]
        }
        
        # Topic-based objectives
        topic_objectives = {
            ConversationTopic.ACADEMIC_HELP: ["peer teaching", "asking for help"],
            ConversationTopic.SHARING_INTERESTS: ["self-expression", "active listening"],
            ConversationTopic.SOLVING_PROBLEMS: ["critical thinking", "collaboration"],
            ConversationTopic.FRIENDSHIP_BUILDING: ["social connection", "empathy"]
        }
        
        objectives_met.extend(context_objectives.get(context, []))
        objectives_met.extend(topic_objectives.get(topic, []))
        
        return objectives_met
    
    def _count_collaboration_successes(self, conversation_turns: List[ConversationTurn]) -> int:
        """Count successful collaboration moments in conversation"""
        success_count = 0
        
        for turn in conversation_turns:
            if turn.speaker == "marcus" and turn.response_quality > 0.7:
                if any(skill in [SocialSkillArea.COOPERATION, SocialSkillArea.COMPROMISE, 
                               SocialSkillArea.LEADERSHIP] for skill in turn.social_skills_demonstrated):
                    success_count += 1
        
        return success_count
    
    def _count_conflicts_resolved(self, conversation_turns: List[ConversationTurn]) -> int:
        """Count conflicts that were resolved during interaction"""
        conflicts_resolved = 0
        
        # Look for conflict resolution patterns in conversation
        for i, turn in enumerate(conversation_turns):
            if turn.speaker == "marcus" and "conflict" in turn.emotion:
                # Check if subsequent turns show resolution
                for j in range(i+1, min(i+4, len(conversation_turns))):
                    next_turn = conversation_turns[j]
                    if next_turn.speaker == "marcus" and "happy" in next_turn.emotion:
                        if SocialSkillArea.CONFLICT_RESOLUTION in next_turn.social_skills_demonstrated:
                            conflicts_resolved += 1
                            break
        
        return conflicts_resolved
    
    def _calculate_success_rating(self, conversation_turns: List[ConversationTurn],
                                social_skills_practiced: List[SocialSkillArea],
                                collaboration_successes: int) -> float:
        """Calculate overall success rating for the interaction"""
        
        if not conversation_turns:
            return 0.0
        
        # Calculate average response quality for Marcus's turns
        marcus_turns = [turn for turn in conversation_turns if turn.speaker == "marcus"]
        if not marcus_turns:
            return 0.0
        
        avg_response_quality = sum(turn.response_quality for turn in marcus_turns) / len(marcus_turns)
        
        # Factor in social skills variety
        skills_variety_bonus = min(len(social_skills_practiced) * 0.1, 0.3)
        
        # Factor in collaboration successes
        collaboration_bonus = min(collaboration_successes * 0.05, 0.2)
        
        # Calculate final rating
        success_rating = avg_response_quality + skills_variety_bonus + collaboration_bonus
        
        return min(success_rating, 1.0)
    
    def _identify_growth_areas(self, conversation_turns: List[ConversationTurn]) -> List[str]:
        """Identify areas where Marcus could improve"""
        growth_areas = []
        
        marcus_turns = [turn for turn in conversation_turns if turn.speaker == "marcus"]
        
        # Low response quality turns indicate growth areas
        low_quality_turns = [turn for turn in marcus_turns if turn.response_quality < 0.5]
        
        if len(low_quality_turns) > len(marcus_turns) * 0.3:  # More than 30% low quality
            growth_areas.append("response appropriateness")
        
        # Check for coaching triggers
        coaching_turns = [turn for turn in marcus_turns if turn.coaching_triggered]
        if len(coaching_turns) > 2:
            growth_areas.append("social skill application")
        
        # Check for missing key social skills
        demonstrated_skills = set()
        for turn in marcus_turns:
            demonstrated_skills.update(turn.social_skills_demonstrated)
        
        expected_skills = {SocialSkillArea.ACTIVE_LISTENING, SocialSkillArea.TURN_TAKING, SocialSkillArea.EMPATHY}
        missing_skills = expected_skills - demonstrated_skills
        
        if missing_skills:
            growth_areas.extend([f"{skill.value} development" for skill in missing_skills])
        
        return growth_areas[:4]  # Limit to top 4 areas
    
    def _generate_peer_feedback(self, peers: List[PeerPersonality], 
                              conversation_turns: List[ConversationTurn]) -> Dict[str, str]:
        """Generate feedback from peers about Marcus's interaction"""
        feedback = {}
        
        for peer in peers:
            # Generate age-appropriate feedback based on personality
            if peer.personality_type == PeerPersonalityType.CONFIDENT_LEADER:
                feedback[peer.name] = random.choice([
                    "Marcus is a good friend to play with!",
                    "I like how Marcus listens to everyone's ideas.",
                    "Marcus helped us solve the problem together."
                ])
            elif peer.personality_type == PeerPersonalityType.SHY_THOUGHTFUL:
                feedback[peer.name] = random.choice([
                    "Marcus makes me feel comfortable.",
                    "I like playing with Marcus because he's kind.",
                    "Marcus helped me when I was shy."
                ])
            elif peer.personality_type == PeerPersonalityType.ENERGETIC_FRIENDLY:
                feedback[peer.name] = random.choice([
                    "Marcus is so fun to play with!",
                    "I love how Marcus joins in our games!",
                    "Marcus makes everything more exciting!"
                ])
            else:
                feedback[peer.name] = "Marcus is a good friend."
        
        return feedback
    
    def _store_interaction_session(self, session: PeerInteractionSession):
        """Store interaction session in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Convert conversation turns for JSON serialization
            serializable_turns = []
            for turn in session.conversation_turns:
                turn_dict = asdict(turn)
                # Convert enum values to strings
                if 'social_skills_demonstrated' in turn_dict:
                    turn_dict['social_skills_demonstrated'] = [
                        skill.value if hasattr(skill, 'value') else str(skill)
                        for skill in turn_dict['social_skills_demonstrated']
                    ]
                serializable_turns.append(turn_dict)
            
            cursor.execute("""
                INSERT INTO peer_interaction_sessions
                (session_id, marcus_id, peers_involved, context, topic, duration_minutes,
                 conversation_data, social_skills_practiced, learning_objectives_met,
                 conflicts_resolved, collaboration_successes, overall_success_rating,
                 marcus_growth_areas, peer_feedback, session_timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.marcus_id,
                json.dumps(session.peers_involved),
                session.context.value,
                session.topic.value,
                session.duration_minutes,
                json.dumps(serializable_turns),
                json.dumps([skill.value for skill in session.social_skills_practiced]),
                json.dumps(session.learning_objectives_met),
                session.conflicts_resolved,
                session.collaboration_successes,
                session.overall_success_rating,
                json.dumps(session.marcus_growth_areas),
                json.dumps(session.peer_feedback),
                session.session_timestamp.isoformat()
            ))
            conn.commit()

    # Additional helper methods continued...
    
    def _update_peer_relationships(self, peers: List[PeerPersonality], success_rating: float):
        """Update peer relationship strength based on interaction success"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for peer in peers:
                # Check if relationship exists
                cursor.execute("""
                    SELECT relationship_strength, interaction_count, positive_interactions
                    FROM peer_relationships
                    WHERE marcus_id = ? AND peer_id = ?
                """, ("marcus", peer.id))
                
                row = cursor.fetchone()
                
                if row:
                    # Update existing relationship
                    old_strength = row[0]
                    interaction_count = row[1] + 1
                    positive_interactions = row[2] + (1 if success_rating > 0.6 else 0)
                    
                    # Calculate new strength (weighted average)
                    new_strength = (old_strength * 0.8) + (success_rating * 0.2)
                    
                    cursor.execute("""
                        UPDATE peer_relationships
                        SET relationship_strength = ?, interaction_count = ?,
                            positive_interactions = ?, last_interaction_date = ?
                        WHERE marcus_id = ? AND peer_id = ?
                    """, (new_strength, interaction_count, positive_interactions,
                          datetime.now().date().isoformat(), "marcus", peer.id))
                else:
                    # Create new relationship
                    cursor.execute("""
                        INSERT INTO peer_relationships
                        (marcus_id, peer_id, relationship_strength, interaction_count,
                         positive_interactions, last_interaction_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, ("marcus", peer.id, success_rating, 1,
                          1 if success_rating > 0.6 else 0,
                          datetime.now().date().isoformat()))
            
            conn.commit()
    
    def _update_skills_progress(self, skills_practiced: List[SocialSkillArea], success_rating: float):
        """Update social skills progress based on practice session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for skill in skills_practiced:
                # Check if skill record exists
                cursor.execute("""
                    SELECT current_level, practice_count, successful_demonstrations
                    FROM social_skills_progress
                    WHERE marcus_id = ? AND skill_area = ?
                """, ("marcus", skill.value))
                
                row = cursor.fetchone()
                
                if row:
                    # Update existing skill
                    current_level = row[0]
                    practice_count = row[1] + 1
                    successful_demonstrations = row[2] + (1 if success_rating > 0.6 else 0)
                    
                    # Calculate new level (gradual improvement)
                    if success_rating > 0.7:
                        new_level = min(1.0, current_level + 0.02)  # Small improvement
                    elif success_rating < 0.4:
                        new_level = max(0.1, current_level - 0.01)  # Small decline
                    else:
                        new_level = current_level  # No change
                    
                    cursor.execute("""
                        UPDATE social_skills_progress
                        SET current_level = ?, practice_count = ?,
                            successful_demonstrations = ?, last_practiced = ?
                        WHERE marcus_id = ? AND skill_area = ?
                    """, (new_level, practice_count, successful_demonstrations,
                          datetime.now().date().isoformat(), "marcus", skill.value))
                else:
                    # Create new skill record
                    initial_level = 0.5  # Starting level
                    successful_demonstrations = 1 if success_rating > 0.6 else 0
                    
                    cursor.execute("""
                        INSERT INTO social_skills_progress
                        (marcus_id, skill_area, current_level, practice_count,
                         successful_demonstrations, last_practiced)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, ("marcus", skill.value, initial_level, 1,
                          successful_demonstrations, datetime.now().date().isoformat()))
            
            conn.commit()
    
    def _categorize_relationship_strength(self, strength: float) -> str:
        """Categorize relationship strength into readable levels"""
        if strength >= 0.8:
            return "close_friend"
        elif strength >= 0.6:
            return "good_friend"
        elif strength >= 0.4:
            return "friendly_acquaintance"
        else:
            return "developing_friendship"
    
    def _get_skill_level_description(self, level: float) -> str:
        """Get description for skill level"""
        if level >= 0.8:
            return "proficient"
        elif level >= 0.6:
            return "developing"
        elif level >= 0.4:
            return "emerging"
        else:
            return "beginning"
    
    def _get_social_development_stage(self, overall_level: float) -> str:
        """Get overall social development stage"""
        if overall_level >= 0.8:
            return "advanced_social_skills"
        elif overall_level >= 0.6:
            return "typical_development"
        elif overall_level >= 0.4:
            return "emerging_skills"
        else:
            return "needs_support"
    
    def _identify_next_focus_areas(self, skills_data: Dict[str, Any]) -> List[str]:
        """Identify next focus areas for social skill development"""
        if not skills_data:
            return ["active_listening", "turn_taking", "cooperation"]
        
        # Sort skills by current level (lowest first)
        sorted_skills = sorted(skills_data.items(), 
                             key=lambda x: x[1]["current_level"])
        
        # Return the 3 lowest skills
        return [skill for skill, _ in sorted_skills[:3]]
    
    def _assign_activity_roles(self, activity: CollaborativeLearningActivity,
                             participants: List[str]) -> Dict[str, str]:
        """Assign roles in collaborative activity based on personalities"""
        role_assignments = {}
        available_roles = activity.roles.copy()
        
        # Marcus gets first role preference based on learning needs
        marcus_role = available_roles[0] if available_roles else "participant"
        role_assignments["marcus"] = marcus_role
        if marcus_role in available_roles:
            available_roles.remove(marcus_role)
        
        # Assign roles to peers based on personalities
        for i, participant in enumerate(participants):
            if participant != "marcus" and participant in self.peers:
                peer = self.peers[participant]
                
                # Match role to personality
                preferred_role = self._get_preferred_role(peer, available_roles)
                role_assignments[participant] = preferred_role
                if preferred_role in available_roles:
                    available_roles.remove(preferred_role)
        
        return role_assignments
    
    def _get_preferred_role(self, peer: PeerPersonality, available_roles: List[str]) -> str:
        """Get preferred role for peer based on personality"""
        if not available_roles:
            return "participant"
        
        personality_role_preferences = {
            PeerPersonalityType.CONFIDENT_LEADER: ["Reporter", "Weather Observer", "Story Starter"],
            PeerPersonalityType.SHY_THOUGHTFUL: ["Data Recorder", "Illustrator", "Chart Manager"],
            PeerPersonalityType.ENERGETIC_FRIENDLY: ["Weather Observer", "Character Creator", "Reporter"],
            PeerPersonalityType.ANALYTICAL_PRECISE: ["Data Recorder", "Chart Manager", "Money Counter"],
            PeerPersonalityType.CREATIVE_IMAGINATIVE: ["Illustrator", "Character Creator", "Ending Maker"],
            PeerPersonalityType.SUPPORTIVE_HELPER: ["Problem Solver", "Chart Manager", "Store Clerk"]
        }
        
        preferred_roles = personality_role_preferences.get(peer.personality_type, [])
        
        # Find first available preferred role
        for role in preferred_roles:
            if role in available_roles:
                return role
        
        # Return first available role if no preference match
        return available_roles[0]
    
    def _simulate_activity_execution(self, activity: CollaborativeLearningActivity,
                                   participants: List[str],
                                   role_assignments: Dict[str, str]) -> Dict[str, Any]:
        """Simulate the execution of a collaborative activity"""
        
        # Simulate group dynamics
        group_dynamics = {
            "engagement_level": random.uniform(0.7, 0.9),
            "cooperation_level": random.uniform(0.6, 0.8),
            "conflict_instances": random.randint(0, 2),
            "leadership_moments": random.randint(1, 3),
            "creative_contributions": random.randint(2, 5)
        }
        
        # Simulate individual contributions
        individual_contributions = {}
        for participant in participants:
            if participant == "marcus":
                # Marcus's performance varies by skill development
                performance = {
                    "task_completion": random.uniform(0.6, 0.8),
                    "social_engagement": random.uniform(0.5, 0.7),
                    "role_fulfillment": random.uniform(0.6, 0.8),
                    "peer_interaction": random.uniform(0.5, 0.8)
                }
            else:
                # Peer performance based on personality
                if participant in self.peers:
                    peer = self.peers[participant]
                    performance = self._simulate_peer_performance(peer, activity)
                else:
                    performance = {
                        "task_completion": 0.7,
                        "social_engagement": 0.7,
                        "role_fulfillment": 0.7,
                        "peer_interaction": 0.7
                    }
            
            individual_contributions[participant] = performance
        
        return {
            "group_dynamics": group_dynamics,
            "individual_contributions": individual_contributions,
            "activity_completion": random.uniform(0.7, 0.9),
            "learning_moments": random.randint(3, 6)
        }
    
    def _simulate_peer_performance(self, peer: PeerPersonality,
                                 activity: CollaborativeLearningActivity) -> Dict[str, float]:
        """Simulate peer performance based on personality and activity"""
        
        base_performance = 0.7
        
        # Adjust based on personality strengths
        if peer.personality_type == PeerPersonalityType.CONFIDENT_LEADER:
            return {
                "task_completion": base_performance + 0.1,
                "social_engagement": base_performance + 0.2,
                "role_fulfillment": base_performance + 0.15,
                "peer_interaction": base_performance + 0.1
            }
        elif peer.personality_type == PeerPersonalityType.SHY_THOUGHTFUL:
            return {
                "task_completion": base_performance + 0.05,
                "social_engagement": base_performance - 0.1,
                "role_fulfillment": base_performance,
                "peer_interaction": base_performance - 0.05
            }
        else:
            return {
                "task_completion": base_performance,
                "social_engagement": base_performance,
                "role_fulfillment": base_performance,
                "peer_interaction": base_performance
            }
    
    def _assess_learning_outcomes(self, activity: CollaborativeLearningActivity,
                                activity_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess learning outcomes from collaborative activity"""
        
        # Check which objectives were met
        objectives_met = []
        for objective in activity.learning_objectives:
            # Simulate objective completion based on activity results
            completion_probability = activity_results["activity_completion"] * random.uniform(0.8, 1.0)
            if completion_probability > 0.7:
                objectives_met.append(objective)
        
        # Assess social skills demonstrated
        social_skills_demonstrated = activity.social_skills_focus.copy()
        
        # Add additional skills based on group dynamics
        if activity_results["group_dynamics"]["cooperation_level"] > 0.7:
            social_skills_demonstrated.append(SocialSkillArea.COOPERATION)
        
        if activity_results["group_dynamics"]["leadership_moments"] > 2:
            social_skills_demonstrated.append(SocialSkillArea.LEADERSHIP)
        
        # Individual performance assessment
        individual_performance = activity_results["individual_contributions"]
        
        # Calculate overall success
        avg_performance = sum(
            sum(perf.values()) / len(perf.values()) 
            for perf in individual_performance.values()
        ) / len(individual_performance)
        
        overall_success = (avg_performance + activity_results["activity_completion"]) / 2
        
        # Identify growth areas
        growth_areas = []
        marcus_performance = individual_performance.get("marcus", {})
        for area, score in marcus_performance.items():
            if score < 0.6:
                growth_areas.append(area.replace("_", " "))
        
        return {
            "objectives_met": objectives_met,
            "social_skills": list(set(social_skills_demonstrated)),
            "individual_performance": individual_performance,
            "overall_success": overall_success,
            "growth_areas": growth_areas
        }
    
    def _generate_activity_recommendations(self, activity: CollaborativeLearningActivity,
                                         learning_assessment: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on activity results"""
        recommendations = []
        
        success_rate = learning_assessment["overall_success"]
        
        if success_rate >= 0.8:
            recommendations.append("Excellent collaboration! Ready for more complex activities.")
            recommendations.append(f"Consider advancing to grade-level activities in {activity.subject_area}.")
        elif success_rate >= 0.6:
            recommendations.append("Good progress! Continue with similar collaborative activities.")
            recommendations.append("Focus on strengthening peer communication skills.")
        else:
            recommendations.append("Needs more practice with collaborative skills.")
            recommendations.append("Provide additional scaffolding and smaller group activities.")
        
        # Add specific growth recommendations
        for growth_area in learning_assessment["growth_areas"][:3]:
            recommendations.append(f"Focus on improving {growth_area} in future activities.")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _recommend_peers_for_skills(self, focus_skills: List[str],
                                   peer_relationships: Dict[str, Any]) -> Dict[str, str]:
        """Recommend specific peers for developing focus skills"""
        recommendations = {}
        
        skill_peer_mapping = {
            "active_listening": ["oliver", "alex"],  # Thoughtful, precise peers
            "turn_taking": ["emma", "sofia"],       # Patient, structured peers  
            "empathy": ["oliver", "sofia"],         # Sensitive, creative peers
            "cooperation": ["emma", "zoe"],         # Collaborative, friendly peers
            "leadership": ["emma", "alex"],         # Confident, organized peers
            "conflict_resolution": ["emma", "oliver"]  # Patient, problem-solving peers
        }
        
        for skill in focus_skills:
            recommended_peers = skill_peer_mapping.get(skill, list(self.peers.keys())[:2])
            best_peer = recommended_peers[0] if recommended_peers else "emma"
            
            # Check relationship strength and recommend accordingly
            relationship = peer_relationships.get(best_peer, {})
            relationship_strength = relationship.get("relationship_strength", 0.5)
            
            if relationship_strength > 0.6:
                reason = f"Strong existing relationship for {skill} practice"
            else:
                reason = f"Good personality match for developing {skill}"
            
            recommendations[best_peer] = reason
        
        return recommendations
    
    def _recommend_activities_for_skills(self, focus_skills: List[str]) -> List[str]:
        """Recommend specific activities for developing focus skills"""
        
        skill_activity_mapping = {
            "active_listening": ["storytelling_collaboration", "science_exploration"],
            "turn_taking": ["math_problem_solving", "science_exploration"],
            "cooperation": ["science_exploration", "storytelling_collaboration"],
            "empathy": ["storytelling_collaboration"],
            "leadership": ["math_problem_solving", "storytelling_collaboration"],
            "conflict_resolution": ["math_problem_solving"]
        }
        
        recommended_activities = set()
        for skill in focus_skills:
            activities = skill_activity_mapping.get(skill, [])
            recommended_activities.update(activities)
        
        return list(recommended_activities)
    
    def _recommend_contexts_for_skills(self, focus_skills: List[str]) -> List[str]:
        """Recommend contexts for practicing focus skills"""
        
        skill_context_mapping = {
            "active_listening": [InteractionContext.LIBRARY, InteractionContext.CLASSROOM],
            "turn_taking": [InteractionContext.PLAYGROUND, InteractionContext.GROUP_PROJECT],
            "cooperation": [InteractionContext.CLASSROOM, InteractionContext.GROUP_PROJECT],
            "empathy": [InteractionContext.LUNCH_TABLE, InteractionContext.FREE_PLAY],
            "leadership": [InteractionContext.GROUP_PROJECT, InteractionContext.CLASSROOM],
            "conflict_resolution": [InteractionContext.PLAYGROUND, InteractionContext.CONFLICT_RESOLUTION]
        }
        
        recommended_contexts = set()
        for skill in focus_skills:
            contexts = skill_context_mapping.get(skill, [])
            recommended_contexts.update(contexts)
        
        return [context.value for context in recommended_contexts]
    
    def _prioritize_next_interactions(self, focus_skills: List[str],
                                    peer_recommendations: Dict[str, str],
                                    activity_recommendations: List[str]) -> List[Dict[str, Any]]:
        """Prioritize the most important next interactions"""
        
        priority_interactions = []
        
        # High priority: practice most needed skill with best peer match
        if focus_skills and peer_recommendations:
            top_skill = focus_skills[0]
            best_peer = list(peer_recommendations.keys())[0]
            
            priority_interactions.append({
                "priority": "high",
                "type": "peer_interaction",
                "skill_focus": top_skill,
                "recommended_peer": best_peer,
                "context": "classroom",
                "duration_minutes": 15,
                "reason": f"Most critical skill development with compatible peer"
            })
        
        # Medium priority: collaborative activity
        if activity_recommendations:
            priority_interactions.append({
                "priority": "medium", 
                "type": "collaborative_activity",
                "activity": activity_recommendations[0],
                "skill_focus": focus_skills[:2] if len(focus_skills) >= 2 else focus_skills,
                "context": "group_project",
                "duration_minutes": 25,
                "reason": "Structured practice with multiple skill opportunities"
            })
        
        # Lower priority: social free play
        priority_interactions.append({
            "priority": "low",
            "type": "free_interaction",
            "context": "playground",
            "skill_focus": ["cooperation", "inclusion"],
            "duration_minutes": 20,
            "reason": "Natural social development through play"
        })
        
        return priority_interactions

class ConversationEngine:
    """Engine for generating realistic peer conversations"""
    
    def __init__(self):
        self.conversation_patterns = self._load_conversation_patterns()
    
    def generate_conversation(self, peers: List[PeerPersonality], 
                            context: InteractionContext,
                            topic: ConversationTopic,
                            duration_minutes: int) -> List[ConversationTurn]:
        """Generate a realistic conversation between Marcus and peers"""
        
        conversation_turns = []
        turn_count = duration_minutes * 2  # Roughly 2 turns per minute
        
        # Start conversation
        conversation_turns.append(self._generate_opening_turn(peers[0], context, topic))
        
        # Generate middle conversation
        for i in range(1, turn_count - 1):
            if i % (len(peers) + 1) == 0:  # Marcus's turn
                turn = self._generate_marcus_turn(peers, context, topic, conversation_turns)
            else:
                peer_index = (i - 1) % len(peers)
                turn = self._generate_peer_turn(peers[peer_index], context, topic, conversation_turns)
            
            conversation_turns.append(turn)
        
        # Generate closing
        conversation_turns.append(self._generate_closing_turn(context, topic))
        
        return conversation_turns
    
    def _generate_opening_turn(self, peer: PeerPersonality, 
                             context: InteractionContext,
                             topic: ConversationTopic) -> ConversationTurn:
        """Generate conversation opening based on peer personality and context"""
        
        opening_messages = peer.typical_responses.get("greeting", ["Hi!"])
        message = random.choice(opening_messages)
        
        # Add context-appropriate elements
        if context == InteractionContext.PLAYGROUND:
            message += " Want to play?"
        elif context == InteractionContext.CLASSROOM:
            message += " Should we work together?"
        
        return ConversationTurn(
            speaker=peer.name.lower(),
            message=message,
            emotion="friendly",
            social_skills_demonstrated=[SocialSkillArea.ACTIVE_LISTENING],
            response_quality=0.8
        )
    
    def _generate_marcus_turn(self, peers: List[PeerPersonality],
                            context: InteractionContext,
                            topic: ConversationTopic,
                            previous_turns: List[ConversationTurn]) -> ConversationTurn:
        """Generate Marcus's conversation turn"""
        
        # Analyze previous context
        last_turn = previous_turns[-1] if previous_turns else None
        
        # Generate appropriate response based on social skill level
        marcus_skill_level = 0.6  # Moderate skill level for kindergarten
        
        # Select appropriate response
        if last_turn and "conflict" in last_turn.emotion:
            message = "How can we solve this problem together?"
            skills = [SocialSkillArea.CONFLICT_RESOLUTION, SocialSkillArea.EMPATHY]
            emotion = "problem_solving"
            quality = marcus_skill_level + random.uniform(-0.2, 0.2)
        elif topic == ConversationTopic.ACADEMIC_HELP:
            message = "I can help you with that! Let me show you."
            skills = [SocialSkillArea.COOPERATION, SocialSkillArea.LEADERSHIP]
            emotion = "helpful"
            quality = marcus_skill_level + random.uniform(-0.1, 0.3)
        else:
            message = "That sounds great! I'd like to try that too."
            skills = [SocialSkillArea.ACTIVE_LISTENING, SocialSkillArea.TURN_TAKING]
            emotion = "engaged"
            quality = marcus_skill_level + random.uniform(-0.2, 0.2)
        
        # Check if coaching is needed
        coaching_triggered = quality < 0.4
        coaching_message = None
        if coaching_triggered:
            coaching_message = "Remember to listen carefully to your friends' ideas."
        
        return ConversationTurn(
            speaker="marcus",
            message=message,
            emotion=emotion,
            social_skills_demonstrated=skills,
            response_quality=max(0.1, min(1.0, quality)),
            coaching_triggered=coaching_triggered,
            coaching_message=coaching_message
        )
    
    def _generate_peer_turn(self, peer: PeerPersonality,
                          context: InteractionContext,
                          topic: ConversationTopic,
                          previous_turns: List[ConversationTurn]) -> ConversationTurn:
        """Generate peer's conversation turn based on their personality"""
        
        # Select message based on personality and context
        if topic == ConversationTopic.CONFLICT_DISCUSSION:
            messages = peer.typical_responses.get("conflict", ["I don't know"])
        elif topic == ConversationTopic.CREATIVE_COLLABORATION:
            messages = peer.typical_responses.get("collaboration", ["Let's work together"])
        else:
            messages = peer.typical_responses.get("greeting", ["Okay"])
        
        message = random.choice(messages)
        
        # Determine emotion based on personality tendencies
        emotion_weights = peer.emotional_tendencies
        emotion = max(emotion_weights.items(), key=lambda x: x[1] * random.random())[0]
        
        return ConversationTurn(
            speaker=peer.name.lower(),
            message=message,
            emotion=emotion,
            social_skills_demonstrated=[SocialSkillArea.ACTIVE_LISTENING],
            response_quality=0.7 + random.uniform(-0.2, 0.2)
        )
    
    def _generate_closing_turn(self, context: InteractionContext,
                             topic: ConversationTopic) -> ConversationTurn:
        """Generate conversation closing"""
        
        closing_messages = [
            "That was fun! Let's play again tomorrow.",
            "Good job working together, everyone!",
            "I had a great time with you all.",
            "Thanks for being such good friends!"
        ]
        
        return ConversationTurn(
            speaker="marcus",
            message=random.choice(closing_messages),
            emotion="satisfied",
            social_skills_demonstrated=[SocialSkillArea.COOPERATION],
            response_quality=0.8
        )
    
    def _load_conversation_patterns(self) -> Dict[str, Any]:
        """Load conversation patterns for different scenarios"""
        return {
            "greeting_patterns": ["Hi!", "Hello!", "Want to play?"],
            "conflict_patterns": ["That's not fair!", "I don't like that.", "Let's find a solution."],
            "collaboration_patterns": ["Let's work together!", "I have an idea!", "What do you think?"],
            "closing_patterns": ["That was fun!", "See you later!", "Good job everyone!"]
        }

class SocialDynamicsModel:
    """Model for tracking and predicting social dynamics"""
    
    def __init__(self):
        self.relationship_factors = {
            "shared_interests": 0.3,
            "complementary_personalities": 0.2,
            "positive_interactions": 0.3,
            "conflict_resolution_success": 0.2
        }
    
    def predict_interaction_success(self, marcus_profile: Dict, 
                                  peer_profiles: List[Dict],
                                  context: InteractionContext) -> float:
        """Predict likelihood of successful interaction"""
        
        success_factors = []
        
        for peer_profile in peer_profiles:
            # Calculate compatibility
            compatibility = self._calculate_compatibility(marcus_profile, peer_profile)
            
            # Factor in context appropriateness
            context_factor = self._get_context_factor(peer_profile, context)
            
            # Combine factors
            peer_success_prediction = (compatibility * 0.7) + (context_factor * 0.3)
            success_factors.append(peer_success_prediction)
        
        # Return average prediction
        return sum(success_factors) / len(success_factors) if success_factors else 0.5
    
    def _calculate_compatibility(self, marcus_profile: Dict, peer_profile: Dict) -> float:
        """Calculate compatibility between Marcus and a peer"""
        
        compatibility_score = 0.5  # Base compatibility
        
        # Shared interests bonus
        marcus_interests = set(marcus_profile.get("interests", []))
        peer_interests = set(peer_profile.get("interests", []))
        shared_interests = len(marcus_interests.intersection(peer_interests))
        compatibility_score += shared_interests * 0.1
        
        # Complementary personality bonus
        marcus_personality = marcus_profile.get("personality_type", "")
        peer_personality = peer_profile.get("personality_type", "")
        
        if self._are_personalities_complementary(marcus_personality, peer_personality):
            compatibility_score += 0.2
        
        return min(1.0, compatibility_score)
    
    def _are_personalities_complementary(self, personality1: str, personality2: str) -> bool:
        """Check if two personalities complement each other"""
        
        complementary_pairs = {
            "confident_leader": ["shy_thoughtful", "supportive_helper"],
            "energetic_friendly": ["analytical_precise", "shy_thoughtful"],
            "creative_imaginative": ["analytical_precise", "curious_questioner"],
            "competitive_driven": ["supportive_helper", "shy_thoughtful"]
        }
        
        return personality2 in complementary_pairs.get(personality1, [])
    
    def _get_context_factor(self, peer_profile: Dict, context: InteractionContext) -> float:
        """Get context appropriateness factor for peer"""
        
        peer_personality = peer_profile.get("personality_type", "")
        
        context_preferences = {
            InteractionContext.PLAYGROUND: ["energetic_friendly", "confident_leader"],
            InteractionContext.CLASSROOM: ["analytical_precise", "shy_thoughtful"],
            InteractionContext.ART_CENTER: ["creative_imaginative", "supportive_helper"],
            InteractionContext.LIBRARY: ["shy_thoughtful", "curious_questioner"],
            InteractionContext.GROUP_PROJECT: ["confident_leader", "supportive_helper"]
        }
        
        if peer_personality in context_preferences.get(context, []):
            return 0.8
        else:
            return 0.6

# Factory function for easy integration
def create_peer_interaction_system(db_path: str = "peer_interactions.db") -> PeerInteractionSimulator:
    """Create and initialize the peer interaction simulation system"""
    return PeerInteractionSimulator(db_path=db_path)

# Demo function
def demo_peer_interaction_system():
    """Demonstrate the peer interaction system capabilities"""
    print("🤝 Peer Interaction Simulation System Demo")
    print("=" * 55)
    
    # Create system
    peer_system = create_peer_interaction_system()
    
    # Demonstrate peer interaction simulation
    print("\n📚 Simulating Classroom Collaboration...")
    session = peer_system.simulate_peer_interaction(
        peers_to_include=["emma", "oliver"],
        context=InteractionContext.CLASSROOM,
        topic=ConversationTopic.ACADEMIC_HELP,
        duration_minutes=10
    )
    
    print(f"  👥 Participants: Marcus + {', '.join(session.peers_involved)}")
    print(f"  🏫 Context: {session.context.value}")
    print(f"  💬 Conversation turns: {len(session.conversation_turns)}")
    print(f"  🎯 Skills practiced: {len(session.social_skills_practiced)}")
    print(f"  ⭐ Success rating: {session.overall_success_rating:.1%}")
    print(f"  🔄 Conflicts resolved: {session.conflicts_resolved}")
    print(f"  🤝 Collaboration successes: {session.collaboration_successes}")
    
    # Demonstrate collaborative activity
    print(f"\n🔬 Conducting Science Exploration Activity...")
    activity_result = peer_system.conduct_collaborative_activity(
        activity_id="science_exploration",
        participants=["marcus", "zoe", "alex"]
    )
    
    print(f"  🧪 Activity: {activity_result['activity_name']}")
    print(f"  👥 Participants: {', '.join(activity_result['participants'])}")
    print(f"  🎯 Learning objectives met: {len(activity_result['learning_objectives_met'])}")
    print(f"  💪 Social skills demonstrated: {len(activity_result['social_skills_demonstrated'])}")
    print(f"  ⭐ Success rating: {activity_result['success_rating']:.1%}")
    
    # Show social skills progress
    print(f"\n📊 Social Skills Progress Report...")
    progress = peer_system.get_social_skills_progress()
    print(f"  📈 Overall social level: {progress['overall_social_level']:.1%}")
    print(f"  🎯 Development stage: {progress['development_stage']}")
    print(f"  📚 Total practice sessions: {progress['total_practice_sessions']}")
    print(f"  ✅ Success rate: {progress['overall_success_rate']:.1%}")
    
    # Generate recommendations
    print(f"\n💡 Interaction Recommendations...")
    recommendations = peer_system.generate_interaction_recommendations()
    print(f"  🎯 Focus skills: {', '.join(recommendations['focus_skills'][:3])}")
    print(f"  👥 Recommended peers: {', '.join(list(recommendations['recommended_peers'].keys())[:3])}")
    print(f"  🎪 Priority interactions: {len(recommendations['priority_interactions'])}")
    
    print(f"\n✅ Peer Interaction System Demo Complete!")

if __name__ == "__main__":
    demo_peer_interaction_system()
