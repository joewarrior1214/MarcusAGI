#!/usr/bin/env python3
"""
Grade Progression Integration Module for Marcus AGI

This module integrates the Grade Progression System with existing Marcus systems:
1. Daily Learning Loop - Adapts difficulty based on grade level
2. Curriculum System - Provides grade-appropriate content
3. Memory System - Tracks cross-grade learning progress
4. Reflection System - Incorporates grade readiness insights
5. EQ System - Considers social-emotional readiness for advancement

This ensures seamless grade progression within Marcus's learning framework.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date, timedelta
from dataclasses import asdict

# Import Marcus systems
from grade_progression_system import (
    GradeProgressionSystem, GradeLevel, AcademicSubject, ReadinessStatus,
    create_grade_progression_system
)
from daily_learning_loop import DailyLearningLoop, LEARNING_CONFIG
from kindergarten_curriculum_expansion import KindergartenCurriculumExpansion
from emotional_intelligence_assessment import EmotionalIntelligenceAssessment
from memory_system import MarcusMemorySystem, LearningConcept

logger = logging.getLogger(__name__)

class GradeProgressionIntegration:
    """Integrates grade progression with Marcus's existing learning systems"""
    
    def __init__(self):
        # Initialize core systems
        self.memory_system = MarcusMemorySystem()
        self.eq_system = EmotionalIntelligenceAssessment()
        self.kindergarten_curriculum = KindergartenCurriculumExpansion()
        self.progression_system = GradeProgressionSystem(
            memory_system=self.memory_system,
            eq_system=self.eq_system,
            kindergarten_curriculum=self.kindergarten_curriculum
        )
        
        # Integration state
        self.current_integration_session = {
            'session_id': f"integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'start_time': datetime.now(),
            'grade_checks_performed': 0,
            'adaptations_made': 0,
            'progression_events': []
        }
    
    def enhanced_daily_learning_session(self, session_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhanced daily learning session that incorporates grade progression
        
        This replaces the standard daily learning loop with grade-aware learning
        """
        logger.info("🎓 Starting Grade-Aware Daily Learning Session")
        
        if not session_data:
            session_data = self._generate_default_session_data()
        
        # 1. Check current grade readiness
        readiness_check = self._perform_grade_readiness_check()
        
        # 2. Adapt learning objectives based on grade level and readiness
        adapted_objectives = self._adapt_learning_objectives_for_grade(
            session_data.get('learning_objectives', []),
            readiness_check
        )
        
        # 3. Scale difficulty appropriately
        scaled_content = self._scale_content_difficulty(adapted_objectives, readiness_check)
        
        # 4. Conduct learning session with grade-appropriate content
        session_results = self._conduct_grade_aware_learning_session(scaled_content, readiness_check)
        
        # 5. Assess progress and determine if grade advancement is warranted
        progression_assessment = self._assess_learning_progress_for_advancement(session_results)
        
        # 6. Update grade progression tracking
        self._update_grade_progression_tracking(progression_assessment)
        
        # 7. Generate next session recommendations
        next_session_recommendations = self._generate_next_session_recommendations(
            session_results, progression_assessment
        )
        
        # Compile comprehensive session report
        enhanced_session_report = {
            'session_id': self.current_integration_session['session_id'],
            'session_date': datetime.now().isoformat(),
            'grade_readiness_check': readiness_check,
            'adapted_objectives': adapted_objectives,
            'scaled_content': scaled_content,
            'session_results': session_results,
            'progression_assessment': progression_assessment,
            'next_session_recommendations': next_session_recommendations,
            'grade_progression_status': self._get_current_progression_status(),
            'integration_metrics': self._calculate_integration_metrics()
        }
        
        return enhanced_session_report
    
    def _perform_grade_readiness_check(self) -> Dict[str, Any]:
        """Perform grade readiness check during learning session"""
        logger.info("📊 Performing grade readiness check...")
        
        # Check if it's time for a readiness assessment
        last_assessment_date = self._get_last_assessment_date()
        days_since_assessment = (date.today() - last_assessment_date).days if last_assessment_date else 999
        
        if days_since_assessment >= 30:  # Monthly assessments
            # Conduct full assessment
            assessment = self.progression_system.assess_grade_readiness()
            readiness_data = {
                'assessment_type': 'full',
                'assessment_date': assessment.assessment_date.isoformat(),
                'current_grade': assessment.current_grade.value,
                'recommended_grade': assessment.recommended_grade.value,
                'overall_readiness': assessment.overall_readiness.value,
                'subject_scores': assessment.subject_scores,
                'strengths': assessment.strengths,
                'areas_for_growth': assessment.areas_for_growth,
                'advancement_ready': assessment.overall_readiness in [ReadinessStatus.READY, ReadinessStatus.ADVANCED]
            }
        else:
            # Quick check based on recent performance
            readiness_data = self._quick_readiness_check()
        
        self.current_integration_session['grade_checks_performed'] += 1
        return readiness_data
    
    def _quick_readiness_check(self) -> Dict[str, Any]:
        """Quick readiness check based on recent performance"""
        current_grade = self.progression_system._get_current_grade()
        
        # Get recent performance data
        recent_performance = self._get_recent_performance_data()
        
        # Estimate readiness based on performance trends
        estimated_readiness = self._estimate_readiness_from_performance(recent_performance)
        
        return {
            'assessment_type': 'quick',
            'assessment_date': datetime.now().isoformat(),
            'current_grade': current_grade.value,
            'estimated_readiness': estimated_readiness,
            'recent_performance': recent_performance,
            'advancement_ready': estimated_readiness in ['ready', 'advanced']
        }
    
    def _adapt_learning_objectives_for_grade(self, base_objectives: List[str], 
                                           readiness_check: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Adapt learning objectives based on current grade and readiness"""
        logger.info("🎯 Adapting learning objectives for grade level...")
        
        current_grade = GradeLevel(readiness_check.get('current_grade', 'kindergarten'))
        adapted_objectives = []
        
        for objective_id in base_objectives:
            # Get base objective from curriculum
            base_objective = self._get_objective_from_curriculum(objective_id, current_grade)
            
            if base_objective:
                # Adapt based on readiness level
                adapted_objective = self._adapt_objective_for_readiness(base_objective, readiness_check)
                adapted_objectives.append(adapted_objective)
            else:
                # Create grade-appropriate alternative
                alternative_objective = self._create_grade_appropriate_alternative(objective_id, current_grade)
                adapted_objectives.append(alternative_objective)
        
        self.current_integration_session['adaptations_made'] += len(adapted_objectives)
        return adapted_objectives
    
    def _scale_content_difficulty(self, objectives: List[Dict[str, Any]], 
                                readiness_check: Dict[str, Any]) -> Dict[str, Any]:
        """Scale content difficulty based on grade level and readiness"""
        logger.info("📈 Scaling content difficulty...")
        
        current_grade = GradeLevel(readiness_check.get('current_grade', 'kindergarten'))
        readiness_level = readiness_check.get('overall_readiness', 'approaching')
        
        scaled_content = {
            'difficulty_level': self._calculate_difficulty_level(current_grade, readiness_level),
            'vocabulary_level': self._get_vocabulary_level(current_grade),
            'complexity_indicators': self._get_complexity_indicators(current_grade),
            'scaffolding_level': self._determine_scaffolding_level(readiness_level),
            'adapted_objectives': objectives,
            'grade_context': current_grade.value
        }
        
        # Apply difficulty scaling to each objective
        for objective in scaled_content['adapted_objectives']:
            objective['scaled_difficulty'] = self._apply_difficulty_scaling(objective, scaled_content)
        
        return scaled_content
    
    def _conduct_grade_aware_learning_session(self, scaled_content: Dict[str, Any],
                                            readiness_check: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct learning session with grade-aware adaptations"""
        logger.info("📚 Conducting grade-aware learning session...")
        
        # Simulate learning session (in real implementation, this would interact with actual learning modules)
        session_start = datetime.now()
        
        # Process each learning objective with grade-appropriate methods
        objective_results = []
        for objective in scaled_content['adapted_objectives']:
            result = self._process_grade_aware_objective(objective, scaled_content)
            objective_results.append(result)
        
        # Calculate session metrics
        session_duration = (datetime.now() - session_start).total_seconds()
        success_rate = sum(1 for result in objective_results if result.get('success', False)) / len(objective_results)
        
        return {
            'session_duration_seconds': session_duration, 
            'objectives_attempted': len(objective_results),
            'objectives_completed': sum(1 for result in objective_results if result.get('completed', False)),
            'success_rate': success_rate,
            'objective_results': objective_results,
            'engagement_level': self._calculate_engagement_level(objective_results),
            'grade_appropriate_performance': self._assess_grade_appropriate_performance(objective_results, scaled_content)
        }
    
    def _assess_learning_progress_for_advancement(self, session_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess learning progress to determine advancement readiness"""
        logger.info("📊 Assessing learning progress for advancement...")
        
        # Analyze session performance
        performance_analysis = self._analyze_session_performance(session_results)
        
        # Check accumulated progress over time
        accumulated_progress = self._check_accumulated_progress()
        
        # Determine advancement indicators
        advancement_indicators = self._identify_advancement_indicators(performance_analysis, accumulated_progress)
        
        # Make advancement recommendation
        advancement_recommendation = self._make_advancement_recommendation(advancement_indicators)
        
        return {
            'performance_analysis': performance_analysis,
            'accumulated_progress': accumulated_progress,
            'advancement_indicators': advancement_indicators,
            'advancement_recommendation': advancement_recommendation,
            'assessment_timestamp': datetime.now().isoformat()
        }
    
    def _update_grade_progression_tracking(self, progression_assessment: Dict[str, Any]):
        """Update grade progression tracking based on assessment"""
        logger.info("💾 Updating grade progression tracking...")
        
        # Store progression data in memory system
        progression_concept = LearningConcept(
            id=f"grade_progression_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            content=json.dumps(progression_assessment),
            subject="grade_progression",
            grade_level=progression_assessment.get('current_grade', 'kindergarten'),
            emotional_context="progressive_learning"
        )
        
        self.memory_system.store_concept(progression_concept)
        
        # Check if advancement should be triggered
        if progression_assessment.get('advancement_recommendation', {}).get('should_advance', False):
            self._trigger_grade_advancement_process(progression_assessment)
    
    def _trigger_grade_advancement_process(self, progression_assessment: Dict[str, Any]):
        """Trigger the grade advancement process"""
        logger.info("🚀 Triggering grade advancement process...")
        
        # Conduct comprehensive assessment
        comprehensive_assessment = self.progression_system.assess_grade_readiness()
        
        # Attempt advancement
        advancement_result = self.progression_system.advance_grade(assessment=comprehensive_assessment)
        
        # Record progression event
        progression_event = {
            'event_type': 'advancement_attempt',
            'timestamp': datetime.now().isoformat(),
            'assessment_data': asdict(comprehensive_assessment),
            'advancement_result': advancement_result,
            'triggered_by': 'daily_learning_integration'
        }
        
        self.current_integration_session['progression_events'].append(progression_event)
        
        if advancement_result['success']:
            logger.info(f"✅ Grade advancement successful: {advancement_result['message']}")
        else:
            logger.info(f"⚠️ Grade advancement not ready: {advancement_result['message']}")
    
    def _generate_next_session_recommendations(self, session_results: Dict[str, Any],
                                             progression_assessment: Dict[str, Any]) -> List[str]:
        """Generate recommendations for next learning session"""
        recommendations = []
        
        # Performance-based recommendations
        if session_results.get('success_rate', 0) < 0.7:
            recommendations.append("Provide additional practice in challenging areas")
            recommendations.append("Consider reducing difficulty level temporarily")
        elif session_results.get('success_rate', 0) > 0.9:
            recommendations.append("Increase challenge level for next session")
            recommendations.append("Introduce more complex concepts")
        
        # Grade progression recommendations
        advancement_rec = progression_assessment.get('advancement_recommendation', {})
        if advancement_rec.get('approaching_readiness', False):
            recommendations.append("Focus on grade transition preparation activities")
            recommendations.append("Increase assessment frequency to monitor readiness")
        
        # Engagement recommendations
        engagement = session_results.get('engagement_level', 0.5)
        if engagement < 0.6:
            recommendations.append("Incorporate more interactive and engaging activities")
            recommendations.append("Consider adjusting instruction mode preferences")
        
        return recommendations
    
    def _get_current_progression_status(self) -> Dict[str, Any]:
        """Get current grade progression status"""
        current_grade = self.progression_system._get_current_grade()
        days_in_grade = self.progression_system._get_days_in_current_grade()
        
        return {
            'current_grade': current_grade.value,
            'days_in_grade': days_in_grade,
            'grade_entry_date': self._get_grade_entry_date(),
            'next_assessment_due': self._get_next_assessment_date(),
            'progression_history_count': len(self._get_progression_history())
        }
    
    def _calculate_integration_metrics(self) -> Dict[str, Any]:
        """Calculate metrics for integration performance"""
        session = self.current_integration_session
        session_duration = (datetime.now() - session['start_time']).total_seconds()
        
        return {
            'session_duration_minutes': session_duration / 60,
            'grade_checks_performed': session['grade_checks_performed'],
            'adaptations_made': session['adaptations_made'],
            'progression_events': len(session['progression_events']),
            'integration_efficiency': self._calculate_integration_efficiency()
        }
    
    # Helper methods for implementation details
    
    def _generate_default_session_data(self) -> Dict[str, Any]:
        """Generate default session data if none provided"""
        return {
            'learning_objectives': ['number_sense_20', 'emotion_identification', 'storytelling_skills'],
            'session_type': 'daily_integrated',
            'duration_minutes': 45,
            'focus_areas': ['academic', 'social_emotional']
        }
    
    def _get_last_assessment_date(self) -> Optional[date]:
        """Get date of last comprehensive assessment"""
        # Implementation would query database for last assessment
        # For demo, return a date 25 days ago to trigger assessment
        return date.today() - timedelta(days=25)
    
    def _get_recent_performance_data(self) -> Dict[str, Any]:
        """Get recent performance data for quick assessment"""
        # Implementation would analyze recent learning session data
        return {
            'average_success_rate': 0.82,
            'engagement_trend': 'increasing',
            'mastery_progress': 0.78,
            'sessions_analyzed': 10
        }
    
    def _estimate_readiness_from_performance(self, performance_data: Dict[str, Any]) -> str:
        """Estimate readiness level from performance data"""
        success_rate = performance_data.get('average_success_rate', 0.5)
        mastery_progress = performance_data.get('mastery_progress', 0.5)
        
        combined_score = (success_rate + mastery_progress) / 2
        
        if combined_score >= 0.9:
            return 'advanced'
        elif combined_score >= 0.8:
            return 'ready'
        elif combined_score >= 0.7:
            return 'approaching'
        else:
            return 'not_ready'
    
    def _get_objective_from_curriculum(self, objective_id: str, grade: GradeLevel) -> Optional[Dict[str, Any]]:
        """Get objective from curriculum system"""
        # Implementation would query curriculum for specific objective
        return {
            'id': objective_id,
            'title': f"Grade-appropriate {objective_id}",
            'description': f"Learning objective adapted for {grade.value}",
            'grade_level': grade.value,
            'difficulty_base': 1.0
        }
    
    def _adapt_objective_for_readiness(self, objective: Dict[str, Any], readiness_check: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt objective based on readiness level"""
        adapted = objective.copy()
        readiness = readiness_check.get('overall_readiness', 'approaching')
        
        if readiness == 'advanced':
            adapted['difficulty_modifier'] = 1.3
            adapted['enrichment_activities'] = True
        elif readiness == 'ready':
            adapted['difficulty_modifier'] = 1.0
        elif readiness == 'approaching':
            adapted['difficulty_modifier'] = 0.8
            adapted['additional_scaffolding'] = True
        else:  # not_ready
            adapted['difficulty_modifier'] = 0.6
            adapted['intensive_support'] = True
        
        return adapted
    
    def _create_grade_appropriate_alternative(self, objective_id: str, grade: GradeLevel) -> Dict[str, Any]:
        """Create grade-appropriate alternative objective"""
        return {
            'id': f"alt_{objective_id}_{grade.value}",
            'title': f"Alternative {objective_id} for {grade.value}",
            'description': f"Grade-appropriate alternative learning objective",
            'grade_level': grade.value,
            'difficulty_base': 1.0,
            'alternative_objective': True
        }
    
    def _calculate_difficulty_level(self, grade: GradeLevel, readiness: str) -> float:
        """Calculate appropriate difficulty level"""
        base_difficulty = {
            GradeLevel.KINDERGARTEN: 1.0,
            GradeLevel.FIRST_GRADE: 1.4,
            GradeLevel.SECOND_GRADE: 1.8,
            GradeLevel.THIRD_GRADE: 2.3
        }.get(grade, 1.0)
        
        readiness_modifier = {
            'not_ready': 0.7,
            'approaching': 0.85,
            'ready': 1.0,
            'advanced': 1.2
        }.get(readiness, 1.0)
        
        return base_difficulty * readiness_modifier
    
    def _get_vocabulary_level(self, grade: GradeLevel) -> int:
        """Get vocabulary level for grade"""
        return {
            GradeLevel.KINDERGARTEN: 300,
            GradeLevel.FIRST_GRADE: 500,
            GradeLevel.SECOND_GRADE: 800,
            GradeLevel.THIRD_GRADE: 1200
        }.get(grade, 300)
    
    def _get_complexity_indicators(self, grade: GradeLevel) -> List[str]:
        """Get complexity indicators for grade"""
        return {
            GradeLevel.KINDERGARTEN: ["Simple sentences", "Familiar vocabulary", "Concrete concepts"],
            GradeLevel.FIRST_GRADE: ["Compound sentences", "Academic vocabulary", "Some abstraction"],
            GradeLevel.SECOND_GRADE: ["Complex sentences", "Subject-specific terms", "Abstract thinking"],
            GradeLevel.THIRD_GRADE: ["Multi-paragraph structure", "Advanced vocabulary", "Complex relationships"]
        }.get(grade, ["Basic level content"])
    
    def _determine_scaffolding_level(self, readiness: str) -> str:
        """Determine scaffolding level needed"""
        return {
            'not_ready': 'intensive',
            'approaching': 'moderate',
            'ready': 'minimal',
            'advanced': 'independent'
        }.get(readiness, 'moderate')
    
    def _apply_difficulty_scaling(self, objective: Dict[str, Any], scaled_content: Dict[str, Any]) -> Dict[str, Any]:
        """Apply difficulty scaling to objective"""
        base_difficulty = objective.get('difficulty_base', 1.0)
        difficulty_modifier = objective.get('difficulty_modifier', 1.0)
        content_difficulty = scaled_content.get('difficulty_level', 1.0)
        
        return {
            'final_difficulty': base_difficulty * difficulty_modifier * content_difficulty,
            'vocabulary_requirement': scaled_content.get('vocabulary_level', 300),
            'scaffolding_needed': scaled_content.get('scaffolding_level', 'moderate'),
            'complexity_features': scaled_content.get('complexity_indicators', [])
        }
    
    def _process_grade_aware_objective(self, objective: Dict[str, Any], scaled_content: Dict[str, Any]) -> Dict[str, Any]:
        """Process objective with grade-aware adaptations"""
        # Simulate processing (in real implementation, this would execute actual learning activities)
        difficulty = objective.get('scaled_difficulty', {}).get('final_difficulty', 1.0)
        
        # Simulate success based on difficulty and other factors
        success_probability = max(0.1, min(0.95, 1.0 - (difficulty - 1.0) * 0.3))
        success = success_probability > 0.5
        
        return {
            'objective_id': objective.get('id'),
            'attempted': True,
            'completed': success,
            'success': success,
            'performance_score': success_probability,
            'difficulty_attempted': difficulty,
            'grade_appropriate': True
        }
    
    def _calculate_engagement_level(self, objective_results: List[Dict[str, Any]]) -> float:
        """Calculate engagement level from objective results"""
        if not objective_results:
            return 0.5
        
        # Simulate engagement calculation
        performance_scores = [result.get('performance_score', 0.5) for result in objective_results]
        return sum(performance_scores) / len(performance_scores)
    
    def _assess_grade_appropriate_performance(self, objective_results: List[Dict[str, Any]], 
                                            scaled_content: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how well performance matches grade expectations"""
        expected_performance = 0.75  # 75% success rate expected
        actual_performance = sum(result.get('success', False) for result in objective_results) / len(objective_results)
        
        return {
            'expected_performance': expected_performance,
            'actual_performance': actual_performance,
            'meets_grade_expectations': actual_performance >= expected_performance * 0.8,
            'performance_gap': expected_performance - actual_performance
        }
    
    def _analyze_session_performance(self, session_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze session performance for advancement indicators"""
        return {
            'success_rate': session_results.get('success_rate', 0.0),
            'engagement_level': session_results.get('engagement_level', 0.0),
            'objectives_completed': session_results.get('objectives_completed', 0),
            'grade_appropriate_performance': session_results.get('grade_appropriate_performance', {}),
            'performance_trend': 'improving'  # Would be calculated from historical data
        }
    
    def _check_accumulated_progress(self) -> Dict[str, Any]:
        """Check accumulated progress over time"""
        return {
            'total_sessions': 45,  # Would query from database
            'average_success_rate': 0.82,
            'mastery_growth': 0.15,  # 15% growth over time period
            'engagement_trend': 'stable',
            'time_in_current_grade': 120  # days
        }
    
    def _identify_advancement_indicators(self, performance_analysis: Dict[str, Any], 
                                       accumulated_progress: Dict[str, Any]) -> Dict[str, Any]:
        """Identify indicators for grade advancement readiness"""
        indicators = {
            'high_success_rate': performance_analysis.get('success_rate', 0) >= 0.85,
            'consistent_mastery': accumulated_progress.get('average_success_rate', 0) >= 0.8,
            'sufficient_time_in_grade': accumulated_progress.get('time_in_current_grade', 0) >= 90,
            'positive_engagement': performance_analysis.get('engagement_level', 0) >= 0.7,
            'grade_appropriate_performance': performance_analysis.get('grade_appropriate_performance', {}).get('meets_grade_expectations', False)
        }
        
        indicators['total_indicators_met'] = sum(indicators.values())
        indicators['advancement_threshold_met'] = indicators['total_indicators_met'] >= 4
        
        return indicators
    
    def _make_advancement_recommendation(self, advancement_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Make recommendation for grade advancement"""
        indicators_met = advancement_indicators.get('total_indicators_met', 0)
        threshold_met = advancement_indicators.get('advancement_threshold_met', False)
        
        if threshold_met:
            return {
                'should_advance': True,
                'confidence_level': 'high',
                'recommendation': 'Recommend comprehensive grade readiness assessment',
                'next_steps': ['Conduct full assessment', 'Review with specialists', 'Plan transition']
            }
        elif indicators_met >= 3:
            return {
                'should_advance': False,
                'approaching_readiness': True,
                'confidence_level': 'moderate',
                'recommendation': 'Continue monitoring, approaching readiness',
                'next_steps': ['Continue current curriculum', 'Monitor progress closely', 'Reassess in 2 weeks']
            }
        else:
            return {
                'should_advance': False,
                'approaching_readiness': False,
                'confidence_level': 'low',
                'recommendation': 'Continue grade-level instruction with support',
                'next_steps': ['Focus on skill building', 'Provide additional support', 'Reassess in 1 month']
            }
    
    def _calculate_integration_efficiency(self) -> float:
        """Calculate efficiency of integration process"""
        session = self.current_integration_session
        adaptations_per_check = session['adaptations_made'] / max(1, session['grade_checks_performed'])
        return min(1.0, adaptations_per_check / 3.0)  # Target 3 adaptations per check
    
    def _get_grade_entry_date(self) -> str:
        """Get date when student entered current grade"""
        # Implementation would query database
        return (date.today() - timedelta(days=120)).isoformat()
    
    def _get_next_assessment_date(self) -> str:
        """Get next scheduled assessment date"""
        return (date.today() + timedelta(days=30)).isoformat()
    
    def _get_progression_history(self) -> List[Dict[str, Any]]:
        """Get grade progression history"""
        # Implementation would query database
        return []  # Empty for demo

# Factory function for easy integration
def create_grade_progression_integration() -> GradeProgressionIntegration:
    """Create and initialize the grade progression integration system"""
    return GradeProgressionIntegration()

# Demo function
def demo_grade_progression_integration():
    """Demonstrate the grade progression integration system"""
    print("🎓 Grade Progression Integration Demo")
    print("=" * 50)
    
    # Create integration system
    integration = create_grade_progression_integration()
    
    # Run enhanced daily learning session
    print("\n📚 Running Enhanced Daily Learning Session...")
    session_report = integration.enhanced_daily_learning_session()
    
    # Display key results
    print(f"\n📊 Session Results:")
    print(f"Session ID: {session_report['session_id']}")
    
    readiness_check = session_report['grade_readiness_check']
    print(f"Grade Readiness: {readiness_check.get('overall_readiness', 'N/A')}")
    print(f"Current Grade: {readiness_check.get('current_grade', 'N/A')}")
    
    session_results = session_report['session_results']
    print(f"Success Rate: {session_results.get('success_rate', 0):.1%}")
    print(f"Objectives Completed: {session_results.get('objectives_completed', 0)}")
    print(f"Engagement Level: {session_results.get('engagement_level', 0):.1%}")
    
    progression_assessment = session_report['progression_assessment']
    advancement_rec = progression_assessment.get('advancement_recommendation', {})
    print(f"Advancement Ready: {advancement_rec.get('should_advance', False)}")
    
    # Show next session recommendations
    recommendations = session_report['next_session_recommendations']
    if recommendations:
        print(f"\n💡 Next Session Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"  {i}. {rec}")
    
    # Show integration metrics
    metrics = session_report['integration_metrics']
    print(f"\n⚙️  Integration Metrics:")
    print(f"Session Duration: {metrics.get('session_duration_minutes', 0):.1f} minutes")
    print(f"Grade Checks: {metrics.get('grade_checks_performed', 0)}")
    print(f"Adaptations Made: {metrics.get('adaptations_made', 0)}")
    print(f"Integration Efficiency: {metrics.get('integration_efficiency', 0):.1%}")
    
    print("\n✅ Grade Progression Integration Demo Complete!")

if __name__ == "__main__":
    demo_grade_progression_integration()
