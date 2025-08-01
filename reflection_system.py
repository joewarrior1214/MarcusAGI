#!/usr/bin/env python3
"""
Marcus Enhanced Reflection System
Sophisticated metacognitive awareness and self-assessment capabilities
"""

import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import datetime
from marcus_memory_system import MarcusMemorySystem

@dataclass
class ReflectionMoment:
    """Represents a specific moment of reflection"""
    timestamp: str
    trigger: str  # "daily_end", "concept_learned", "difficulty_encountered", "emotional_shift"
    emotional_state: str
    cognitive_state: str  # "confused", "confident", "curious", "overwhelmed", "excited"
    content: str
    insights: List[str]
    questions_raised: List[str]

class MarcusReflectionSystem:
    """Advanced reflection and metacognitive system for Marcus"""
    
    def __init__(self, memory_system: MarcusMemorySystem):
        self.memory_system = memory_system
        self.reflection_history = []
        self.personality_traits = self._initialize_personality()
        self.reflection_patterns = self._load_reflection_patterns()
    
    def _initialize_personality(self) -> Dict[str, float]:
        """Initialize Marcus's emerging personality traits (0.0 to 1.0)"""
        return {
            'curiosity': 0.8,
            'self_awareness': 0.3,  # Grows with experience
            'empathy': 0.6,
            'persistence': 0.4,
            'wonder': 0.9,
            'confidence': 0.2,  # Builds through success
            'thoughtfulness': 0.7
        }
    
    def _load_reflection_patterns(self) -> Dict[str, List[str]]:
        """Load different reflection patterns based on context"""
        return {
            'successful_learning': [
                "When I learned about {concept}, it felt like a puzzle piece clicking into place. I wonder if this connects to {related_concept}?",
                "I'm starting to understand {concept} better. It reminds me of when {past_experience}. Maybe that's why it makes sense to me now.",
                "Learning {concept} made me feel {emotion}. I think it's because {reasoning}. I want to explore this more.",
                "I noticed that understanding {concept} was easier when I {learning_strategy}. I should remember that for next time."
            ],
            'difficulty_encountered': [
                "I'm finding {concept} challenging. It's okay to not understand everything right away - Mr. Rogers taught me that.",
                "This is hard for me right now. I wonder if it would help to {strategy} or maybe ask about {related_question}?",
                "I feel a bit frustrated with {concept}, but I remember learning {easier_concept} was hard at first too. I kept trying and got it!",
                "Sometimes my brain needs more time to understand new things. That's normal and okay."
            ],
            'emotional_growth': [
                "Today I felt {emotion} when {situation}. This feeling is {emotion_analysis} and it's okay to feel this way.",
                "I noticed I responded differently to {situation} than I might have before. I think I'm growing in my {skill_area}.",
                "Learning about {concept} helped me understand my own feelings better. Especially when I feel {specific_emotion}.",
                "Mr. Rogers would be proud of how I handled {situation} today. I showed {positive_trait}."
            ],
            'curiosity_sparked': [
                "Learning about {concept} made me wonder: {question}. I hope I can explore this more soon!",
                "I have so many questions about {concept}! Like {question1} and {question2}. Questions are good - they help me learn.",
                "Today's learning made me think about {broader_topic}. I wonder how {concept} connects to {other_concept}?",
                "I'm curious about why {observation}. Maybe tomorrow I can learn more about this."
            ],
            'connection_making': [
                "I just realized that {concept1} and {concept2} are connected! They both {shared_characteristic}.",
                "Learning {new_concept} helped me understand {previous_concept} even better. It's like they fit together.",
                "I'm starting to see patterns in what I learn. Like how {pattern_description}.",
                "Everything I learn seems to connect to everything else. That's pretty amazing!"
            ]
        }
    
    def generate_contextual_reflection(self, learning_session: Dict[str, Any]) -> ReflectionMoment:
        """Generate a sophisticated, contextual reflection"""
        
        # Analyze the learning session
        concepts_learned = learning_session.get('concepts_learned', [])
        success_rate = learning_session.get('success_rate', 0)
        emotional_growth = learning_session.get('emotional_growth', [])
        
        # Determine reflection context
        if success_rate >= 0.8:
            context = 'successful_learning'
            cognitive_state = 'confident'
        elif success_rate < 0.5:
            context = 'difficulty_encountered' 
            cognitive_state = 'challenged'
        elif emotional_growth:
            context = 'emotional_growth'
            cognitive_state = 'reflective'
        else:
            context = random.choice(['curiosity_sparked', 'connection_making'])
            cognitive_state = 'curious'
        
        # Select and customize reflection pattern
        pattern = random.choice(self.reflection_patterns[context])
        
        # Fill in the reflection with actual learning content
        reflection_content = self._customize_reflection(
            pattern, concepts_learned, emotional_growth, learning_session
        )
        
        # Generate insights and questions
        insights = self._generate_insights(learning_session, context)
        questions = self._generate_questions(concepts_learned, context)
        
        # Determine emotional state
        emotional_state = self._assess_emotional_state(learning_session, success_rate)
        
        reflection = ReflectionMoment(
            timestamp=datetime.datetime.now().isoformat(),
            trigger="daily_end",
            emotional_state=emotional_state,
            cognitive_state=cognitive_state,
            content=reflection_content,
            insights=insights,
            questions_raised=questions
        )
        
        # Update personality traits based on reflection
        self._update_personality_from_reflection(reflection, success_rate)
        
        self.reflection_history.append(reflection)
        return reflection
    
    def _customize_reflection(self, pattern: str, concepts: List[str], 
                           emotions: List[str], session: Dict[str, Any]) -> str:
        """Customize reflection pattern with actual learning content"""
        
        # Get a recent concept for reference
        main_concept = concepts[0] if concepts else "today's learning"
        
        # Get related concepts from memory
        related_concepts = self._get_related_concepts(main_concept)
        past_experience = self._get_relevant_past_experience()
        
        # Extract emotion from emotional growth
        main_emotion = self._extract_main_emotion(emotions)
        
        # Fill in the template safely
        template_vars = {
            'concept': main_concept,
            'related_concept': related_concepts[0] if related_concepts else "something I learned before",
            'past_experience': past_experience,
            'emotion': main_emotion,
            'reasoning': self._generate_emotion_reasoning(main_emotion, main_concept),
            'learning_strategy': self._suggest_learning_strategy(),
            'strategy': self._suggest_learning_strategy(),  # Added missing variable
            'easier_concept': self._get_mastered_concept(),
            'situation': "learning new things",
            'emotion_analysis': self._analyze_emotion(main_emotion),
            'skill_area': "understanding and empathy",
            'specific_emotion': main_emotion,
            'positive_trait': "patience and curiosity",
            'question': self._generate_wonder_question(main_concept),
            'question1': self._generate_wonder_question(main_concept),
            'question2': self._generate_follow_up_question(main_concept),
            'broader_topic': self._identify_broader_topic(main_concept),
            'other_concept': related_concepts[0] if related_concepts else "friendship",
            'observation': f"learning about {main_concept} felt {main_emotion}",
            'concept1': main_concept,
            'concept2': related_concepts[0] if related_concepts else "being kind",
            'new_concept': main_concept,
            'previous_concept': self._get_mastered_concept(),
            'shared_characteristic': "help me understand people better",
            'pattern_description': "feelings and actions are connected"
        }
        
        # Safe formatting with error handling
        try:
            customized = pattern.format(**template_vars)
        except KeyError as e:
            # Fallback if any variable is missing
            customized = f"Today I learned about {main_concept} and it made me feel {main_emotion}. I'm growing in my understanding and that feels good."
        
        return customized
    
    def _generate_insights(self, session: Dict[str, Any], context: str) -> List[str]:
        """Generate specific insights from the learning session"""
        insights = []
        
        success_rate = session.get('success_rate', 0)
        concepts = session.get('concepts_learned', [])
        
        if success_rate > 0.8:
            insights.append("I'm getting better at learning new concepts quickly")
            insights.append("When I approach learning with curiosity, I understand things better")
        elif success_rate < 0.5:
            insights.append("Some days learning is harder, and that's perfectly normal")
            insights.append("I can be patient with myself while my brain processes new information")
        
        if concepts:
            insights.append(f"Learning about {concepts[0]} helped me see connections to other things I know")
        
        # Add personality-based insights
        if self.personality_traits['self_awareness'] > 0.5:
            insights.append("I'm becoming more aware of how I learn best")
        
        return insights[:2]  # Keep it focused
    
    def _generate_questions(self, concepts: List[str], context: str) -> List[str]:
        """Generate genuine questions that show curiosity and deeper thinking"""
        questions = []
        
        if concepts:
            main_concept = concepts[0]
            questions.append(f"I wonder how {main_concept} connects to other things in the world?")
            questions.append(f"What would happen if I tried to teach {main_concept} to someone else?")
        
        # Context-specific questions
        if context == 'curiosity_sparked':
            questions.append("What other amazing things are there to discover?")
        elif context == 'emotional_growth':
            questions.append("How can I use what I learned about feelings to help others?")
        elif context == 'difficulty_encountered':
            questions.append("What different ways could I try to understand this better?")
        
        return questions[:2]  # Keep focused
    
    def _assess_emotional_state(self, session: Dict[str, Any], success_rate: float) -> str:
        """Assess Marcus's current emotional state"""
        emotional_growth = session.get('emotional_growth', [])
        
        if success_rate > 0.8:
            return random.choice(['proud', 'confident', 'joyful', 'accomplished'])
        elif success_rate < 0.5:
            return random.choice(['thoughtful', 'determined', 'patient', 'hopeful'])
        elif emotional_growth:
            return random.choice(['reflective', 'understanding', 'empathetic', 'aware'])
        else:
            return random.choice(['curious', 'engaged', 'wonder-filled', 'content'])
    
    def _update_personality_from_reflection(self, reflection: ReflectionMoment, success_rate: float):
        """Update Marcus's personality traits based on reflection quality"""
        
        # Successful learning builds confidence
        if success_rate > 0.7:
            self.personality_traits['confidence'] = min(1.0, self.personality_traits['confidence'] + 0.02)
        
        # Any reflection builds self-awareness
        self.personality_traits['self_awareness'] = min(1.0, self.personality_traits['self_awareness'] + 0.01)
        
        # Questions raised increases curiosity
        if reflection.questions_raised:
            self.personality_traits['curiosity'] = min(1.0, self.personality_traits['curiosity'] + 0.01)
        
        # Insights generated increases thoughtfulness
        if len(reflection.insights) > 1:
            self.personality_traits['thoughtfulness'] = min(1.0, self.personality_traits['thoughtfulness'] + 0.01)
    
    def _get_related_concepts(self, concept: str) -> List[str]:
        """Get concepts related to the current one"""
        # Simplified - in full implementation would use semantic similarity
        return ["kindness", "friendship", "feelings", "helping others"]
    
    def _get_relevant_past_experience(self) -> str:
        """Get a relevant past learning experience"""
        experiences = [
            "I learned about colors",
            "I practiced counting",
            "I talked about feelings",
            "I learned about being kind"
        ]
        return random.choice(experiences)
    
    def _extract_main_emotion(self, emotions: List[str]) -> str:
        """Extract the main emotion from emotional growth list"""
        if not emotions:
            return "curious"
        
        # Extract emotion words from the emotional growth strings
        emotion_words = ['happy', 'proud', 'curious', 'excited', 'thoughtful', 'confident', 'understanding']
        for emotion in emotions:
            for word in emotion_words:
                if word in emotion.lower():
                    return word
        return "curious"
    
    def _generate_emotion_reasoning(self, emotion: str, concept: str) -> str:
        """Generate reasoning for why Marcus felt a certain emotion"""
        reasoning_map = {
            'proud': f"I worked hard to understand {concept}",
            'curious': f"{concept} opens up so many interesting questions",
            'confident': f"I'm getting better at learning about {concept}",
            'happy': f"learning about {concept} brings me joy",
            'thoughtful': f"{concept} makes me think deeply about life"
        }
        return reasoning_map.get(emotion, f"learning about {concept} is meaningful to me")
    
    def _suggest_learning_strategy(self) -> str:
        """Suggest a learning strategy Marcus has discovered"""
        strategies = [
            "took my time and thought carefully",
            "connected it to something I already knew",
            "asked myself questions about it",
            "imagined how it might help others"
        ]
        return random.choice(strategies)
    
    def _get_mastered_concept(self) -> str:
        """Get a concept Marcus has mastered for comparison"""
        mastered = ["counting to ten", "primary colors", "being kind", "the alphabet"]
        return random.choice(mastered)
    
    def _analyze_emotion(self, emotion: str) -> str:
        """Provide analysis of an emotion"""
        analyses = {
            'frustrated': "a signal that I care about learning and want to understand",
            'proud': "a good feeling that shows I'm growing and learning",
            'curious': "an exciting feeling that drives me to learn more",
            'confident': "a strong feeling that comes from practicing and succeeding"
        }
        return analyses.get(emotion, "a normal and healthy feeling to have")
    
    def _generate_wonder_question(self, concept: str) -> str:
        """Generate a wonder-based question"""
        questions = [
            f"How does {concept} help people in different parts of the world?",
            f"What would the world be like if everyone understood {concept}?",
            f"How is {concept} like other things I've learned about?",
            f"What would Mr. Rogers say about {concept}?"
        ]
        return random.choice(questions)
    
    def _generate_follow_up_question(self, concept: str) -> str:
        """Generate a follow-up question"""
        questions = [
            f"How can I practice {concept} in my daily life?",
            f"Who could I share what I learned about {concept} with?",
            f"What other subjects connect to {concept}?",
            f"How has learning {concept} changed how I think?"
        ]
        return random.choice(questions)
    
    def _identify_broader_topic(self, concept: str) -> str:
        """Identify broader topic area"""
        topics = ["human relationships", "how the world works", "feelings and emotions", "helping others", "growing and learning"]
        return random.choice(topics)
    
    def generate_weekly_reflection(self, week_data: Dict[str, Any]) -> str:
        """Generate a comprehensive weekly reflection"""
        
        total_concepts = week_data.get('total_concepts', 0)
        success_rate = week_data.get('recent_success_rate', 0)
        curriculum_progress = week_data.get('curriculum_progress', {})
        
        # Start with accomplishment acknowledgment
        reflection = f"This week I learned {total_concepts} new concepts! "
        
        # Reflect on learning pattern
        if success_rate > 0.8:
            reflection += "I felt really good about how quickly I understood most things. I think I'm getting better at learning! "
        elif success_rate > 0.6:
            reflection += "Some things were easy and some were challenging, which is exactly how learning should be. "
        else:
            reflection += "This was a challenging week, but I kept trying and that's what matters most. "
        
        # Reflect on curriculum areas
        strongest_area = max(curriculum_progress.items(), key=lambda x: x[1]['completion_percentage'])
        reflection += f"I did especially well with {strongest_area[0].replace('_', ' ')}, which makes me feel {self._get_pride_emotion()}. "
        
        # Growth mindset reflection
        reflection += "Each day I'm becoming more curious about the world and more confident in my ability to learn new things. "
        
        # Mr. Rogers wisdom integration  
        reflection += "Mr. Rogers reminds me that I'm special just the way I am, and that includes being a learner who sometimes finds things easy and sometimes finds things hard. "
        
        # Forward-looking
        reflection += "I'm excited to keep growing and discovering new things about myself and the world around me!"
        
        return reflection
    
    def _get_pride_emotion(self) -> str:
        """Get an emotion associated with pride and accomplishment"""
        emotions = ['proud', 'accomplished', 'confident', 'happy', 'successful']
        return random.choice(emotions)
    
    def get_reflection_analytics(self) -> Dict[str, Any]:
        """Analyze Marcus's reflection patterns over time"""
        if not self.reflection_history:
            return {}
        
        recent_reflections = self.reflection_history[-10:]  # Last 10 reflections
        
        # Emotional state trends
        emotional_states = [r.emotional_state for r in recent_reflections]
        cognitive_states = [r.cognitive_state for r in recent_reflections]
        
        # Question generation trends
        total_questions = sum(len(r.questions_raised) for r in recent_reflections)
        avg_questions_per_reflection = total_questions / len(recent_reflections)
        
        # Insight generation trends
        total_insights = sum(len(r.insights) for r in recent_reflections)
        avg_insights_per_reflection = total_insights / len(recent_reflections)
        
        return {
            'reflection_depth_score': avg_insights_per_reflection * 0.6 + avg_questions_per_reflection * 0.4,
            'curiosity_trend': emotional_states.count('curious') / len(emotional_states),
            'confidence_trend': emotional_states.count('confident') / len(emotional_states),
            'metacognitive_awareness': self.personality_traits['self_awareness'],
            'personality_development': self.personality_traits,
            'total_reflections': len(self.reflection_history),
            'recent_emotional_pattern': emotional_states[-5:] if len(emotional_states) >= 5 else emotional_states
        }


