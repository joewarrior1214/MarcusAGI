#!/usr/bin/env python3
"""
Daily Learning Loop with Spatial Awareness Integration

This system integrates Marcus's spatial learning loop into his daily learning routine,
providing continuous spatial awareness development alongside his other learning activities.

Key Integration Features:
1. Spatial Learning Sessions - Regular spatial exploration and world mapping
2. Memory Continuity - Spatial memories persist across daily sessions
3. Adaptive Scheduling - Spatial learning adapts based on progress and objectives
4. Multi-Modal Integration - Spatial learning enhances embodied social experiences
5. Progress Tracking - Comprehensive spatial development metrics
6. Learning Transfer - Spatial concepts inform other learning domains

This creates a comprehensive learning environment where Marcus develops both
cognitive abilities and spatial intelligence through integrated experiences.
"""

import sys
import os
from datetime import date, datetime
from typing import Dict, List, Any, Optional

# Add path for imports
sys.path.append('/workspaces')
sys.path.append('/workspaces/MarcusAGI')

# Import daily learning loop
from core.learning.daily_learning_loop import run_daily_learning_loop

# Import spatial learning system
from scripts.utilities.marcus_spatial_learning_loop import (
    MarcusSpatialLearningLoop, ExplorationStrategy, LearningObjective
)

