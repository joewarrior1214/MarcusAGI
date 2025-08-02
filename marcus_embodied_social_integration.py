#!/usr/bin/env python3
"""
Marcus AGI Embodied Social Learning Integration System

This system integrates Marcus's virtual simple body world with social learning
for comprehensive multi-sensory development including:

1. Virtual Body World - Physical exploration and sensory training
2. Social Interaction Simulation - Peer relationship development  
3. Daily Learning Loop - Academic and embodied learning sessions
4. EQ System - Emotional intelligence with physical awareness
5. Grade Progression - Assessment including physical readiness
6. Multi-Sensory Learning - Vision, touch, movement, and social senses

Enhanced Features:
- Embodied social interactions (physical proximity and movement)
- Sensory-social learning (touch, vision, spatial awareness in social contexts)
- Physical play simulation with peers
- Body language and spatial communication training
- Multi-modal learning experiences
"""

import json
import logging
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from enum import Enum

# Import existing systems
from marcus_simple_body import MarcusGridWorld, EmbodiedLearning
from peer_interaction_simulation import (
    create_peer_interaction_system, PeerInteractionSimulator,
    InteractionContext, ConversationTopic, SocialSkillArea
)

try:
    from marcus_social_integration import (
        MarcusSocialLearningIntegration, IntegratedLearningSession,
        SocialReadinessLevel, EQCoachingSession
    )
    SOCIAL_INTEGRATION_AVAILABLE = True
except ImportError:
    SOCIAL_INTEGRATION_AVAILABLE = False
    logging.warning("Social Integration System not available")

try:
    from daily_learning_loop import run_learning_session, calculate_mastery_levels
    DAILY_LOOP_AVAILABLE = True
except ImportError:
    DAILY_LOOP_AVAILABLE = False
    logging.warning("Daily Learning Loop not available")

try:
    from emotional_intelligence_assessment import (
        EmotionalIntelligenceAssessment, EQDomain, EQSkillLevel
    )
    EQ_SYSTEM_AVAILABLE = True
except ImportError:
    EQ_SYSTEM_AVAILABLE = False
    logging.warning("EQ System not available")

try:
    from grade_progression_system import (
        GradeProgressionSystem, GradeLevel, AcademicSubject
    )
    GRADE_SYSTEM_AVAILABLE = True
