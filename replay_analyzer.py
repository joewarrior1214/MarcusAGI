#!/usr/bin/env python3
"""
Replay Analyzer Interface - Social Interaction Analysis

This module provides comprehensive analysis of saved social interaction replays to:
- Debug misalignment between intended and actual social behaviors
- Reflect on poor coherence patterns and identify improvement opportunities  
- Reinforce successful behaviors by highlighting effective interaction patterns
- Generate learning insights from historical social interaction data
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np

class SocialInteractionReplayAnalyzer:
    """Analyzer for social interaction replay data"""
    
    def __init__(self, sessions_dir: str = "output/integrated_sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.analysis_dir = Path("output/replay_analysis")
        self.analysis_dir.mkdir(exist_ok=True)
        
    def load_interaction_replays(self, days_back: int = 30) -> List[Dict[str, Any]]:
        """Load social interaction replay data from recent sessions"""
        replays = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        if not self.sessions_dir.exists():
            print(f"📁 Sessions directory not found: {self.sessions_dir}")
            return replays
            
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
                    # Extract social interaction replays from peer_interactions
                    peer_interactions = session_data.get('peer_interactions', [])
                    social_sessions = session_data.get('social_sessions', [])
                    
                    # Process peer_interactions
                    for interaction in peer_interactions:
                        if interaction.get('type') in ['social_practice', 'morning_warmup']:
                            replay_data = {
                                'session_file': str(session_file),
                                'session_date': session_date,
                                'session_id': interaction.get('session', {}).get('session_id'),
                                'interaction_data': interaction.get('session', {}),
                                'success_rating': interaction.get('success_rating', interaction.get('session', {}).get('overall_success_rating', 0)),
                                'skills_practiced': interaction.get('skills_practiced', [])
                            }
                            replays.append(replay_data)
                    
                    # Process social_sessions if they exist
                    for social_session in social_sessions:
                        if social_session.get('type') == 'social_practice':
                            replay_data = {
                                'session_file': str(session_file),
                                'session_date': session_date,
                                'session_id': social_session.get('session', {}).get('session_id'),
                                'interaction_data': social_session.get('session', {}),
                                'success_rating': social_session.get('success_rating', 0),
                                'skills_practiced': social_session.get('skills_practiced', [])
                            }
                            replays.append(replay_data)
                            
            except Exception as e:
                print(f"⚠️ Error loading {session_file}: {e}")
                continue
                
        return sorted(replays, key=lambda x: x['session_date'])
    
    def debug_misalignment_patterns(self, replays: List[Dict]) -> Dict[str, Any]:
        """Debug patterns of misalignment between intended and actual behaviors"""
        misalignments = []
        alignment_issues = defaultdict(list)
        
        for replay in replays:
            interaction = replay['interaction_data']
            conversation_turns = interaction.get('conversation_turns', [])
            success_rating = replay['success_rating']
            
            # Low success rating indicates potential misalignment
            if success_rating < 0.6:
                misalignment_analysis = {
                    'session_id': replay['session_id'],
                    'date': replay['session_date'].strftime('%Y-%m-%d'),
                    'success_rating': success_rating,
                    'peers_involved': interaction.get('peers_involved', []),
                    'skills_attempted': replay['skills_practiced'],
                    'issues_identified': []
                }
                
                # Analyze conversation turns for issues
                for turn in conversation_turns:
                    if turn.get('speaker') == 'marcus':
                        response_quality = turn.get('response_quality', 1.0)
                        if response_quality < 0.5:
                            issue = {
                                'turn_message': turn.get('message', ''),
                                'emotion': turn.get('emotion', ''),
                                'response_quality': response_quality,
                                'skills_attempted': turn.get('social_skills_demonstrated', []),
                                'coaching_triggered': turn.get('coaching_triggered', False)
                            }
                            misalignment_analysis['issues_identified'].append(issue)
                            
                            # Categorize the type of misalignment
                            if response_quality < 0.3:
                                alignment_issues['severe_response_quality'].append(issue)
                            elif turn.get('coaching_triggered'):
                                alignment_issues['coaching_required'].append(issue)
                            else:
                                alignment_issues['mild_misalignment'].append(issue)
                
                if misalignment_analysis['issues_identified']:
                    misalignments.append(misalignment_analysis)
        
        # Pattern analysis
        common_issues = {}
        for issue_type, issues in alignment_issues.items():
            if issues:
                common_emotions = Counter(issue.get('emotion', 'unknown') for issue in issues)
                common_skills = Counter(str(skill) for issue in issues for skill in issue.get('skills_attempted', []))
                
                common_issues[issue_type] = {
                    'frequency': len(issues),
                    'common_emotions': dict(common_emotions.most_common(3)),
                    'problematic_skills': dict(common_skills.most_common(3)),
                    'avg_quality': np.mean([issue.get('response_quality', 0) for issue in issues])
                }
        
        return {
            'total_misalignments': len(misalignments),
            'misalignment_sessions': misalignments,
            'pattern_analysis': common_issues,
            'improvement_suggestions': self._generate_misalignment_suggestions(common_issues)
        }
    
    def analyze_coherence_patterns(self, replays: List[Dict]) -> Dict[str, Any]:
        """Analyze social-physical coherence patterns for reflection"""
        coherence_data = []
        low_coherence_sessions = []
        
        for replay in replays:
            interaction = replay['interaction_data']
            
            # Look for coherence metrics if available
            coherence_score = interaction.get('social_physical_coherence', None)
            if coherence_score is not None:
                coherence_analysis = {
                    'session_id': replay['session_id'],
                    'date': replay['session_date'].strftime('%Y-%m-%d'),
                    'coherence_score': coherence_score,
                    'success_rating': replay['success_rating'],
                    'peers_involved': interaction.get('peers_involved', []),
                    'context': interaction.get('context', 'unknown')
                }
                coherence_data.append(coherence_analysis)
                
                # Flag low coherence sessions for detailed analysis
                if coherence_score < 0.4:
                    detailed_analysis = self._analyze_low_coherence_session(replay)
                    coherence_analysis.update(detailed_analysis)
                    low_coherence_sessions.append(coherence_analysis)
        
        if not coherence_data:
            return {'error': 'No coherence data found in replay sessions'}
        
        # Statistical analysis
        coherence_scores = [c['coherence_score'] for c in coherence_data]
        
        return {
            'total_sessions_analyzed': len(coherence_data),
            'average_coherence': np.mean(coherence_scores),
            'coherence_trend': self._calculate_coherence_trend(coherence_data),
            'low_coherence_sessions': len(low_coherence_sessions),
            'coherence_distribution': {
                'excellent': len([c for c in coherence_scores if c >= 0.8]),
                'good': len([c for c in coherence_scores if 0.6 <= c < 0.8]),
                'needs_work': len([c for c in coherence_scores if 0.4 <= c < 0.6]),
                'poor': len([c for c in coherence_scores if c < 0.4])
            },
            'detailed_low_coherence_analysis': low_coherence_sessions[:5],  # Top 5 for detailed review
            'coherence_improvement_plan': self._generate_coherence_improvement_plan(low_coherence_sessions)
        }
    
    def identify_successful_behavior_patterns(self, replays: List[Dict]) -> Dict[str, Any]:
        """Identify and reinforce successful social behavior patterns"""
        successful_sessions = []
        success_patterns = defaultdict(list)
        
        for replay in replays:
            interaction = replay['interaction_data']
            success_rating = replay['success_rating']
            
            # High success sessions (>= 0.8) for pattern analysis
            if success_rating >= 0.8:
                success_analysis = {
                    'session_id': replay['session_id'],
                    'date': replay['session_date'].strftime('%Y-%m-%d'),
                    'success_rating': success_rating,
                    'peers_involved': interaction.get('peers_involved', []),
                    'skills_demonstrated': replay['skills_practiced'],
                    'conversation_highlights': []
                }
                
                # Extract successful conversation patterns
                conversation_turns = interaction.get('conversation_turns', [])
                for turn in conversation_turns:
                    if turn.get('speaker') == 'marcus' and turn.get('response_quality', 0) >= 0.8:
                        highlight = {
                            'message': turn.get('message', ''),
                            'emotion': turn.get('emotion', ''),
                            'skills_shown': turn.get('social_skills_demonstrated', []),
                            'quality_score': turn.get('response_quality', 0)
                        }
                        success_analysis['conversation_highlights'].append(highlight)
                        
                        # Categorize successful patterns
                        for skill in turn.get('social_skills_demonstrated', []):
                            success_patterns[str(skill)].append({
                                'message': turn.get('message', ''),
                                'emotion': turn.get('emotion', ''),
                                'quality': turn.get('response_quality', 0),
                                'context': interaction.get('context', 'unknown')
                            })
                
                successful_sessions.append(success_analysis)
        
        # Pattern analysis for reinforcement
        reinforcement_patterns = {}
        for skill, examples in success_patterns.items():
            if examples:
                avg_quality = np.mean([e['quality'] for e in examples])
                common_emotions = Counter(e['emotion'] for e in examples)
                common_contexts = Counter(e['context'] for e in examples)
                
                reinforcement_patterns[skill] = {
                    'success_frequency': len(examples),
                    'average_quality': avg_quality,
                    'best_example': max(examples, key=lambda x: x['quality']),
                    'common_emotions': dict(common_emotions.most_common(3)),
                    'effective_contexts': dict(common_contexts.most_common(3)),
                    'reinforcement_strategies': self._generate_reinforcement_strategies(skill, examples)
                }
        
        return {
            'total_successful_sessions': len(successful_sessions),
            'success_rate': len(successful_sessions) / len(replays) if replays else 0,
            'successful_sessions_detail': successful_sessions[:10],  # Top 10 for review
            'successful_behavior_patterns': reinforcement_patterns,
            'key_success_factors': self._identify_key_success_factors(successful_sessions),
            'reinforcement_recommendations': self._generate_success_reinforcement_plan(reinforcement_patterns)
        }
    
    def generate_learning_insights(self, replays: List[Dict]) -> Dict[str, Any]:
        """Generate actionable learning insights from replay analysis"""
        if not replays:
            return {'error': 'No replay data available for analysis'}
        
        # Comprehensive analysis
        misalignment_analysis = self.debug_misalignment_patterns(replays)
        coherence_analysis = self.analyze_coherence_patterns(replays)
        success_analysis = self.identify_successful_behavior_patterns(replays)
        
        # Overall insights
        total_sessions = len(replays)
        avg_success_rate = np.mean([r['success_rating'] for r in replays])
        
        # Trend analysis
        replays_by_date = sorted(replays, key=lambda x: x['session_date'])
        early_sessions = replays_by_date[:len(replays_by_date)//2] if len(replays_by_date) > 4 else replays_by_date
        recent_sessions = replays_by_date[len(replays_by_date)//2:] if len(replays_by_date) > 4 else replays_by_date
        
        early_avg = np.mean([r['success_rating'] for r in early_sessions]) if early_sessions else 0
        recent_avg = np.mean([r['success_rating'] for r in recent_sessions]) if recent_sessions else 0
        improvement_trend = recent_avg - early_avg
        
        insights = {
            'analysis_summary': {
                'total_sessions_analyzed': total_sessions,
                'analysis_period': f"{replays[0]['session_date'].strftime('%Y-%m-%d')} to {replays[-1]['session_date'].strftime('%Y-%m-%d')}",
                'average_success_rate': avg_success_rate,
                'improvement_trend': improvement_trend,
                'trend_direction': 'improving' if improvement_trend > 0.05 else 'declining' if improvement_trend < -0.05 else 'stable'
            },
            'misalignment_insights': misalignment_analysis,
            'coherence_insights': coherence_analysis if 'error' not in coherence_analysis else None,
            'success_insights': success_analysis,
            'actionable_recommendations': self._generate_actionable_recommendations(
                misalignment_analysis, coherence_analysis, success_analysis, improvement_trend
            )
        }
        
        return insights
    
    def _analyze_low_coherence_session(self, replay: Dict) -> Dict[str, Any]:
        """Detailed analysis of low coherence session"""
        interaction = replay['interaction_data']
        
        # Look for indicators of poor coherence
        conversation_turns = interaction.get('conversation_turns', [])
        marcus_turns = [t for t in conversation_turns if t.get('speaker') == 'marcus']
        
        coherence_issues = []
        for turn in marcus_turns:
            if turn.get('response_quality', 1.0) < 0.5:
                coherence_issues.append({
                    'message': turn.get('message', ''),
                    'quality': turn.get('response_quality', 0),
                    'emotion': turn.get('emotion', ''),
                    'skills_attempted': turn.get('social_skills_demonstrated', [])
                })
        
        return {
            'coherence_issues_count': len(coherence_issues),
            'specific_coherence_problems': coherence_issues,
            'suggested_improvements': self._generate_coherence_suggestions(coherence_issues)
        }
    
    def _calculate_coherence_trend(self, coherence_data: List[Dict]) -> str:
        """Calculate coherence improvement trend"""
        if len(coherence_data) < 3:
            return "insufficient_data"
        
        sorted_data = sorted(coherence_data, key=lambda x: x['date'])
        scores = [d['coherence_score'] for d in sorted_data]
        
        # Simple trend calculation
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = np.mean(first_half)
        second_avg = np.mean(second_half)
        
        if second_avg > first_avg + 0.1:
            return "improving"
        elif second_avg < first_avg - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _generate_misalignment_suggestions(self, issues: Dict[str, Any]) -> List[str]:
        """Generate suggestions for addressing misalignment patterns"""
        suggestions = []
        
        for issue_type, data in issues.items():
            if data['frequency'] > 0:
                if issue_type == 'severe_response_quality':
                    suggestions.append("Focus on improving response quality through additional practice with structured scenarios")
                elif issue_type == 'coaching_required':
                    suggestions.append("Implement more proactive coaching interventions before response quality degrades")
                elif issue_type == 'mild_misalignment':
                    suggestions.append("Fine-tune social response patterns through targeted skill practice")
        
        return suggestions
    
    def _generate_coherence_improvement_plan(self, low_coherence_sessions: List[Dict]) -> List[str]:
        """Generate plan for improving social-physical coherence"""
        if not low_coherence_sessions:
            return ["Coherence levels are satisfactory - continue current approach"]
        
        plan = [
            "Increase focus on integrating physical and social actions during practice",
            "Practice social interactions in varied physical contexts",
            "Work on coordinating verbal responses with appropriate physical positioning"
        ]
        
        # Add specific recommendations based on common issues
        common_contexts = Counter(session.get('context', 'unknown') for session in low_coherence_sessions)
        if common_contexts:
            most_problematic = common_contexts.most_common(1)[0][0]
            plan.append(f"Provide additional practice in {most_problematic} context where coherence challenges are most frequent")
        
        return plan
    
    def _generate_reinforcement_strategies(self, skill: str, examples: List[Dict]) -> List[str]:
        """Generate strategies for reinforcing successful behaviors"""
        strategies = []
        
        # Skill-specific reinforcement
        if 'cooperation' in skill.lower():
            strategies.append("Continue practicing collaborative language and shared decision-making")
        elif 'listening' in skill.lower():
            strategies.append("Reinforce active listening behaviors through positive feedback")
        elif 'turn_taking' in skill.lower():
            strategies.append("Practice turn-taking in various conversational contexts")
        
        # Context-based reinforcement
        contexts = [e.get('context', 'unknown') for e in examples]
        if contexts:
            most_successful_context = Counter(contexts).most_common(1)[0][0]
            strategies.append(f"Leverage success patterns from {most_successful_context} context in other settings")
        
        return strategies
    
    def _identify_key_success_factors(self, successful_sessions: List[Dict]) -> List[str]:
        """Identify key factors contributing to social success"""
        factors = []
        
        # Analyze peer involvement patterns
        all_peers = [peer for session in successful_sessions for peer in session.get('peers_involved', [])]
        if all_peers:
            peer_counter = Counter(all_peers)
            most_successful_peer = peer_counter.most_common(1)[0][0]
            factors.append(f"Strong success rate with peer: {most_successful_peer}")
        
        # Analyze skill combinations
        all_skills = [str(skill) for session in successful_sessions for skill in session.get('skills_demonstrated', [])]
        if all_skills:
            skill_counter = Counter(all_skills)
            top_skills = [skill for skill, count in skill_counter.most_common(3)]
            factors.append(f"Most effective skills: {', '.join(top_skills)}")
        
        return factors
    
    def _generate_success_reinforcement_plan(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate plan for reinforcing successful behavior patterns"""
        plan = []
        
        if not patterns:
            return ["Continue current social interaction practices"]
        
        # Focus on most successful skills
        best_skills = sorted(patterns.items(), key=lambda x: x[1]['average_quality'], reverse=True)
        
        for skill, data in best_skills[:3]:  # Top 3 skills
            plan.append(f"Continue leveraging {skill} - current success rate: {data['average_quality']:.1%}")
            plan.extend(data.get('reinforcement_strategies', []))
        
        return plan
    
    def _generate_coherence_suggestions(self, issues: List[Dict]) -> List[str]:
        """Generate suggestions for specific coherence problems"""
        if not issues:
            return ["No specific coherence issues identified"]
        
        suggestions = [
            "Practice coordinating verbal and physical responses",
            "Focus on maintaining appropriate emotional expression during interactions",
            "Work on integrating social awareness with physical positioning"
        ]
        
        return suggestions
    
    def _generate_actionable_recommendations(self, misalignment: Dict, coherence: Dict, success: Dict, trend: float) -> List[str]:
        """Generate overall actionable recommendations"""
        recommendations = []
        
        # Trend-based recommendations
        if trend > 0.1:
            recommendations.append("🎉 Excellent progress! Continue current social learning approach")
        elif trend < -0.1:
            recommendations.append("⚠️ Address declining performance through increased practice and coaching")
        else:
            recommendations.append("📊 Stable performance - consider introducing new challenges")
        
        # Misalignment recommendations
        if misalignment['total_misalignments'] > 0:
            recommendations.extend(misalignment.get('improvement_suggestions', []))
        
        # Success reinforcement
        if success['total_successful_sessions'] > 0:
            recommendations.extend(success.get('reinforcement_recommendations', [])[:2])
        
        # Coherence improvements
        if coherence and not isinstance(coherence, dict) or 'error' not in coherence:
            if coherence.get('low_coherence_sessions', 0) > 0:
                recommendations.extend(coherence.get('coherence_improvement_plan', [])[:2])
        
        return recommendations[:8]  # Limit to top 8 recommendations
    
    def save_replay_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Save replay analysis to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"replay_analysis_{timestamp}.json"
        filepath = self.analysis_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def create_analysis_report(self, analysis_data: Dict[str, Any]) -> str:
        """Create human-readable analysis report"""
        report = []
        report.append("🎞️ Marcus AGI Social Interaction Replay Analysis")
        report.append("=" * 55)
        
        summary = analysis_data.get('analysis_summary', {})
        report.append(f"📅 Analysis Period: {summary.get('analysis_period', 'unknown')}")
        report.append(f"📊 Sessions Analyzed: {summary.get('total_sessions_analyzed', 0)}")
        report.append(f"📈 Average Success Rate: {summary.get('average_success_rate', 0):.1%}")
        report.append(f"📊 Trend: {summary.get('trend_direction', 'unknown').title()}")
        report.append("")
        
        # Misalignment Analysis
        misalignment = analysis_data.get('misalignment_insights', {})
        report.append("🔍 MISALIGNMENT ANALYSIS")
        report.append(f"   Total Misalignments: {misalignment.get('total_misalignments', 0)}")
        
        patterns = misalignment.get('pattern_analysis', {})
        for issue_type, data in patterns.items():
            report.append(f"   {issue_type.replace('_', ' ').title()}: {data.get('frequency', 0)} occurrences")
        
        suggestions = misalignment.get('improvement_suggestions', [])
        if suggestions:
            report.append("   Improvement Suggestions:")
            for suggestion in suggestions:
                report.append(f"     • {suggestion}")
        report.append("")
        
        # Success Analysis
        success = analysis_data.get('success_insights', {})
        report.append("🌟 SUCCESS PATTERN ANALYSIS")
        report.append(f"   Successful Sessions: {success.get('total_successful_sessions', 0)}")
        report.append(f"   Success Rate: {success.get('success_rate', 0):.1%}")
        
        key_factors = success.get('key_success_factors', [])
        if key_factors:
            report.append("   Key Success Factors:")
            for factor in key_factors:
                report.append(f"     • {factor}")
        report.append("")
        
        # Coherence Analysis
        coherence = analysis_data.get('coherence_insights')
        if coherence and 'error' not in coherence:
            report.append("🎯 COHERENCE ANALYSIS")
            report.append(f"   Average Coherence: {coherence.get('average_coherence', 0):.1%}")
            report.append(f"   Low Coherence Sessions: {coherence.get('low_coherence_sessions', 0)}")
            
            distribution = coherence.get('coherence_distribution', {})
            report.append("   Coherence Distribution:")
            for level, count in distribution.items():
                report.append(f"     {level.title()}: {count}")
            report.append("")
        
        # Actionable Recommendations
        recommendations = analysis_data.get('actionable_recommendations', [])
        if recommendations:
            report.append("🎯 ACTIONABLE RECOMMENDATIONS")
            for i, rec in enumerate(recommendations, 1):
                report.append(f"   {i}. {rec}")
        
        return "\n".join(report)