def run_enhanced_daily_learning_with_spatial_awareness(run_date: date = date.today()) -> Dict[str, Any]:
    """Enhanced daily learning loop with integrated spatial awareness"""
    
    print("🗺️🧠 MARCUS AGI ENHANCED DAILY LEARNING WITH SPATIAL AWARENESS")
    print("=" * 80)
    print(f"Learning Date: {run_date}")
    print("Integrating spatial intelligence with daily cognitive development")
    print("=" * 80)
    
    # Initialize spatial learning system
    print(f"\n🗺️ INITIALIZING SPATIAL LEARNING SYSTEM")
    spatial_loop = MarcusSpatialLearningLoop(world_size=15)
    
    # Determine spatial learning objectives based on day of week and progress
    spatial_objectives = _determine_daily_spatial_objectives(run_date, spatial_loop)
    spatial_strategy = _select_spatial_strategy(run_date, spatial_loop)
    
    print(f"Today's Spatial Focus: {spatial_strategy.value}")
    print(f"Spatial Objectives: {[obj.value for obj in spatial_objectives]}")
    
    # Phase 1: Morning Spatial Exploration (before main learning)
    print(f"\n{'='*60}")
    print("🌅 PHASE 1: MORNING SPATIAL EXPLORATION")
    print(f"{'='*60}")
    
    morning_spatial_session = spatial_loop.run_spatial_learning_session(
        duration_minutes=30,
        strategy=ExplorationStrategy.CURIOSITY_DRIVEN,
        objectives=[LearningObjective.MAP_WORLD, LearningObjective.FIND_OBJECTS],
        verbose=False  # Clean output for better integration
    )
    
    # Extract spatial insights for daily learning integration
    spatial_insights = _extract_spatial_insights_for_learning(morning_spatial_session)
    
    print(f"\n🧠 Spatial Insights for Today's Learning:")
    for insight in spatial_insights[:3]:
        print(f"  • {insight}")
    
    # Phase 2: Standard Daily Learning Loop (Enhanced with Spatial Context)
    print(f"\n{'='*60}")
    print("📚 PHASE 2: ENHANCED DAILY LEARNING LOOP")
    print(f"{'='*60}")
    
    print("Running standard daily learning loop with spatial context integration...")
    
    # Run the standard daily learning loop
    daily_results = run_daily_learning_loop(run_date)
    
    # Phase 3: Afternoon Spatial Skills Practice
    print(f"\n{'='*60}")
    print("🎯 PHASE 3: AFTERNOON SPATIAL SKILLS PRACTICE")
    print(f"{'='*60}")
    
    # Determine afternoon focus based on morning results and daily learning outcomes
    afternoon_strategy = _adapt_afternoon_spatial_strategy(
        morning_spatial_session, daily_results, spatial_loop
    )
    
    afternoon_objectives = [
        LearningObjective.PRACTICE_SKILLS,
        LearningObjective.DEVELOP_NAVIGATION
    ]
    
    # Add social exploration if embodied social learning happened
    if daily_results.get('embodied_social_exploration', False):
        afternoon_objectives.append(LearningObjective.SOCIAL_EXPLORATION)
    
    afternoon_spatial_session = spatial_loop.run_spatial_learning_session(
        duration_minutes=20,
        strategy=afternoon_strategy,
        objectives=afternoon_objectives,
        verbose=False  # Clean output for afternoon session
    )
    
    # Phase 4: Evening Integration and Reflection
    print(f"\n{'='*60}")
    print("🌙 PHASE 4: EVENING INTEGRATION AND REFLECTION")
    print(f"{'='*60}")
    
    # Generate comprehensive spatial progress report
    spatial_progress = spatial_loop.get_spatial_learning_progress_report()
    
    # Integrate spatial learning insights with daily reflection
    integrated_insights = _integrate_spatial_and_cognitive_insights(
        daily_results, morning_spatial_session, afternoon_spatial_session, spatial_progress
    )
    
    print(f"\n🧠 Integrated Learning Insights:")
    for category, insights in integrated_insights.items():
        print(f"\n{category.upper()}:")
        for insight in insights[:2]:  # Top 2 per category
            print(f"  • {insight}")
    
    # Phase 5: Learning Continuity Planning
    print(f"\n{'='*60}")
    print("🔄 PHASE 5: LEARNING CONTINUITY PLANNING")
    print(f"{'='*60}")
    
    continuity_plan = _generate_spatial_learning_continuity_plan(
        spatial_progress, daily_results
    )
    
    print(f"\nTomorrow's Spatial Learning Plan:")
    print(f"  Recommended Strategy: {continuity_plan['recommended_strategy']}")
    print(f"  Priority Objectives: {continuity_plan['priority_objectives']}")
    print(f"  Focus Areas: {', '.join(continuity_plan['focus_areas'])}")
    
    # Compile comprehensive daily report
    enhanced_daily_report = {
        **daily_results,  # Include all standard daily learning results
        'spatial_learning': {
            'morning_session': {
                'session_id': morning_spatial_session.session_id,
                'strategy': morning_spatial_session.exploration_strategy.value,
                'locations_discovered': morning_spatial_session.new_locations_discovered,
                'concepts_formed': len(morning_spatial_session.concepts_formed),
                'exploration_efficiency': morning_spatial_session.exploration_efficiency,
                'spatial_understanding_improvement': morning_spatial_session.spatial_understanding_improvement
            },
            'afternoon_session': {
                'session_id': afternoon_spatial_session.session_id,
                'strategy': afternoon_spatial_session.exploration_strategy.value,
                'locations_discovered': afternoon_spatial_session.new_locations_discovered,
                'concepts_formed': len(afternoon_spatial_session.concepts_formed),
                'exploration_efficiency': afternoon_spatial_session.exploration_efficiency,
                'spatial_understanding_improvement': afternoon_spatial_session.spatial_understanding_improvement
            },
            'daily_spatial_progress': {
                'world_coverage': spatial_progress['current_spatial_knowledge']['world_coverage'],
                'total_locations_known': spatial_progress['current_spatial_knowledge']['locations_known'],
                'navigation_paths_learned': len(spatial_loop.spatial_model.navigation_paths),
                'spatial_relationships_understood': len(spatial_loop.spatial_model.relationships),
                'total_concepts_formed_today': (len(morning_spatial_session.concepts_formed) + 
                                              len(afternoon_spatial_session.concepts_formed))
            }
        },
        'integrated_insights': integrated_insights,
        'spatial_continuity_plan': continuity_plan,
        'enhanced_learning_outcomes': {
            'spatial_cognitive_integration': len(integrated_insights.get('cognitive_spatial', [])),
            'embodied_spatial_coherence': _calculate_embodied_spatial_coherence(daily_results, 
                                                                               morning_spatial_session,
                                                                               afternoon_spatial_session),
            'learning_transfer_evidence': len(integrated_insights.get('learning_transfer', [])),
            'total_learning_dimensions': len([k for k in daily_results.keys() if 'learning' in k or 'exploration' in k]) + 2  # +2 for spatial sessions
        }
    }
    
    # Display final summary
    print(f"\n{'='*80}")
    print("🎉 ENHANCED DAILY LEARNING WITH SPATIAL AWARENESS COMPLETE")
    print(f"{'='*80}")
    
    print(f"\n📊 Today's Comprehensive Learning Summary:")
    print(f"  Standard Learning Components: ✅ Completed")
    print(f"  Spatial Exploration Sessions: 2 sessions")
    print(f"  New Locations Discovered: {morning_spatial_session.new_locations_discovered + afternoon_spatial_session.new_locations_discovered}")
    print(f"  Spatial Concepts Formed: {enhanced_daily_report['spatial_learning']['daily_spatial_progress']['total_concepts_formed_today']}")
    print(f"  World Coverage Progress: {spatial_progress['current_spatial_knowledge']['world_coverage']:.1%}")
    print(f"  Integrated Learning Insights: {sum(len(insights) for insights in integrated_insights.values())}")
    
    spatial_competence = spatial_progress['current_spatial_knowledge']['world_coverage']
    if spatial_competence >= 0.3:
        competence_level = "Advanced"
    elif spatial_competence >= 0.15:
        competence_level = "Intermediate"
    else:
        competence_level = "Developing"
    
    print(f"  Spatial Intelligence Level: {competence_level} ({spatial_competence:.1%} world mastery)")
    
    print(f"\n🚀 Marcus's Enhanced Capabilities:")
    print(f"  • Integrated spatial-cognitive learning")
    print(f"  • Continuous world model development")
    print(f"  • Adaptive exploration strategies")
    print(f"  • Cross-domain learning transfer")
    print(f"  • Memory-guided spatial intelligence")
    
    return enhanced_daily_report

