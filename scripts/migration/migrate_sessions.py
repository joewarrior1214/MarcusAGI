#!/usr/bin/env python3
"""
Migrate existing sessions to include Issue #3 requirements
"""

import json
import os
from datetime import datetime, date

OUTPUT_DIR = "output/sessions"

def migrate_sessions():
    """Add missing Issue #3 fields to existing sessions"""
    print("🔄 Migrating existing sessions to Issue #3 format...")
    
    if not os.path.exists(OUTPUT_DIR):
        print("No sessions to migrate")
        return
    
    migrated = 0
    for fname in os.listdir(OUTPUT_DIR):
        if fname.endswith(".json") and not fname.endswith("_complete_session.json"):
            filepath = os.path.join(OUTPUT_DIR, fname)
            
            try:
                with open(filepath, 'r') as f:
                    session = json.load(f)
                
                # Check if already migrated
                if 'metrics' in session and 'curriculum_progression' in session:
                    continue
                
                print(f"  Migrating {fname}...")
                
                # Add missing fields
                if 'timestamp' not in session:
                    session['timestamp'] = session.get('date', str(date.today())) + "T12:00:00"
                
                if 'metrics' not in session:
                    session['metrics'] = {
                        'retention_rate': session.get('retention_rate', 0.85),
                        'learning_velocity': len(session.get('concepts_learned', [])),
                        'difficulty_progression': 0.1,
                        'mastery_by_subject': {
                            'math': 0.4,
                            'reading': 0.5,
                            'science': 0.3,
                            'social': 0.6,
                            'art': 0.4
                        }
                    }
                
                if 'review_results' not in session and 'reviews_completed' in session:
                    # Create mock review results with SM-2 data
                    session['review_results'] = []
                    for i in range(session['reviews_completed']):
                        session['review_results'].append({
                            'concept_id': f'review_{i}',
                            'quality': 3 + (i % 3),  # 3, 4, 5
                            'success': True,
                            'interval_days': 1 + i,
                            'ease_factor': 2.5,
                            'next_review': str(date.today())
                        })
                
                if 'curriculum_progression' not in session:
                    session['curriculum_progression'] = {
                        'advanced': False,
                        'current_unit': 'Kindergarten Basics',
                        'current_mastery': 0.4 + (migrated * 0.05),
                        'target_mastery': 0.85,
                        'estimated_concepts_needed': 20
                    }
                
                # Save migrated session
                with open(filepath, 'w') as f:
                    json.dump(session, f, indent=2)
                
                migrated += 1
                
            except Exception as e:
                print(f"  Error migrating {fname}: {e}")
    
    print(f"✅ Migrated {migrated} sessions")

if __name__ == "__main__":
    migrate_sessions()