def generate_replay_analysis(days_back: int = 30) -> Dict[str, str]:
    """Generate and save replay analysis"""
    analyzer = SocialInteractionReplayAnalyzer()
    
    # Load replay data
    replays = analyzer.load_interaction_replays(days_back)
    
    if not replays:
        return {"error": "No replay data found for analysis"}
    
    # Generate analysis
    analysis_data = analyzer.generate_learning_insights(replays)
    
    # Save analysis
    json_path = analyzer.save_replay_analysis(analysis_data)
    
    # Create text report
    text_report = analyzer.create_analysis_report(analysis_data)
    text_path = json_path.replace('.json', '.txt')
    
    with open(text_path, 'w') as f:
        f.write(text_report)
    
    print(f"🎞️ Replay analysis saved to: {json_path}")
    print(f"📋 Report saved to: {text_path}")
    
    return {
        "analysis_path": json_path,
        "report_path": text_path,
        "sessions_analyzed": analysis_data['analysis_summary']['total_sessions_analyzed'],
        "success_rate": analysis_data['analysis_summary']['average_success_rate']
    }


def demo_replay_analyzer():
    """Demonstrate replay analyzer capabilities"""
    print("🎞️ Replay Analyzer Demo")
    print("=" * 30)
    
    result = generate_replay_analysis(days_back=30)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    print(f"\n✅ Analysis Generated Successfully!")
    print(f"   📊 Sessions Analyzed: {result['sessions_analyzed']}")
    print(f"   📈 Average Success Rate: {result['success_rate']:.1%}")
    print(f"   📁 Files: {result['analysis_path']}, {result['report_path']}")
    
    # Display sample analysis report
    with open(result['report_path'], 'r') as f:
        report_lines = f.readlines()
    
    print(f"\n📋 Sample Analysis Preview:")
    for line in report_lines[:25]:  # Show first 25 lines
        print(f"   {line.rstrip()}")
    
    if len(report_lines) > 25:
        print(f"   ... ({len(report_lines) - 25} more lines)")


if __name__ == "__main__":
    demo_replay_analyzer()
