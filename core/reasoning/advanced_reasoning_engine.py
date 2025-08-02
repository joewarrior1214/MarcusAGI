#!/usr/bin/env python3
"""
Advanced Reasoning Engine for Marcus AGI (Issue #4)

This module implements sophisticated reasoning capabilities that build on 
Marcus's embodied learning foundation to solve complex problems through:

- Causal reasoning from physical experiences
- Analogical reasoning across domains
- Goal-oriented multi-step planning
- Abstract pattern recognition
- Logical inference and deduction

The system leverages Marcus's physical world knowledge to ground abstract
reasoning in concrete experience.
"""

import json
import random
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CausalRelation:
    """Represents a cause-effect relationship learned from experience"""
    cause: str
    effect: str
    confidence: float
    evidence_count: int
    contexts: List[str] = field(default_factory=list)
    
    def strengthen(self, context: str = ""):
        """Strengthen this causal relation with more evidence"""
        self.evidence_count += 1
        self.confidence = min(1.0, self.confidence + 0.1)
        if context and context not in self.contexts:
            self.contexts.append(context)

@dataclass
class ReasoningProblem:
    """Represents a problem that requires reasoning to solve"""
    id: str
    description: str
    domain: str
    goal: str
    givens: List[str]
    constraints: List[str] = field(default_factory=list)
    solution_steps: List[str] = field(default_factory=list)
    difficulty: float = 0.5

@dataclass
class ReasoningResult:
    """Result of applying reasoning to a problem"""
    problem_id: str
    solution: List[str]
    reasoning_type: str
    confidence: float
    steps_taken: int
    analogies_used: List[str] = field(default_factory=list)
    causal_chains: List[str] = field(default_factory=list)
    success: bool = False

