#!/usr/bin/env python3
"""
Marcus AGI Social Learning Integration System

This module integrates the Peer Interaction Simulation System (Issue #8) with:
1. Daily Learning Loop (Issue #3) - Regular social practice sessions
2. EQ System (Issue #6) - Emotional intelligence coaching
3. Grade Progression System (Issue #7) - Social readiness assessment
4. Kindergarten deployment environment

The integration ensures Marcus develops social skills alongside academic abilities.
"""

import json
import logging
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, date, timedelta
from enum import Enum

# Import existing systems
from .peer_interaction_simulation import (
    create_peer_interaction_system, PeerInteractionSimulator,
    InteractionContext, ConversationTopic, SocialSkillArea
)

try:
    from ..learning.daily_learning_loop import run_learning_session, calculate_mastery_levels
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
    from ..learning.grade_progression_system import (
        GradeProgressionSystem, GradeLevel, AcademicSubject
    )
    GRADE_SYSTEM_AVAILABLE = True
except ImportError:
    GRADE_SYSTEM_AVAILABLE = False
    logging.warning("Grade Progression System not available")

logger = logging.getLogger(__name__)

class SocialLearningPhase(Enum):
    """Phases of social learning integration"""
    MORNING_WARMUP = "morning_warmup"           # Start day with social connection
    ACADEMIC_COLLABORATION = "academic_collaboration"  # Peer learning during lessons
    SOCIAL_PRACTICE = "social_practice"         # Dedicated social skills time
    CONFLICT_RESOLUTION = "conflict_resolution"  # Address social challenges
    REFLECTION_SHARING = "reflection_sharing"    # Process social experiences
    EVENING_FRIENDSHIP = "evening_friendship"    # End day with positive interaction

class SocialReadinessLevel(Enum):
    """Social readiness for academic advancement"""
    EMERGING = "emerging"          # Basic social awareness
    DEVELOPING = "developing"      # Inconsistent social skills
    PROFICIENT = "proficient"     # Grade-appropriate social skills
    ADVANCED = "advanced"         # Leadership and mentoring abilities

@dataclass
class IntegratedLearningSession:
    """Combined academic and social learning session"""
    session_id: str
    date: datetime
    academic_focus: List[str]
    social_focus: List[SocialSkillArea]
    peer_interactions: List[Dict[str, Any]]
    collaborative_activities: List[Dict[str, Any]]
    eq_coaching_moments: List[Dict[str, Any]]
    social_readiness_assessment: Dict[str, Any]
    integration_success_metrics: Dict[str, float]
    recommendations: List[str]