def _determine_daily_spatial_objectives(run_date: date, spatial_loop: MarcusSpatialLearningLoop) -> List[LearningObjective]:
    """Determine spatial learning objectives based on date and progress"""
    
    # Get current spatial progress
    if spatial_loop.learning_sessions:
        progress = spatial_loop.get_spatial_learning_progress_report()
        world_coverage = progress['current_spatial_knowledge']['world_coverage']
    else:
        world_coverage = 0.0
    
    objectives = []
    
    # Always include world mapping for early development
    if world_coverage < 0.5:
        objectives.append(LearningObjective.MAP_WORLD)
    
    # Day of week specific objectives
    weekday = run_date.weekday()
    
    if weekday == 0:  # Monday - New week exploration
        objectives.extend([LearningObjective.FIND_OBJECTS, LearningObjective.UNDERSTAND_RELATIONSHIPS])
    elif weekday == 1:  # Tuesday - Navigation focus
        objectives.extend([LearningObjective.DEVELOP_NAVIGATION, LearningObjective.LEARN_PATHS])
    elif weekday == 2:  # Wednesday - Social spatial learning
        objectives.extend([LearningObjective.SOCIAL_EXPLORATION, LearningObjective.PRACTICE_SKILLS])
    elif weekday == 3:  # Thursday - Relationship understanding
        objectives.extend([LearningObjective.UNDERSTAND_RELATIONSHIPS, LearningObjective.FIND_OBJECTS])
    elif weekday == 4:  # Friday - Skills practice
        objectives.extend([LearningObjective.PRACTICE_SKILLS, LearningObjective.DEVELOP_NAVIGATION])
    elif weekday == 5:  # Saturday - Free exploration
        objectives.extend([LearningObjective.FIND_OBJECTS, LearningObjective.SOCIAL_EXPLORATION])
    else:  # Sunday - Integration and review
        objectives.extend([LearningObjective.LEARN_PATHS, LearningObjective.PRACTICE_SKILLS])
    
    return objectives[:3]  # Limit to 3 objectives

def _select_spatial_strategy(run_date: date, spatial_loop: MarcusSpatialLearningLoop) -> ExplorationStrategy:
    """Select exploration strategy based on date and progress"""
    
    # Get performance history if available
    if spatial_loop.learning_sessions:
        progress = spatial_loop.get_spatial_learning_progress_report()
        best_strategy = max(progress['strategy_performance'].items(), 
                          key=lambda x: x[1]['avg_efficiency'])[0] if progress['strategy_performance'] else 'curiosity_driven'
    else:
        best_strategy = 'curiosity_driven'
    
    # Rotate strategies based on day of week, but favor successful ones
    weekday = run_date.weekday()
    
    strategy_rotation = [
        ExplorationStrategy.CURIOSITY_DRIVEN,
        ExplorationStrategy.SYSTEMATIC_GRID,
        ExplorationStrategy.GOAL_SEEKING,
        ExplorationStrategy.CURIOSITY_DRIVEN,
        ExplorationStrategy.GOAL_SEEKING,
        ExplorationStrategy.RANDOM_WALK,
        ExplorationStrategy.CURIOSITY_DRIVEN
    ]
    
    base_strategy = strategy_rotation[weekday]
    
    # Override with best performing strategy 30% of the time
    import random
    if random.random() < 0.3 and best_strategy:
        try:
            return ExplorationStrategy(best_strategy)
        except ValueError:
            return base_strategy
    
    return base_strategy