class AdvancedReasoningEngine:
    """
    Advanced reasoning engine that builds on Marcus's embodied learning
    to solve complex problems through multiple reasoning strategies
    """
    
    def __init__(self, memory_system=None):
        self.memory_system = memory_system
        self.causal_relations: Dict[str, CausalRelation] = {}
        self.analogies: Dict[str, List[str]] = defaultdict(list)
        self.reasoning_patterns: Dict[str, List[str]] = {}
        self.problem_history: List[ReasoningResult] = []
        
        # Initialize with basic physical reasoning patterns from embodied learning
        self._initialize_physical_reasoning()
    
    def _initialize_physical_reasoning(self):
        """Initialize reasoning patterns based on physical world experience"""
        
        # Basic causal relations from physical world
        physical_causals = [
            CausalRelation("apply_force", "object_moves", 0.9, 5, ["physics", "movement"]),
            CausalRelation("object_too_heavy", "cannot_lift", 0.95, 8, ["physics", "weight"]),
            CausalRelation("hit_boundary", "movement_stops", 0.98, 10, ["physics", "collision"]),
            CausalRelation("drop_object", "object_falls", 0.99, 12, ["physics", "gravity"]),
            CausalRelation("low_energy", "reduced_performance", 0.8, 6, ["biology", "energy"]),
        ]
        
        for causal in physical_causals:
            self.causal_relations[f"{causal.cause}->{causal.effect}"] = causal
        
        # Basic analogical patterns
        self.analogies["resistance_patterns"] = [
            "heavy_object :: more_effort",
            "difficult_concept :: more_practice",
            "complex_problem :: more_time",
            "steep_hill :: more_energy"
        ]
        
        self.analogies["boundary_patterns"] = [
            "physical_wall :: impassable_barrier",
            "skill_limit :: learning_boundary", 
            "energy_depletion :: performance_limit",
            "attention_span :: focus_boundary"
        ]
        
        logger.info("🧠 Advanced Reasoning Engine initialized with physical experience patterns")
    
    def extract_causal_relations_from_session(self, session_data: Dict[str, Any]):
        """Extract new causal relations from a learning session"""
        
        # Look for physical exploration data
        if session_data.get('physical_exploration'):
            key_insights = session_data.get('key_insights', [])
            
            for insight in key_insights:
                self._parse_insight_for_causality(insight, "physical_exploration")
        
        # Look for learning patterns in review results
        review_results = session_data.get('review_results', [])
        for review in review_results:
            if review.get('success'):
                cause = f"practice_{review.get('content', 'concept')}"
                effect = "improved_retention"
                self._add_causal_relation(cause, effect, "learning")
            else:
                cause = f"insufficient_practice_{review.get('content', 'concept')}"
                effect = "poor_retention"
                self._add_causal_relation(cause, effect, "learning")
    
    def _parse_insight_for_causality(self, insight: str, context: str):
        """Parse a learning insight to extract causal relationships"""
        insight_lower = insight.lower()
        
        # Pattern matching for common causal structures
        if "uses energy" in insight_lower:
            self._add_causal_relation("movement", "energy_consumption", context)
        
        if "cannot" in insight_lower and "heavy" in insight_lower:
            self._add_causal_relation("excessive_weight", "lift_failure", context)
        
        if "boundary" in insight_lower or "edge" in insight_lower:
            self._add_causal_relation("reach_limit", "action_blocked", context)
        
        if "see" in insight_lower and "objects" in insight_lower:
            self._add_causal_relation("proximity", "visibility", context)
    
    def _add_causal_relation(self, cause: str, effect: str, context: str):
        """Add or strengthen a causal relation"""
        key = f"{cause}->{effect}"
        
        if key in self.causal_relations:
            self.causal_relations[key].strengthen(context)
        else:
            self.causal_relations[key] = CausalRelation(
                cause=cause, 
                effect=effect, 
                confidence=0.6, 
                evidence_count=1,
                contexts=[context]
            )
    
    def solve_problem_with_reasoning(self, problem: ReasoningProblem) -> ReasoningResult:
        """
        Solve a problem using multiple reasoning strategies
        """
        logger.info(f"🎯 Attempting to solve problem: {problem.description}")
        
        # Try different reasoning approaches
        reasoning_strategies = [
            self._try_causal_reasoning,
            self._try_analogical_reasoning,
            self._try_pattern_recognition,
            self._try_goal_decomposition
        ]
        
        best_result = None
        best_confidence = 0.0
        
        for strategy in reasoning_strategies:
            try:
                result = strategy(problem)
                if result and result.confidence > best_confidence:
                    best_result = result
                    best_confidence = result.confidence
            except Exception as e:
                logger.warning(f"Reasoning strategy failed: {e}")
        
        if best_result:
            best_result.success = best_confidence > 0.6
            self.problem_history.append(best_result)
            logger.info(f"✅ Problem solved with {best_result.reasoning_type} (confidence: {best_confidence:.2f})")
        else:
            # Create a default result indicating failure
            best_result = ReasoningResult(
                problem_id=problem.id,
                solution=["Unable to solve with current reasoning capabilities"],
                reasoning_type="failed_attempt",
                confidence=0.0,
                steps_taken=0,
                success=False
            )
            logger.warning(f"❌ Could not solve problem: {problem.description}")
        
        return best_result
    
    def _try_causal_reasoning(self, problem: ReasoningProblem) -> Optional[ReasoningResult]:
        """Attempt to solve using causal reasoning"""
        
        # Find relevant causal chains
        relevant_causals = []
        for key, causal in self.causal_relations.items():
            if any(given.lower() in causal.cause.lower() or 
                   given.lower() in causal.effect.lower() 
                   for given in problem.givens):
                relevant_causals.append(causal)
        
        if not relevant_causals:
            return None
        
        # Build causal chain toward goal
        solution_steps = []
        causal_chains = []
        
        for causal in relevant_causals[:3]:  # Use top 3 most relevant
            if causal.confidence > 0.7:
                step = f"Since {causal.cause}, we expect {causal.effect}"
                solution_steps.append(step)
                causal_chains.append(f"{causal.cause} → {causal.effect}")
        
        if solution_steps:
            goal_step = f"Therefore, to achieve '{problem.goal}', we should consider these causal relationships"
            solution_steps.append(goal_step)
            
            confidence = sum(c.confidence for c in relevant_causals) / len(relevant_causals)
            
            return ReasoningResult(
                problem_id=problem.id,
                solution=solution_steps,
                reasoning_type="causal_reasoning",
                confidence=confidence,
                steps_taken=len(solution_steps),
                causal_chains=causal_chains
            )
        
        return None
    
    def _try_analogical_reasoning(self, problem: ReasoningProblem) -> Optional[ReasoningResult]:
        """Attempt to solve using analogical reasoning"""
        
        # Find analogous patterns
        relevant_analogies = []
        for category, analogies in self.analogies.items():
            for analogy in analogies:
                if any(given.lower() in analogy.lower() for given in problem.givens):
                    relevant_analogies.append(analogy)
        
        if not relevant_analogies:
            return None
        
        solution_steps = []
        analogies_used = []
        
        for analogy in relevant_analogies[:2]:  # Use top 2 analogies
            parts = analogy.split(" :: ")
            if len(parts) == 2:
                pattern, outcome = parts
                step = f"By analogy with '{pattern}', we expect '{outcome}'"
                solution_steps.append(step)
                analogies_used.append(analogy)
        
        if solution_steps:
            goal_step = f"Applying these analogies to achieve '{problem.goal}'"
            solution_steps.append(goal_step)
            
            return ReasoningResult(
                problem_id=problem.id,
                solution=solution_steps,
                reasoning_type="analogical_reasoning", 
                confidence=0.75,
                steps_taken=len(solution_steps),
                analogies_used=analogies_used
            )
        
        return None
    
    def _try_pattern_recognition(self, problem: ReasoningProblem) -> Optional[ReasoningResult]:
        """Attempt to solve using pattern recognition"""
        
        # Look for patterns in problem history
        similar_problems = [
            result for result in self.problem_history 
            if result.success and problem.domain in result.problem_id.lower()
        ]
        
        if not similar_problems:
            return None
        
        # Use patterns from successful similar problems
        solution_steps = []
        
        if similar_problems:
            pattern_solution = similar_problems[-1]  # Most recent successful pattern
            solution_steps.append(f"Based on similar problem pattern: {pattern_solution.reasoning_type}")
            solution_steps.extend(pattern_solution.solution[:2])  # Adapt first 2 steps
            solution_steps.append(f"Adapting this pattern for: {problem.goal}")
            
            return ReasoningResult(
                problem_id=problem.id,
                solution=solution_steps,
                reasoning_type="pattern_recognition",
                confidence=0.7,
                steps_taken=len(solution_steps)
            )
        
        return None
    
    def _try_goal_decomposition(self, problem: ReasoningProblem) -> Optional[ReasoningResult]:
        """Attempt to solve by decomposing the goal into sub-goals"""
        
        solution_steps = []
        
        # Basic goal decomposition strategy
        solution_steps.append(f"Goal: {problem.goal}")
        solution_steps.append("Breaking down into sub-goals:")
        
        # Simple heuristic decomposition
        if "move" in problem.goal.lower():
            solution_steps.append("1. Check if path is clear")
            solution_steps.append("2. Ensure sufficient energy")
            solution_steps.append("3. Execute movement")
        elif "lift" in problem.goal.lower() or "grab" in problem.goal.lower():
            solution_steps.append("1. Assess object weight")
            solution_steps.append("2. Position appropriately")
            solution_steps.append("3. Apply appropriate force")
        elif "learn" in problem.goal.lower():
            solution_steps.append("1. Identify knowledge gaps")
            solution_steps.append("2. Practice systematically")
            solution_steps.append("3. Review and reinforce")
        else:
            solution_steps.append("1. Analyze current state")
            solution_steps.append("2. Identify required actions")
            solution_steps.append("3. Execute step by step")
        
        solution_steps.append("4. Verify goal achievement")
        
        return ReasoningResult(
            problem_id=problem.id,
            solution=solution_steps,
            reasoning_type="goal_decomposition",
            confidence=0.65,
            steps_taken=len(solution_steps)
        )
    
    def get_reasoning_insights(self) -> Dict[str, Any]:
        """Get insights about the reasoning system's current state"""
        
        total_problems = len(self.problem_history)
        successful_problems = sum(1 for p in self.problem_history if p.success)
        
        reasoning_types = defaultdict(int)
        for problem in self.problem_history:
            reasoning_types[problem.reasoning_type] += 1
        
        return {
            'total_causal_relations': len(self.causal_relations),
            'total_problems_attempted': total_problems,
            'successful_problems': successful_problems,
            'success_rate': successful_problems / total_problems if total_problems > 0 else 0,
            'reasoning_type_distribution': dict(reasoning_types),
            'strongest_causal_relations': [
                {'relation': key, 'confidence': causal.confidence}
                for key, causal in sorted(
                    self.causal_relations.items(), 
                    key=lambda x: x[1].confidence, 
                    reverse=True
                )[:5]
            ]
        }