class MarcusSocialLearningIntegration:
    """Main integration class for social learning across all systems"""
    
    def __init__(self, db_path: str = "marcus_integrated_learning.db"):
        """Initialize the integrated social learning system"""
        self.db_path = db_path
        
        # Initialize peer interaction system
        self.peer_system = create_peer_interaction_system()
        logger.info("Peer Interaction System initialized")
        
        # Initialize other systems if available
        self.eq_system = EmotionalIntelligenceAssessment() if EQ_SYSTEM_AVAILABLE else None
        self.grade_system = GradeProgressionSystem() if GRADE_SYSTEM_AVAILABLE else None
        
        # Social learning configuration
        self.social_learning_config = {
            "daily_social_minutes": 30,        # Minimum daily social practice
            "peer_interactions_per_day": 3,    # Target peer interactions
            "collaboration_frequency": 0.7,    # Fraction of lessons with collaboration
            "conflict_resolution_threshold": 2, # Max conflicts before intervention
            "social_readiness_threshold": 0.75, # Threshold for grade advancement
            "eq_coaching_frequency": 0.5       # Fraction of sessions with EQ coaching
        }
        
        logger.info("Marcus Social Learning Integration System initialized")
    
    def run_integrated_daily_session(self, session_date: Optional[date] = None) -> IntegratedLearningSession:
        """Run a complete integrated learning session with social and academic components"""
        if session_date is None:
            session_date = date.today()
        
        session_id = f"integrated_session_{session_date.strftime('%Y%m%d')}_{datetime.now().strftime('%H%M%S')}"
        
        logger.info(f"Starting integrated learning session: {session_id}")
        
        # 1. Morning Social Warmup
        morning_interaction = self._conduct_morning_warmup()
        
        # 2. Academic Learning with Social Integration
        academic_session = self._run_academic_session_with_peers(session_date)
        
        # 3. Dedicated Social Practice Time
        social_practice = self._conduct_social_practice_session()
        
        # 4. EQ Coaching Integration
        eq_coaching = self._integrate_eq_coaching(morning_interaction, social_practice)
        
        # 5. Social Readiness Assessment
        social_readiness = self._assess_social_readiness()
        
        # 6. Generate Integration Metrics
        integration_metrics = self._calculate_integration_metrics(
            morning_interaction, academic_session, social_practice, eq_coaching
        )
        
        # 7. Generate Recommendations
        recommendations = self._generate_daily_recommendations(
            integration_metrics, social_readiness
        )
        
        # Create integrated session record
        integrated_session = IntegratedLearningSession(
            session_id=session_id,
            date=datetime.combine(session_date, datetime.now().time()),
            academic_focus=academic_session.get("subjects_covered", []),
            social_focus=self._extract_social_skills_practiced(
                morning_interaction, social_practice
            ),
            peer_interactions=[morning_interaction, social_practice],
            collaborative_activities=academic_session.get("collaborative_activities", []),
            eq_coaching_moments=eq_coaching,
            social_readiness_assessment=social_readiness,
            integration_success_metrics=integration_metrics,
            recommendations=recommendations
        )
        
        # Store session data
        self._store_integrated_session(integrated_session)
        
        logger.info(f"Integrated learning session completed: {session_id}")
        return integrated_session
    
    def _conduct_morning_warmup(self) -> Dict[str, Any]:
        """Start the day with a social warmup interaction"""
        logger.info("Conducting morning social warmup")
        
        # Select a friendly peer for morning interaction
        available_peers = list(self.peer_system.peers.keys())
        morning_peer = available_peers[0]  # Emma - Confident Leader is good for warmups
        
        # Conduct friendship-building interaction
        session = self.peer_system.simulate_peer_interaction(
            peers_to_include=[morning_peer],
            context=InteractionContext.CLASSROOM,
            topic=ConversationTopic.FRIENDSHIP_BUILDING,
            duration_minutes=5
        )
        
        return {
            "type": "morning_warmup",
            "peer": morning_peer,
            "session": asdict(session),
            "success_rating": session.overall_success_rating,
            "skills_practiced": [skill.value for skill in session.social_skills_practiced]
        }
    
    def _run_academic_session_with_peers(self, session_date: date) -> Dict[str, Any]:
        """Run academic learning session with integrated peer collaboration"""
        logger.info("Running academic session with peer collaboration")
        
        academic_results = {"subjects_covered": [], "collaborative_activities": []}
        
        # Run base academic session if available
        if DAILY_LOOP_AVAILABLE:
            try:
                from ..learning.daily_learning_loop import load_all_sessions
                session_history = load_all_sessions()
                if not session_history:
                    session_history = [{"date": session_date.strftime("%Y-%m-%d"), "mastery_levels": {}}]
                
                academic_session = run_learning_session(session_history, session_date.strftime("%Y-%m-%d"))
                academic_results["subjects_covered"] = academic_session.get("concepts_learned", [])
            except Exception as e:
                logger.warning(f"Could not run academic session: {e}")
        
        # Add collaborative learning activities
        if random.random() < self.social_learning_config["collaboration_frequency"]:
            collaborative_activity = self._select_collaborative_activity(academic_results["subjects_covered"])
            activity_result = self.peer_system.conduct_collaborative_activity(
                activity_id=collaborative_activity["activity_id"],
                participants=collaborative_activity["participants"]
            )
            academic_results["collaborative_activities"].append(activity_result)
        
        return academic_results
    
    def _select_collaborative_activity(self, academic_subjects: List[str]) -> Dict[str, Any]:
        """Select appropriate collaborative activity based on current academic focus"""
        available_activities = list(self.peer_system.collaborative_activities.keys())
        
        # Default to first activity if no specific matching
        selected_activity_id = available_activities[0]
        
        # Try to match activity to academic content
        for subject in academic_subjects:
            if "math" in subject.lower() or "counting" in subject.lower():
                # Look for math activity
                math_activities = [aid for aid, activity in self.peer_system.collaborative_activities.items() 
                                 if "math" in activity.subject_area.lower()]
                if math_activities:
                    selected_activity_id = math_activities[0]
                    break
            elif "reading" in subject.lower() or "letter" in subject.lower():
                # Look for language arts activity
                lang_activities = [aid for aid, activity in self.peer_system.collaborative_activities.items() 
                                 if "language" in activity.subject_area.lower()]
                if lang_activities:
                    selected_activity_id = lang_activities[0]
                    break
        
        # Select participants
        available_peers = list(self.peer_system.peers.keys())
        activity = self.peer_system.collaborative_activities[selected_activity_id]
        num_peers = min(activity.max_participants - 1, len(available_peers))
        selected_peers = available_peers[:num_peers]
        
        return {
            "activity_id": selected_activity_id,
            "participants": ["marcus"] + selected_peers,
            "reason": f"Supports academic learning in: {', '.join(academic_subjects)}"
        }
    
    def _conduct_social_practice_session(self) -> Dict[str, Any]:
        """Dedicated social skills practice time"""
        logger.info("Conducting dedicated social practice session")
        
        # Get current social skills progress to focus practice
        progress = self.peer_system.get_social_skills_progress()
        focus_skills = progress.get("next_focus_areas", [])
        
        # Select appropriate interaction based on focus skills
        if "leadership" in [skill.lower() for skill in focus_skills]:
            context = InteractionContext.GROUP_PROJECT
            topic = ConversationTopic.SOLVING_PROBLEMS
        elif "empathy" in [skill.lower() for skill in focus_skills]:
            context = InteractionContext.PLAYGROUND
            topic = ConversationTopic.FRIENDSHIP_BUILDING
        else:
            context = InteractionContext.CLASSROOM
            topic = ConversationTopic.ACADEMIC_HELP
        
        # Select diverse peers for practice
        available_peers = list(self.peer_system.peers.keys())
        practice_peers = available_peers[:2]  # Practice with 2 peers
        
        session = self.peer_system.simulate_peer_interaction(
            peers_to_include=practice_peers,
            context=context,
            topic=topic,
            duration_minutes=10
        )
        
        return {
            "type": "social_practice",
            "focus_skills": focus_skills,
            "peers": practice_peers,
            "session": asdict(session),
            "success_rating": session.overall_success_rating,
            "conflicts_resolved": session.conflicts_resolved
        }
    
    def _integrate_eq_coaching(self, morning_interaction: Dict, social_practice: Dict) -> List[Dict[str, Any]]:
        """Integrate EQ coaching based on social interactions"""
        eq_coaching_moments = []
        
        if not self.eq_system:
            return eq_coaching_moments
        
        # Analyze morning interaction for EQ coaching opportunities
        morning_success = morning_interaction.get("success_rating", 0)
        if morning_success < 0.8:
            eq_coaching_moments.append({
                "moment": "morning_warmup_support",
                "domain": EQDomain.SOCIAL_SKILLS.value,
                "coaching_focus": "Building confidence in social greetings",
                "suggested_activity": "Practice friendly greetings with different personality types"
            })
        
        # Analyze social practice for EQ development
        conflicts = social_practice.get("conflicts_resolved", 0)
        if conflicts > 0:
            eq_coaching_moments.append({
                "moment": "conflict_resolution_learning",
                "domain": EQDomain.EMPATHY.value,
                "coaching_focus": "Understanding different perspectives in disagreements",
                "suggested_activity": "Role-play seeing situations from others' viewpoints"
            })
        
        # Check for emotional regulation needs
        practice_success = social_practice.get("success_rating", 0)
        if practice_success < 0.7:
            eq_coaching_moments.append({
                "moment": "emotional_regulation_support",
                "domain": EQDomain.SELF_REGULATION.value,
                "coaching_focus": "Managing emotions during challenging social situations",
                "suggested_activity": "Deep breathing and positive self-talk practice"
            })
        
        return eq_coaching_moments
    
    def _assess_social_readiness(self) -> Dict[str, Any]:
        """Assess Marcus's social readiness for academic advancement"""
        social_progress = self.peer_system.get_social_skills_progress()
        
        # Calculate overall social readiness score
        overall_level = social_progress.get("overall_social_level", 0.5)
        individual_skills = social_progress.get("individual_skills", {})
        
        # Determine readiness level
        if overall_level >= 0.85:
            readiness_level = SocialReadinessLevel.ADVANCED
        elif overall_level >= 0.75:
            readiness_level = SocialReadinessLevel.PROFICIENT
        elif overall_level >= 0.5:
            readiness_level = SocialReadinessLevel.DEVELOPING
        else:
            readiness_level = SocialReadinessLevel.EMERGING
        
        # Identify strengths and areas for growth
        strengths = []
        growth_areas = []
        
        for skill, data in individual_skills.items():
            skill_level = data.get("current_level", 0) if isinstance(data, dict) else data
            if skill_level >= 0.8:
                strengths.append(skill)
            elif skill_level < 0.6:
                growth_areas.append(skill)
        
        return {
            "overall_level": overall_level,
            "readiness_level": readiness_level.value,
            "strengths": strengths,
            "growth_areas": growth_areas,
            "grade_advancement_ready": overall_level >= self.social_learning_config["social_readiness_threshold"],
            "assessment_date": datetime.now().isoformat()
        }
    
    def _calculate_integration_metrics(self, morning_interaction: Dict, academic_session: Dict, 
                                     social_practice: Dict, eq_coaching: List[Dict]) -> Dict[str, float]:
        """Calculate metrics for how well social and academic learning integrated"""
        
        # Social engagement metrics
        morning_success = morning_interaction.get("success_rating", 0)
        practice_success = social_practice.get("success_rating", 0)
        social_engagement = (morning_success + practice_success) / 2
        
        # Academic collaboration metrics
        collaborative_activities = academic_session.get("collaborative_activities", [])
        collaboration_success = 0.0
        if collaborative_activities:
            collaboration_success = sum(
                activity.get("success_rating", 0) for activity in collaborative_activities
            ) / len(collaborative_activities)
        
        # EQ coaching integration
        eq_integration = min(len(eq_coaching) / 3, 1.0)  # Normalize to 0-1
        
        # Overall integration success
        overall_integration = (social_engagement * 0.4 + collaboration_success * 0.4 + eq_integration * 0.2)
        
        return {
            "social_engagement": social_engagement,
            "academic_collaboration": collaboration_success,
            "eq_coaching_integration": eq_integration,
            "overall_integration_success": overall_integration,
            "daily_social_minutes": 15 + social_practice.get("session", {}).get("duration_minutes", 10),
            "peer_interactions_completed": 2,  # Morning + practice
            "conflicts_resolved_today": social_practice.get("conflicts_resolved", 0)
        }
    
    def _extract_social_skills_practiced(self, morning_interaction: Dict, social_practice: Dict) -> List[SocialSkillArea]:
        """Extract all social skills practiced during the day"""
        skills_practiced = set()
        
        # From morning interaction
        morning_skills = morning_interaction.get("skills_practiced", [])
        for skill in morning_skills:
            if isinstance(skill, str):
                # Convert string to SocialSkillArea enum
                try:
                    skills_practiced.add(SocialSkillArea(skill))
                except ValueError:
                    pass
        
        # From social practice
        practice_session = social_practice.get("session", {})
        practice_skills = practice_session.get("social_skills_practiced", [])
        for skill in practice_skills:
            if hasattr(skill, 'value'):
                skills_practiced.add(skill)
        
        return list(skills_practiced)
    
    def _generate_daily_recommendations(self, integration_metrics: Dict, social_readiness: Dict) -> List[str]:
        """Generate personalized recommendations for tomorrow's learning"""
        recommendations = []
        
        # Social engagement recommendations
        if integration_metrics["social_engagement"] < 0.7:
            recommendations.append(
                "Focus on building confidence in social interactions through structured activities"
            )
        
        # Academic collaboration recommendations
        if integration_metrics["academic_collaboration"] < 0.6:
            recommendations.append(
                "Increase collaborative learning activities to strengthen peer learning skills"
            )
        
        # EQ coaching recommendations
        if integration_metrics["eq_coaching_integration"] < 0.5:
            recommendations.append(
                "Incorporate more emotional intelligence coaching during social interactions"
            )
        
        # Social readiness recommendations
        readiness_level = social_readiness.get("readiness_level", "emerging")
        if readiness_level == "emerging":
            recommendations.append(
                "Focus on basic social skills: greetings, sharing, and taking turns"
            )
        elif readiness_level == "developing":
            recommendations.append(
                "Practice consistent application of social skills in various contexts"
            )
        elif readiness_level == "proficient":
            recommendations.append(
                "Explore leadership opportunities and helping peers with social skills"
            )
        
        # Growth area recommendations
        growth_areas = social_readiness.get("growth_areas", [])
        if growth_areas:
            recommendations.append(
                f"Focus tomorrow's practice on: {', '.join(growth_areas[:2])}"
            )
        
        return recommendations
    
    def _store_integrated_session(self, session: IntegratedLearningSession):
        """Store integrated session data for progress tracking"""
        # For now, save to JSON file
        # In production, this would go to a proper database
        session_data = asdict(session)
        
        import os
        os.makedirs("output/integrated_sessions", exist_ok=True)
        
        filename = f"output/integrated_sessions/{session.session_id}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        logger.info(f"Integrated session stored: {filename}")
    
    def get_social_readiness_for_grade_advancement(self) -> Dict[str, Any]:
        """Get comprehensive social readiness assessment for grade progression system"""
        if not self.grade_system:
            logger.warning("Grade progression system not available")
            return {"error": "Grade progression system not available"}
        
        # Get current social skills progress
        social_progress = self.peer_system.get_social_skills_progress()
        
        # Get peer relationship status
        peer_relationships = {}
        for peer_id in self.peer_system.peers.keys():
            relationship = self.peer_system.get_peer_relationship_status(peer_id)
            peer_relationships[peer_id] = relationship
        
        # Calculate social readiness metrics for grade advancement
        overall_social_level = social_progress.get("overall_social_level", 0.5)
        
        # Social skills criteria for grade advancement
        grade_readiness_criteria = {
            "kindergarten_to_first": {
                "min_social_level": 0.65,
                "required_skills": ["cooperation", "turn_taking", "active_listening"],
                "min_peer_relationships": 2,
                "min_relationship_strength": 0.6
            },
            "first_to_second": {
                "min_social_level": 0.75,
                "required_skills": ["cooperation", "leadership", "empathy", "compromise"],
                "min_peer_relationships": 3,
                "min_relationship_strength": 0.7
            }
        }
        
        # Assess readiness for next grade
        current_grade = "kindergarten"  # This would come from grade system
        next_grade_key = f"{current_grade}_to_first"
        
        criteria = grade_readiness_criteria.get(next_grade_key, grade_readiness_criteria["kindergarten_to_first"])
        
        # Check criteria
        meets_social_level = overall_social_level >= criteria["min_social_level"]
        
        # Check required skills
        individual_skills = social_progress.get("individual_skills", {})
        required_skills_met = []
        for skill in criteria["required_skills"]:
            skill_data = individual_skills.get(skill, {})
            skill_level = skill_data.get("current_level", 0) if isinstance(skill_data, dict) else skill_data
            if skill_level >= 0.7:
                required_skills_met.append(skill)
        
        meets_skill_requirements = len(required_skills_met) >= len(criteria["required_skills"]) * 0.75
        
        # Check peer relationships
        strong_relationships = sum(1 for rel in peer_relationships.values() 
                                 if rel.get("relationship_strength", 0) >= criteria["min_relationship_strength"])
        meets_relationship_requirements = strong_relationships >= criteria["min_peer_relationships"]
        
        # Overall grade readiness
        grade_advancement_ready = all([
            meets_social_level,
            meets_skill_requirements, 
            meets_relationship_requirements
        ])
        
        return {
            "overall_social_level": overall_social_level,
            "grade_advancement_ready": grade_advancement_ready,
            "criteria_met": {
                "social_level": meets_social_level,
                "required_skills": meets_skill_requirements,
                "peer_relationships": meets_relationship_requirements
            },
            "required_skills_progress": {skill: individual_skills.get(skill, {}).get("current_level", 0) 
                                       for skill in criteria["required_skills"]},
            "peer_relationship_summary": {
                "total_relationships": len(peer_relationships),
                "strong_relationships": strong_relationships,
                "average_relationship_strength": sum(rel.get("relationship_strength", 0) 
                                                   for rel in peer_relationships.values()) / len(peer_relationships) if peer_relationships else 0
            },
            "next_focus_areas": social_progress.get("next_focus_areas", []),
            "assessment_date": datetime.now().isoformat()
        }
    
    def generate_kindergarten_deployment_report(self) -> Dict[str, Any]:
        """Generate comprehensive report for kindergarten classroom deployment"""
        logger.info("Generating kindergarten deployment report")
        
        # Get current status from all systems
        social_progress = self.peer_system.get_social_skills_progress()
        social_readiness = self._assess_social_readiness()
        grade_readiness = self.get_social_readiness_for_grade_advancement()
        
        # Get peer relationship overview
        peer_overview = {}
        for peer_id, peer in self.peer_system.peers.items():
            relationship = self.peer_system.get_peer_relationship_status(peer_id)
            peer_overview[peer_id] = {
                "name": peer.name,
                "personality_type": peer.personality_type.value,
                "relationship_strength": relationship.get("relationship_strength", 0),
                "interaction_count": relationship.get("interaction_count", 0),
                "relationship_status": relationship.get("status", "unknown")
            }
        
        # Get interaction recommendations
        recommendations = self.peer_system.generate_interaction_recommendations()
        
        # Compile deployment readiness assessment
        deployment_readiness = {
            "social_skills_ready": social_progress.get("overall_social_level", 0) >= 0.6,
            "peer_interaction_ready": len([p for p in peer_overview.values() 
                                         if p["relationship_strength"] >= 0.5]) >= 2,
            "collaboration_ready": any("cooperation" in skill or "leadership" in skill 
                                     for skill in social_progress.get("individual_skills", {}).keys()),
            "conflict_resolution_ready": social_progress.get("development_stage", "") != "emerging_skills"
        }
        
        overall_deployment_ready = sum(deployment_readiness.values()) >= 3
        
        return {
            "deployment_date": datetime.now().isoformat(),
            "marcus_social_profile": {
                "overall_social_level": social_progress.get("overall_social_level", 0),
                "development_stage": social_progress.get("development_stage", "unknown"),
                "strongest_skills": [skill for skill, data in social_progress.get("individual_skills", {}).items()
                                   if (data.get("current_level", 0) if isinstance(data, dict) else data) >= 0.8],
                "growth_areas": social_readiness.get("growth_areas", [])
            },
            "peer_relationship_status": peer_overview,
            "classroom_integration_recommendations": recommendations,
            "deployment_readiness": deployment_readiness,
            "overall_deployment_ready": overall_deployment_ready,
            "recommended_classroom_activities": [
                "Morning circle time with peer greetings",
                "Collaborative learning centers with 2-3 students",
                "Structured play time with conflict resolution support",
                "Daily reflection sharing with peer feedback"
            ],
            "teacher_guidance": [
                "Monitor peer interactions for social coaching opportunities",
                "Provide structured collaborative activities daily",
                "Support conflict resolution with guided questions",
                "Celebrate social successes and growth progress"
            ],
            "parent_communication_highlights": [
                f"Marcus shows {social_readiness.get('readiness_level', 'developing')} social readiness",
                f"Strong relationships with {len([p for p in peer_overview.values() if p['relationship_strength'] >= 0.7])} classroom peers",
                f"Focus areas for home support: {', '.join(social_readiness.get('growth_areas', [])[:2])}"
            ]
        }