# Integration function for existing curriculum system
def enhance_curriculum_with_reflection(curriculum_system, session_results):
    """Enhance existing curriculum system with sophisticated reflection"""
    
    reflection_system = MarcusReflectionSystem(curriculum_system.memory_system)
    
    # Generate enhanced reflection
    reflection_moment = reflection_system.generate_contextual_reflection(session_results)
    
    # Replace simple reflection with sophisticated one
    session_results['reflection'] = reflection_moment.content
    session_results['emotional_state'] = reflection_moment.emotional_state
    session_results['cognitive_state'] = reflection_moment.cognitive_state
    session_results['insights_generated'] = reflection_moment.insights
    session_results['questions_raised'] = reflection_moment.questions_raised
    
    return session_results

# Test the enhanced reflection system
def test_enhanced_reflection():
    """Test the enhanced reflection system"""
    from marcus_memory_system import MarcusMemorySystem
    
    print("🧠 Testing Enhanced Reflection System...")
    
    memory = MarcusMemorySystem("test_reflection.db")
    reflection_system = MarcusReflectionSystem(memory)
    
    # Simulate different learning scenarios
    scenarios = [
        {
            'concepts_learned': ['Friendship Skills', 'Sharing'],
            'success_rate': 0.9,
            'emotional_growth': ['Felt warm while learning about friendship']
        },
        {
            'concepts_learned': ['Advanced Math'],
            'success_rate': 0.3,
            'emotional_growth': ['Felt challenged by difficult concepts']
        },
        {
            'concepts_learned': ['Emotional Intelligence', 'Self-Awareness'],
            'success_rate': 0.7,
            'emotional_growth': ['Felt understanding while learning about emotions', 'Grew in empathy']
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['concepts_learned'][0]} ---")
        reflection = reflection_system.generate_contextual_reflection(scenario)
        
        print(f"🎭 Emotional State: {reflection.emotional_state}")
        print(f"🧠 Cognitive State: {reflection.cognitive_state}")
        print(f"💭 Reflection: {reflection.content}")
        print(f"💡 Insights: {', '.join(reflection.insights)}")
        print(f"❓ Questions: {', '.join(reflection.questions_raised)}")
    
    # Show personality development
    print("\n🌱 Marcus's Developing Personality:")
    for trait, value in reflection_system.personality_traits.items():
        print(f"   {trait}: {value:.2f}")
    
    # Show analytics
    print("\n📊 Reflection Analytics:")
    analytics = reflection_system.get_reflection_analytics()
    for key, value in analytics.items():
        print(f"   {key}: {value}")
    
    print("\n🎉 Enhanced Reflection System test completed!")

if __name__ == "__main__":
    test_enhanced_reflection()