# Test problems for the reasoning engine
def create_test_problems() -> List[ReasoningProblem]:
    """Create test problems to validate reasoning capabilities"""
    
    problems = [
        ReasoningProblem(
            id="physics_movement_1",
            description="How to move a heavy object across the room",
            domain="physics",
            goal="move heavy object to target location",
            givens=["heavy object", "target location", "limited energy"],
            constraints=["object weight > lift capacity", "energy consumption per movement"],
            difficulty=0.7
        ),
        
        ReasoningProblem(
            id="learning_retention_1", 
            description="How to improve memory retention of difficult concepts",
            domain="learning",
            goal="achieve 90% retention of difficult concepts",
            givens=["difficult concepts", "current retention 60%", "study time available"],
            constraints=["limited study time", "concept difficulty"],
            difficulty=0.6
        ),
        
        ReasoningProblem(
            id="planning_energy_1",
            description="How to complete all tasks with limited energy",
            domain="planning",
            goal="complete all assigned tasks before energy depletion",
            givens=["task list", "current energy level", "energy cost per task"],
            constraints=["no energy regeneration", "tasks must be completed in order"],
            difficulty=0.8
        )
    ]
    
    return problems

# Testing function
def test_reasoning_engine():
    """Test the advanced reasoning engine"""
    
    print("🧠 Testing Advanced Reasoning Engine...")
    
    # Initialize engine
    reasoning_engine = AdvancedReasoningEngine()
    
    # Create test session data with physical insights
    test_session = {
        'physical_exploration': True,
        'key_insights': [
            'Moving uses energy',
            'Heavy objects cannot be lifted', 
            'World has edges I cannot pass',
            'I can see objects within 3 spaces'
        ],
        'review_results': [
            {'content': 'math_concept', 'success': True},
            {'content': 'reading_concept', 'success': False}
        ]
    }
    
    # Extract causal relations from session
    reasoning_engine.extract_causal_relations_from_session(test_session)
    
    # Test with problems
    test_problems = create_test_problems()
    
    results = []
    for problem in test_problems:
        result = reasoning_engine.solve_problem_with_reasoning(problem)
        results.append(result)
        
        print(f"\n🎯 Problem: {problem.description}")
        print(f"   Solution ({result.reasoning_type}):")
        for i, step in enumerate(result.solution, 1):
            print(f"   {i}. {step}")
        print(f"   Confidence: {result.confidence:.2f} | Success: {result.success}")
    
    # Show reasoning insights
    insights = reasoning_engine.get_reasoning_insights()
    print(f"\n📊 Reasoning Engine Insights:")
    print(f"   Causal Relations: {insights['total_causal_relations']}")
    print(f"   Success Rate: {insights['success_rate']:.1%}")
    print(f"   Reasoning Types: {insights['reasoning_type_distribution']}")
    
    return reasoning_engine, results

if __name__ == "__main__":
    test_reasoning_engine()
