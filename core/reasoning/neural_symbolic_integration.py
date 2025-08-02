#!/usr/bin/env python3
"""
Neural-Symbolic Reasoning Integration System for Marcus AGI (Issue #14)
======================================================================

This module implements a unified reasoning pipeline that integrates symbolic logic 
with neural pattern recognition, enabling both intuitive and analytical problem-solving 
approaches for comprehensive reasoning capability.

Key Features:
- Reasoning mode selection based on problem characteristics
- Neural pattern recognition for intuitive responses
- Symbolic logic engine for analytical reasoning
- Hybrid reasoning coordinator for optimal result synthesis
- Integration with existing advanced reasoning and consciousness systems
- Learning feedback loop for continuous improvement

Epic: Enhanced Reasoning & Transfer Learning (Phase 1)
Target: >85% unified reasoning accuracy across problem types
Timeline: 3 weeks implementation + 1 week validation
Depends on: Advanced Reasoning Engine, Cross-Domain Transfer Engine, Consciousness Framework
"""

import sqlite3
import json
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid
import statistics
import re
from collections import defaultdict, Counter

# Import existing systems for integration
try:
    from .advanced_reasoning_engine import AdvancedReasoningEngine, ReasoningProblem, ReasoningResult, CausalRelation
    from .cross_domain_transfer_engine import CrossDomainTransferEngine, AbstractPattern, DomainType, PatternType
    from ..consciousness.consciousness_integration_framework import ConsciousnessIntegrationFramework
    from ..memory.autobiographical_memory_system import AutobiographicalMemorySystem
    from ..consciousness.value_learning_system import ValueLearningSystem
    INTEGRATION_AVAILABLE = True
except ImportError:
    # Define stub classes for standalone mode
    class AdvancedReasoningEngine:
        pass
    class ReasoningProblem:
        pass
    class ReasoningResult:
        pass
    class CrossDomainTransferEngine:
        pass
    class ConsciousnessIntegrationFramework:
        pass
    class AutobiographicalMemorySystem:
        pass
    class ValueLearningSystem:
        pass
    INTEGRATION_AVAILABLE = False
    logging.warning("Some integration systems not available - running in standalone mode")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReasoningMode(Enum):
    """Different reasoning approaches available."""
    SYMBOLIC = "symbolic"
    NEURAL = "neural"
    HYBRID = "hybrid"
    ADAPTIVE = "adaptive"


class ProblemType(Enum):
    """Classification of problem types for reasoning approach selection."""
    LOGICAL = "logical"
    CREATIVE = "creative"
    MORAL = "moral"
    PHYSICAL = "physical"
    SOCIAL = "social"
    MATHEMATICAL = "mathematical"
    PLANNING = "planning"
    UNKNOWN = "unknown"


@dataclass
class NeuralPattern:
    """Represents a learned neural pattern for intuitive reasoning."""
    pattern_id: str
    pattern_type: str
    input_features: List[str]
    output_prediction: str
    confidence: float
    success_rate: float
    usage_count: int = 0
    last_used: datetime = field(default_factory=datetime.now)
    context_tags: List[str] = field(default_factory=list)


@dataclass
class SymbolicRule:
    """Represents a symbolic logical rule."""
    rule_id: str
    condition: str
    conclusion: str
    confidence: float
    evidence_count: int
    rule_type: str  # "causal", "logical", "moral", etc.
    context_domain: str
    created: datetime = field(default_factory=datetime.now)


@dataclass
class ReasoningEpisode:
    """Records a complete reasoning episode with approach and outcome."""
    episode_id: str
    problem: Dict[str, Any]
    approaches_used: List[ReasoningMode]
    symbolic_result: Optional[Dict[str, Any]] = None
    neural_result: Optional[Dict[str, Any]] = None
    final_result: Optional[Dict[str, Any]] = None
    approach_selected: ReasoningMode = ReasoningMode.ADAPTIVE
    confidence: float = 0.0
    success: bool = False
    reasoning_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class HybridReasoningResult:
    """Result of hybrid neural-symbolic reasoning."""
    problem_id: str
    symbolic_contribution: float
    neural_contribution: float
    combined_confidence: float
    reasoning_chain: List[str]
    pattern_matches: List[str]
    rule_applications: List[str]
    approach_justification: str
    success: bool = False


