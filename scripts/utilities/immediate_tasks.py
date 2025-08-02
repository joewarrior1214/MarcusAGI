#!/usr/bin/env python3
"""
Immediate Task Implementation - Combined Interface

This module provides a single interface to run both immediate tasks:
1. Social Growth Dashboard - Weekly progress tracking
2. Replay Analyzer Interface - Social interaction analysis

Usage: python immediate_tasks.py
"""

import sys
from datetime import datetime
from social_growth_dashboard import generate_social_growth_dashboard
from replay_analyzer import generate_replay_analysis

def run_immediate_tasks():
    """Run both immediate tasks and provide combined results"""
    print("🚀 Running Immediate Strategic Tasks")
    print("=" * 50)
    print(f"📅 Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Task 1: Social Growth Dashboard
    print("📈 TASK 1: Social Growth Dashboard")
    print("-" * 35)
    
    try:
        dashboard_result = generate_social_growth_dashboard(weeks_back=4)
        
        if "error" in dashboard_result:
            print(f"❌ Dashboard Error: {dashboard_result['error']}")
        else:
            print(f"✅ Dashboard Generated Successfully!")
            print(f"   📊 Sessions Analyzed: {dashboard_result['sessions_analyzed']}")
            print(f"   📈 Overall Score: {dashboard_result['overall_score']:.1%}")
            print(f"   📁 Dashboard: {dashboard_result['dashboard_path']}")
            print(f"   📋 Report: {dashboard_result['report_path']}")
            
    except Exception as e:
        print(f"❌ Dashboard Generation Failed: {e}")
    
    print()
    
    # Task 2: Replay Analyzer
    print("🎞️ TASK 2: Replay Analyzer Interface")
    print("-" * 40)
    
    try:
        replay_result = generate_replay_analysis(days_back=30)
        
        if "error" in replay_result:
            print(f"❌ Replay Analysis Error: {replay_result['error']}")
        else:
            print(f"✅ Replay Analysis Generated Successfully!")
            print(f"   📊 Sessions Analyzed: {replay_result['sessions_analyzed']}")
            print(f"   📈 Success Rate: {replay_result['success_rate']:.1%}")
            print(f"   📁 Analysis: {replay_result['analysis_path']}")
            print(f"   📋 Report: {replay_result['report_path']}")
            
    except Exception as e:
        print(f"❌ Replay Analysis Failed: {e}")
    
    print()
    print("🎯 IMMEDIATE TASKS SUMMARY")
    print("-" * 30)
    
    # Check if both tasks completed successfully
    dashboard_success = 'dashboard_result' in locals() and "error" not in dashboard_result
    replay_success = 'replay_result' in locals() and "error" not in replay_result
    
    if dashboard_success and replay_success:
        print("✅ Both immediate tasks completed successfully!")
        print(f"📊 Combined Analysis: {dashboard_result['sessions_analyzed']} dashboard sessions, {replay_result['sessions_analyzed']} replay interactions")
        print("🎉 Marcus AGI analytics capabilities enhanced!")
    elif dashboard_success or replay_success:
        print("⚠️ Partial completion - one task succeeded")
        if dashboard_success:
            print("✅ Dashboard task completed")
        if replay_success:
            print("✅ Replay analysis completed")
    else:
        print("❌ Both tasks encountered issues")
    
    print()
    print("📋 NEXT STEPS:")
    print("   1. Review generated reports for insights")
    print("   2. Use analytics to inform short-term strategic options")
    print("   3. Consider implementing enhanced SEL curriculum")
    print("   4. Refine peer personality simulation based on analysis")
    
    return {
        'dashboard_success': dashboard_success,
        'replay_success': replay_success,
        'dashboard_result': dashboard_result if dashboard_success else None,
        'replay_result': replay_result if replay_success else None
    }

if __name__ == "__main__":
    results = run_immediate_tasks()
    
    # Exit with appropriate code
    if results['dashboard_success'] and results['replay_success']:
        sys.exit(0)  # Success
    elif results['dashboard_success'] or results['replay_success']:
        sys.exit(1)  # Partial success
    else:
        sys.exit(2)  # Failure