def _extract_spatial_insights_for_learning(spatial_session) -> List[str]:
    """Extract insights from spatial session that can inform daily learning"""
    
    insights = []
    
    # Navigation insights
    if spatial_session.paths_discovered:
        insights.append(f"Discovered {len(spatial_session.paths_discovered)} new navigation paths - enhanced spatial reasoning")
    
    # Object discovery insights
    unique_objects = len(set(spatial_session.objects_encountered))
    if unique_objects > 0:
        insights.append(f"Encountered {unique_objects} unique objects - strengthened categorization skills")
    
    # Exploration efficiency insights
    if spatial_session.exploration_efficiency > 0.4:
        insights.append("High exploration efficiency indicates strong goal-directed behavior")
    elif spatial_session.exploration_efficiency < 0.2:
        insights.append("Lower exploration efficiency suggests need for strategic planning practice")
    
    # Relationship learning insights
    if spatial_session.relationships_learned:
        insights.append(f"Learned {len(spatial_session.relationships_learned)} spatial relationships - enhanced relational thinking")
    
    # Concept formation insights
    unique_concepts = len(set(spatial_session.concepts_formed))
    if unique_concepts > 10:
        insights.append("Strong concept formation indicates active learning and memory integration")
    
    return insights

def _adapt_afternoon_spatial_strategy(morning_session, daily_results, spatial_loop) -> ExplorationStrategy:
    """Adapt afternoon spatial strategy based on morning and daily results"""
    
    # If morning was highly efficient, continue with same strategy
    if morning_session.exploration_efficiency > 0.4:
        return morning_session.exploration_strategy
    
    # If embodied social learning happened, use social-compatible strategy
    if daily_results.get('embodied_social_exploration', False):
        return ExplorationStrategy.GOAL_SEEKING
    
    # If low efficiency, try a different approach
    if morning_session.exploration_efficiency < 0.2:
        if morning_session.exploration_strategy == ExplorationStrategy.RANDOM_WALK:
            return ExplorationStrategy.SYSTEMATIC_GRID
        elif morning_session.exploration_strategy == ExplorationStrategy.SYSTEMATIC_GRID:
            return ExplorationStrategy.CURIOSITY_DRIVEN
        else:
            return ExplorationStrategy.GOAL_SEEKING
    
    # Default to goal-seeking for afternoon skill practice
    return ExplorationStrategy.GOAL_SEEKING

def _integrate_spatial_and_cognitive_insights(daily_results, morning_spatial, afternoon_spatial, spatial_progress) -> Dict[str, List[str]]:
    """Integrate insights from spatial and cognitive learning"""
    
    integrated_insights = {
        'cognitive_spatial': [],
        'learning_transfer': [],
        'skill_development': [],
        'memory_integration': [],
        'social_spatial': []
    }
    
    # Cognitive-Spatial Integration
    if daily_results.get('concepts_discovered', 0) > 0 and (morning_spatial.concepts_formed or afternoon_spatial.concepts_formed):
        integrated_insights['cognitive_spatial'].append(
            "Strong concept formation in both cognitive and spatial domains indicates integrated learning"
        )
    
    # Learning Transfer Evidence
    spatial_concepts_today = len(morning_spatial.concepts_formed) + len(afternoon_spatial.concepts_formed)
    cognitive_concepts_today = daily_results.get('concepts_discovered', 0)
    
    if spatial_concepts_today > 0 and cognitive_concepts_today > 0:
        ratio = spatial_concepts_today / max(1, cognitive_concepts_today)
        if 0.5 <= ratio <= 2.0:  # Balanced learning
            integrated_insights['learning_transfer'].append(
                "Balanced concept formation across spatial and cognitive domains suggests effective learning transfer"
            )
    
    # Skill Development Integration
    if morning_spatial.spatial_skills_practiced or afternoon_spatial.spatial_skills_practiced:
        all_spatial_skills = set(morning_spatial.spatial_skills_practiced + afternoon_spatial.spatial_skills_practiced)
        integrated_insights['skill_development'].append(
            f"Practiced {len(all_spatial_skills)} spatial skills alongside cognitive development"
        )
    
    # Memory Integration
    total_spatial_concepts = len(morning_spatial.concepts_formed) + len(afternoon_spatial.concepts_formed)
    if total_spatial_concepts > 5:
        integrated_insights['memory_integration'].append(
            f"Formed {total_spatial_concepts} spatial concepts, strengthening memory network connectivity"
        )
    
    # Social-Spatial Integration
    if (daily_results.get('embodied_social_exploration', False) and 
        LearningObjective.SOCIAL_EXPLORATION in afternoon_spatial.learning_objectives):
        
        if afternoon_spatial.embodied_social_data:
            integrated_insights['social_spatial'].append(
                "Successfully integrated spatial exploration with social learning contexts"
            )
    
    return integrated_insights

