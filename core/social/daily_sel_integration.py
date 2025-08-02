#!/usr/bin/env python3
"""
Daily SEL Integration System for Marcus AGI

This module integrates the SEL Curriculum Expansion with Marcus's existing
daily learning loop, providing seamless social-emotional learning throughout
the day while building on the comprehensive foundations already in place.

Features:
1. SEL lesson integration with daily academic subjects
2. Emotion regulation practice during transitions
3. Conflict resolution coaching during social interactions  
4. Empathy exercises integrated with peer interactions
5. Progress tracking and assessment
6. Mr. Rogers wisdom integration
7. Real-time SEL coaching based on session data
"""

import json
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Import the SEL curriculum system
from .sel_curriculum_expansion import (
    SELCurriculumExpansion, SELSkillArea, SELDifficultyLevel, 
    SELLesson, EmotionRegulationDrill, ConflictResolutionScenario, EmpathyExercise
)

logger = logging.getLogger(__name__)

@dataclass
class DailySELIntegration:
    """Daily SEL integration configuration and state"""
    date: datetime
    morning_sel_focus: SELSkillArea
    academic_integrations: Dict[str, List[str]]
    regulation_practice_schedule: List[Dict[str, Any]]
    conflict_resolution_readiness: Dict[str, Any]
    empathy_opportunities: List[Dict[str, Any]]
    evening_reflection_prompts: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'date': self.date.isoformat(),
            'morning_sel_focus': self.morning_sel_focus.value,
            'academic_integrations': self.academic_integrations,
            'regulation_practice_schedule': self.regulation_practice_schedule,
            'conflict_resolution_readiness': self.conflict_resolution_readiness,
            'empathy_opportunities': self.empathy_opportunities,
            'evening_reflection_prompts': self.evening_reflection_prompts
        }

