#!/usr/bin/env python3
"""
Run multiple learning sessions to test analytics and progression
"""

import os
import json
import time
from datetime import date, datetime, timedelta

# First, let's check what was saved
print("📁 Checking saved sessions...")
print("=" * 50)

OUTPUT_DIR = "output/sessions"

if os.path.exists(OUTPUT_DIR):
    files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.json')])
    print(f"Found {len(files)} saved files:")
    for f in files:
        print(f"  - {f}")
        
    # Read and display the most recent session
    if files:
        latest = files[-1]
        with open(os.path.join(OUTPUT_DIR, latest), 'r') as f:
            session = json.load(f)
        
        print(f"\n📄 Latest session ({latest}):")
        print(json.dumps(session, indent=2))

# Now let's simulate multiple days of learning
print("\n" + "="*50)
print("🚀 Simulating multiple learning sessions...")
print("=" * 50)

# We'll modify the date in the sessions to simulate multiple days
from daily_learning_loop import run_daily_learning_loop
import daily_learning_loop

# Save original TODAY value
original_today = daily_learning_loop.TODAY

try:
    # Run sessions for the past few days
    for days_ago in range(4, -1, -1):  # 4, 3, 2, 1, 0 days ago
        # Calculate the date
        session_date = date.today() - timedelta(days=days_ago)
        date_str = str(session_date)
        
        # Temporarily change the date in the module
        daily_learning_loop.TODAY = date_str
        
        print(f"\n📅 Running session for {date_str}...")
        print("-" * 30)
        
        # Skip if session already exists
        session_file = os.path.join(OUTPUT_DIR, f"session_{date_str}.json")
        if os.path.exists(session_file):
            print(f"  ⏭️  Session already exists, skipping...")
            continue
        
        # Run the session
        session = run_daily_learning_loop()
        
        print(f"  ✅ Session for {date_str} completed!")
        time.sleep(0.5)  # Small delay to see the output

finally:
    # Restore original date
    daily_learning_loop.TODAY = original_today

# Now let's check the analytics
print("\n" + "="*50)
print("📊 Checking generated analytics...")
print("=" * 50)

analytics_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith('analytics_')]
if analytics_files:
    print(f"Found {len(analytics_files)} analytics files:")
    for f in analytics_files:
        print(f"  - {f}")
    
    # Display the latest analytics
    if analytics_files:
        latest_analytics = sorted(analytics_files)[-1]
        with open(os.path.join(OUTPUT_DIR, latest_analytics), 'r') as f:
            analytics = json.load(f)
        
        print(f"\n📈 Latest Analytics ({latest_analytics}):")
        print(json.dumps(analytics, indent=2))
else:
    print("No analytics generated yet (need 5+ sessions)")

# Summary
print("\n" + "="*50)
print("🎯 Summary")
print("=" * 50)

all_sessions = [f for f in os.listdir(OUTPUT_DIR) if f.startswith('session_')]
print(f"Total sessions saved: {len(all_sessions)}")
print(f"Analytics files: {len(analytics_files)}")

if len(all_sessions) >= 5:
    print("\n✅ You now have enough data for analytics!")
    print("Each new session will generate an analytics report.")
else:
    print(f"\n📊 Need {5 - len(all_sessions)} more sessions for analytics to start.")

print("\n💡 Next steps:")
print("1. Run 'python daily_learning_loop.py' daily")
print("2. After 5+ sessions, analytics will be generated automatically")
print("3. Check output/sessions/ for all saved data")
print("4. Consider upgrading to resilience_mode.py for advanced features")