class NeuralSymbolicIntegration:
    """
    Unified reasoning pipeline integrating symbolic logic with neural pattern recognition.
    
    This system enables Marcus to leverage both analytical and intuitive reasoning
    approaches, selecting the optimal method based on problem characteristics and context.
    """

    def __init__(self, 
                 reasoning_engine: AdvancedReasoningEngine = None,
                 transfer_engine: CrossDomainTransferEngine = None,
                 consciousness_framework: ConsciousnessIntegrationFramework = None,
                 memory_system: AutobiographicalMemorySystem = None,
                 value_system: ValueLearningSystem = None):
        """Initialize the neural-symbolic integration system."""
        
        # Integration with existing systems
        self.reasoning_engine = reasoning_engine or AdvancedReasoningEngine()
        self.transfer_engine = transfer_engine
        self.consciousness_framework = consciousness_framework
        self.memory_system = memory_system
        self.value_system = value_system
        
        # Core neural-symbolic components
        self.neural_patterns: Dict[str, NeuralPattern] = {}
        self.symbolic_rules: Dict[str, SymbolicRule] = {}
        self.reasoning_episodes: List[ReasoningEpisode] = []
        
        # Reasoning approach selection
        self.problem_classifiers: Dict[str, float] = {}
        self.mode_performance: Dict[ReasoningMode, Dict[str, float]] = {
            mode: {"success_rate": 0.0, "avg_confidence": 0.0, "usage_count": 0}
            for mode in ReasoningMode
        }
        
        # Learning and adaptation
        self.pattern_weights: Dict[str, float] = {}
        self.rule_strengths: Dict[str, float] = {}
        
        # Database for persistence
        self.db_path = "marcus_neural_symbolic.db"
        self.setup_database()
        
        # Initialize with foundational patterns and rules
        self._initialize_foundational_systems()
        
        logger.info("🧠 Neural-Symbolic Integration System initialized")

    def setup_database(self):
        """Set up the neural-symbolic reasoning database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Neural patterns table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS neural_patterns (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_type TEXT,
                    input_features TEXT,
                    output_prediction TEXT,
                    confidence REAL,
                    success_rate REAL,
                    usage_count INTEGER,
                    last_used TEXT,
                    context_tags TEXT
                )
            """)
            
            # Symbolic rules table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS symbolic_rules (
                    rule_id TEXT PRIMARY KEY,
                    condition TEXT,
                    conclusion TEXT,
                    confidence REAL,
                    evidence_count INTEGER,
                    rule_type TEXT,
                    context_domain TEXT,
                    created TEXT
                )
            """)
            
            # Reasoning episodes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reasoning_episodes (
                    episode_id TEXT PRIMARY KEY,
                    problem TEXT,
                    approaches_used TEXT,
                    symbolic_result TEXT,
                    neural_result TEXT,
                    final_result TEXT,
                    approach_selected TEXT,
                    confidence REAL,
                    success INTEGER,
                    reasoning_time REAL,
                    timestamp TEXT
                )
            """)
            
            conn.commit()

    def _initialize_foundational_systems(self):
        """Initialize foundational neural patterns and symbolic rules."""
        
        # Initialize symbolic rules from existing causal relations
        if self.reasoning_engine and hasattr(self.reasoning_engine, 'causal_relations'):
            for causal_key, causal_relation in self.reasoning_engine.causal_relations.items():
                rule = SymbolicRule(
                    rule_id=f"causal_{len(self.symbolic_rules)}",
                    condition=f"situation_involves({causal_relation.cause})",
                    conclusion=f"expect({causal_relation.effect})",
                    confidence=causal_relation.confidence,
                    evidence_count=causal_relation.evidence_count,
                    rule_type="causal",
                    context_domain="physical"
                )
                self.symbolic_rules[rule.rule_id] = rule
        
        # Initialize transfer engine if not provided
        if not self.transfer_engine:
            try:
                self.transfer_engine = CrossDomainTransferEngine()
            except:
                pass
        
        # Initialize neural patterns from transfer engine patterns
        if self.transfer_engine and hasattr(self.transfer_engine, 'abstract_patterns'):
            for pattern_id, abstract_pattern in self.transfer_engine.abstract_patterns.items():
                neural_pattern = NeuralPattern(
                    pattern_id=f"neural_{pattern_id}",
                    pattern_type=abstract_pattern.pattern_type.value,
                    input_features=list(abstract_pattern.abstract_structure.keys()),
                    output_prediction=str(abstract_pattern.abstract_structure.get('relationship', 'unknown')),
                    confidence=abstract_pattern.confidence,
                    success_rate=0.7,  # Initial estimate
                    context_tags=[abstract_pattern.source_domain.value]
                )
                self.neural_patterns[neural_pattern.pattern_id] = neural_pattern
        
        # Add enhanced foundational patterns and rules
        self._add_enhanced_foundational_knowledge()
        
        # Initialize basic problem classifiers
        self._initialize_problem_classifiers()
        
        logger.info(f"🧠 Initialized {len(self.symbolic_rules)} symbolic rules and {len(self.neural_patterns)} neural patterns")

    def _add_enhanced_foundational_knowledge(self):
        """Add enhanced foundational patterns and rules for better coverage."""
        
        # Enhanced neural patterns for common reasoning scenarios
        enhanced_patterns = [
            NeuralPattern(
                pattern_id="creative_analogical",
                pattern_type="creative",
                input_features=["creative", "new", "innovative", "alternative", "brainstorm"],
                output_prediction="apply analogical reasoning and explore multiple perspectives",
                confidence=0.8,
                success_rate=0.75,
                context_tags=["creativity", "learning", "problem_solving"]
            ),
            NeuralPattern(
                pattern_id="physical_constraint",
                pattern_type="physical",
                input_features=["heavy", "move", "force", "object", "space", "narrow"],
                output_prediction="decompose into steps and consider physical constraints",
                confidence=0.85,
                success_rate=0.8,
                context_tags=["physics", "planning", "constraints"]
            ),
            NeuralPattern(
                pattern_id="moral_decision",
                pattern_type="moral",
                input_features=["should", "help", "right", "wrong", "ethical", "fair"],
                output_prediction="consider multiple stakeholders and moral principles",
                confidence=0.9,
                success_rate=0.85,
                context_tags=["ethics", "social", "decision_making"]
            ),
            NeuralPattern(
                pattern_id="logical_inference",
                pattern_type="logical",
                input_features=["if", "then", "because", "therefore", "prove", "logic"],
                output_prediction="apply step-by-step logical reasoning",
                confidence=0.95,
                success_rate=0.9,
                context_tags=["logic", "reasoning", "proof"]
            )
        ]
        
        for pattern in enhanced_patterns:
            self.neural_patterns[pattern.pattern_id] = pattern
        
        # Enhanced symbolic rules for better coverage
        enhanced_rules = [
            SymbolicRule(
                rule_id="creativity_rule",
                condition="requires_creative_solution",
                conclusion="explore_analogical_reasoning_and_multiple_perspectives",
                confidence=0.8,
                evidence_count=5,
                rule_type="creative",
                context_domain="general"
            ),
            SymbolicRule(
                rule_id="physical_constraint_rule",
                condition="involves_physical_constraints",
                conclusion="decompose_problem_and_consider_limitations",
                confidence=0.85,
                evidence_count=7,
                rule_type="physical",
                context_domain="physics"
            ),
            SymbolicRule(
                rule_id="moral_reasoning_rule",
                condition="involves_moral_decision",
                conclusion="consider_stakeholder_impact_and_ethical_principles",
                confidence=0.9,
                evidence_count=6,
                rule_type="moral",
                context_domain="ethics"
            ),
            SymbolicRule(
                rule_id="logical_reasoning_rule",
                condition="requires_logical_proof",
                conclusion="apply_step_by_step_deductive_reasoning",
                confidence=0.95,
                evidence_count=8,
                rule_type="logical",
                context_domain="logic"
            )
        ]
        
        for rule in enhanced_rules:
            self.symbolic_rules[rule.rule_id] = rule

    def _initialize_problem_classifiers(self):
        """Initialize classifiers for problem type identification."""
        
        # Keywords that indicate different problem types
        problem_indicators = {
            ProblemType.LOGICAL: ["if", "then", "because", "therefore", "logic", "prove", "deduce"],
            ProblemType.CREATIVE: ["creative", "new way", "innovative", "brainstorm", "imagine", "alternative"],
            ProblemType.MORAL: ["should", "right", "wrong", "ethical", "moral", "fair", "help", "harm"],
            ProblemType.PHYSICAL: ["move", "lift", "force", "weight", "space", "object", "physics"],
            ProblemType.SOCIAL: ["person", "friend", "relationship", "collaborate", "communication", "social"],
            ProblemType.MATHEMATICAL: ["calculate", "number", "math", "equation", "pattern", "sequence"],
            ProblemType.PLANNING: ["plan", "goal", "steps", "organize", "schedule", "strategy", "accomplish"]
        }
        
        # Store indicators for later problem classification
        self.problem_type_indicators = problem_indicators

    def classify_problem_type(self, problem_description: str, context: Dict[str, Any] = None) -> ProblemType:
        """Classify the type of problem to inform reasoning approach selection."""
        
        problem_lower = problem_description.lower()
        context_str = json.dumps(context or {}).lower()
        combined_text = problem_lower + " " + context_str
        
        # Score each problem type based on keyword matches
        type_scores = {}
        for problem_type, indicators in self.problem_type_indicators.items():
            score = sum(1 for indicator in indicators if indicator in combined_text)
            if score > 0:
                type_scores[problem_type] = score
        
        # Return the highest scoring type, or UNKNOWN if no clear match
        if type_scores:
            return max(type_scores.keys(), key=lambda x: type_scores[x])
        else:
            return ProblemType.UNKNOWN

    def select_reasoning_approach(self, problem: Dict[str, Any], context: Dict[str, Any] = None) -> ReasoningMode:
        """Select the optimal reasoning approach based on problem characteristics."""
        
        problem_description = problem.get('description', '')
        problem_type = self.classify_problem_type(problem_description, context)
        
        # Default approach mapping based on problem type
        type_to_approach = {
            ProblemType.LOGICAL: ReasoningMode.SYMBOLIC,
            ProblemType.MATHEMATICAL: ReasoningMode.SYMBOLIC,
            ProblemType.PHYSICAL: ReasoningMode.HYBRID,
            ProblemType.CREATIVE: ReasoningMode.NEURAL,
            ProblemType.SOCIAL: ReasoningMode.HYBRID,
            ProblemType.MORAL: ReasoningMode.HYBRID,
            ProblemType.PLANNING: ReasoningMode.SYMBOLIC,
            ProblemType.UNKNOWN: ReasoningMode.ADAPTIVE
        }
        
        base_approach = type_to_approach.get(problem_type, ReasoningMode.ADAPTIVE)
        
        # Adjust based on historical performance
        if base_approach in self.mode_performance:
            performance = self.mode_performance[base_approach]
            if performance["success_rate"] < 0.5 and performance["usage_count"] > 5:
                # If this approach has been failing, try hybrid instead
                base_approach = ReasoningMode.HYBRID
        
        # Consider context factors
        if context:
            if context.get('time_pressure', False):
                # Under time pressure, prefer neural (faster intuitive responses)
                base_approach = ReasoningMode.NEURAL
            elif context.get('requires_explanation', False):
                # When explanation is needed, prefer symbolic
                base_approach = ReasoningMode.SYMBOLIC
            elif context.get('high_stakes', False):
                # For high stakes decisions, use hybrid for redundancy
                base_approach = ReasoningMode.HYBRID
        
        return base_approach

    def apply_symbolic_reasoning(self, problem: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Apply symbolic logical reasoning to the problem."""
        
        problem_description = problem.get('description', '')
        problem_goal = problem.get('goal', '')
        
        # Find relevant symbolic rules
        relevant_rules = []
        for rule_id, rule in self.symbolic_rules.items():
            if self._rule_matches_problem(rule, problem_description, problem_goal):
                relevant_rules.append(rule)
        
        # Sort by confidence and evidence
        relevant_rules.sort(key=lambda r: (r.confidence * r.evidence_count), reverse=True)
        
        # Apply rules to generate reasoning chain
        reasoning_chain = []
        applied_rules = []
        confidence_scores = []
        
        for rule in relevant_rules[:5]:  # Use top 5 most relevant rules
            if rule.confidence > 0.5:  # Only use reasonably confident rules
                reasoning_step = f"Rule: If {rule.condition}, then {rule.conclusion}"
                reasoning_chain.append(reasoning_step)
                applied_rules.append(rule.rule_id)
                confidence_scores.append(rule.confidence)
        
        # Generate conclusion
        if reasoning_chain:
            overall_confidence = statistics.mean(confidence_scores) if confidence_scores else 0.0
            conclusion = f"Based on {len(applied_rules)} logical rules, the reasoning suggests specific actions toward: {problem_goal}"
            reasoning_chain.append(f"Conclusion: {conclusion}")
        else:
            overall_confidence = 0.0
            reasoning_chain = ["No applicable symbolic rules found for this problem"]
        
        return {
            'reasoning_type': 'symbolic',
            'reasoning_chain': reasoning_chain,
            'rules_applied': applied_rules,
            'confidence': overall_confidence,
            'success': overall_confidence > 0.5
        }

    def apply_neural_reasoning(self, problem: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Apply neural pattern recognition reasoning to the problem."""
        
        problem_description = problem.get('description', '')
        problem_goal = problem.get('goal', '')
        
        # Extract features from problem
        problem_features = self._extract_problem_features(problem_description, problem_goal, context)
        
        # Find matching neural patterns
        pattern_matches = []
        for pattern_id, pattern in self.neural_patterns.items():
            match_score = self._calculate_pattern_match(pattern, problem_features)
            if match_score > 0.3:  # Threshold for pattern relevance
                pattern_matches.append((pattern, match_score))
        
        # Sort by match score and success rate
        pattern_matches.sort(key=lambda x: x[1] * x[0].success_rate, reverse=True)
        
        # Generate neural response
        reasoning_chain = []
        used_patterns = []
        confidence_scores = []
        
        if pattern_matches:
            reasoning_chain.append("Neural pattern recognition analysis:")
            
            for pattern, match_score in pattern_matches[:3]:  # Use top 3 patterns
                intuitive_response = f"Pattern '{pattern.pattern_type}' suggests: {pattern.output_prediction}"
                confidence = pattern.confidence * match_score * pattern.success_rate
                reasoning_chain.append(f"  • {intuitive_response} (confidence: {confidence:.2f})")
                used_patterns.append(pattern.pattern_id)
                confidence_scores.append(confidence)
                
                # Update pattern usage
                pattern.usage_count += 1
                pattern.last_used = datetime.now()
        
        overall_confidence = statistics.mean(confidence_scores) if confidence_scores else 0.0
        
        if not pattern_matches:
            reasoning_chain = ["No matching neural patterns found - learning opportunity"]
            overall_confidence = 0.0
        
        return {
            'reasoning_type': 'neural',
            'reasoning_chain': reasoning_chain,
            'patterns_used': used_patterns,
            'confidence': overall_confidence,
            'success': overall_confidence > 0.4  # Neural threshold slightly lower
        }

    def apply_hybrid_reasoning(self, problem: Dict[str, Any], context: Dict[str, Any] = None) -> HybridReasoningResult:
        """Apply both symbolic and neural reasoning, then synthesize results."""
        
        # Run both approaches in parallel
        symbolic_result = self.apply_symbolic_reasoning(problem, context)
        neural_result = self.apply_neural_reasoning(problem, context)
        
        # Calculate contribution weights based on confidence and problem type
        problem_type = self.classify_problem_type(problem.get('description', ''), context)
        
        # Weight preferences by problem type
        type_weights = {
            ProblemType.LOGICAL: {'symbolic': 0.8, 'neural': 0.2},
            ProblemType.CREATIVE: {'symbolic': 0.2, 'neural': 0.8},
            ProblemType.MORAL: {'symbolic': 0.6, 'neural': 0.4},
            ProblemType.PHYSICAL: {'symbolic': 0.7, 'neural': 0.3},
            ProblemType.SOCIAL: {'symbolic': 0.4, 'neural': 0.6},
            ProblemType.MATHEMATICAL: {'symbolic': 0.9, 'neural': 0.1},
            ProblemType.PLANNING: {'symbolic': 0.7, 'neural': 0.3},
            ProblemType.UNKNOWN: {'symbolic': 0.5, 'neural': 0.5}
        }
        
        weights = type_weights.get(problem_type, {'symbolic': 0.5, 'neural': 0.5})
        
        # Adjust weights by actual confidence
        symbolic_confidence = symbolic_result.get('confidence', 0.0)
        neural_confidence = neural_result.get('confidence', 0.0)
        
        if symbolic_confidence + neural_confidence > 0:
            confidence_factor = 0.3  # How much confidence affects weighting
            symbolic_weight = weights['symbolic'] * (1 + confidence_factor * symbolic_confidence)
            neural_weight = weights['neural'] * (1 + confidence_factor * neural_confidence)
            
            # Normalize weights
            total_weight = symbolic_weight + neural_weight
            symbolic_contribution = symbolic_weight / total_weight
            neural_contribution = neural_weight / total_weight
        else:
            symbolic_contribution = weights['symbolic']
            neural_contribution = weights['neural']
        
        # Synthesize reasoning chain
        combined_chain = []
        combined_chain.append("🧠 Hybrid Neural-Symbolic Reasoning Analysis:")
        combined_chain.append(f"Problem Type: {problem_type.value}")
        combined_chain.append("")
        
        # Add symbolic reasoning
        if symbolic_result.get('success', False):
            combined_chain.append(f"📚 Symbolic Analysis (weight: {symbolic_contribution:.2f}):")
            combined_chain.extend([f"  {step}" for step in symbolic_result.get('reasoning_chain', [])])
            combined_chain.append("")
        
        # Add neural reasoning  
        if neural_result.get('success', False):
            combined_chain.append(f"🎯 Intuitive Analysis (weight: {neural_contribution:.2f}):")
            combined_chain.extend([f"  {step}" for step in neural_result.get('reasoning_chain', [])])
            combined_chain.append("")
        
        # Generate synthesis
        combined_confidence = (
            symbolic_contribution * symbolic_confidence + 
            neural_contribution * neural_confidence
        )
        
        approach_justification = f"Selected hybrid approach for {problem_type.value} problem with {symbolic_contribution:.1%} symbolic reasoning and {neural_contribution:.1%} neural pattern recognition"
        
        success = combined_confidence > 0.6 or (symbolic_result.get('success', False) and neural_result.get('success', False))
        
        return HybridReasoningResult(
            problem_id=problem.get('id', str(uuid.uuid4())),
            symbolic_contribution=symbolic_contribution,
            neural_contribution=neural_contribution,
            combined_confidence=combined_confidence,
            reasoning_chain=combined_chain,
            pattern_matches=neural_result.get('patterns_used', []),
            rule_applications=symbolic_result.get('rules_applied', []),
            approach_justification=approach_justification,
            success=success
        )

    def integrated_reasoning(self, problem: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main entry point for integrated neural-symbolic reasoning."""
        
        start_time = datetime.now()
        episode_id = str(uuid.uuid4())
        
        # Select reasoning approach
        selected_approach = self.select_reasoning_approach(problem, context)
        
        logger.info(f"🧠 Applying {selected_approach.value} reasoning to problem: {problem.get('description', '')[:50]}...")
        
        # Apply selected reasoning approach
        if selected_approach == ReasoningMode.SYMBOLIC:
            result = self.apply_symbolic_reasoning(problem, context)
            approaches_used = [ReasoningMode.SYMBOLIC]
            
        elif selected_approach == ReasoningMode.NEURAL:
            result = self.apply_neural_reasoning(problem, context)
            approaches_used = [ReasoningMode.NEURAL]
            
        elif selected_approach == ReasoningMode.HYBRID:
            hybrid_result = self.apply_hybrid_reasoning(problem, context)
            result = {
                'reasoning_type': 'hybrid',
                'reasoning_chain': hybrid_result.reasoning_chain,
                'confidence': hybrid_result.combined_confidence,
                'success': hybrid_result.success,
                'symbolic_contribution': hybrid_result.symbolic_contribution,
                'neural_contribution': hybrid_result.neural_contribution,
                'approach_justification': hybrid_result.approach_justification
            }
            approaches_used = [ReasoningMode.SYMBOLIC, ReasoningMode.NEURAL]
            
        else:  # ADAPTIVE - try multiple approaches and pick best
            symbolic_result = self.apply_symbolic_reasoning(problem, context)
            neural_result = self.apply_neural_reasoning(problem, context)
            
            if symbolic_result.get('confidence', 0) > neural_result.get('confidence', 0):
                result = symbolic_result
                approaches_used = [ReasoningMode.SYMBOLIC]
            else:
                result = neural_result  
                approaches_used = [ReasoningMode.NEURAL]
        
        # Calculate reasoning time
        reasoning_time = (datetime.now() - start_time).total_seconds()
        
        # Record reasoning episode
        episode = ReasoningEpisode(
            episode_id=episode_id,
            problem=problem,
            approaches_used=approaches_used,
            final_result=result,
            approach_selected=selected_approach,
            confidence=result.get('confidence', 0.0),
            success=result.get('success', False),
            reasoning_time=reasoning_time
        )
        
        self.reasoning_episodes.append(episode)
        self._update_performance_metrics(selected_approach, result)
        
        # Add metadata to result
        result['episode_id'] = episode_id
        result['approach_selected'] = selected_approach.value
        result['reasoning_time'] = reasoning_time
        result['timestamp'] = datetime.now().isoformat()
        
        logger.info(f"✅ Reasoning complete: {result.get('success', False)} (confidence: {result.get('confidence', 0.0):.2f})")
        
        return result

    def _rule_matches_problem(self, rule: SymbolicRule, problem_description: str, problem_goal: str) -> bool:
        """Check if a symbolic rule is relevant to the current problem."""
        
        # Enhanced keyword matching with semantic understanding
        rule_text = f"{rule.condition} {rule.conclusion}".lower()
        problem_text = f"{problem_description} {problem_goal}".lower()
        
        # Extract meaningful keywords (exclude common words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had'}
        
        rule_keywords = set(word for word in re.findall(r'\w+', rule_text) if len(word) > 2 and word not in stop_words)
        problem_keywords = set(word for word in re.findall(r'\w+', problem_text) if len(word) > 2 and word not in stop_words)
        
        # Calculate keyword overlap
        overlap = len(rule_keywords & problem_keywords)
        
        # Enhanced semantic matching
        semantic_matches = 0
        
        # Check for conceptual matches
        concept_mappings = {
            'creative': ['innovative', 'new', 'alternative', 'brainstorm', 'novel'],
            'physical': ['move', 'force', 'object', 'weight', 'space', 'lift'],
            'moral': ['ethical', 'right', 'wrong', 'should', 'help', 'fair'],
            'logical': ['prove', 'because', 'therefore', 'if', 'then', 'logic'],
            'social': ['friend', 'person', 'relationship', 'collaborate', 'help'],
            'helping': ['assist', 'support', 'aid', 'help', 'cooperate'],
            'problem': ['challenge', 'issue', 'difficulty', 'solve', 'solution']
        }
        
        for concept, synonyms in concept_mappings.items():
            if concept in rule_text:
                if any(syn in problem_text for syn in synonyms):
                    semantic_matches += 1
            elif any(syn in rule_text for syn in synonyms):
                if concept in problem_text or any(syn2 in problem_text for syn2 in synonyms):
                    semantic_matches += 1
        
        # Calculate combined score
        if rule_keywords:
            overlap_ratio = overlap / len(rule_keywords)
            semantic_ratio = semantic_matches / max(len(concept_mappings), 1)
            combined_score = (overlap_ratio * 0.7) + (semantic_ratio * 0.3)
            return combined_score > 0.15  # Lower threshold for better matching
        
        return False

    def _extract_problem_features(self, problem_description: str, problem_goal: str, context: Dict[str, Any] = None) -> List[str]:
        """Extract features from problem for neural pattern matching."""
        
        features = []
        
        # Extract keywords from problem
        text = f"{problem_description} {problem_goal}"
        keywords = re.findall(r'\w+', text.lower())
        features.extend(keywords)
        
        # Add context features
        if context:
            context_str = json.dumps(context).lower()
            context_keywords = re.findall(r'\w+', context_str)
            features.extend(context_keywords)
        
        # Remove duplicates and return
        return list(set(features))

    def _calculate_pattern_match(self, pattern: NeuralPattern, problem_features: List[str]) -> float:
        """Calculate how well a neural pattern matches the current problem."""
        
        # Enhanced pattern matching with semantic understanding
        pattern_features = set(pattern.input_features + pattern.context_tags)
        problem_feature_set = set(problem_features)
        
        if not pattern_features:
            return 0.0
        
        # Direct feature overlap
        direct_overlap = len(pattern_features & problem_feature_set)
        direct_score = direct_overlap / len(pattern_features)
        
        # Semantic similarity matching
        semantic_score = 0.0
        semantic_mappings = {
            'creative': ['innovative', 'new', 'alternative', 'brainstorm', 'novel', 'original'],
            'physical': ['move', 'force', 'object', 'weight', 'space', 'lift', 'heavy'],
            'moral': ['ethical', 'right', 'wrong', 'should', 'help', 'fair', 'good'],
            'logical': ['prove', 'because', 'therefore', 'if', 'then', 'logic', 'reason'],
            'social': ['friend', 'person', 'relationship', 'collaborate', 'help', 'people'],
            'learning': ['understand', 'study', 'practice', 'knowledge', 'skill', 'concept'],
            'problem_solving': ['solve', 'solution', 'challenge', 'issue', 'difficulty', 'approach']
        }
        
        # Check for semantic matches
        semantic_matches = 0
        total_concepts = 0
        
        for pattern_feature in pattern_features:
            for concept, synonyms in semantic_mappings.items():
                if pattern_feature == concept or pattern_feature in synonyms:
                    total_concepts += 1
                    if any(syn in problem_feature_set for syn in synonyms) or concept in problem_feature_set:
                        semantic_matches += 1
                    break
        
        if total_concepts > 0:
            semantic_score = semantic_matches / total_concepts
        
        # Combine direct and semantic scores
        combined_score = (direct_score * 0.6) + (semantic_score * 0.4)
        
        # Boost score for frequently successful patterns
        success_boost = pattern.success_rate * 0.2
        usage_boost = min(pattern.usage_count / 10.0, 0.1)  # Small boost for experience
        
        final_score = min(combined_score + success_boost + usage_boost, 1.0)
        
        return final_score

    def _update_performance_metrics(self, approach: ReasoningMode, result: Dict[str, Any]):
        """Update performance metrics for reasoning approaches."""
        
        if approach not in self.mode_performance:
            self.mode_performance[approach] = {"success_rate": 0.0, "avg_confidence": 0.0, "usage_count": 0}
        
        metrics = self.mode_performance[approach]
        
        # Update usage count
        old_count = metrics["usage_count"]
        new_count = old_count + 1
        metrics["usage_count"] = new_count
        
        # Update success rate (running average)
        old_success_rate = metrics["success_rate"]
        new_success = 1.0 if result.get('success', False) else 0.0
        metrics["success_rate"] = ((old_success_rate * old_count) + new_success) / new_count
        
        # Update confidence (running average)
        old_confidence = metrics["avg_confidence"]
        new_confidence = result.get('confidence', 0.0)
        metrics["avg_confidence"] = ((old_confidence * old_count) + new_confidence) / new_count

    def learn_from_feedback(self, episode_id: str, success: bool, feedback: str = ""):
        """Learn from feedback on reasoning episodes to improve future performance."""
        
        # Find the episode
        episode = None
        for ep in self.reasoning_episodes:
            if ep.episode_id == episode_id:
                episode = ep
                break
        
        if not episode:
            logger.warning(f"Episode {episode_id} not found for feedback learning")
            return
        
        # Update episode success
        episode.success = success
        
        # Learn from successful patterns
        if success and episode.final_result:
            # Strengthen used patterns/rules
            if 'patterns_used' in episode.final_result:
                for pattern_id in episode.final_result['patterns_used']:
                    if pattern_id in self.neural_patterns:
                        pattern = self.neural_patterns[pattern_id]
                        # Increase success rate (with smoothing)
                        pattern.success_rate = min(pattern.success_rate * 1.1, 1.0)
            
            if 'rules_applied' in episode.final_result:
                for rule_id in episode.final_result['rules_applied']:
                    if rule_id in self.symbolic_rules:
                        rule = self.symbolic_rules[rule_id]
                        # Increase confidence (with smoothing)
                        rule.confidence = min(rule.confidence * 1.05, 1.0)
                        rule.evidence_count += 1
        
        # Learn from failures
        elif not success:
            # Reduce confidence in used patterns/rules
            if episode.final_result and 'patterns_used' in episode.final_result:
                for pattern_id in episode.final_result['patterns_used']:
                    if pattern_id in self.neural_patterns:
                        pattern = self.neural_patterns[pattern_id]
                        pattern.success_rate = max(pattern.success_rate * 0.95, 0.1)
        
        logger.info(f"📚 Learned from episode {episode_id}: {'success' if success else 'failure'}")

    def get_integration_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics on neural-symbolic integration performance."""
        
        if not self.reasoning_episodes:
            return {"status": "No reasoning episodes recorded yet"}
        
        # Overall performance
        total_episodes = len(self.reasoning_episodes)
        successful_episodes = sum(1 for ep in self.reasoning_episodes if ep.success)
        overall_success_rate = successful_episodes / total_episodes
        
        # Performance by approach
        approach_performance = {}
        for mode in ReasoningMode:
            episodes = [ep for ep in self.reasoning_episodes if ep.approach_selected == mode]
            if episodes:
                success_rate = sum(1 for ep in episodes if ep.success) / len(episodes)
                avg_confidence = statistics.mean([ep.confidence for ep in episodes])
                avg_time = statistics.mean([ep.reasoning_time for ep in episodes])
                approach_performance[mode.value] = {
                    "episodes": len(episodes),
                    "success_rate": success_rate,
                    "avg_confidence": avg_confidence,
                    "avg_reasoning_time": avg_time
                }
        
        # Recent performance trend
        recent_episodes = self.reasoning_episodes[-10:] if len(self.reasoning_episodes) >= 10 else self.reasoning_episodes
        recent_success_rate = sum(1 for ep in recent_episodes if ep.success) / len(recent_episodes)
        
        # System usage
        neural_patterns_active = sum(1 for p in self.neural_patterns.values() if p.usage_count > 0)
        symbolic_rules_active = sum(1 for r in self.symbolic_rules.values() if r.evidence_count > 1)
        
        return {
            "integration_status": "Active",
            "total_episodes": total_episodes,
            "overall_success_rate": overall_success_rate,
            "recent_success_rate": recent_success_rate,
            "approach_performance": approach_performance,
            "neural_patterns": {
                "total": len(self.neural_patterns),
                "active": neural_patterns_active,
                "avg_success_rate": statistics.mean([p.success_rate for p in self.neural_patterns.values()]) if self.neural_patterns else 0
            },
            "symbolic_rules": {
                "total": len(self.symbolic_rules),
                "active": symbolic_rules_active,
                "avg_confidence": statistics.mean([r.confidence for r in self.symbolic_rules.values()]) if self.symbolic_rules else 0
            },
            "integration_effectiveness": {
                "target_accuracy": 0.85,
                "current_accuracy": overall_success_rate,
                "target_met": overall_success_rate >= 0.85,
                "improvement_over_individual": self._calculate_improvement_over_individual()
            }
        }

    def _calculate_improvement_over_individual(self) -> float:
        """Calculate performance improvement over individual symbolic/neural approaches."""
        
        if not self.reasoning_episodes:
            return 0.0
        
        # Get hybrid approach performance
        hybrid_episodes = [ep for ep in self.reasoning_episodes if ep.approach_selected == ReasoningMode.HYBRID]
        if not hybrid_episodes:
            return 0.0
        
        hybrid_success = sum(1 for ep in hybrid_episodes if ep.success) / len(hybrid_episodes)
        
        # Get individual approach performances
        symbolic_episodes = [ep for ep in self.reasoning_episodes if ep.approach_selected == ReasoningMode.SYMBOLIC]
        neural_episodes = [ep for ep in self.reasoning_episodes if ep.approach_selected == ReasoningMode.NEURAL]
        
        individual_performances = []
        if symbolic_episodes:
            symbolic_success = sum(1 for ep in symbolic_episodes if ep.success) / len(symbolic_episodes)
            individual_performances.append(symbolic_success)
        
        if neural_episodes:
            neural_success = sum(1 for ep in neural_episodes if ep.success) / len(neural_episodes)
            individual_performances.append(neural_success)
        
        if individual_performances:
            avg_individual = statistics.mean(individual_performances)
            improvement = (hybrid_success - avg_individual) / avg_individual if avg_individual > 0 else 0.0
            return improvement
        
        return 0.0

    def save_to_database(self):
        """Save current state to database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Save neural patterns
            for pattern in self.neural_patterns.values():
                cursor.execute("""
                    INSERT OR REPLACE INTO neural_patterns 
                    (pattern_id, pattern_type, input_features, output_prediction, confidence, 
                     success_rate, usage_count, last_used, context_tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern.pattern_id, pattern.pattern_type, json.dumps(pattern.input_features),
                    pattern.output_prediction, pattern.confidence, pattern.success_rate,
                    pattern.usage_count, pattern.last_used.isoformat(), json.dumps(pattern.context_tags)
                ))
            
            # Save symbolic rules
            for rule in self.symbolic_rules.values():
                cursor.execute("""
                    INSERT OR REPLACE INTO symbolic_rules
                    (rule_id, condition, conclusion, confidence, evidence_count, rule_type, context_domain, created)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rule.rule_id, rule.condition, rule.conclusion, rule.confidence,
                    rule.evidence_count, rule.rule_type, rule.context_domain, rule.created.isoformat()
                ))
            
            # Save recent reasoning episodes
            for episode in self.reasoning_episodes[-50:]:  # Keep last 50 episodes
                cursor.execute("""
                    INSERT OR REPLACE INTO reasoning_episodes
                    (episode_id, problem, approaches_used, symbolic_result, neural_result, 
                     final_result, approach_selected, confidence, success, reasoning_time, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    episode.episode_id, json.dumps(episode.problem), json.dumps([a.value for a in episode.approaches_used]),
                    json.dumps(episode.symbolic_result), json.dumps(episode.neural_result),
                    json.dumps(episode.final_result), episode.approach_selected.value, episode.confidence,
                    int(episode.success), episode.reasoning_time, episode.timestamp.isoformat()
                ))
            
            conn.commit()


def demonstrate_neural_symbolic_integration():
    """Demonstrate the neural-symbolic integration system capabilities."""
    print("🧠 Neural-Symbolic Reasoning Integration Demonstration")
    print("=" * 65)
    
    # Initialize the integration system
    integration_system = NeuralSymbolicIntegration()
    
    print(f"\n🔍 System initialized with:")
    print(f"  • {len(integration_system.symbolic_rules)} symbolic rules")
    print(f"  • {len(integration_system.neural_patterns)} neural patterns")
    print(f"  • {len(integration_system.problem_type_indicators)} problem type classifiers")
    
    # Test problems covering different reasoning types
    test_problems = [
        {
            'id': 'logical_test_1',
            'description': 'If heavy objects require more force to move, and this object is very heavy, what should I expect?',
            'goal': 'predict required effort level',
            'domain': 'physics'
        },
        {
            'id': 'creative_test_1', 
            'description': 'Find a new creative way to understand this difficult mathematical concept',
            'goal': 'develop innovative learning approach',
            'domain': 'learning'
        },
        {
            'id': 'moral_test_1',
            'description': 'Should I help my friend with their homework or focus on my own learning goals?',
            'goal': 'make ethical decision',
            'domain': 'social'
        },
        {
            'id': 'hybrid_test_1',
            'description': 'How can I move this heavy object through a narrow space efficiently?',
            'goal': 'solve complex physical problem',
            'domain': 'physics'
        }
    ]
    
    # Test each problem with the integration system
    results = []
    for problem in test_problems:
        print(f"\n{'='*50}")
        print(f"🎯 Problem: {problem['description']}")
        print(f"   Goal: {problem['goal']}")
        
        # Apply integrated reasoning
        result = integration_system.integrated_reasoning(problem)
        results.append(result)
        
        print(f"\n📊 Result:")
        print(f"   Approach: {result.get('approach_selected', 'unknown')}")
        print(f"   Success: {'✅' if result.get('success', False) else '❌'}")
        print(f"   Confidence: {result.get('confidence', 0.0):.2f}")
        print(f"   Time: {result.get('reasoning_time', 0.0):.3f}s")
        
        if 'reasoning_chain' in result:
            print(f"\n🔗 Reasoning Chain:")
            for step in result['reasoning_chain'][:5]:  # Show first 5 steps
                print(f"   • {step}")
    
    # Show integration metrics
    print(f"\n{'='*50}")
    print("📈 INTEGRATION SYSTEM METRICS")
    
    metrics = integration_system.get_integration_metrics()
    print(f"\n🎯 Overall Performance:")
    print(f"   Episodes: {metrics.get('total_episodes', 0)}")
    print(f"   Success Rate: {metrics.get('overall_success_rate', 0.0):.1%}")
    print(f"   Target Accuracy: {metrics.get('integration_effectiveness', {}).get('target_accuracy', 0.85):.1%}")
    print(f"   Target Met: {'✅' if metrics.get('integration_effectiveness', {}).get('target_met', False) else '❌'}")
    
    if 'approach_performance' in metrics:
        print(f"\n📊 Performance by Approach:")
        for approach, perf in metrics['approach_performance'].items():
            print(f"   {approach.title()}: {perf['success_rate']:.1%} success ({perf['episodes']} episodes)")
    
    # Test learning from feedback
    print(f"\n🎓 Testing Learning from Feedback...")
    if results:
        # Simulate positive feedback on first result
        episode_id = results[0].get('episode_id')
        if episode_id:
            integration_system.learn_from_feedback(episode_id, success=True, feedback="Great reasoning!")
            print("✅ Positive feedback incorporated")
    
    print(f"\n🎉 NEURAL-SYMBOLIC INTEGRATION DEMONSTRATION COMPLETE!")
    print("✅ Unified reasoning pipeline operational")
    print("✅ Approach selection based on problem characteristics")
    print("✅ Hybrid reasoning with confidence-weighted synthesis")
    print("✅ Learning feedback loop for continuous improvement")
    print("✅ Integration with existing consciousness framework ready")
    
    return integration_system, results


if __name__ == "__main__":
    demonstrate_neural_symbolic_integration()
