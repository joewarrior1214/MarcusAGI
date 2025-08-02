#!/usr/bin/env python3
"""
Social Growth Dashboard - Weekly Progress Tracking

This module creates comprehensive dashboards for tracking Marcus's social development
over time using existing session data. Provides visual analytics for:
- Emotional regulation progress
- Conflict resolution success rates  
- Turn-taking accuracy improvements
- Perspective-taking development
- Peer relationship strength trends
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
import numpy as np

class SocialGrowthDashboard:
    """Dashboard for visualizing Marcus's social development over time"""
    
    def __init__(self, sessions_dir: str = "output/integrated_sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.dashboard_dir = Path("output/dashboards")
        self.dashboard_dir.mkdir(exist_ok=True)
        
    def load_session_data(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """Load session data from the last N days"""
        sessions = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        if not self.sessions_dir.exists():
            print(f"📁 Sessions directory not found: {self.sessions_dir}")
            return sessions
            
        for session_file in self.sessions_dir.glob("integrated_session_*.json"):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    
                # Extract date from session data or filename
                session_date_str = session_data.get('session_date', session_file.stem.split('_')[-1])
                try:
                    if len(session_date_str) == 8:  # YYYYMMDD format
                        session_date = datetime.strptime(session_date_str, '%Y%m%d')
                        
                    # Handle integrated session filename format: integrated_session_20250802_064024
                    elif 'integrated_session_' in session_file.stem:
                        date_part = session_file.stem.split('_')[2]  # Extract YYYYMMDD part
                        session_date = datetime.strptime(date_part, '%Y%m%d')
                    else:
                        session_date = datetime.fromisoformat(session_date_str.split('T')[0])
                except Exception as e:
                    print(f"⚠️ Date parsing error for {session_file}: {e}")
                    continue
                    
                if session_date >= cutoff_date:
                    session_data['parsed_date'] = session_date
                    sessions.append(session_data)
                    
            except Exception as e:
                print(f"⚠️ Error loading {session_file}: {e}")
                continue
                
        return sorted(sessions, key=lambda x: x['parsed_date'])
    
    def analyze_emotional_regulation(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Analyze emotional regulation progress over time"""
        daily_scores = defaultdict(list)
        
        for session in sessions:
            date = session['parsed_date'].strftime('%Y-%m-%d')
            
            # Extract EQ coaching moments
            eq_moments = session.get('eq_coaching_moments', [])
            eq_success = len([m for m in eq_moments if m.get('success', True)])
            total_eq = len(eq_moments) if eq_moments else 1
            eq_score = eq_success / total_eq
            
            # Overall session success as emotion regulation indicator
            overall_success = session.get('integration_success_metrics', {}).get('social_engagement', 0)
            
            daily_scores[date].append({
                'eq_coaching_success': eq_score,
                'social_engagement': overall_success,
                'composite_score': (eq_score + overall_success) / 2
            })
        
        # Calculate daily averages
        daily_averages = {}
        for date, scores in daily_scores.items():
            avg_composite = np.mean([s['composite_score'] for s in scores])
            daily_averages[date] = avg_composite
            
        return {
            'daily_scores': daily_averages,
            'trend': self._calculate_trend(list(daily_averages.values())),
            'current_level': list(daily_averages.values())[-1] if daily_averages else 0,
            'improvement': self._calculate_improvement(list(daily_averages.values()))
        }
    
    def analyze_conflict_resolution(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Analyze conflict resolution success rates"""
        daily_stats = defaultdict(lambda: {'resolved': 0, 'total': 0})
        
        for session in sessions:
            date = session['parsed_date'].strftime('%Y-%m-%d')
            
            # Check social practice sessions for conflicts
            social_sessions = session.get('social_sessions', [])
            for social_session in social_sessions:
                if social_session.get('type') == 'social_practice':
                    session_data = social_session.get('session', {})
                    conflicts_resolved = session_data.get('conflicts_resolved', 0)
                    
                    # Estimate total conflicts from conversation analysis
                    turns = session_data.get('conversation_turns', [])
                    conflict_indicators = sum(1 for turn in turns 
                                           if 'conflict' in turn.get('message', '').lower() 
                                           or turn.get('emotion') in ['angry', 'frustrated'])
                    
                    daily_stats[date]['resolved'] += conflicts_resolved
                    daily_stats[date]['total'] += max(conflict_indicators, conflicts_resolved)
        
        # Calculate success rates
        daily_success_rates = {}
        for date, stats in daily_stats.items():
            if stats['total'] > 0:
                daily_success_rates[date] = stats['resolved'] / stats['total']
            else:
                daily_success_rates[date] = 1.0  # No conflicts = perfect resolution
                
        return {
            'daily_success_rates': daily_success_rates,
            'trend': self._calculate_trend(list(daily_success_rates.values())),
            'total_conflicts_resolved': sum(s['resolved'] for s in daily_stats.values()),
            'resolution_improvement': self._calculate_improvement(list(daily_success_rates.values()))
        }
    
    def analyze_turn_taking(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Analyze turn-taking accuracy over time"""
        daily_scores = defaultdict(list)
        
        for session in sessions:
            date = session['parsed_date'].strftime('%Y-%m-%d')
            
            # Extract turn-taking skill demonstrations
            social_sessions = session.get('social_sessions', [])
            for social_session in social_sessions:
                session_data = social_session.get('session', {})
                skills_practiced = session_data.get('social_skills_practiced', [])
                
                # Check for turn-taking skill
                turn_taking_practiced = any('turn_taking' in str(skill).lower() for skill in skills_practiced)
                if turn_taking_practiced:
                    success_rating = session_data.get('overall_success_rating', 0)
                    daily_scores[date].append(success_rating)
        
        # Calculate daily averages
        daily_averages = {}
        for date, scores in daily_scores.items():
            if scores:
                daily_averages[date] = np.mean(scores)
            
        return {
            'daily_accuracy': daily_averages,
            'trend': self._calculate_trend(list(daily_averages.values())),
            'current_accuracy': list(daily_averages.values())[-1] if daily_averages else 0,
            'practice_frequency': len([s for session_scores in daily_scores.values() for s in session_scores])
        }
    
    def analyze_perspective_taking(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Analyze perspective-taking development"""
        daily_scores = defaultdict(list)
        
        for session in sessions:
            date = session['parsed_date'].strftime('%Y-%m-%d')
            
            # Look for empathy-related growth areas and achievements
            social_sessions = session.get('social_sessions', [])
            for social_session in social_sessions:
                session_data = social_session.get('session', {})
                
                # Check for empathy in growth areas (reverse indicator)
                growth_areas = session_data.get('marcus_growth_areas', [])
                empathy_needs_work = any('empathy' in str(area).lower() for area in growth_areas)
                
                # Check for empathy in demonstrated skills
                conversation_turns = session_data.get('conversation_turns', [])
                empathy_demonstrations = sum(1 for turn in conversation_turns 
                                          if turn.get('speaker') == 'marcus' 
                                          and any('empathy' in str(skill).lower() 
                                                for skill in turn.get('social_skills_demonstrated', [])))
                
                # Calculate perspective-taking score
                if conversation_turns:
                    perspective_score = empathy_demonstrations / len(conversation_turns)
                    if empathy_needs_work:
                        perspective_score *= 0.8  # Slight penalty for identified growth need
                    daily_scores[date].append(perspective_score)
        
        # Calculate daily averages
        daily_averages = {}
        for date, scores in daily_scores.items():
            if scores:
                daily_averages[date] = np.mean(scores)
        
        return {
            'daily_perspective_scores': daily_averages,
            'trend': self._calculate_trend(list(daily_averages.values())),
            'empathy_demonstrations': sum(len(scores) for scores in daily_scores.values()),
            'development_progress': self._calculate_improvement(list(daily_averages.values()))
        }
    
    def analyze_peer_relationships(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Analyze peer relationship strength over time"""
        daily_relationship_data = defaultdict(list)
        peer_interaction_counts = defaultdict(int)
        
        for session in sessions:
            date = session['parsed_date'].strftime('%Y-%m-%d')
            
            # Extract peer interaction success
            social_sessions = session.get('social_sessions', [])
            for social_session in social_sessions:
                session_data = social_session.get('session', {})
                peers_involved = session_data.get('peers_involved', [])
                success_rating = session_data.get('overall_success_rating', 0)
                
                for peer in peers_involved:
                    peer_interaction_counts[peer] += 1
                    daily_relationship_data[date].append({
                        'peer': peer,
                        'interaction_success': success_rating
                    })
        
        # Calculate daily relationship strength
        daily_averages = {}
        for date, interactions in daily_relationship_data.items():
            if interactions:
                daily_averages[date] = np.mean([i['interaction_success'] for i in interactions])
        
        return {
            'daily_relationship_strength': daily_averages,
            'peer_interaction_counts': dict(peer_interaction_counts),
            'relationship_trend': self._calculate_trend(list(daily_averages.values())),
            'most_frequent_peer': max(peer_interaction_counts.items(), key=lambda x: x[1])[0] if peer_interaction_counts else None
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from values"""
        if len(values) < 2:
            return "insufficient_data"
        
        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        slope = (n * sum(x[i] * values[i] for i in range(n)) - sum(x) * sum(values)) / (n * sum(x[i]**2 for i in range(n)) - sum(x)**2)
        
        if slope > 0.01:
            return "improving"
        elif slope < -0.01:
            return "declining"
        else:
            return "stable"
    
    def _calculate_improvement(self, values: List[float]) -> float:
        """Calculate improvement percentage"""
        if len(values) < 2:
            return 0.0
        
        return ((values[-1] - values[0]) / values[0]) * 100 if values[0] > 0 else 0.0
    
    def generate_weekly_dashboard(self, weeks_back: int = 4) -> Dict[str, Any]:
        """Generate comprehensive weekly dashboard"""
        days_back = weeks_back * 7
        sessions = self.load_session_data(days_back)
        
        if not sessions:
            return {"error": "No session data found for dashboard generation"}
        
        print(f"📊 Analyzing {len(sessions)} sessions from last {weeks_back} weeks...")
        
        # Analyze all growth areas
        emotional_regulation = self.analyze_emotional_regulation(sessions)
        conflict_resolution = self.analyze_conflict_resolution(sessions)
        turn_taking = self.analyze_turn_taking(sessions)
        perspective_taking = self.analyze_perspective_taking(sessions)
        peer_relationships = self.analyze_peer_relationships(sessions)
        
        dashboard = {
            "dashboard_generated": datetime.now().isoformat(),
            "analysis_period": f"{weeks_back} weeks",
            "sessions_analyzed": len(sessions),
            "emotional_regulation": emotional_regulation,
            "conflict_resolution": conflict_resolution,
            "turn_taking": turn_taking,
            "perspective_taking": perspective_taking,
            "peer_relationships": peer_relationships,
            "overall_social_growth": self._calculate_overall_growth([
                emotional_regulation.get('current_level', 0),
                conflict_resolution.get('daily_success_rates', {}).get(list(conflict_resolution.get('daily_success_rates', {}).keys())[-1] if conflict_resolution.get('daily_success_rates') else 0, 0),
                turn_taking.get('current_accuracy', 0),
                perspective_taking.get('daily_perspective_scores', {}).get(list(perspective_taking.get('daily_perspective_scores', {}).keys())[-1] if perspective_taking.get('daily_perspective_scores') else 0, 0),
                peer_relationships.get('daily_relationship_strength', {}).get(list(peer_relationships.get('daily_relationship_strength', {}).keys())[-1] if peer_relationships.get('daily_relationship_strength') else 0, 0)
            ])
        }
        
        return dashboard
    
    def _calculate_overall_growth(self, scores: List[float]) -> Dict[str, Any]:
        """Calculate overall social growth metrics"""
        valid_scores = [s for s in scores if s > 0]
        if not valid_scores:
            return {"overall_score": 0, "growth_level": "needs_assessment"}
        
        overall_score = np.mean(valid_scores)
        
        if overall_score >= 0.85:
            growth_level = "excellent"
        elif overall_score >= 0.70:
            growth_level = "good"
        elif overall_score >= 0.55:
            growth_level = "developing"
        else:
            growth_level = "needs_support"
            
        return {
            "overall_score": overall_score,
            "growth_level": growth_level,
            "areas_assessed": len(valid_scores),
            "confidence": "high" if len(valid_scores) >= 4 else "medium"
        }
    
    def save_dashboard(self, dashboard_data: Dict[str, Any]) -> str:
        """Save dashboard data to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"social_growth_dashboard_{timestamp}.json"
        filepath = self.dashboard_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(dashboard_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def create_text_report(self, dashboard_data: Dict[str, Any]) -> str:
        """Create human-readable text report from dashboard data"""
        report = []
        report.append("🌟 Marcus AGI Social Growth Dashboard")
        report.append("=" * 50)
        report.append(f"📅 Analysis Period: {dashboard_data['analysis_period']}")
        report.append(f"📊 Sessions Analyzed: {dashboard_data['sessions_analyzed']}")
        report.append(f"🕒 Generated: {dashboard_data['dashboard_generated']}")
        report.append("")
        
        # Overall Growth Summary
        overall = dashboard_data.get('overall_social_growth', {})
        report.append("🎯 OVERALL SOCIAL GROWTH")
        report.append(f"   📈 Overall Score: {overall.get('overall_score', 0):.1%}")
        report.append(f"   🏆 Growth Level: {overall.get('growth_level', 'unknown').title()}")
        report.append(f"   📊 Confidence: {overall.get('confidence', 'unknown').title()}")
        report.append("")
        
        # Individual Area Analysis
        areas = [
            ("🎭 Emotional Regulation", "emotional_regulation"),
            ("🤝 Conflict Resolution", "conflict_resolution"), 
            ("🔄 Turn-Taking", "turn_taking"),
            ("👁️ Perspective-Taking", "perspective_taking"),
            ("👥 Peer Relationships", "peer_relationships")
        ]
        
        for title, key in areas:
            data = dashboard_data.get(key, {})
            report.append(title)
            
            if key == "emotional_regulation":
                report.append(f"   Current Level: {data.get('current_level', 0):.1%}")
                report.append(f"   Trend: {data.get('trend', 'unknown').title()}")
                report.append(f"   Improvement: {data.get('improvement', 0):+.1f}%")
            elif key == "conflict_resolution":
                report.append(f"   Total Resolved: {data.get('total_conflicts_resolved', 0)}")
                report.append(f"   Trend: {data.get('trend', 'unknown').title()}")
                report.append(f"   Success Improvement: {data.get('resolution_improvement', 0):+.1f}%")
            elif key == "turn_taking":
                report.append(f"   Current Accuracy: {data.get('current_accuracy', 0):.1%}")
                report.append(f"   Practice Sessions: {data.get('practice_frequency', 0)}")
                report.append(f"   Trend: {data.get('trend', 'unknown').title()}")
            elif key == "perspective_taking":
                report.append(f"   Empathy Demonstrations: {data.get('empathy_demonstrations', 0)}")
                report.append(f"   Development Progress: {data.get('development_progress', 0):+.1f}%")
                report.append(f"   Trend: {data.get('trend', 'unknown').title()}")
            elif key == "peer_relationships":
                report.append(f"   Relationship Trend: {data.get('relationship_trend', 'unknown').title()}")
                report.append(f"   Most Frequent Peer: {data.get('most_frequent_peer', 'none')}")
                peer_counts = data.get('peer_interaction_counts', {})
                if peer_counts:
                    report.append(f"   Total Peer Interactions: {sum(peer_counts.values())}")
            
            report.append("")
        
        return "\n".join(report)


def generate_social_growth_dashboard(weeks_back: int = 4) -> Dict[str, str]:
    """Generate and save social growth dashboard"""
    dashboard = SocialGrowthDashboard()
    
    # Generate dashboard data
    dashboard_data = dashboard.generate_weekly_dashboard(weeks_back)
    
    if "error" in dashboard_data:
        return {"error": dashboard_data["error"]}
    
    # Save dashboard data
    json_path = dashboard.save_dashboard(dashboard_data)
    
    # Create text report
    text_report = dashboard.create_text_report(dashboard_data)
    text_path = json_path.replace('.json', '.txt')
    
    with open(text_path, 'w') as f:
        f.write(text_report)
    
    print(f"📊 Dashboard saved to: {json_path}")
    print(f"📋 Report saved to: {text_path}")
    
    return {
        "dashboard_path": json_path,
        "report_path": text_path,
        "sessions_analyzed": dashboard_data['sessions_analyzed'],
        "overall_score": dashboard_data['overall_social_growth']['overall_score']
    }


def demo_social_growth_dashboard():
    """Demonstrate social growth dashboard capabilities"""
    print("🌟 Social Growth Dashboard Demo")
    print("=" * 40)
    
    result = generate_social_growth_dashboard(weeks_back=4)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    print(f"\n✅ Dashboard Generated Successfully!")
    print(f"   📊 Sessions Analyzed: {result['sessions_analyzed']}")
    print(f"   📈 Overall Score: {result['overall_score']:.1%}")
    print(f"   📁 Files: {result['dashboard_path']}, {result['report_path']}")
    
    # Display sample text report
    with open(result['report_path'], 'r') as f:
        report_lines = f.readlines()
    
    print(f"\n📋 Sample Report Preview:")
    for line in report_lines[:20]:  # Show first 20 lines
        print(f"   {line.rstrip()}")
    
    if len(report_lines) > 20:
        print(f"   ... ({len(report_lines) - 20} more lines)")


if __name__ == "__main__":
    demo_social_growth_dashboard()