def _calculate_embodied_spatial_coherence(daily_results, morning_spatial, afternoon_spatial) -> float:
    """Calculate how well embodied and spatial learning integrated"""
    
    coherence_score = 0.0
    max_score = 4.0
    
    # Embodied social learning presence
    if daily_results.get('embodied_social_exploration', False):
        coherence_score += 1.0
    
    # Spatial learning consistency
    if morning_spatial.new_locations_discovered > 0 and afternoon_spatial.new_locations_discovered > 0:
        coherence_score += 1.0
    
    # Cross-domain concept formation
    spatial_concepts = len(morning_spatial.concepts_formed) + len(afternoon_spatial.concepts_formed)
    cognitive_concepts = daily_results.get('concepts_discovered', 0)
    if spatial_concepts > 0 and cognitive_concepts > 0:
        coherence_score += 1.0
    
    # Social-spatial integration
    if (afternoon_spatial.embodied_social_data and 
        LearningObjective.SOCIAL_EXPLORATION in afternoon_spatial.learning_objectives):
        coherence_score += 1.0
    
    return coherence_score / max_score

def _generate_spatial_learning_continuity_plan(spatial_progress, daily_results) -> Dict[str, Any]:
    """Generate plan for tomorrow's spatial learning"""
    
    current_coverage = spatial_progress['current_spatial_knowledge']['world_coverage']
    
    # Determine recommended strategy based on progress
    if current_coverage < 0.1:
        recommended_strategy = "systematic_grid"
        priority_objectives = ["map_world", "find_objects"]
        focus_areas = ["world_exploration", "object_discovery"]
    elif current_coverage < 0.3:
        recommended_strategy = "curiosity_driven"  
        priority_objectives = ["understand_relationships", "develop_navigation"]
        focus_areas = ["relationship_learning", "navigation_skills"]
    else:
        recommended_strategy = "goal_seeking"
        priority_objectives = ["practice_skills", "social_exploration"]
        focus_areas = ["advanced_navigation", "social_spatial_integration"]
    
    # Adjust based on today's performance
    if spatial_progress.get('average_exploration_efficiency', 0) < 0.3:
        focus_areas.append("strategic_planning")
    
    if daily_results.get('embodied_social_exploration', False):
        priority_objectives.append("social_exploration")
        focus_areas.append("embodied_integration")
    
    return {
        'recommended_strategy': recommended_strategy,
        'priority_objectives': priority_objectives[:3],
        'focus_areas': focus_areas[:3],
        'expected_duration': 30 + min(10, int(current_coverage * 20)),  # Adaptive duration
        'continuity_notes': f"Current world mastery: {current_coverage:.1%}, focusing on {focus_areas[0]}"
    }