except ImportError:
    GRADE_SYSTEM_AVAILABLE = False
    logging.warning("Grade Progression System not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SensoryModalType(Enum):
    """Different sensory modalities for learning"""
    VISUAL = "visual"
    TACTILE = "tactile"
    SPATIAL = "spatial"
    SOCIAL = "social"
    KINESTHETIC = "kinesthetic"
    MULTI_MODAL = "multi_modal"


class PhysicalSocialContext(Enum):
    """Physical contexts for social interactions"""
    PLAYGROUND = "playground"
    CLASSROOM_CIRCLE = "classroom_circle"
    SHARED_WORKSPACE = "shared_workspace"
    OUTDOOR_EXPLORATION = "outdoor_exploration"
    GROUP_ACTIVITY = "group_activity"
    FREE_PLAY = "free_play"


@dataclass
class SensoryLearningExperience:
    """A multi-sensory learning experience combining physical and social elements"""
    session_id: str
    timestamp: datetime
    sensory_modalities: List[SensoryModalType]
    physical_context: PhysicalSocialContext
    social_participants: List[str]
    
    # Physical world data
    marcus_position: Tuple[int, int]
    objects_interacted: List[str]
    movements_made: List[str]
    touch_experiences: List[Dict[str, Any]]
    visual_observations: List[Dict[str, Any]]
    
    # Social interaction data
    social_exchanges: List[Dict[str, Any]]
    peer_proximities: Dict[str, float]  # Distance to each peer
    collaborative_actions: List[str]
    
    # Learning outcomes
    physical_skills_practiced: List[str]
    social_skills_practiced: List[str]
    concepts_discovered: List[str]
    emotional_responses: List[str]
    
    # Integration metrics
    sensory_integration_score: float
    social_physical_coherence: float
    learning_engagement_level: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        result['sensory_modalities'] = [m.value for m in self.sensory_modalities]
        result['physical_context'] = self.physical_context.value
        return result


@dataclass
class EmbodiedSocialSkill:
    """Social skills that involve physical embodiment"""
    name: str
    description: str
    physical_components: List[str]
    social_components: List[str]
    sensory_requirements: List[SensoryModalType]
    practice_contexts: List[PhysicalSocialContext]
    mastery_level: float = 0.0
    practice_sessions: int = 0
    
    def practice(self, success_rate: float):
        """Update skill based on practice session"""
        self.practice_sessions += 1
        # Update mastery with learning rate
        learning_rate = 0.1
        self.mastery_level += learning_rate * (success_rate - self.mastery_level)
        self.mastery_level = min(1.0, max(0.0, self.mastery_level))


class EmbodiedSocialWorld:
    """Extended grid world that includes social peer positions and interactions"""
    
    def __init__(self, size: int = 15):
        self.base_world = MarcusGridWorld(size)
        self.size = size
        
        # Social elements
        self.peer_positions = {}
        self.social_objects = {}
        self.interaction_zones = {}
        
        # Enhanced sensory capabilities
        self.social_vision_range = 5
        self.peer_detection_range = 4
        self.touch_interaction_range = 1.5
        
        # Activity contexts
        self.current_context = PhysicalSocialContext.FREE_PLAY
        self.active_peers = []
        
        self._initialize_social_world()
    
    def _initialize_social_world(self):
        """Add social elements to the physical world"""
        
        # Add peer starting positions
        self.peer_positions = {
            "Alice": [3, 8],
            "Bob": [8, 3], 
            "Charlie": [11, 11],
            "Diana": [2, 12]
        }
        
        # Add social objects (toys, books, shared materials)
        self.social_objects = {
            "playground_ball": {
                "type": "shared_toy",
                "pos": [7, 7],
                "users": [],
                "interaction_type": "cooperative_play"
            },
            "story_book": {
                "type": "shared_learning",
                "pos": [5, 5],
                "users": [],
                "interaction_type": "collaborative_reading"
            },
            "building_blocks": {
                "type": "construction_play",
                "pos": [10, 6],
                "users": [],
                "interaction_type": "cooperative_building"
            }
        }
        
        # Define interaction zones
        self.interaction_zones = {
            "circle_time": {"center": [7, 7], "radius": 3},
            "reading_corner": {"center": [2, 2], "radius": 2},
            "play_area": {"center": [12, 12], "radius": 4}
        }
        
        # Update visual grid to include peers
        self._update_social_grid()
    
    def _update_social_grid(self):
        """Update grid to show both physical objects and social peers"""
        self.base_world._update_grid()
        
        # Add peers to visualization (value 4 for peers)
        for peer_name, pos in self.peer_positions.items():
            if pos:  # Peer is present
                x, y = pos
                if 0 <= x < self.size and 0 <= y < self.size:
                    self.base_world.grid[x, y] = 4
    
    def move_marcus_with_social_awareness(self, direction: str) -> Dict[str, Any]:
        """Enhanced movement that considers social proximity"""
        result = self.base_world.move(direction)
        
        if result['success']:
            # Check for social interactions triggered by movement
            social_encounters = self._check_social_proximity()
            
            if social_encounters:
                result['social_encounters'] = social_encounters
                result['learning_enhanced'] = True
            
            # Update social grid
            self._update_social_grid()
        
        return result
    
    def _check_social_proximity(self) -> List[Dict[str, Any]]:
        """Check if Marcus is close enough to interact with peers"""
        encounters = []
        marcus_pos = self.base_world.marcus_pos
        
        for peer_name, peer_pos in self.peer_positions.items():
            if peer_pos:
                distance = self._calculate_distance(marcus_pos, peer_pos)
                
                if distance <= self.peer_detection_range:
                    encounters.append({
                        "peer": peer_name,
                        "distance": distance,
                        "interaction_possible": distance <= self.touch_interaction_range,
                        "social_signal": self._generate_social_signal(peer_name, distance)
                    })
        
        return encounters
    
    def _calculate_distance(self, pos1: List[int], pos2: List[int]) -> float:
        """Calculate Euclidean distance between positions"""
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _generate_social_signal(self, peer_name: str, distance: float) -> str:
        """Generate social cue based on proximity"""
        if distance <= 1.5:
            return f"{peer_name} is right next to you and smiles"
        elif distance <= 3:
            return f"{peer_name} notices you and waves"
        else:
            return f"{peer_name} is nearby playing"
    
    def social_look(self) -> Dict[str, Any]:
        """Enhanced look that includes social awareness"""
        base_vision = self.base_world.look()
        
        # Add social observations
        social_observations = []
        marcus_pos = self.base_world.marcus_pos
        
        for peer_name, peer_pos in self.peer_positions.items():
            if peer_pos:
                distance = self._calculate_distance(marcus_pos, peer_pos)
                if distance <= self.social_vision_range:
                    # Generate social observation
                    activity = self._infer_peer_activity(peer_name, peer_pos)
                    social_observations.append({
                        "peer": peer_name,
                        "position": peer_pos,
                        "distance": distance,
                        "activity": activity,
                        "body_language": self._generate_body_language(peer_name, distance),
                        "interaction_opportunity": distance <= 2.0
                    })
        
        # Check for social objects
        social_object_observations = []
        for obj_name, obj_data in self.social_objects.items():
            obj_pos = obj_data["pos"]
            distance = self._calculate_distance(marcus_pos, obj_pos)
            if distance <= self.social_vision_range:
                social_object_observations.append({
                    "object": obj_name,
                    "type": obj_data["type"],
                    "distance": distance,
                    "current_users": obj_data["users"],
                    "interaction_type": obj_data["interaction_type"],
                    "available": len(obj_data["users"]) < 3
                })
        
        base_vision.update({
            "social_observations": social_observations,
            "social_objects": social_object_observations,
            "interaction_zones": self._get_nearby_zones(marcus_pos)
        })
        
        return base_vision
    
    def _infer_peer_activity(self, peer_name: str, peer_pos: List[int]) -> str:
        """Infer what the peer is doing based on position and context"""
        activities = [
            "playing with blocks",
            "reading a book", 
            "drawing pictures",
            "looking around curiously",
            "organizing materials"
        ]
        return random.choice(activities)
    
    def _generate_body_language(self, peer_name: str, distance: float) -> str:
        """Generate body language cues"""
        if distance <= 2:
            return random.choice([
                "making eye contact and smiling",
                "gesturing for you to come over",
                "showing you something interesting"
            ])
        else:
            return random.choice([
                "focused on their activity",
                "looking up occasionally",
                "moving around actively"
            ])
    
    def _get_nearby_zones(self, marcus_pos: List[int]) -> List[Dict[str, Any]]:
        """Get interaction zones Marcus is near"""
        nearby_zones = []
        
        for zone_name, zone_data in self.interaction_zones.items():
            center = zone_data["center"]
            radius = zone_data["radius"]
            distance = self._calculate_distance(marcus_pos, center)
            
            if distance <= radius + 1:  # Include just outside radius
                nearby_zones.append({
                    "zone": zone_name,
                    "distance_to_center": distance,
                    "inside_zone": distance <= radius,
                    "activity_suggestion": self._get_zone_activity(zone_name)
                })
        
        return nearby_zones
    
    def _get_zone_activity(self, zone_name: str) -> str:
        """Get suggested activity for zone"""
        activities = {
            "circle_time": "Join group discussion or story time",
            "reading_corner": "Read books together with peers", 
            "play_area": "Engage in cooperative play activities"
        }
        return activities.get(zone_name, "Explore and interact")
    
    def initiate_social_interaction(self, peer_name: str, interaction_type: str = "greeting") -> Dict[str, Any]:
        """Start a social interaction with a peer"""
        if peer_name not in self.peer_positions:
            return {"success": False, "reason": "Peer not found"}
        
        peer_pos = self.peer_positions[peer_name]
        marcus_pos = self.base_world.marcus_pos
        distance = self._calculate_distance(marcus_pos, peer_pos)
        
        if distance > self.touch_interaction_range:
            return {
                "success": False, 
                "reason": "Too far away", 
                "suggestion": f"Move closer to {peer_name} first"
            }
        
        # Simulate the social interaction
        interaction_success = random.uniform(0.6, 0.95)  # Generally positive
        
        interaction_result = {
            "success": True,
            "peer": peer_name,
            "interaction_type": interaction_type,
            "success_rate": interaction_success,
            "peer_response": self._generate_peer_response(peer_name, interaction_type, interaction_success),
            "social_learning": self._extract_social_learning(interaction_type, interaction_success),
            "physical_awareness": f"Standing close to {peer_name}, can see their facial expressions clearly"
        }
        
        return interaction_result
    
    def _generate_peer_response(self, peer_name: str, interaction_type: str, success_rate: float) -> str:
        """Generate realistic peer response"""
        if success_rate > 0.8:
            responses = {
                "greeting": f"{peer_name} smiles warmly and says 'Hi Marcus! Want to play?'",
                "collaboration": f"{peer_name} nods enthusiastically: 'Yes! Let's work together!'",
                "sharing": f"{peer_name} happily shares: 'Of course! Here you go!'",
                "comfort": f"{peer_name} gently responds: 'It's okay, I understand how you feel.'"
            }
        else:
            responses = {
                "greeting": f"{peer_name} looks up briefly and gives a small wave",
                "collaboration": f"{peer_name} hesitates: 'I'm not sure... maybe later?'",
                "sharing": f"{peer_name} considers: 'I need this right now, but you can have it next'",
                "comfort": f"{peer_name} nods: 'That sounds hard. I hope you feel better.'"
            }
        
        return responses.get(interaction_type, f"{peer_name} responds thoughtfully")
    
    def _extract_social_learning(self, interaction_type: str, success_rate: float) -> str:
        """Extract learning from social interaction"""
        learnings = {
            "greeting": "Friendly greetings help start positive interactions",
            "collaboration": "Working together can be more fun than working alone",
            "sharing": "Sharing creates good feelings between friends",
            "comfort": "Being kind when someone is sad helps them feel better"
        }
        
        base_learning = learnings.get(interaction_type, "Social interactions teach me about others")
        
        if success_rate > 0.8:
            return f"{base_learning} - This interaction went really well!"
        else:
            return f"{base_learning} - Sometimes interactions don't go as expected, and that's okay"


class MarcusEmbodiedSocialIntegration:
    """Main integration system combining virtual body world with social learning"""
    
    def __init__(self, world_size: int = 15):
        # Initialize embodied social world
        self.embodied_world = EmbodiedSocialWorld(world_size)
        
        # Initialize existing systems
        self.peer_simulator = create_peer_interaction_system()
        
        # Initialize available integrated systems
        self.social_integration = None
        if SOCIAL_INTEGRATION_AVAILABLE:
            try:
                self.social_integration = MarcusSocialLearningIntegration()
            except Exception as e:
                logger.warning(f"Could not initialize social integration: {e}")
        
        # Embodied social skills to develop
        self.embodied_social_skills = self._initialize_embodied_skills()
        
        # Learning tracking
        self.learning_sessions = []
        self.sensory_experiences = []
        
        # Configuration
        self.session_id_counter = 1
    
    def _initialize_embodied_skills(self) -> Dict[str, EmbodiedSocialSkill]:
        """Initialize embodied social skills Marcus will develop"""
        skills = {}
        
        skills["personal_space_awareness"] = EmbodiedSocialSkill(
            name="Personal Space Awareness",
            description="Understanding comfortable distances in social interactions",
            physical_components=["proximity_sensing", "movement_control", "spatial_awareness"],
            social_components=["reading_comfort_cues", "respecting_boundaries", "appropriate_closeness"],
            sensory_requirements=[SensoryModalType.SPATIAL, SensoryModalType.VISUAL, SensoryModalType.SOCIAL],
            practice_contexts=[PhysicalSocialContext.CLASSROOM_CIRCLE, PhysicalSocialContext.FREE_PLAY]
        )
        
        skills["collaborative_movement"] = EmbodiedSocialSkill(
            name="Collaborative Movement",
            description="Coordinating physical actions with peers",
            physical_components=["synchronized_movement", "following_leaders", "spatial_coordination"],
            social_components=["taking_turns", "following_instructions", "group_coordination"],
            sensory_requirements=[SensoryModalType.KINESTHETIC, SensoryModalType.VISUAL, SensoryModalType.SOCIAL],
            practice_contexts=[PhysicalSocialContext.GROUP_ACTIVITY, PhysicalSocialContext.PLAYGROUND]
        )
        
        skills["touch_social_communication"] = EmbodiedSocialSkill(
            name="Touch-Social Communication",
            description="Using appropriate touch in social contexts",
            physical_components=["gentle_touch", "touch_sensitivity", "touch_timing"],
            social_components=["consent_understanding", "comfort_expression", "affection_appropriateness"],
            sensory_requirements=[SensoryModalType.TACTILE, SensoryModalType.SOCIAL],
            practice_contexts=[PhysicalSocialContext.SHARED_WORKSPACE, PhysicalSocialContext.FREE_PLAY]
        )
        
        skills["visual_social_tracking"] = EmbodiedSocialSkill(
            name="Visual Social Tracking",
            description="Using vision to understand social dynamics",
            physical_components=["eye_movement", "attention_direction", "visual_scanning"],
            social_components=["reading_expressions", "following_social_cues", "group_awareness"],
            sensory_requirements=[SensoryModalType.VISUAL, SensoryModalType.SOCIAL],
            practice_contexts=[PhysicalSocialContext.CLASSROOM_CIRCLE, PhysicalSocialContext.GROUP_ACTIVITY]
        )
        
        skills["shared_object_play"] = EmbodiedSocialSkill(
            name="Shared Object Play",
            description="Playing cooperatively with shared physical objects",
            physical_components=["object_manipulation", "sharing_movements", "cooperative_handling"],
            social_components=["turn_taking", "sharing_negotiation", "collaborative_creativity"],
            sensory_requirements=[SensoryModalType.TACTILE, SensoryModalType.VISUAL, SensoryModalType.SOCIAL],
            practice_contexts=[PhysicalSocialContext.SHARED_WORKSPACE, PhysicalSocialContext.FREE_PLAY]
        )
        
        return skills
    
    def run_embodied_social_session(self, duration_minutes: int = 30, 
                                   context: PhysicalSocialContext = PhysicalSocialContext.FREE_PLAY) -> SensoryLearningExperience:
        """Run a comprehensive embodied social learning session"""
        
        session_id = f"embodied_social_{self.session_id_counter}"
        self.session_id_counter += 1
        
        print(f"\n🎮🤝 Starting Embodied Social Learning Session: {session_id}")
        print(f"Context: {context.value} | Duration: {duration_minutes} minutes")
        
        # Initialize session tracking
        sensory_modalities = []
        social_participants = []
        objects_interacted = []
        movements_made = []
        touch_experiences = []
        visual_observations = []
        social_exchanges = []
        peer_proximities = {}
        collaborative_actions = []
        physical_skills_practiced = []
        social_skills_practiced = []
        concepts_discovered = []
        emotional_responses = []
        
        # Set world context
        self.embodied_world.current_context = context
        
        # Phase 1: Environmental Awareness (5 minutes)
        print("\n👁️ Phase 1: Multi-Sensory Environmental Awareness")
        
        # Enhanced looking with social awareness
        vision_result = self.embodied_world.social_look()
        visual_observations.append(vision_result)
        sensory_modalities.append(SensoryModalType.VISUAL)
        
        print(f"Visual observations: {len(vision_result['visible_objects'])} objects, {len(vision_result['social_observations'])} peers")
        
        if vision_result['social_observations']:
            for obs in vision_result['social_observations']:
                peer_name = obs['peer']
                social_participants.append(peer_name)
                peer_proximities[peer_name] = obs['distance']
                print(f"  - {peer_name}: {obs['activity']}, {obs['body_language']}")
        
        # Phase 2: Physical Exploration with Social Awareness (10 minutes)
        print("\n🚶‍♂️ Phase 2: Physical Exploration with Social Awareness")
        
        exploration_actions = ['move', 'touch', 'social_approach', 'object_interaction']
        
        for i in range(8):  # 8 exploration actions
            action = random.choice(exploration_actions)
            
            if action == 'move':
                direction = random.choice(['north', 'south', 'east', 'west'])
                move_result = self.embodied_world.move_marcus_with_social_awareness(direction)
                movements_made.append(f"{direction}: {move_result['success']}")
                sensory_modalities.append(SensoryModalType.KINESTHETIC)
                
                if move_result.get('social_encounters'):
                    for encounter in move_result['social_encounters']:
                        social_exchanges.append({
                            'type': 'proximity_encounter',
                            'peer': encounter['peer'],
                            'message': encounter['social_signal']
                        })
                        print(f"  Social encounter: {encounter['social_signal']}")
            
            elif action == 'touch':
                touch_result = self.embodied_world.base_world.touch()
                touch_experiences.append(touch_result)
                sensory_modalities.append(SensoryModalType.TACTILE)
                
                if touch_result.get('learning'):
                    # Handle different learning data structures
                    learning_data = touch_result['learning']
                    if isinstance(learning_data, dict):
                        # Learning is an experience object
                        learning_text = learning_data.get('learning', str(learning_data))
                    else:
                        # Learning is a string
                        learning_text = str(learning_data)
                    
                    concepts_discovered.append(learning_text)
                    print(f"  Touch learning: {learning_text}")
            
            elif action == 'social_approach':
                # Find nearest peer and approach
                vision = self.embodied_world.social_look()
                if vision['social_observations']:
                    nearest_peer = min(vision['social_observations'], key=lambda x: x['distance'])
                    peer_name = nearest_peer['peer']
                    
                    # Move toward peer
                    peer_pos = self.embodied_world.peer_positions[peer_name]
                    marcus_pos = self.embodied_world.base_world.marcus_pos
                    
                    # Simple approach logic
                    if marcus_pos[0] < peer_pos[0]:
                        approach_result = self.embodied_world.move_marcus_with_social_awareness('south')
                    elif marcus_pos[0] > peer_pos[0]:
                        approach_result = self.embodied_world.move_marcus_with_social_awareness('north')
                    elif marcus_pos[1] < peer_pos[1]:
                        approach_result = self.embodied_world.move_marcus_with_social_awareness('east')
                    elif marcus_pos[1] > peer_pos[1]:
                        approach_result = self.embodied_world.move_marcus_with_social_awareness('west')
                    
                    movements_made.append(f"approach_{peer_name}")
                    print(f"  Approaching {peer_name}")
            
            elif action == 'object_interaction':
                # Try to grab or interact with nearby objects
                grab_result = self.embodied_world.base_world.grab()
                if grab_result['success']:
                    objects_interacted.append(grab_result['holding'])
                    sensory_modalities.extend([SensoryModalType.TACTILE, SensoryModalType.VISUAL])
                    
                    # Check if object can be shared
                    obj_name = grab_result['holding']
                    if obj_name in self.embodied_world.social_objects:
                        collaborative_actions.append(f"picked_up_shared_{obj_name}")
                        print(f"  Picked up shared object: {obj_name}")
        
        # Phase 3: Direct Social Interactions (10 minutes)
        print("\n🤝 Phase 3: Direct Social Interactions")
        
        interaction_types = ['greeting', 'collaboration', 'sharing', 'comfort']
        
        # Try 4 social interactions
        for i in range(4):
            # Find available peers nearby
            vision = self.embodied_world.social_look()
            available_peers = [obs for obs in vision['social_observations'] 
                             if obs['interaction_opportunity']]
            
            if available_peers:
                peer_obs = random.choice(available_peers)
                peer_name = peer_obs['peer']
                interaction_type = random.choice(interaction_types)
                
                interaction_result = self.embodied_world.initiate_social_interaction(
                    peer_name, interaction_type
                )
                
                if interaction_result['success']:
                    social_exchanges.append({
                        'type': interaction_type,
                        'peer': peer_name,
                        'success_rate': interaction_result['success_rate'],
                        'response': interaction_result['peer_response'],
                        'learning': interaction_result['social_learning']
                    })
                    
                    concepts_discovered.append(interaction_result['social_learning'])
                    
                    # Practice embodied social skills
                    if interaction_type == 'greeting':
                        self.embodied_social_skills['personal_space_awareness'].practice(
                            interaction_result['success_rate']
                        )
                        self.embodied_social_skills['visual_social_tracking'].practice(
                            interaction_result['success_rate']
                        )
                        physical_skills_practiced.extend([
                            'personal_space_awareness', 'visual_social_tracking'
                        ])
                    
                    elif interaction_type == 'collaboration':
                        self.embodied_social_skills['collaborative_movement'].practice(
                            interaction_result['success_rate']
                        )
                        collaborative_actions.append(f"collaborated_with_{peer_name}")
                        physical_skills_practiced.append('collaborative_movement')
                    
                    elif interaction_type == 'sharing':
                        self.embodied_social_skills['shared_object_play'].practice(
                            interaction_result['success_rate']
                        )
                        if self.embodied_world.base_world.holding:
                            collaborative_actions.append(f"shared_{self.embodied_world.base_world.holding}")
                        physical_skills_practiced.append('shared_object_play')
                    
                    social_skills_practiced.append(interaction_type)
                    sensory_modalities.append(SensoryModalType.SOCIAL)
                    
                    print(f"  {interaction_type.title()} with {peer_name}: {interaction_result['success_rate']:.2f} success")
                    print(f"    Response: {interaction_result['peer_response']}")
        
        # Phase 4: Reflection and Integration (5 minutes)
        print("\n🧠 Phase 4: Multi-Sensory Integration and Reflection")
        
        # Calculate integration metrics
        unique_modalities = list(set(sensory_modalities))
        sensory_integration_score = len(unique_modalities) / len(SensoryModalType) 
        
        social_physical_coherence = 0.0
        if social_exchanges and (movements_made or touch_experiences):
            # Calculate how well social and physical activities were integrated
            social_actions = len(social_exchanges)
            physical_actions = len(movements_made) + len(touch_experiences)
            coherence_ratio = min(social_actions, physical_actions) / max(social_actions, physical_actions, 1)
            social_physical_coherence = coherence_ratio
        
        learning_engagement_level = 0.0
        if concepts_discovered:
            # Base engagement on variety and number of discoveries
            unique_concepts = len(set(concepts_discovered))
            learning_engagement_level = min(1.0, unique_concepts / 10)  # Scale to 0-1
        
        # Generate emotional responses
        if social_exchanges:
            positive_interactions = sum(1 for ex in social_exchanges if ex.get('success_rate', 0) > 0.7)
            if positive_interactions > len(social_exchanges) * 0.6:
                emotional_responses.append("happy_social_connection")
            if collaborative_actions:
                emotional_responses.append("proud_cooperation")
        
        if concepts_discovered:
            emotional_responses.append("curious_discovery")
            
        # Create comprehensive learning experience
        experience = SensoryLearningExperience(
            session_id=session_id,
            timestamp=datetime.now(),
            sensory_modalities=unique_modalities,
            physical_context=context,
            social_participants=list(set(social_participants)),
            marcus_position=tuple(self.embodied_world.base_world.marcus_pos),
            objects_interacted=objects_interacted,
            movements_made=movements_made,
            touch_experiences=touch_experiences,
            visual_observations=visual_observations,
            social_exchanges=social_exchanges,
            peer_proximities=peer_proximities,
            collaborative_actions=collaborative_actions,
            physical_skills_practiced=physical_skills_practiced,
            social_skills_practiced=social_skills_practiced,
            concepts_discovered=concepts_discovered,
            emotional_responses=emotional_responses,
            sensory_integration_score=sensory_integration_score,
            social_physical_coherence=social_physical_coherence,
            learning_engagement_level=learning_engagement_level
        )
        
        self.sensory_experiences.append(experience)
        
        # Display session summary
        print(f"\n📊 Session Summary:")
        print(f"Sensory Integration: {sensory_integration_score:.2f} ({len(unique_modalities)}/{len(SensoryModalType)} modalities)")
        print(f"Social-Physical Coherence: {social_physical_coherence:.2f}")
        print(f"Learning Engagement: {learning_engagement_level:.2f}")
        print(f"Social Interactions: {len(social_exchanges)}")
        print(f"Concepts Discovered: {len(set(concepts_discovered))}")
        print(f"Skills Practiced: {len(set(physical_skills_practiced + social_skills_practiced))}")
        
        return experience
    
    def get_embodied_social_progress_report(self) -> Dict[str, Any]:
        """Generate comprehensive progress report on embodied social learning"""
        
        if not self.sensory_experiences:
            return {"status": "No learning sessions completed yet"}
        
        # Calculate overall metrics
        avg_sensory_integration = np.mean([exp.sensory_integration_score for exp in self.sensory_experiences])
        avg_social_physical_coherence = np.mean([exp.social_physical_coherence for exp in self.sensory_experiences])
        avg_learning_engagement = np.mean([exp.learning_engagement_level for exp in self.sensory_experiences])
        
        # Skill development analysis
        skill_progress = {}
        for skill_name, skill in self.embodied_social_skills.items():
            skill_progress[skill_name] = {
                "mastery_level": skill.mastery_level,
                "practice_sessions": skill.practice_sessions,
                "description": skill.description,
                "readiness_level": self._assess_skill_readiness(skill)
            }
        
        # Sensory modality usage analysis
        all_modalities = []
        for exp in self.sensory_experiences:
            all_modalities.extend(exp.sensory_modalities)
        
        modality_frequency = {}
        for modality in SensoryModalType:
            count = all_modalities.count(modality)
            modality_frequency[modality.value] = {
                "usage_count": count,
                "usage_percentage": count / len(all_modalities) * 100 if all_modalities else 0
            }
        
        # Social interaction analysis
        all_social_exchanges = []
        for exp in self.sensory_experiences:
            all_social_exchanges.extend(exp.social_exchanges)
        
        social_interaction_success = []
        for exchange in all_social_exchanges:
            if 'success_rate' in exchange:
                social_interaction_success.append(exchange['success_rate'])
        
        avg_social_success = np.mean(social_interaction_success) if social_interaction_success else 0.0
        
        # Physical context diversity
        contexts_used = [exp.physical_context for exp in self.sensory_experiences]
        context_diversity = len(set(contexts_used)) / len(PhysicalSocialContext)
        
        # Learning trend analysis
        recent_sessions = self.sensory_experiences[-5:] if len(self.sensory_experiences) >= 5 else self.sensory_experiences
        recent_avg_engagement = np.mean([exp.learning_engagement_level for exp in recent_sessions])
        
        engagement_trend = "improving" if recent_avg_engagement > avg_learning_engagement else "stable"
        
        # Overall readiness assessment
        overall_readiness = self._calculate_embodied_social_readiness()
        
        return {
            "total_sessions": len(self.sensory_experiences),
            "overall_metrics": {
                "sensory_integration_score": round(avg_sensory_integration, 3),
                "social_physical_coherence": round(avg_social_physical_coherence, 3), 
                "learning_engagement_level": round(avg_learning_engagement, 3),
                "social_interaction_success_rate": round(avg_social_success, 3)
            },
            "skill_development": skill_progress,
            "sensory_modality_usage": modality_frequency,
            "social_interaction_metrics": {
                "total_interactions": len(all_social_exchanges),
                "average_success_rate": round(avg_social_success, 3),
                "interaction_types_practiced": len(set(ex.get('type', 'unknown') for ex in all_social_exchanges))
            },
            "learning_diversity": {
                "physical_contexts_explored": len(set(contexts_used)),
                "context_diversity_score": round(context_diversity, 3),
                "unique_peers_interacted": len(set().union(*[exp.social_participants for exp in self.sensory_experiences]))
            },
            "development_trends": {
                "engagement_trend": engagement_trend,
                "recent_session_performance": round(recent_avg_engagement, 3),
                "sessions_in_analysis": len(recent_sessions)
            },
            "embodied_social_readiness": overall_readiness,
            "recommendations": self._generate_learning_recommendations()
        }
    
    def _assess_skill_readiness(self, skill: EmbodiedSocialSkill) -> str:
        """Assess readiness level for a specific embodied social skill"""
        if skill.mastery_level >= 0.8:
            return "Advanced"
        elif skill.mastery_level >= 0.6:
            return "Proficient"  
        elif skill.mastery_level >= 0.4:
            return "Developing"
        elif skill.mastery_level >= 0.2:
            return "Beginning"
        else:
            return "Emerging"
    
    def _calculate_embodied_social_readiness(self) -> Dict[str, Any]:
        """Calculate overall readiness for embodied social learning environments"""
        
        if not self.sensory_experiences:
            return {"readiness_level": "Not Yet Assessed", "readiness_score": 0.0}
        
        # Factor weights
        weights = {
            "sensory_integration": 0.25,
            "social_physical_coherence": 0.25,
            "skill_mastery": 0.30,
            "learning_engagement": 0.20
        }
        
        # Calculate component scores
        sensory_score = np.mean([exp.sensory_integration_score for exp in self.sensory_experiences])
        coherence_score = np.mean([exp.social_physical_coherence for exp in self.sensory_experiences])
        engagement_score = np.mean([exp.learning_engagement_level for exp in self.sensory_experiences])
        
        skill_scores = [skill.mastery_level for skill in self.embodied_social_skills.values()]
        skill_mastery_score = np.mean(skill_scores) if skill_scores else 0.0
        
        # Calculate weighted overall score
        overall_score = (
            sensory_score * weights["sensory_integration"] +
            coherence_score * weights["social_physical_coherence"] +
            skill_mastery_score * weights["skill_mastery"] +
            engagement_score * weights["learning_engagement"]
        )
        
        # Determine readiness level
        if overall_score >= 0.85:
            readiness_level = "Fully Ready for Advanced Embodied Social Learning"
        elif overall_score >= 0.70:
            readiness_level = "Ready for Full Embodied Social Integration"
        elif overall_score >= 0.55:
            readiness_level = "Ready for Structured Embodied Social Activities"
        elif overall_score >= 0.40:
            readiness_level = "Ready for Guided Embodied Social Practice"
        else:
            readiness_level = "Needs Foundational Embodied Social Development"
        
        return {
            "readiness_level": readiness_level,
            "readiness_score": round(overall_score, 3),
            "component_scores": {
                "sensory_integration": round(sensory_score, 3),
                "social_physical_coherence": round(coherence_score, 3),
                "skill_mastery": round(skill_mastery_score, 3),
                "learning_engagement": round(engagement_score, 3)
            }
        }
    
    def _generate_learning_recommendations(self) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        if not self.sensory_experiences:
            return ["Complete initial embodied social learning sessions to generate recommendations"]
        
        # Analyze recent performance
        recent_exp = self.sensory_experiences[-1]
        
        # Sensory integration recommendations
        if recent_exp.sensory_integration_score < 0.6:
            recommendations.append("Focus on multi-sensory activities that combine touch, vision, and movement")
        
        # Social-physical coherence recommendations
        if recent_exp.social_physical_coherence < 0.5:
            recommendations.append("Practice activities that require coordination between social interaction and physical movement")
        
        # Skill-specific recommendations
        for skill_name, skill in self.embodied_social_skills.items():
            if skill.mastery_level < 0.5 and skill.practice_sessions > 0:
                recommendations.append(f"Continue practicing {skill.description.lower()} in varied contexts")
            elif skill.practice_sessions == 0:
                recommendations.append(f"Begin practicing {skill.description.lower()}")
        
        # Context diversity recommendations
        contexts_used = set(exp.physical_context for exp in self.sensory_experiences)
        if len(contexts_used) < 3:
            unused_contexts = set(PhysicalSocialContext) - contexts_used
            if unused_contexts:
                recommendations.append(f"Explore new learning contexts: {', '.join(c.value for c in list(unused_contexts)[:2])}")
        
        # Social interaction recommendations
        all_exchanges = []
        for exp in self.sensory_experiences:
            all_exchanges.extend(exp.social_exchanges)
        
        interaction_types = set(ex.get('type', 'unknown') for ex in all_exchanges)
        if len(interaction_types) < 3:
            recommendations.append("Practice more diverse types of social interactions (greeting, collaboration, sharing, comfort)")
        
        # Engagement recommendations
        if recent_exp.learning_engagement_level < 0.6:
            recommendations.append("Engage in more exploratory activities to discover new concepts and connections")
        
        return recommendations
    
    def save_embodied_social_data(self, filename: str = "marcus_embodied_social_learning.json"):
        """Save comprehensive embodied social learning data"""
        
        def convert_for_json(obj):
            """Convert complex objects to JSON-serializable format"""
            if isinstance(obj, bool):
                return obj
            elif isinstance(obj, (int, float, str)):
                return obj
            elif isinstance(obj, (list, tuple)):
                return [convert_for_json(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_for_json(value) for key, value in obj.items()}
            elif hasattr(obj, '__dict__'):
                return convert_for_json(obj.__dict__)
            else:
                return str(obj)
        
        data = {
            "system_info": {
                "integration_type": "embodied_social_learning",
                "world_size": self.embodied_world.size,
                "total_sessions": len(self.sensory_experiences),
                "creation_timestamp": datetime.now().isoformat()
            },
            "embodied_social_skills": {
                name: {
                    "description": skill.description,
                    "mastery_level": float(skill.mastery_level),
                    "practice_sessions": int(skill.practice_sessions),
                    "physical_components": skill.physical_components,
                    "social_components": skill.social_components,
                    "sensory_requirements": [req.value for req in skill.sensory_requirements],
                    "practice_contexts": [ctx.value for ctx in skill.practice_contexts]
                }
                for name, skill in self.embodied_social_skills.items()
            },
            "learning_experiences": [convert_for_json(exp.to_dict()) for exp in self.sensory_experiences],
            "progress_report": convert_for_json(self.get_embodied_social_progress_report())
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved embodied social learning data: {len(self.sensory_experiences)} sessions, {len(self.embodied_social_skills)} skills tracked")


# Example usage and demonstration
def demo_embodied_social_integration():
    """Demonstrate the complete embodied social learning integration"""
    
    print("🎮🤝 Marcus AGI Embodied Social Learning Integration Demo")
    print("=" * 60)
    
    # Initialize the integration system
    integration = MarcusEmbodiedSocialIntegration(world_size=12)
    
    # Run multiple learning sessions in different contexts
    contexts = [
        PhysicalSocialContext.FREE_PLAY,
        PhysicalSocialContext.CLASSROOM_CIRCLE,
        PhysicalSocialContext.PLAYGROUND,
        PhysicalSocialContext.SHARED_WORKSPACE
    ]
    
    print(f"\n🎯 Running {len(contexts)} embodied social learning sessions...")
    
    for i, context in enumerate(contexts):
        print(f"\n{'='*50}")
        print(f"Session {i+1}: {context.value}")
        print(f"{'='*50}")
        
        experience = integration.run_embodied_social_session(
            duration_minutes=25, 
            context=context
        )
        
        print(f"\nSession {i+1} completed successfully!")
        print(f"Integration Score: {experience.sensory_integration_score:.3f}")
        print(f"Social-Physical Coherence: {experience.social_physical_coherence:.3f}")
        print(f"Learning Engagement: {experience.learning_engagement_level:.3f}")
    
    # Generate comprehensive progress report
    print(f"\n{'='*60}")
    print("📊 COMPREHENSIVE EMBODIED SOCIAL PROGRESS REPORT")
    print(f"{'='*60}")
    
    report = integration.get_embodied_social_progress_report()
    
    print(f"\n🎯 Overall Performance:")
    metrics = report['overall_metrics']
    print(f"  Sensory Integration: {metrics['sensory_integration_score']:.3f}")
    print(f"  Social-Physical Coherence: {metrics['social_physical_coherence']:.3f}")
    print(f"  Learning Engagement: {metrics['learning_engagement_level']:.3f}")
    print(f"  Social Success Rate: {metrics['social_interaction_success_rate']:.3f}")
    
    print(f"\n🧠 Embodied Social Skills Development:")
    for skill_name, skill_data in report['skill_development'].items():
        print(f"  {skill_name}: {skill_data['mastery_level']:.3f} ({skill_data['readiness_level']})")
    
    print(f"\n👥 Social Interaction Analysis:")
    social_metrics = report['social_interaction_metrics']
    print(f"  Total Interactions: {social_metrics['total_interactions']}")
    print(f"  Average Success Rate: {social_metrics['average_success_rate']:.3f}")
    print(f"  Interaction Types Practiced: {social_metrics['interaction_types_practiced']}")
    
    print(f"\n🌍 Learning Environment Diversity:")
    diversity = report['learning_diversity']
    print(f"  Physical Contexts Explored: {diversity['physical_contexts_explored']}")
    print(f"  Context Diversity Score: {diversity['context_diversity_score']:.3f}")
    print(f"  Unique Peers Interacted: {diversity['unique_peers_interacted']}")
    
    print(f"\n🎓 Embodied Social Readiness Assessment:")
    readiness = report['embodied_social_readiness']
    print(f"  Readiness Level: {readiness['readiness_level']}")
    print(f"  Overall Score: {readiness['readiness_score']:.3f}")
    
    component_scores = readiness['component_scores']
    print(f"  Component Breakdown:")
    print(f"    Sensory Integration: {component_scores['sensory_integration']:.3f}")
    print(f"    Social-Physical Coherence: {component_scores['social_physical_coherence']:.3f}")
    print(f"    Skill Mastery: {component_scores['skill_mastery']:.3f}")
    print(f"    Learning Engagement: {component_scores['learning_engagement']:.3f}")
    
    print(f"\n💡 Learning Recommendations:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    # Save the data
    integration.save_embodied_social_data()
    
    print(f"\n✅ Embodied Social Learning Integration Demo Complete!")
    print(f"Marcus has successfully completed comprehensive multi-sensory social learning")
    print(f"with {metrics['sensory_integration_score']:.1%} sensory integration success")
    print(f"and {readiness['readiness_score']:.1%} overall embodied social readiness!")
    
    return integration


if __name__ == "__main__":
    demo_embodied_social_integration()