def create_marcus_social_integration() -> MarcusSocialLearningIntegration:
    """Factory function to create the integrated social learning system"""
    return MarcusSocialLearningIntegration()

if __name__ == "__main__":
    # Demo the integrated system
    print("🤝 Marcus AGI Social Learning Integration System")
    print("=" * 55)
    
    try:
        # Create integrated system
        integration = create_marcus_social_integration()
        
        # Run integrated daily session
        print("\n🚀 Running integrated daily learning session...")
        session = integration.run_integrated_daily_session()
        
        print(f"\n📊 Session Results:")
        print(f"  Academic Focus: {', '.join(session.academic_focus)}")
        print(f"  Social Skills Practiced: {len(session.social_focus)}")
        print(f"  Peer Interactions: {len(session.peer_interactions)}")
        print(f"  Integration Success: {session.integration_success_metrics['overall_integration_success']:.1%}")
        
        # Generate kindergarten deployment report
        print("\n🏫 Generating kindergarten deployment report...")
        deployment_report = integration.generate_kindergarten_deployment_report()
        
        print(f"\n📋 Deployment Readiness:")
        print(f"  Overall Ready: {'✅' if deployment_report['overall_deployment_ready'] else '⚠️'}")
        print(f"  Social Level: {deployment_report['marcus_social_profile']['overall_social_level']:.1%}")
        print(f"  Development Stage: {deployment_report['marcus_social_profile']['development_stage']}")
        
        print(f"\n🎯 Recommendations Generated: {len(session.recommendations)}")
        for i, rec in enumerate(session.recommendations[:3], 1):
            print(f"  {i}. {rec}")
        
        print("\n✅ Integration system working successfully!")
        
    except Exception as e:
        import traceback
        print(f"\n❌ Integration failed: {e}")
        print(f"📝 Traceback: {traceback.format_exc()}")