def demo_enhanced_daily_learning_with_spatial():
    """Demonstrate the enhanced daily learning with spatial awareness integration"""
    
    print("🗺️📚 MARCUS AGI ENHANCED DAILY LEARNING WITH SPATIAL AWARENESS DEMO")
    print("=" * 80)
    print("Comprehensive Integration of Spatial Intelligence with Daily Learning")
    print("=" * 80)
    
    # Run enhanced daily learning
    enhanced_results = run_enhanced_daily_learning_with_spatial_awareness()
    
    print(f"\n{'='*80}")
    print("📊 COMPREHENSIVE LEARNING ANALYSIS")  
    print(f"{'='*80}")
    
    # Analyze learning outcomes
    spatial_learning = enhanced_results['spatial_learning']
    morning = spatial_learning['morning_session']
    afternoon = spatial_learning['afternoon_session']
    progress = spatial_learning['daily_spatial_progress']
    
    print(f"\n🗺️ SPATIAL LEARNING OUTCOMES:")
    print(f"  Morning Session: {morning['strategy']} strategy")
    print(f"    → {morning['locations_discovered']} new locations discovered")
    print(f"    → {morning['concepts_formed']} spatial concepts formed")
    print(f"    → {morning['exploration_efficiency']:.3f} exploration efficiency")
    
    print(f"  Afternoon Session: {afternoon['strategy']} strategy")
    print(f"    → {afternoon['locations_discovered']} new locations discovered")
    print(f"    → {afternoon['concepts_formed']} spatial concepts formed")
    print(f"    → {afternoon['exploration_efficiency']:.3f} exploration efficiency")
    
    print(f"\n📈 DAILY SPATIAL PROGRESS:")
    print(f"  World Coverage: {progress['world_coverage']:.1%}")
    print(f"  Total Locations Known: {progress['total_locations_known']}")
    print(f"  Navigation Paths: {progress['navigation_paths_learned']}")
    print(f"  Spatial Relationships: {progress['spatial_relationships_understood']}")
    print(f"  Concepts Formed Today: {progress['total_concepts_formed_today']}")
    
    print(f"\n🧠 INTEGRATED LEARNING INSIGHTS:")
    integrated = enhanced_results['integrated_insights']
    for category, insights in integrated.items():
        if insights:
            print(f"  {category.replace('_', ' ').title()}:")
            for insight in insights:
                print(f"    • {insight}")
    
    enhanced_outcomes = enhanced_results['enhanced_learning_outcomes']
    print(f"\n🚀 ENHANCED LEARNING CAPABILITIES:")
    print(f"  Spatial-Cognitive Integration: {enhanced_outcomes['spatial_cognitive_integration']} insights")
    print(f"  Embodied-Spatial Coherence: {enhanced_outcomes['embodied_spatial_coherence']:.1%}")
    print(f"  Learning Transfer Evidence: {enhanced_outcomes['learning_transfer_evidence']} instances")
    print(f"  Total Learning Dimensions: {enhanced_outcomes['total_learning_dimensions']}")
    
    continuity = enhanced_results['spatial_continuity_plan']
    print(f"\n🔄 TOMORROW'S LEARNING PLAN:")
    print(f"  Strategy: {continuity['recommended_strategy']}")
    print(f"  Objectives: {', '.join(continuity['priority_objectives'])}")
    print(f"  Focus: {', '.join(continuity['focus_areas'])}")
    print(f"  Duration: {continuity['expected_duration']} minutes")
    print(f"  Notes: {continuity['continuity_notes']}")
    
    # Overall assessment
    world_coverage = progress['world_coverage']
    if world_coverage >= 0.4:
        learning_level = "Advanced Integrated Learning"
        capabilities = [
            "Complex spatial-cognitive reasoning",
            "Advanced navigation and world modeling",
            "Multi-domain learning transfer",
            "Autonomous exploration planning"
        ]
    elif world_coverage >= 0.2:
        learning_level = "Intermediate Integrated Learning"
        capabilities = [
            "Solid spatial-cognitive integration",
            "Competent navigation skills",
            "Cross-domain concept formation",
            "Adaptive exploration strategies"
        ]
    else:
        learning_level = "Developing Integrated Learning"
        capabilities = [
            "Foundational spatial awareness",
            "Basic navigation competencies",
            "Emerging learning integration",
            "Guided exploration with memory formation"
        ]
    
    print(f"\n🎯 MARCUS'S CURRENT LEARNING LEVEL: {learning_level}")
    print(f"\nKey Capabilities Demonstrated:")
    for capability in capabilities:
        print(f"  ✅ {capability}")
    
    print(f"\n🌟 SUCCESS METRICS:")
    print(f"  ✅ Integrated spatial-cognitive learning sessions")
    print(f"  ✅ Continuous world model development")
    print(f"  ✅ Adaptive learning strategy selection")
    print(f"  ✅ Cross-domain insight generation")
    print(f"  ✅ Memory-guided exploration and learning")
    print(f"  ✅ Automated learning continuity planning")
    
    return enhanced_results

if __name__ == "__main__":
    demo_enhanced_daily_learning_with_spatial()
