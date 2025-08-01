#!/usr/bin/env python3
"""
Corrected Daily Learning Loop
Removed the problematic import from resilience_mode
"""

from datetime import date
import json
import os
from reflection_system import generate_reflection
from concept_graph_system import learn_new_concepts, review_previous_concepts

# Constants
OUTPUT_DIR = "output/sessions"
TODAY = str(date.today())

def generate_analytics_report(session_history):
    """Generate simple analytics from session history"""
    if not session_history:
        return {
            "total_sessions": 0,
            "total_concepts": 0,
            "average_retention": 0
        }
    
    total_concepts = sum(len(s.get('concepts_learned', [])) for s in session_history)
    total_reviews = sum(s.get('reviews_completed', 0) for s in session_history)
    avg_retention = sum(s.get('retention_rate', 0) for s in session_history) / len(session_history)
    
    return {
        "total_sessions": len(session_history),
        "total_concepts_learned": total_concepts,
        "total_reviews_completed": total_reviews,
        "average_retention_rate": round(avg_retention, 2),
        "concepts_per_session": round(total_concepts / len(session_history), 1) if session_history else 0
    }

def run_daily_learning_loop():
    print("🌸 Marcus Daily Session Complete")
    print("=" * 50)
    
    # Step 1: Load yesterday's session (if it exists)
    session_history = []
    if os.path.exists(OUTPUT_DIR):
        for fname in sorted(os.listdir(OUTPUT_DIR)):
            if fname.endswith(".json"):
                try:
                    with open(os.path.join(OUTPUT_DIR, fname)) as f:
                        session = json.load(f)
                        session_history.append(session)
                except Exception as e:
                    print(f"Warning: Could not load {fname}: {e}")

    print(f"📚 Loaded {len(session_history)} previous sessions")

    # Step 2: Review Concepts
    print("\n🔄 Reviewing previous concepts...")
    reviews = review_previous_concepts(session_history)
    for i, review in enumerate(reviews, 1):
        print(f"  {i}. Reviewing: {review}")
    
    # Step 3: Learn New Concepts
    print("\n📘 Learning new concepts...")
    new_concepts = learn_new_concepts()
    for i, concept in enumerate(new_concepts, 1):
        print(f"  {i}. Learning: {concept}")
    
    # Step 4: Reflect
    print("\n💭 Generating reflection...")
    reflection = generate_reflection()

    # Step 5: Calculate retention rate (simplified)
    # In a real system, this would be based on review performance
    if reviews:
        retention_rate = 0.75 + (len(reviews) * 0.05)  # Better with more reviews
        retention_rate = min(retention_rate, 1.0)  # Cap at 100%
    else:
        retention_rate = 1.0  # Perfect for first session

    # Step 6: Create session data
    session = {
        "date": TODAY,
        "reviews_completed": len(reviews),
        "concepts_learned": new_concepts,
        "reflection": reflection,
        "retention_rate": retention_rate
    }

    # Step 7: Save session
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"session_{TODAY}.json")
    with open(out_path, "w") as f:
        json.dump(session, f, indent=2)

    # Step 8: Generate analytics if we have enough sessions
    if len(session_history) >= 5:
        print("\n📊 Generating analytics report...")
        analytics = generate_analytics_report(session_history + [session])
        analytics_path = os.path.join(OUTPUT_DIR, f"analytics_{TODAY}.json")
        with open(analytics_path, "w") as f:
            json.dump(analytics, f, indent=2)
        
        print(f"📈 Analytics Summary:")
        print(f"  - Total sessions: {analytics['total_sessions']}")
        print(f"  - Total concepts learned: {analytics['total_concepts_learned']}")
        print(f"  - Average retention: {analytics['average_retention_rate']:.1%}")
        print(f"  - Concepts per session: {analytics['concepts_per_session']}")

    # Print summary
    print("\n" + "="*50)
    print("✅ Session Complete!")
    print("="*50)
    print(f"📅 Date: {TODAY}")
    print(f"🔄 Reviews completed: {len(reviews)}")
    print(f"🧠 New concepts learned: {len(new_concepts)}")
    print(f"💬 Reflection: {reflection}")
    print(f"🎯 Retention rate: {session['retention_rate']:.2%}")
    print(f"📁 Session saved to: {out_path}")

    return session

if __name__ == "__main__":
    run_daily_learning_loop()