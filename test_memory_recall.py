from memory_system import MarcusMemorySystem

# Initialize Marcus's memory system
memory = MarcusMemorySystem("marcus_memory.db")

# Fetch all learned concepts
concepts = memory.fetch_all_concepts()

# Display them
print("\n🧠 Marcus's Learned Concepts:")
for concept in concepts:
    print(f"🔹 ID: {concept.id}")
    print(f"   Content: {concept.content}")
    print(f"   Subject: {concept.subject}")
    print(f"   Grade: {concept.grade_level}")
    print(f"   Emotion: {concept.emotional_context}")
    print("-" * 40)
