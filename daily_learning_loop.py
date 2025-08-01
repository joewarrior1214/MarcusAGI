from datetime import date
import json
import os
from resilience_mode import generate_analytics_report
from reflection_system import generate_reflection
from concept_graph_system import learn_new_concepts, review_previous_concepts

# Constants
OUTPUT_DIR = "output/sessions"
TODAY = str(date.today())

def run_daily_learning_loop():
    print("🌸 Marcus Daily Session Complete")
    
    # Step 1: Load yesterday’s session (if it exists)
    session_history = []
    if os.path.exists(OUTPUT_DIR):
        for fname in sorted(os.listdir(OUTPUT_DIR)):
            if fname.endswith(".json"):
                with open(os.path.join(OUTPUT_DIR, fname)) as f:
                    session = json.load(f)
                    session_history.append(session)

    # Step 2: Review Concepts
    reviews = review_previous_concepts(session_history)
    
    # Step 3: Learn New Concepts
    new_concepts = learn_new_concepts()
    
    # Step 4: Reflect
    reflection = generate_reflection()

    # Step 5: Save session
    session = {
        "date": TODAY,
        "reviews_completed": len(reviews),
        "concepts_learned": new_concepts,
        "reflection": reflection,
        "retention_rate": 1.0  # Temporary fixed value
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"session_{TODAY}.json")
    with open(out_path, "w") as f:
        json.dump(session, f, indent=2)

    # Print summary
    print(f"📅 Date: {TODAY}")
    print(f"🔄 Reviews completed: {len(reviews)}")
    print(f"🧠 New concepts learned: {len(new_concepts)}")
    print(f"💬 Reflection: {reflection}")
    print(f"🧠 Retention rate: {session['retention_rate']:.2f}")
    print(f"📁 Session saved to: {out_path}")

    return session

if __name__ == "__main__":
    run_daily_learning_loop()
