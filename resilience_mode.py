#!/usr/bin/env python3
"""
Fixed Daily Learning Loop - Standalone version
This version works without importing from resilience_mode
"""

from datetime import date
import json
import os

# Import your existing systems
try:
    from reflection_system import generate_reflection
    from concept_graph_system import learn_new_concepts, review_previous_concepts
except ImportError:
    print("⚠️ Warning: Could not import reflection_system or concept_graph_system")
    print("Using mock functions instead")
    
    # Mock functions if imports fail
    def generate_reflection():
        return "Today I learned new things and practiced what I know!"
    
    def learn_new_concepts():
        return ["colors", "shapes", "numbers", "letters", "kindness"]
    
    def review_previous_concepts(history):
        return ["review1", "review2", "review3"]

# Constants
OUTPUT_DIR = "output/sessions"
TODAY = str(date.today())

def generate_analytics_report(session_history):
    """Simple analytics report generation"""
    if not session_history:
        return {}
    
    total_concepts = sum(len(s.get('concepts_learned', [])) for s in session_history)
    total_reviews = sum(s.get('reviews_completed', 0) for s in session_history)
    avg_retention = sum(s.get('retention_rate', 0) for s in session_history) / len(session_history)
    
    return {
        'total_sessions': len(session_history),
        'total_concepts_learned': total_concepts,
        'total_reviews': total_reviews,
        'average_retention': avg_retention,
        'daily_average_concepts': total_concepts / len(session_history) if session_history else 0
    }

def run_daily_learning_loop():
    print("🌸 Marcus Daily Learning Session")
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
                    print(f"Could not load {fname}: {e}")

    print(f"📚 Loaded {len(session_history)} previous sessions")

    # Step 2: Review Concepts
    print("\n🔄 Reviewing previous concepts...")
    reviews = review_previous_concepts(session_history)
    print(f"  Completed {len(reviews)} reviews")
    
    # Step 3: Learn New Concepts
    print("\n📘 Learning new concepts...")
    new_concepts = learn_new_concepts()
    for concept in new_concepts:
        print(f"  ✓ Learned: {concept}")
    
    # Step 4: Reflect
    print("\n💭 Generating reflection...")
    reflection = generate_reflection()

    # Step 5: Calculate retention rate
    # For now, simulate based on review count
    retention_rate = 0.85 if len(reviews) > 0 else 1.0

    # Step 6: Save session
    session = {
        "date": TODAY,
        "reviews_completed": len(reviews),
        "concepts_learned": new_concepts,
        "reflection": reflection,
        "retention_rate": retention_rate
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{TODAY}_session.json")
    with open(out_path, "w") as f:
        json.dump(session, f, indent=2)

    # Step 7: Generate analytics if we have enough history
    if len(session_history) >= 7:
        print("\n📊 Generating analytics...")
        analytics = generate_analytics_report(session_history + [session])
        analytics_path = os.path.join(OUTPUT_DIR, f"{TODAY}_analytics.json")
        with open(analytics_path, "w") as f:
            json.dump(analytics, f, indent=2)
        print(f"  Analytics saved to: {analytics_path}")

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