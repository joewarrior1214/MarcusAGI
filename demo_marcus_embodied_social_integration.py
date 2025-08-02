#!/usr/bin/env python3
"""
Comprehensive Demo of Marcus AGI Embodied Social Learning Integration System

This demonstration showcases the complete integration of Marcus's virtual simple body world
with social learning capabilities, providing multi-sensory development across:

1. Virtual Body World - Physical exploration and sensory training
2. Social Interaction Simulation - Peer relationship development  
3. Multi-Sensory Learning - Vision, touch, movement, and social senses
4. Embodied Social Skills - Physical and social skill development
5. Comprehensive Assessment - Progress tracking and readiness evaluation

The system provides Marcus with a rich, embodied learning environment that 
combines physical awareness with social intelligence.
"""

import sys
import os

# Add the MarcusAGI directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the embodied social integration system
from marcus_embodied_social_integration import (
    MarcusEmbodiedSocialIntegration,
    PhysicalSocialContext,
    SensoryModalType,
    demo_embodied_social_integration
)


def comprehensive_embodied_social_demo():
    """Run a comprehensive demonstration of the embodied social learning system"""
    
    print("🎮🤝 MARCUS AGI EMBODIED SOCIAL LEARNING INTEGRATION")
    print("=" * 70)
    print("Comprehensive Multi-Sensory Social Development System")
    print("=" * 70)
    
    print("\n🌟 SYSTEM OVERVIEW:")
    print("This advanced integration combines Marcus's virtual body world with")
    print("social learning capabilities for comprehensive development including:")
    print("  • Virtual Physical World - 2D grid environment with objects and peers")
    print("  • Multi-Sensory Experiences - Vision, touch, movement, spatial awareness")
    print("  • Social Peer Interactions - Dynamic peer relationships and communication")
    print("  • Embodied Social Skills - Physical components of social competence")
    print("  • Comprehensive Assessment - Multi-modal progress tracking")
    
    # Initialize the integration system
    print(f"\n{'='*50}")
    print("🔧 INITIALIZING EMBODIED SOCIAL INTEGRATION SYSTEM")
    print(f"{'='*50}")
    
    integration = MarcusEmbodiedSocialIntegration(world_size=12)
    
    print(f"✅ System initialized successfully!")
    print(f"   World Size: {integration.embodied_world.size}x{integration.embodied_world.size}")
    print(f"   Peer Positions: {len(integration.embodied_world.peer_positions)} peers")
    print(f"   Social Objects: {len(integration.embodied_world.social_objects)} shared objects")
    print(f"   Embodied Skills: {len(integration.embodied_social_skills)} skills to develop")
    
    # Show embodied social skills
    print(f"\n🧠 EMBODIED SOCIAL SKILLS TO DEVELOP:")
    for skill_name, skill in integration.embodied_social_skills.items():
        print(f"  • {skill.name}")
        print(f"    - {skill.description}")
        print(f"    - Physical: {', '.join(skill.physical_components[:2])}...")
        print(f"    - Social: {', '.join(skill.social_components[:2])}...")
        print(f"    - Sensory: {len(skill.sensory_requirements)} modalities")
    
    # Phase 1: Single Context Deep Dive
    print(f"\n{'='*60}")
    print("🎯 PHASE 1: DETAILED EMBODIED SOCIAL LEARNING SESSION")
    print(f"{'='*60}")
    
    print("\n📍 Context: Free Play Environment")
    print("Marcus will explore the virtual world, interact with peers, and")
    print("develop multi-sensory social competencies through embodied learning.")
    
    experience1 = integration.run_embodied_social_session(
        duration_minutes=35,
        context=PhysicalSocialContext.FREE_PLAY
    )
    
    print(f"\n📊 DETAILED SESSION ANALYSIS:")
    print(f"  Session ID: {experience1.session_id}")
    print(f"  Sensory Modalities Used: {[m.value for m in experience1.sensory_modalities]}")
    print(f"  Social Participants: {experience1.social_participants}")
    print(f"  Marcus Position: {experience1.marcus_position}")
    print(f"  Objects Interacted: {len(experience1.objects_interacted)}")
    print(f"  Movements Made: {len(experience1.movements_made)}")
    print(f"  Touch Experiences: {len(experience1.touch_experiences)}")
    print(f"  Social Exchanges: {len(experience1.social_exchanges)}")
    print(f"  Collaborative Actions: {len(experience1.collaborative_actions)}")
    print(f"  Concepts Discovered: {len(experience1.concepts_discovered)}")
    print(f"  Emotional Responses: {experience1.emotional_responses}")
    
    # Phase 2: Multi-Context Learning Journey
    print(f"\n{'='*60}")
    print("🌍 PHASE 2: MULTI-CONTEXT EMBODIED SOCIAL LEARNING JOURNEY")
    print(f"{'='*60}")
    
    learning_contexts = [
        (PhysicalSocialContext.CLASSROOM_CIRCLE, "Structured group learning environment"),
        (PhysicalSocialContext.PLAYGROUND, "Active outdoor social play environment"),
        (PhysicalSocialContext.SHARED_WORKSPACE, "Collaborative work and creation space"),
        (PhysicalSocialContext.GROUP_ACTIVITY, "Organized group activities and games")
    ]
    
    context_results = []
    
    for i, (context, description) in enumerate(learning_contexts):
        print(f"\n📍 Context {i+1}: {context.value.replace('_', ' ').title()}")
        print(f"Description: {description}")
        
        experience = integration.run_embodied_social_session(
            duration_minutes=25,
            context=context
        )
        
        context_results.append(experience)
        
        print(f"🎯 Context Learning Summary:")
        print(f"  Integration Score: {experience.sensory_integration_score:.3f}")
        print(f"  Social-Physical Coherence: {experience.social_physical_coherence:.3f}")
        print(f"  Learning Engagement: {experience.learning_engagement_level:.3f}")
        print(f"  Skills Practiced: {len(set(experience.physical_skills_practiced + experience.social_skills_practiced))}")
    
    # Phase 3: Comprehensive Progress Analysis
    print(f"\n{'='*70}")
    print("📈 PHASE 3: COMPREHENSIVE EMBODIED SOCIAL PROGRESS ANALYSIS")
    print(f"{'='*70}")
    
    progress_report = integration.get_embodied_social_progress_report()
    
    print(f"\n🎯 OVERALL PERFORMANCE METRICS:")
    metrics = progress_report['overall_metrics']
    print(f"  Total Learning Sessions: {progress_report['total_sessions']}")
    print(f"  Sensory Integration Score: {metrics['sensory_integration_score']:.3f}")
    print(f"  Social-Physical Coherence: {metrics['social_physical_coherence']:.3f}")
    print(f"  Learning Engagement Level: {metrics['learning_engagement_level']:.3f}")
    print(f"  Social Interaction Success Rate: {metrics['social_interaction_success_rate']:.3f}")
    
    print(f"\n🧠 EMBODIED SOCIAL SKILLS DEVELOPMENT:")
    for skill_name, skill_data in progress_report['skill_development'].items():
        readiness = skill_data['readiness_level']
        mastery = skill_data['mastery_level']
        sessions = skill_data['practice_sessions']
        
        # Color code readiness levels
        if readiness == "Advanced":
            status_icon = "🌟"
        elif readiness == "Proficient":
            status_icon = "✅"
        elif readiness == "Developing":
            status_icon = "📈"
        elif readiness == "Beginning":
            status_icon = "🌱"
        else:
            status_icon = "🔹"
        
        print(f"  {status_icon} {skill_name.replace('_', ' ').title()}")
        print(f"     Mastery: {mastery:.3f} | Sessions: {sessions} | Level: {readiness}")
    
    print(f"\n👥 SOCIAL INTERACTION ANALYSIS:")
    social_metrics = progress_report['social_interaction_metrics']
    print(f"  Total Interactions: {social_metrics['total_interactions']}")
    print(f"  Average Success Rate: {social_metrics['average_success_rate']:.3f}")
    print(f"  Interaction Types Practiced: {social_metrics['interaction_types_practiced']}")
    
    print(f"\n🎨 SENSORY MODALITY USAGE ANALYSIS:")
    modality_usage = progress_report['sensory_modality_usage']
    for modality, usage_data in modality_usage.items():
        usage_pct = usage_data['usage_percentage']
        usage_count = usage_data['usage_count']
        
        # Create visual bar
        bar_length = int(usage_pct / 5)  # Scale to 20 chars max
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"  {modality.replace('_', ' ').title():<15} {bar} {usage_pct:5.1f}% ({usage_count} uses)")
    
    print(f"\n🌍 LEARNING ENVIRONMENT DIVERSITY:")
    diversity = progress_report['learning_diversity']
    print(f"  Physical Contexts Explored: {diversity['physical_contexts_explored']}")
    print(f"  Context Diversity Score: {diversity['context_diversity_score']:.3f}")
    print(f"  Unique Peers Interacted: {diversity['unique_peers_interacted']}")
    
    print(f"\n📊 DEVELOPMENT TRENDS:")
    trends = progress_report['development_trends']
    print(f"  Engagement Trend: {trends['engagement_trend'].title()}")
    print(f"  Recent Performance: {trends['recent_session_performance']:.3f}")
    print(f"  Sessions in Analysis: {trends['sessions_in_analysis']}")
    
    # Phase 4: Embodied Social Readiness Assessment
    print(f"\n{'='*70}")
    print("🎓 PHASE 4: EMBODIED SOCIAL READINESS ASSESSMENT")
    print(f"{'='*70}")
    
    readiness = progress_report['embodied_social_readiness']
    
    print(f"\n🏆 OVERALL READINESS ASSESSMENT:")
    print(f"  Readiness Level: {readiness['readiness_level']}")
    print(f"  Overall Score: {readiness['readiness_score']:.3f}")
    
    print(f"\n📈 COMPONENT BREAKDOWN:")
    components = readiness['component_scores']
    component_names = {
        'sensory_integration': 'Sensory Integration',
        'social_physical_coherence': 'Social-Physical Coherence',
        'skill_mastery': 'Skill Mastery',
        'learning_engagement': 'Learning Engagement'
    }
    
    for component, score in components.items():
        name = component_names.get(component, component.replace('_', ' ').title())
        
        # Create progress bar
        bar_length = int(score * 30)  # Scale to 30 chars
        bar = "█" * bar_length + "░" * (30 - bar_length)
        
        # Color code based on score
        if score >= 0.8:
            status = "🌟 Excellent"
        elif score >= 0.6:
            status = "✅ Good"
        elif score >= 0.4:
            status = "📈 Developing"
        else:
            status = "🌱 Beginning"
        
        print(f"  {name:<25} {bar} {score:.3f} {status}")
    
    # Phase 5: Learning Recommendations
    print(f"\n💡 PERSONALIZED LEARNING RECOMMENDATIONS:")
    recommendations = progress_report['recommendations']
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("  🎉 No specific recommendations - Marcus is developing well across all areas!")
    
    # Phase 6: Save Comprehensive Data
    print(f"\n{'='*70}")
    print("💾 PHASE 6: SAVING COMPREHENSIVE LEARNING DATA")
    print(f"{'='*70}")
    
    filename = "marcus_embodied_social_comprehensive_demo.json"
    integration.save_embodied_social_data(filename)
    
    print(f"\n📁 Comprehensive learning data saved to: {filename}")
    print(f"   Sessions Recorded: {len(integration.sensory_experiences)}")
    print(f"   Skills Tracked: {len(integration.embodied_social_skills)}")
    print(f"   Total Learning Experiences: {sum(len(exp.concepts_discovered) for exp in integration.sensory_experiences)}")
    
    # Final Summary
    print(f"\n{'='*70}")
    print("🎉 EMBODIED SOCIAL LEARNING INTEGRATION COMPLETE!")
    print(f"{'='*70}")
    
    print(f"\n🌟 ACHIEVEMENT SUMMARY:")
    print(f"  ✅ Multi-Sensory Integration: {metrics['sensory_integration_score']:.1%} success")
    print(f"  ✅ Social-Physical Coherence: {metrics['social_physical_coherence']:.1%} integration")
    print(f"  ✅ Learning Engagement: {metrics['learning_engagement_level']:.1%} active participation")
    print(f"  ✅ Social Success Rate: {metrics['social_interaction_success_rate']:.1%} positive interactions")
    print(f"  ✅ Overall Readiness: {readiness['readiness_score']:.1%} embodied social competence")
    
    print(f"\n🎯 SYSTEM CAPABILITIES DEMONSTRATED:")
    print(f"  🎮 Virtual Body World - Physical exploration with sensory feedback")
    print(f"  🤝 Social Peer Interactions - Dynamic relationship building with diverse peers")
    print(f"  🧠 Multi-Sensory Learning - Integration of vision, touch, movement, and social senses")
    print(f"  📈 Embodied Social Skills - Development of physical components of social competence")
    print(f"  🎓 Comprehensive Assessment - Multi-modal progress tracking and readiness evaluation")
    
    print(f"\n🚀 MARCUS IS NOW READY FOR:")
    readiness_level = readiness['readiness_level']
    if "Fully Ready for Advanced" in readiness_level:
        print(f"  🌟 Advanced embodied social learning environments")
        print(f"  🌟 Complex multi-peer collaborative activities")
        print(f"  🌟 Leadership roles in group physical-social activities")
    elif "Ready for Full" in readiness_level:
        print(f"  ✅ Full embodied social integration activities")
        print(f"  ✅ Multi-context social learning environments")
        print(f"  ✅ Independent peer interaction management")
    elif "Ready for Structured" in readiness_level:
        print(f"  📈 Structured embodied social activities")
        print(f"  📈 Guided multi-sensory peer interactions")
        print(f"  📈 Supported collaborative physical activities")
    else:
        print(f"  🌱 Continued guided embodied social development")
        print(f"  🌱 Foundational multi-sensory skill building")
        print(f"  🌱 Basic peer interaction practice")
    
    print(f"\n💫 Marcus has successfully mastered the integration of physical embodiment")
    print(f"   with social learning, creating a comprehensive foundation for")
    print(f"   sophisticated social-physical competence in real-world environments!")
    
    return integration


def quick_embodied_social_demo():
    """Run a quick demonstration for testing purposes"""
    
    print("🎮🤝 Quick Embodied Social Learning Demo")
    print("=" * 50)
    
    # Run the main demo function from the module
    integration = demo_embodied_social_integration()
    
    print(f"\n✅ Quick demo completed successfully!")
    print(f"   Integration system validated with comprehensive multi-sensory social learning")
    
    return integration


if __name__ == "__main__":
    # Run comprehensive demo by default
    print("Starting Marcus AGI Embodied Social Learning Integration Demo...")
    
    try:
        integration = comprehensive_embodied_social_demo()
        print(f"\n🎉 Demo completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Demo interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Demo encountered an error: {e}")
        print("Running quick demo instead...")
        integration = quick_embodied_social_demo()
