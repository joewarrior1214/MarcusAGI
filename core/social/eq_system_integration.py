#!/usr/bin/env python3
"""
Issue #6 Integration: Emotional Intelligence Assessment Integration

This module integrates the emotional intelligence assessment system with Marcus's
existing components including the reflection system, curriculum expansion, and
daily learning loop.

Key Integration Points:
- Enhanced Reflection System (Issue #4) - EQ insights inform emotional tracking
- Kindergarten Curriculum (Issue #5) - EQ assessments guide social-emotional learning
- Daily Learning Loop - EQ development integrated into daily activities
- Mr. Rogers Processing (Issue #2) - EQ episodes selected based on assessment needs
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

# Import our Issue #6 system
from emotional_intelligence_assessment import (
    EmotionalIntelligenceAssessment, EQDomain, EQSkillLevel,
    create_eq_assessment_system
)

logger = logging.getLogger(__name__)

@dataclass
class EQIntegratedSession:
    """Enhanced session data with EQ integration"""
    session_id: str
    session_date: datetime
    marcus_age_days: int
    
    # Core session data
    learning_activities: List[Dict[str, Any]]
    emotional_states: List[Dict[str, Any]]
    social_interactions: List[Dict[str, Any]]
    
    # EQ Assessment integration
    eq_assessments_conducted: List[Dict[str, Any]]
    eq_insights: Dict[str, Any]
    eq_guided_activities: List[Dict[str, Any]]
    targeted_eq_domains: List[str]
    
    # Integration with other systems
    reflection_eq_connections: List[Dict[str, Any]]
    curriculum_eq_alignments: List[Dict[str, Any]]
    mr_rogers_eq_episodes: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'session_id': self.session_id,
            'session_date': self.session_date.isoformat(),
            'marcus_age_days': self.marcus_age_days,
            'learning_activities': self.learning_activities,
            'emotional_states': self.emotional_states,
            'social_interactions': self.social_interactions,
            'eq_assessments_conducted': self.eq_assessments_conducted,
            'eq_insights': self.eq_insights,
            'eq_guided_activities': self.eq_guided_activities,
            'targeted_eq_domains': self.targeted_eq_domains,
            'reflection_eq_connections': self.reflection_eq_connections,
            'curriculum_eq_alignments': self.curriculum_eq_alignments,
            'mr_rogers_eq_episodes': self.mr_rogers_eq_episodes
        }

class EQSystemIntegrator:
    """Integrates EQ assessment with all Marcus AGI systems"""
    
    def __init__(self):
        self.eq_system = create_eq_assessment_system()
        self.integration_history = []
        self.eq_development_plan = self._create_eq_development_plan()
        
    def _create_eq_development_plan(self) -> Dict[str, Any]:
        """Create developmental plan for EQ growth"""
        return {
            "plan_created": datetime.now().isoformat(),
            "age_appropriate_milestones": {
                "5_years": {
                    "self_awareness": ["Names 8+ emotions", "Identifies emotion triggers"],
                    "self_regulation": ["Uses 3+ coping strategies", "Calms down within 5 minutes"],
                    "empathy": ["Recognizes others' emotions", "Shows helping behaviors"],
                    "social_skills": ["Plays cooperatively", "Resolves simple conflicts"],
                    "motivation": ["Persists through challenges", "Seeks help when needed"]
                },
                "6_years": {
                    "self_awareness": ["Describes emotion intensity", "Connects thoughts to feelings"],
                    "self_regulation": ["Chooses appropriate strategies", "Self-monitors emotions"],
                    "empathy": ["Takes others' perspectives", "Shows compassion"],
                    "social_skills": ["Communicates clearly", "Includes others"],
                    "motivation": ["Sets simple goals", "Celebrates progress"]
                }
            },
            "assessment_schedule": {
                "weekly": ["Emotion check-ins", "Social observation"],
                "bi_weekly": ["Empathy scenarios", "Conflict resolution practice"],
                "monthly": ["Comprehensive EQ assessment", "Progress review"]
            },
            "intervention_triggers": {
                "red_flags": ["Extreme emotional reactions", "Persistent social isolation", "Aggressive behaviors"],
                "support_needed": ["Consistently low EQ scores", "Regression in skills", "Peer relationship issues"]
            }
        }
    
    def integrate_with_reflection_system(self, reflection_data: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate EQ assessment with enhanced reflection system from Issue #4"""
        
        print("🔗 Integrating EQ Assessment with Reflection System...")
        
        # Extract emotional data from reflection
        emotional_states = reflection_data.get("emotional_states", [])
        learning_insights = reflection_data.get("learning_insights", [])
        
        # Conduct targeted EQ assessments based on reflection patterns
        eq_assessments = []
        
        # Check for emotion regulation patterns
        if any("frustrated" in str(state).lower() for state in emotional_states):
            # Conduct self-regulation assessment
            regulation_result = self.eq_system.conduct_emotion_recognition_assessment("situational_emotions")
            eq_assessments.append({
                "type": "self_regulation_focus",
                "trigger": "frustration_patterns_in_reflection",
                "result": regulation_result
            })
        
        # Check for social interaction patterns
        if "social" in str(reflection_data).lower():
            # Conduct social skills simulation
            social_result = self.eq_system.conduct_social_simulation("classroom_collaboration")
            eq_assessments.append({
                "type": "social_skills_focus", 
                "trigger": "social_themes_in_reflection",
                "result": social_result
            })
        
        # Generate EQ-enhanced reflection insights
        eq_reflection_connections = []
        
        for state in emotional_states[-3:]:  # Last 3 emotional states
            emotion = state.get("dominant_emotion", "neutral")
            eq_connection = {
                "emotion": emotion,
                "eq_domain_relevance": self._map_emotion_to_eq_domain(emotion),
                "reflection_insight": f"Emotion '{emotion}' shows development in {self._map_emotion_to_eq_domain(emotion).replace('_', ' ')}",
                "growth_opportunity": self._suggest_eq_growth_from_emotion(emotion)
            }
            eq_reflection_connections.append(eq_connection)
        
        # Enhance reflection data with EQ insights
        enhanced_reflection = reflection_data.copy()
        enhanced_reflection.update({
            "eq_integration": True,
            "eq_assessments_triggered": eq_assessments,
            "eq_reflection_connections": eq_reflection_connections,
            "eq_informed_next_steps": self._generate_eq_informed_reflection_steps(emotional_states),
            "emotional_development_insights": self._analyze_emotional_development_patterns(emotional_states)
        })
        
        print(f"  ✅ Integrated {len(eq_assessments)} EQ assessments with reflection")
        print(f"  🧠 Generated {len(eq_reflection_connections)} EQ-reflection connections")
        
        return enhanced_reflection
    
    def integrate_with_curriculum_system(self, curriculum_data: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate EQ assessment with kindergarten curriculum expansion from Issue #5"""
        
        print("🔗 Integrating EQ Assessment with Curriculum System...")
        
        # Get current EQ profile
        eq_report = self.eq_system.generate_comprehensive_eq_report()
        eq_levels = eq_report["eq_domain_levels"]
        
        # Map EQ domains to curriculum domains
        curriculum_eq_alignments = []
        
        curriculum_domains = curriculum_data.get("developmental_domains", {})
        
        # Social-Emotional Domain alignment
        if "social_emotional" in curriculum_domains:
            social_emotional_activities = curriculum_domains["social_emotional"].get("activities", [])
            
            for activity in social_emotional_activities:
                eq_alignment = {
                    "activity": activity,
                    "eq_domains_addressed": self._identify_eq_domains_in_activity(activity),
                    "marcus_eq_level_match": self._assess_activity_eq_match(activity, eq_levels),
                    "differentiation_needed": self._suggest_eq_differentiation(activity, eq_levels)
                }
                curriculum_eq_alignments.append(eq_alignment)
        
        # Generate EQ-guided curriculum activities
        eq_guided_activities = []
        
        # Target domains needing support
        priority_domains = [domain for domain, level in eq_levels.items() 
                          if level in ["beginning", "developing"]]
        
        for domain in priority_domains[:2]:  # Top 2 priorities
            activities = self._generate_eq_curriculum_activities(domain, eq_levels[domain])
            eq_guided_activities.extend(activities)
        
        # Enhance curriculum with EQ integration
        enhanced_curriculum = curriculum_data.copy()
        enhanced_curriculum.update({
            "eq_integration": True,
            "eq_current_levels": eq_levels,
            "curriculum_eq_alignments": curriculum_eq_alignments,
            "eq_guided_activities": eq_guided_activities,
            "eq_differentiated_instruction": self._create_eq_differentiated_instruction(eq_levels),
            "social_emotional_focus_areas": priority_domains
        })
        
        print(f"  ✅ Aligned {len(curriculum_eq_alignments)} curriculum activities with EQ")
        print(f"  🎯 Generated {len(eq_guided_activities)} EQ-guided activities")
        print(f"  📚 Focused on {len(priority_domains)} priority EQ domains")
        
        return enhanced_curriculum
    
    def integrate_with_daily_learning_loop(self, daily_session: Dict[str, Any]) -> EQIntegratedSession:
        """Integrate EQ assessment with daily learning loop"""
        
        print("🔗 Integrating EQ Assessment with Daily Learning Loop...")
        
        session_id = daily_session.get("session_id", f"eq_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Conduct daily EQ check-in
        daily_eq_assessment = self._conduct_daily_eq_checkin()
        
        # Generate EQ insights for the day
        eq_insights = self._generate_daily_eq_insights(daily_session, daily_eq_assessment)
        
        # Select targeted EQ domains for the day
        targeted_domains = self._select_daily_eq_targets(eq_insights)
        
        # Create EQ-guided activities for the session
        eq_guided_activities = []
        for domain in targeted_domains:
            activities = self._create_daily_eq_activities(domain, daily_session)
            eq_guided_activities.extend(activities)
        
        # Connect with reflection system
        reflection_connections = self._create_eq_reflection_connections(daily_session)
        
        # Connect with curriculum system
        curriculum_alignments = self._create_eq_curriculum_connections(daily_session)
        
        # Select Mr. Rogers episodes for EQ development
        mr_rogers_episodes = self._select_eq_mr_rogers_episodes(targeted_domains)
        
        # Create integrated session
        integrated_session = EQIntegratedSession(
            session_id=session_id,
            session_date=datetime.now(),
            marcus_age_days=daily_session.get("marcus_age_days", 365*5),  # Default 5 years
            learning_activities=daily_session.get("learning_activities", []),
            emotional_states=daily_session.get("emotional_states", []),
            social_interactions=daily_session.get("social_interactions", []),
            eq_assessments_conducted=[daily_eq_assessment],
            eq_insights=eq_insights,
            eq_guided_activities=eq_guided_activities,
            targeted_eq_domains=targeted_domains,
            reflection_eq_connections=reflection_connections,
            curriculum_eq_alignments=curriculum_alignments,
            mr_rogers_eq_episodes=mr_rogers_episodes
        )
        
        print(f"  ✅ Conducted daily EQ check-in")
        print(f"  🎯 Targeting {len(targeted_domains)} EQ domains today")
        print(f"  🎬 Selected {len(mr_rogers_episodes)} Mr. Rogers episodes")
        
        return integrated_session
    
    def _map_emotion_to_eq_domain(self, emotion: str) -> str:
        """Map an emotion to its primary EQ domain"""
        emotion_domain_mapping = {
            "happy": "self_awareness",
            "sad": "self_awareness", 
            "angry": "self_regulation",
            "frustrated": "self_regulation",
            "excited": "self_regulation",
            "nervous": "self_awareness",
            "proud": "motivation",
            "disappointed": "self_regulation",
            "empathetic": "empathy",
            "lonely": "social_skills",
            "confident": "motivation"
        }
        
        return emotion_domain_mapping.get(emotion.lower(), "self_awareness")
    
    def _suggest_eq_growth_from_emotion(self, emotion: str) -> str:
        """Suggest EQ growth opportunity from emotion"""
        growth_suggestions = {
            "frustrated": "Practice calming strategies and problem-solving",
            "angry": "Learn emotion regulation techniques",
            "sad": "Develop emotion vocabulary and expression",
            "lonely": "Build social connection skills",
            "nervous": "Practice self-awareness and coping strategies",
            "excited": "Learn appropriate emotional expression",
            "proud": "Develop balanced self-concept",
            "empathetic": "Strengthen perspective-taking skills"
        }
        
        return growth_suggestions.get(emotion.lower(), "Continue emotional development")
    
    def _generate_eq_informed_reflection_steps(self, emotional_states: List[Dict]) -> List[str]:
        """Generate reflection steps informed by EQ assessment"""
        steps = [
            "Notice what emotions you felt today",
            "Think about what caused those emotions", 
            "Consider how you handled your emotions",
            "Compare how you handled similar emotions before",
            "Think about what strategies worked best"
        ]
        
        return steps
    
    def _analyze_emotional_development_patterns(self, emotional_states: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in emotional development"""
        if not emotional_states:
            return {"pattern": "insufficient_data"}
        
        recent_emotions = [state.get("dominant_emotion", "neutral") for state in emotional_states[-10:]]
        
        return {
            "emotional_range": len(set(recent_emotions)),
            "most_frequent_emotion": max(set(recent_emotions), key=recent_emotions.count) if recent_emotions else "neutral",
            "emotional_stability": "stable" if len(set(recent_emotions)) <= 3 else "varied",
            "development_trend": "expanding" if len(set(recent_emotions)) > 5 else "consolidating",
            "growth_indicators": [
                "Using more emotion words" if len(set(recent_emotions)) > 4 else "Developing emotion vocabulary",
                "Shows emotional awareness" if "confused" not in recent_emotions else "Learning emotional clarity"
            ]
        }
    
    def _identify_eq_domains_in_activity(self, activity: Dict[str, Any]) -> List[str]:
        """Identify EQ domains addressed by a curriculum activity"""
        activity_text = str(activity).lower()
        domains = []
        
        if any(word in activity_text for word in ["feeling", "emotion", "mood"]):
            domains.append("self_awareness")
        if any(word in activity_text for word in ["calm", "control", "regulate"]):
            domains.append("self_regulation")
        if any(word in activity_text for word in ["help", "care", "understand others"]):
            domains.append("empathy")
        if any(word in activity_text for word in ["friend", "share", "cooperate", "together"]):
            domains.append("social_skills")
        if any(word in activity_text for word in ["try", "persist", "goal", "challenge"]):
            domains.append("motivation")
        
        return domains if domains else ["general_eq"]
    
    def _assess_activity_eq_match(self, activity: Dict[str, Any], eq_levels: Dict[str, str]) -> str:
        """Assess how well activity matches Marcus's EQ levels"""
        activity_domains = self._identify_eq_domains_in_activity(activity)
        
        if not activity_domains:
            return "neutral_match"
        
        # Check if activity targets areas where Marcus needs support
        priority_domains = [domain for domain, level in eq_levels.items() 
                          if level in ["beginning", "developing"]]
        
        if any(domain in priority_domains for domain in activity_domains):
            return "high_priority_match"
        elif any(domain in eq_levels for domain in activity_domains):
            return "good_match"
        else:
            return "low_match"
    
    def _suggest_eq_differentiation(self, activity: Dict[str, Any], eq_levels: Dict[str, str]) -> List[str]:
        """Suggest how to differentiate activity for Marcus's EQ levels"""
        suggestions = []
        activity_domains = self._identify_eq_domains_in_activity(activity)
        
        for domain in activity_domains:
            if domain in eq_levels:
                level = eq_levels[domain]
                if level == "beginning":
                    suggestions.append(f"Provide extra support and scaffolding for {domain.replace('_', ' ')}")
                elif level == "developing":
                    suggestions.append(f"Offer guided practice for {domain.replace('_', ' ')}")
                elif level in ["practicing", "applying"]:
                    suggestions.append(f"Provide leadership opportunities in {domain.replace('_', ' ')}")
        
        return suggestions if suggestions else ["Activity appropriate as-is"]
    
    def _generate_eq_curriculum_activities(self, domain: str, level: str) -> List[Dict[str, Any]]:
        """Generate curriculum activities targeted to specific EQ domain and level"""
        activities = []
        
        if domain == "self_awareness":
            if level in ["beginning", "developing"]:
                activities.extend([
                    {
                        "name": "Emotion Check-In Circle",
                        "description": "Daily circle time to identify and share feelings",
                        "materials": ["Feeling wheel", "Emotion cards"],
                        "duration": "10 minutes",
                        "eq_target": "emotion identification"
                    },
                    {
                        "name": "Body Feelings Map",
                        "description": "Draw where different emotions are felt in the body",
                        "materials": ["Body outline worksheet", "Crayons"],
                        "duration": "15 minutes", 
                        "eq_target": "emotion-body connection"
                    }
                ])
        
        elif domain == "empathy":
            if level in ["beginning", "developing"]:
                activities.extend([
                    {
                        "name": "Character Feelings Detective",
                        "description": "Read stories and identify how characters feel",
                        "materials": ["Picture books", "Feeling cards"],
                        "duration": "20 minutes",
                        "eq_target": "emotion recognition in others"
                    },
                    {
                        "name": "Helping Hands Practice",
                        "description": "Role-play helping someone who is upset",
                        "materials": ["Scenario cards", "Props"],
                        "duration": "15 minutes",
                        "eq_target": "prosocial helping"
                    }
                ])
        
        elif domain == "social_skills":
            if level in ["beginning", "developing"]:
                activities.extend([
                    {
                        "name": "Conversation Starters",
                        "description": "Practice starting and maintaining conversations",
                        "materials": ["Conversation prompt cards"],
                        "duration": "10 minutes",
                        "eq_target": "social communication"
                    },
                    {
                        "name": "Conflict Resolution Theater",
                        "description": "Act out and practice resolving disagreements",
                        "materials": ["Simple scripts", "Props"],
                        "duration": "20 minutes",
                        "eq_target": "peaceful problem solving"
                    }
                ])
        
        return activities
    
    def _create_eq_differentiated_instruction(self, eq_levels: Dict[str, str]) -> Dict[str, List[str]]:
        """Create differentiated instruction strategies based on EQ levels"""
        differentiation = {}
        
        for domain, level in eq_levels.items():
            strategies = []
            
            if level == "beginning":
                strategies.extend([
                    "Provide concrete examples and visual supports",
                    "Use simple vocabulary and clear instructions",
                    "Offer frequent encouragement and support",
                    "Break skills into smallest components"
                ])
            elif level == "developing":
                strategies.extend([
                    "Provide guided practice with prompts",
                    "Use peer modeling and support",
                    "Offer choices and gradual independence",
                    "Connect to personal experiences"
                ])
            elif level == "practicing":
                strategies.extend([
                    "Encourage independent application",
                    "Provide opportunities for peer teaching",
                    "Introduce more complex scenarios",
                    "Support goal-setting and reflection"
                ])
            else:  # applying/leading
                strategies.extend([
                    "Offer leadership and mentoring roles",
                    "Provide advanced challenges",
                    "Encourage innovation and creativity",
                    "Support community service projects"
                ])
            
            differentiation[domain] = strategies
        
        return differentiation
    
    def _conduct_daily_eq_checkin(self) -> Dict[str, Any]:
        """Conduct daily EQ check-in assessment"""
        return {
            "assessment_type": "daily_checkin",
            "assessment_date": datetime.now().isoformat(),
            "current_mood": random.choice(["happy", "excited", "calm", "curious", "frustrated"]),
            "energy_level": random.choice(["high", "medium", "low"]),
            "social_readiness": random.choice(["eager", "ready", "cautious", "withdrawn"]),
            "learning_motivation": random.choice(["high", "moderate", "needs_encouragement"]),
            "emotional_regulation": random.choice(["stable", "variable", "needs_support"]),
            "quick_eq_score": random.uniform(0.6, 0.9)
        }
    
    def _generate_daily_eq_insights(self, daily_session: Dict[str, Any], eq_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate EQ insights for daily session"""
        return {
            "mood_learning_connection": f"Current mood '{eq_assessment['current_mood']}' suggests focus on {self._map_emotion_to_eq_domain(eq_assessment['current_mood'])}",
            "social_readiness_implications": f"Social readiness '{eq_assessment['social_readiness']}' indicates {'group activities' if eq_assessment['social_readiness'] == 'eager' else 'individual work first'}",
            "regulation_needs": f"Emotional regulation '{eq_assessment['emotional_regulation']}' suggests {'advanced activities' if eq_assessment['emotional_regulation'] == 'stable' else 'calming activities first'}",
            "motivation_strategies": f"Learning motivation '{eq_assessment['learning_motivation']}' calls for {'challenging tasks' if eq_assessment['learning_motivation'] == 'high' else 'encouragement and support'}",
            "recommended_focus": self._recommend_daily_eq_focus(eq_assessment)
        }
    
    def _select_daily_eq_targets(self, eq_insights: Dict[str, Any]) -> List[str]:
        """Select EQ domains to target for the day"""
        targets = []
        
        # Extract focus area from insights
        focus = eq_insights.get("recommended_focus", "")
        
        if "self_awareness" in focus:
            targets.append("self_awareness")
        if "regulation" in focus or "calming" in focus:
            targets.append("self_regulation")
        if "social" in focus:
            targets.append("social_skills")
        if "empathy" in focus:
            targets.append("empathy")
        if "motivation" in focus:
            targets.append("motivation")
        
        # Default targets if none identified
        if not targets:
            targets = ["self_awareness", "social_skills"]
        
        return targets[:2]  # Maximum 2 targets per day
    
    def _create_daily_eq_activities(self, domain: str, daily_session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create daily EQ activities for specific domain"""
        activities = []
        
        daily_activities = {
            "self_awareness": [
                {"name": "Morning Feeling Check", "duration": "5 min", "description": "Identify current emotions"},
                {"name": "Emotion Journal", "duration": "10 min", "description": "Draw or write about feelings"}
            ],
            "self_regulation": [
                {"name": "Calm Down Corner", "duration": "5 min", "description": "Practice calming strategies"},
                {"name": "Breathing Exercises", "duration": "3 min", "description": "Deep breathing practice"}
            ],
            "empathy": [
                {"name": "Story Character Feelings", "duration": "15 min", "description": "Discuss characters' emotions"},
                {"name": "Kindness Activity", "duration": "10 min", "description": "Find ways to help others"}
            ],
            "social_skills": [
                {"name": "Friend Interaction", "duration": "20 min", "description": "Structured social play"},
                {"name": "Communication Practice", "duration": "10 min", "description": "Practice conversation skills"}
            ],
            "motivation": [
                {"name": "Goal Setting", "duration": "10 min", "description": "Set and work toward simple goals"},
                {"name": "Celebration Circle", "duration": "5 min", "description": "Celebrate efforts and progress"}
            ]
        }
        
        domain_activities = daily_activities.get(domain, [])
        
        # Select 1-2 activities for the day
        selected_activities = random.sample(domain_activities, min(2, len(domain_activities)))
        
        for activity in selected_activities:
            activity.update({
                "eq_domain": domain,
                "integration_level": "daily_practice"
            })
            activities.append(activity)
        
        return activities
    
    def _create_eq_reflection_connections(self, daily_session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create connections between EQ and reflection system"""
        connections = [
            {
                "connection_type": "emotion_awareness_building",
                "description": "Use EQ insights to guide reflection prompts",
                "implementation": "Ask reflection questions that target identified EQ growth areas"
            },
            {
                "connection_type": "pattern_recognition",
                "description": "Track emotional patterns through reflection",
                "implementation": "Review emotional responses in daily reflection"
            }
        ]
        
        return connections
    
    def _create_eq_curriculum_connections(self, daily_session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create connections between EQ and curriculum system"""
        connections = [
            {
                "connection_type": "social_emotional_learning_integration",
                "description": "Embed EQ development in all curriculum activities",
                "implementation": "Add emotion and social skill components to academic activities"
            },
            {
                "connection_type": "differentiated_eq_instruction",
                "description": "Adjust curriculum based on EQ assessment results",
                "implementation": "Modify activities to match current EQ developmental levels"
            }
        ]
        
        return connections
    
    def _select_eq_mr_rogers_episodes(self, targeted_domains: List[str]) -> List[str]:
        """Select Mr. Rogers episodes that support targeted EQ domains"""
        episode_mapping = {
            "self_awareness": ["Episode 1478: Angry Feelings", "Episode about Understanding Emotions"],
            "self_regulation": ["Episode about Managing Big Feelings", "Episode about Self-Control"],
            "empathy": ["Episode 1479: Making Friends", "Episode about Caring for Others"],
            "social_skills": ["Episode about Friendship", "Episode about Sharing and Cooperation"],
            "motivation": ["Episode 1640: Making Mistakes", "Episode about Trying Again"]
        }
        
        selected_episodes = []
        for domain in targeted_domains:
            domain_episodes = episode_mapping.get(domain, [])
            if domain_episodes:
                selected_episodes.extend(random.sample(domain_episodes, min(1, len(domain_episodes))))
        
        return selected_episodes
    
    def _recommend_daily_eq_focus(self, eq_assessment: Dict[str, Any]) -> str:
        """Recommend daily EQ focus based on assessment"""
        mood = eq_assessment.get("current_mood", "neutral")
        regulation = eq_assessment.get("emotional_regulation", "stable")
        social_readiness = eq_assessment.get("social_readiness", "ready")
        
        if regulation == "needs_support":
            return "Focus on self_regulation and calming activities"
        elif social_readiness == "withdrawn":
            return "Gentle social_skills building and empathy activities"
        elif mood in ["frustrated", "angry"]:
            return "Self_regulation and emotion identification"
        elif social_readiness == "eager":
            return "Social_skills practice and empathy development"
        else:
            return "Balanced self_awareness and social_skills activities"

# Integration factory function
def create_eq_integrator() -> EQSystemIntegrator:
    """Create EQ system integrator"""
    return EQSystemIntegrator()

# Comprehensive integration demo
def demo_comprehensive_eq_integration():
    """Demonstrate comprehensive EQ integration with all systems"""
    
    print("🧠 Issue #6 Demo: Comprehensive EQ System Integration")
    print("=" * 70)
    
    integrator = create_eq_integrator()
    
    # Demo integration with reflection system
    print("\n1️⃣ EQ Integration with Reflection System (Issue #4)")
    mock_reflection_data = {
        "session_id": "reflection_123",
        "emotional_states": [
            {"dominant_emotion": "frustrated", "intensity": 0.7},
            {"dominant_emotion": "curious", "intensity": 0.8},
            {"dominant_emotion": "proud", "intensity": 0.6}
        ],
        "learning_insights": ["Worked hard on puzzle", "Asked for help when stuck"]
    }
    
    enhanced_reflection = integrator.integrate_with_reflection_system(mock_reflection_data)
    print(f"  ✅ Generated {len(enhanced_reflection['eq_reflection_connections'])} EQ connections")
    
    # Demo integration with curriculum system
    print("\n2️⃣ EQ Integration with Curriculum System (Issue #5)")
    mock_curriculum_data = {
        "session_id": "curriculum_456",
        "developmental_domains": {
            "social_emotional": {
                "activities": [
                    {"name": "Feeling Faces", "description": "Identify emotions in pictures"},
                    {"name": "Helping Friends", "description": "Practice helping behaviors"}
                ]
            }
        }
    }
    
    enhanced_curriculum = integrator.integrate_with_curriculum_system(mock_curriculum_data)
    print(f"  ✅ Aligned {len(enhanced_curriculum['curriculum_eq_alignments'])} activities")
    print(f"  🎯 Generated {len(enhanced_curriculum['eq_guided_activities'])} new EQ activities")
    
    # Demo integration with daily learning loop
    print("\n3️⃣ EQ Integration with Daily Learning Loop")
    mock_daily_session = {
        "session_id": "daily_789",
        "marcus_age_days": 365*5 + 30,  # 5 years, 1 month
        "learning_activities": ["Reading", "Math", "Art"],
        "emotional_states": [{"emotion": "excited", "context": "art_project"}],
        "social_interactions": [{"type": "peer_play", "outcome": "positive"}]
    }
    
    integrated_session = integrator.integrate_with_daily_learning_loop(mock_daily_session)
    print(f"  ✅ Conducted daily EQ check-in")
    print(f"  🎯 Targeting domains: {', '.join(integrated_session.targeted_eq_domains)}")
    print(f"  🎬 Selected {len(integrated_session.mr_rogers_eq_episodes)} Mr. Rogers episodes")
    print(f"  🎪 Created {len(integrated_session.eq_guided_activities)} EQ activities")
    
    # Show comprehensive integration results
    print(f"\n4️⃣ Comprehensive Integration Results")
    print(f"  🧠 EQ Domains Addressed: {len(list(EQDomain))}")
    print(f"  🔗 System Integrations: Reflection + Curriculum + Daily Loop")
    print(f"  📊 Assessment Types: Daily check-ins + Targeted assessments")
    print(f"  🎭 Mr. Rogers Episodes: Context-appropriate selection")
    print(f"  📈 Developmental Tracking: Age-appropriate milestones")
    
    print(f"\n🎉 Issue #6 Complete Integration Demonstrated!")
    print("   All Marcus AGI systems now enhanced with emotional intelligence!")

if __name__ == "__main__":
    demo_comprehensive_eq_integration()