class DailySELIntegrationSystem:
    """System for integrating SEL throughout Marcus's daily learning"""
    
    def __init__(self, sessions_dir: str = "output/integrated_sessions"):
        self.sel_curriculum = SELCurriculumExpansion()
        self.sessions_dir = Path(sessions_dir)
        self.output_dir = Path("output/daily_sel_integration")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Load Marcus's current SEL levels from recent sessions
        self.marcus_sel_levels = self._assess_current_sel_levels()
        
    def _assess_current_sel_levels(self) -> Dict[SELSkillArea, SELDifficultyLevel]:
        """Assess Marcus's current SEL levels from recent session data"""
        default_levels = {
            SELSkillArea.EMOTION_IDENTIFICATION: SELDifficultyLevel.BUILDING,
            SELSkillArea.EMOTION_REGULATION: SELDifficultyLevel.FOUNDATION, 
            SELSkillArea.CONFLICT_RESOLUTION: SELDifficultyLevel.BUILDING,
            SELSkillArea.EMPATHY_DEVELOPMENT: SELDifficultyLevel.BUILDING,
            SELSkillArea.SOCIAL_AWARENESS: SELDifficultyLevel.FOUNDATION,
            SELSkillArea.RELATIONSHIP_SKILLS: SELDifficultyLevel.BUILDING,
            SELSkillArea.RESPONSIBLE_DECISION_MAKING: SELDifficultyLevel.FOUNDATION,
            SELSkillArea.STRESS_MANAGEMENT: SELDifficultyLevel.FOUNDATION
        }
        
        if not self.sessions_dir.exists():
            print(f"📁 Using default SEL levels - sessions directory not found: {self.sessions_dir}")
            return default_levels
        
        # Analyze recent sessions for SEL indicators
        recent_sessions = []
        for session_file in sorted(self.sessions_dir.glob("integrated_session_*.json"))[-5:]:  # Last 5 sessions
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    recent_sessions.append(session_data)
            except Exception as e:
                logger.warning(f"Could not load session {session_file}: {e}")
        
        if not recent_sessions:
            print("📊 Using default SEL levels - no recent sessions found")
            return default_levels
        
        # Analyze sessions for SEL skill indicators
        analyzed_levels = default_levels.copy()
        
        # Analyze emotion regulation from overall success rates
        avg_success = sum(s.get('overall_success_rating', 0.5) for s in recent_sessions) / len(recent_sessions)
        if avg_success > 0.8:
            analyzed_levels[SELSkillArea.EMOTION_REGULATION] = SELDifficultyLevel.PRACTICING
        elif avg_success > 0.6:
            analyzed_levels[SELSkillArea.EMOTION_REGULATION] = SELDifficultyLevel.BUILDING

        # Analyze conflict resolution from conflicts resolved
        conflicts_resolved = sum(s.get('conflicts_resolved', 0) for s in recent_sessions)
        total_conflicts = sum(len(s.get('peer_interactions', [])) for s in recent_sessions if 'conflict' in str(s).lower())
        if total_conflicts > 0 and conflicts_resolved / total_conflicts > 0.7:
            analyzed_levels[SELSkillArea.CONFLICT_RESOLUTION] = SELDifficultyLevel.PRACTICING
        
        # Analyze relationship skills from peer relationship strength
        avg_relationship_strength = sum(s.get('peer_relationship_strength', 0.5) for s in recent_sessions) / len(recent_sessions)
        if avg_relationship_strength > 0.9:
            analyzed_levels[SELSkillArea.RELATIONSHIP_SKILLS] = SELDifficultyLevel.PRACTICING
        elif avg_relationship_strength > 0.7:
            analyzed_levels[SELSkillArea.RELATIONSHIP_SKILLS] = SELDifficultyLevel.BUILDING
            
        print(f"📊 Assessed SEL levels from {len(recent_sessions)} recent sessions")
        return analyzed_levels
    
    def create_daily_sel_plan(self, academic_subjects: List[str]) -> DailySELIntegration:
        """Create comprehensive daily SEL integration plan"""
        today = datetime.now()
        
        # Choose morning SEL focus based on lowest skill area
        morning_focus = min(self.marcus_sel_levels.items(), key=lambda x: list(SELDifficultyLevel).index(x[1]))[0]
        
        # Create academic integrations
        academic_integrations = self.sel_curriculum.integrate_with_daily_learning(academic_subjects)
        
        # Schedule emotion regulation practice
        regulation_schedule = self._create_regulation_schedule()
        
        # Prepare conflict resolution readiness
        conflict_readiness = self._prepare_conflict_resolution()
        
        # Plan empathy opportunities
        empathy_opportunities = self._plan_empathy_opportunities()
        
        # Create evening reflection prompts
        reflection_prompts = self._create_reflection_prompts(morning_focus)
        
        return DailySELIntegration(
            date=today,
            morning_sel_focus=morning_focus,
            academic_integrations=academic_integrations,
            regulation_practice_schedule=regulation_schedule,
            conflict_resolution_readiness=conflict_readiness,
            empathy_opportunities=empathy_opportunities,
            evening_reflection_prompts=reflection_prompts
        )
    
    def _create_regulation_schedule(self) -> List[Dict[str, Any]]:
        """Create emotion regulation practice schedule throughout the day"""
        current_level = self.marcus_sel_levels[SELSkillArea.EMOTION_REGULATION]
        
        schedule = [
            {
                "time": "morning_start",
                "activity": "Morning Breathing Check-in",
                "description": "Take 3 deep breaths and notice how your body feels",
                "skill_practiced": "body_awareness",
                "duration_minutes": 2
            },
            {
                "time": "before_challenging_activity", 
                "activity": "Pre-Challenge Preparation",
                "description": "Practice calm breathing before starting something new or difficult",
                "skill_practiced": "anticipatory_regulation",
                "duration_minutes": 1
            },
            {
                "time": "transition_moments",
                "activity": "Transition Breathing",
                "description": "One deep breath between activities to stay centered",
                "skill_practiced": "transition_management", 
                "duration_minutes": 1
            },
            {
                "time": "afternoon_reset",
                "activity": "Midday Emotion Check",
                "description": "Notice current emotions and use regulation tools if needed",
                "skill_practiced": "emotional_awareness",
                "duration_minutes": 3
            }
        ]
        
        # Add level-appropriate regulation drills
        if current_level in [SELDifficultyLevel.BUILDING, SELDifficultyLevel.PRACTICING]:
            schedule.append({
                "time": "structured_practice",
                "activity": "Daily Regulation Drill",
                "description": "Practice specific emotion regulation technique",
                "skill_practiced": "regulation_mastery",
                "duration_minutes": 5,
                "drill_type": "targeted_emotion_practice"
            })
        
        return schedule
    
    def _prepare_conflict_resolution(self) -> Dict[str, Any]:
        """Prepare conflict resolution resources and strategies"""
        current_level = self.marcus_sel_levels[SELSkillArea.CONFLICT_RESOLUTION]
        
        # Select appropriate conflict resolution scenarios
        available_scenarios = [
            scenario for scenario in self.sel_curriculum.conflict_resolution_scenarios
            if scenario.conflict_type in ["resource_sharing", "rule_disagreement", "emotional_harm"]
        ]
        
        return {
            "current_skill_level": current_level.value,
            "ready_scenarios": [s.scenario_name for s in available_scenarios[:2]],
            "coaching_reminders": [
                "Remember the problem-solving steps: Stop, Talk, Listen, Try Again",
                "Use 'I' statements to share feelings",
                "Listen to understand, not to argue",
                "Look for solutions that work for everyone"
            ],
            "success_indicators": [
                "Pauses before reacting to conflict",
                "Uses words instead of physical responses", 
                "Shows empathy for other person's perspective",
                "Participates in finding solutions"
            ]
        }
    
    def _plan_empathy_opportunities(self) -> List[Dict[str, Any]]:
        """Plan empathy development opportunities throughout the day"""
        current_level = self.marcus_sel_levels[SELSkillArea.EMPATHY_DEVELOPMENT]
        
        opportunities = [
            {
                "context": "reading_time",
                "activity": "Character Emotion Discussion",
                "description": "Discuss how characters in stories might be feeling",
                "empathy_focus": "perspective_taking",
                "coaching_questions": [
                    "How do you think this character is feeling?",
                    "Why might they feel that way?",
                    "What would you want if you were in their situation?"
                ]
            },
            {
                "context": "peer_interactions",
                "activity": "Friend Feeling Check-ins",
                "description": "Notice and respond to friends' emotions during play",
                "empathy_focus": "emotion_recognition",
                "coaching_questions": [
                    "How does your friend seem to be feeling?",
                    "What clues tell you that?", 
                    "How can you show you care about their feelings?"
                ]
            },
            {
                "context": "daily_activities",
                "activity": "Kindness Opportunities",
                "description": "Look for chances to help or show kindness to others",
                "empathy_focus": "caring_action",
                "coaching_questions": [
                    "How can you help someone who seems to need it?",
                    "What would make someone feel better in this situation?",
                    "How does it feel when someone is kind to you?"
                ]
            }
        ]
        
        # Add advanced empathy exercises for higher levels
        if current_level in [SELDifficultyLevel.PRACTICING, SELDifficultyLevel.MASTERING]:
            opportunities.append({
                "context": "reflection_time",
                "activity": "Empathy Journaling",
                "description": "Reflect on times when you understood someone else's feelings",
                "empathy_focus": "empathy_awareness",
                "coaching_questions": [
                    "When did you notice someone else's feelings today?",
                    "How did you show that you cared?",
                    "What did you learn about that person?"
                ]
            })
        
        return opportunities
    
    def _create_reflection_prompts(self, morning_focus: SELSkillArea) -> List[str]:
        """Create evening reflection prompts based on daily SEL focus"""
        base_prompts = [
            "What emotions did you notice in yourself today?",
            "How did you handle challenging moments?",
            "What are you proud of from today?",
            "How did you show kindness to others?"
        ]
        
        # Add focus-specific prompts
        focus_prompts = {
            SELSkillArea.EMOTION_IDENTIFICATION: [
                "What new emotions did you notice today?",
                "When did you recognize emotions in others?"
            ],
            SELSkillArea.EMOTION_REGULATION: [
                "When did you use your calm-down strategies?",
                "How well did your regulation tools work?"
            ],
            SELSkillArea.CONFLICT_RESOLUTION: [
                "Did you have any problems with friends today? How did you handle them?",
                "When did you use your problem-solving steps?"
            ],
            SELSkillArea.EMPATHY_DEVELOPMENT: [
                "When did you think about how someone else was feeling?",
                "How did you show care for others' feelings?"
            ]
        }
        
        return base_prompts + focus_prompts.get(morning_focus, [])
    
    def provide_realtime_sel_coaching(self, session_context: Dict[str, Any]) -> Dict[str, Any]:
        """Provide real-time SEL coaching based on current session context"""
        coaching_response = {
            "coaching_type": "none",
            "coaching_message": "",
            "skill_practiced": "",
            "success_reinforcement": ""
        }
        
        # Analyze context for SEL coaching opportunities
        if 'peer_interactions' in session_context:
            interactions = session_context['peer_interactions']
            
            # Check for conflict situations
            conflict_indicators = ['disagreement', 'argument', 'conflict', 'upset', 'angry']
            has_conflict = any(indicator in str(interactions).lower() for indicator in conflict_indicators)
            
            if has_conflict:
                coaching_response.update({
                    "coaching_type": "conflict_resolution",
                    "coaching_message": "I notice there might be a disagreement. Let's use our problem-solving steps: Stop, Talk, Listen, Try Again.",
                    "skill_practiced": "conflict_resolution",
                    "regulation_support": "Take a deep breath first. How are you feeling right now?"
                })
            
            # Check for empathy opportunities
            emotion_indicators = ['sad', 'happy', 'excited', 'worried', 'frustrated']
            peer_emotions = [indicator for indicator in emotion_indicators if indicator in str(interactions).lower()]
            
            if peer_emotions:
                coaching_response.update({
                    "coaching_type": "empathy_development",
                    "coaching_message": f"I notice someone might be feeling {peer_emotions[0]}. How do you think they're feeling?",
                    "skill_practiced": "empathy",
                    "empathy_prompt": "What could you do to show you care about their feelings?"
                })
        
        # Check for emotion regulation needs
        if 'overall_success_rating' in session_context:
            success_rate = session_context['overall_success_rating']
            if success_rate < 0.5:  # Low success might indicate regulation challenges
                coaching_response.update({
                    "coaching_type": "emotion_regulation", 
                    "coaching_message": "This seems challenging. Let's try some deep breathing to help you feel more calm and focused.",
                    "skill_practiced": "emotion_regulation",
                    "regulation_technique": "deep_breathing"
                })
        
        return coaching_response
    
    def assess_daily_sel_progress(self, session_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess SEL progress from daily sessions"""
        progress_report = {
            "date": datetime.now().isoformat(),
            "sessions_analyzed": len(session_data),
            "sel_skill_observations": {},
            "growth_highlights": [],
            "areas_for_practice": [],
            "coaching_effectiveness": {},
            "recommendations": []
        }
        
        if not session_data:
            return progress_report
        
        # Analyze emotion regulation indicators
        avg_success = sum(s.get('overall_success_rating', 0.5) for s in session_data) / len(session_data)
        eq_coaching_moments = sum(len(s.get('eq_coaching_moments', [])) for s in session_data)
        
        progress_report["sel_skill_observations"]["emotion_regulation"] = {
            "average_success_rate": avg_success,
            "coaching_moments": eq_coaching_moments,
            "assessment": "improving" if avg_success > 0.7 else "needs_practice"
        }
        
        # Analyze conflict resolution
        conflicts_resolved = sum(s.get('conflicts_resolved', 0) for s in session_data)
        collaboration_successes = sum(s.get('collaboration_successes', 0) for s in session_data)
        
        progress_report["sel_skill_observations"]["conflict_resolution"] = {
            "conflicts_resolved": conflicts_resolved,
            "collaboration_successes": collaboration_successes,
            "assessment": "strong" if conflicts_resolved >= collaboration_successes else "developing"
        }
        
        # Analyze relationship skills
        avg_relationship_strength = sum(s.get('peer_relationship_strength', 0.5) for s in session_data) / len(session_data)
        
        progress_report["sel_skill_observations"]["relationship_skills"] = {
            "average_relationship_strength": avg_relationship_strength,
            "assessment": "excellent" if avg_relationship_strength > 0.8 else "good" if avg_relationship_strength > 0.6 else "developing"
        }
        
        # Generate growth highlights
        if avg_success > 0.8:
            progress_report["growth_highlights"].append("Excellent emotional regulation - high success rates")
        if conflicts_resolved > 0:
            progress_report["growth_highlights"].append(f"Successfully resolved {conflicts_resolved} conflicts")
        if avg_relationship_strength > 0.8:
            progress_report["growth_highlights"].append("Strong peer relationships - showing care and connection")
        
        # Generate practice recommendations
        if avg_success < 0.6:
            progress_report["areas_for_practice"].append("Emotion regulation strategies")
            progress_report["recommendations"].append("Practice daily breathing exercises and calm-down techniques")
        
        if eq_coaching_moments > 3:
            progress_report["areas_for_practice"].append("Independent emotion management")
            progress_report["recommendations"].append("Work on recognizing emotion warning signs earlier")
            
        if avg_relationship_strength < 0.7:
            progress_report["areas_for_practice"].append("Peer relationship building")
            progress_report["recommendations"].append("Focus on empathy exercises and perspective-taking practice")
        
        return progress_report
    
    def generate_daily_sel_report(self, daily_plan: DailySELIntegration, session_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive daily SEL report"""
        progress_assessment = self.assess_daily_sel_progress(session_data)
        
        report = {
            "report_type": "daily_sel_integration",
            "date": daily_plan.date.isoformat(),
            "sel_focus_area": daily_plan.morning_sel_focus.value,
            "planned_activities": {
                "academic_integrations": daily_plan.academic_integrations,
                "regulation_practice": len(daily_plan.regulation_practice_schedule),
                "empathy_opportunities": len(daily_plan.empathy_opportunities)
            },
            "progress_assessment": progress_assessment,
            "sel_skill_development": {
                skill_area.value: level.value 
                for skill_area, level in self.marcus_sel_levels.items()
            },
            "daily_reflections": daily_plan.evening_reflection_prompts,
            "next_day_focus": self._recommend_next_focus()
        }
        
        return report
    
    def _recommend_next_focus(self) -> str:
        """Recommend tomorrow's SEL focus based on current levels"""
        lowest_skills = sorted(
            self.marcus_sel_levels.items(), 
            key=lambda x: list(SELDifficultyLevel).index(x[1])
        )
        
        # Rotate through lowest skills for balanced development
        return lowest_skills[0][0].value
    
    def save_daily_integration_plan(self, daily_plan: DailySELIntegration, session_data: List[Dict[str, Any]] = None):
        """Save daily SEL integration plan and progress"""
        timestamp = daily_plan.date.strftime("%Y%m%d_%H%M%S")
        
        # Save the plan
        plan_data = daily_plan.to_dict()
        plan_file = self.output_dir / f"daily_sel_plan_{timestamp}.json"
        with open(plan_file, 'w') as f:
            json.dump(plan_data, f, indent=2)
        
        # Save progress report if session data provided
        if session_data:
            report = self.generate_daily_sel_report(daily_plan, session_data)
            report_file = self.output_dir / f"daily_sel_report_{timestamp}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Also save text summary
            text_file = self.output_dir / f"daily_sel_summary_{timestamp}.txt"
            with open(text_file, 'w') as f:
                f.write(self._format_text_summary(report))
        
        print(f"✅ Daily SEL integration saved to {self.output_dir}")
    
    def _format_text_summary(self, report: Dict[str, Any]) -> str:
        """Format SEL report as readable text summary"""
        date = datetime.fromisoformat(report['date']).strftime("%B %d, %Y")
        
        summary = f"""📚 MARCUS AGI - DAILY SEL INTEGRATION REPORT
Date: {date}
Focus Area: {report['sel_focus_area'].replace('_', ' ').title()}

🎯 PLANNED ACTIVITIES:
• Academic Integrations: {len(report['planned_activities']['academic_integrations'])} subjects
• Emotion Regulation Practice: {report['planned_activities']['regulation_practice']} activities  
• Empathy Opportunities: {report['planned_activities']['empathy_opportunities']} exercises

📊 PROGRESS ASSESSMENT:
Sessions Analyzed: {report['progress_assessment']['sessions_analyzed']}

SEL Skill Observations:
"""
        
        for skill, data in report['progress_assessment']['sel_skill_observations'].items():
            assessment = data.get('assessment', 'developing')
            summary += f"• {skill.replace('_', ' ').title()}: {assessment.title()}\n"
        
        if report['progress_assessment']['growth_highlights']:
            summary += f"\n🌟 GROWTH HIGHLIGHTS:\n"
            for highlight in report['progress_assessment']['growth_highlights']:
                summary += f"• {highlight}\n"
        
        if report['progress_assessment']['areas_for_practice']:
            summary += f"\n💪 AREAS FOR PRACTICE:\n"
            for area in report['progress_assessment']['areas_for_practice']:
                summary += f"• {area}\n"
        
        if report['progress_assessment']['recommendations']:
            summary += f"\n🎯 RECOMMENDATIONS:\n"
            for rec in report['progress_assessment']['recommendations']:
                summary += f"• {rec}\n"
        
        summary += f"\n🔄 TOMORROW'S FOCUS: {report['next_day_focus'].replace('_', ' ').title()}\n"
        
        return summary

def main():
    """Demonstrate Daily SEL Integration System"""
    print("🎯 Daily SEL Integration System - Strategic Option A Complete")
    print("=" * 60)
    
    # Initialize the system
    integration_system = DailySELIntegrationSystem()
    
    # Show current SEL assessment
    print(f"\n📊 Marcus's Current SEL Levels:")
    for skill_area, level in integration_system.marcus_sel_levels.items():
        print(f"  • {skill_area.value.replace('_', ' ').title()}: {level.value.title()}")
    
    # Create daily plan
    academic_subjects = ["reading", "math", "science", "art", "social_studies"]
    daily_plan = integration_system.create_daily_sel_plan(academic_subjects)
    
    print(f"\n📅 Today's SEL Integration Plan:")
    print(f"  Focus Area: {daily_plan.morning_sel_focus.value.replace('_', ' ').title()}")
    print(f"  Academic Integrations: {len(daily_plan.academic_integrations)} subjects")
    print(f"  Regulation Practice: {len(daily_plan.regulation_practice_schedule)} activities")
    print(f"  Empathy Opportunities: {len(daily_plan.empathy_opportunities)} exercises")
    
    # Show some specific integration examples
    print(f"\n🔗 Academic Integration Examples:")
    for subject, suggestions in list(daily_plan.academic_integrations.items())[:2]:
        print(f"  {subject.title()}:")
        for suggestion in suggestions[:2]:
            print(f"    - {suggestion}")
    
    # Show regulation practice schedule
    print(f"\n💪 Emotion Regulation Schedule:")
    for activity in daily_plan.regulation_practice_schedule[:3]:
        print(f"  • {activity['activity']} ({activity['duration_minutes']} min)")
        print(f"    {activity['description']}")
    
    # Show empathy opportunities
    print(f"\n❤️ Empathy Development Opportunities:")
    for opportunity in daily_plan.empathy_opportunities[:2]:
        print(f"  • {opportunity['activity']} - {opportunity['context']}")
        print(f"    {opportunity['description']}")
    
    # Demonstrate real-time coaching
    print(f"\n🎯 Real-time SEL Coaching Example:")
    sample_context = {
        "peer_interactions": [{"type": "disagreement", "emotion": "frustrated"}],
        "overall_success_rating": 0.4
    }
    coaching = integration_system.provide_realtime_sel_coaching(sample_context)
    if coaching['coaching_type'] != 'none':
        print(f"  Coaching Type: {coaching['coaching_type']}")
        print(f"  Message: {coaching['coaching_message']}")
    
    # Save the daily plan
    integration_system.save_daily_integration_plan(daily_plan)
    
    print(f"\n🎉 Daily SEL Integration System Complete!")
    print("✅ Comprehensive SEL curriculum expansion successfully implemented!")
    print("🔄 Ready for seamless integration with Marcus's daily learning loop!")

if __name__ == "__main__":
    main()
