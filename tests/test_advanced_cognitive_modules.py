#!/usr/bin/env python3
"""
Test Suite for Advanced Cognitive Modules
=========================================

Comprehensive testing of the advanced cognitive modules including
Transformer NLP, Graph Neural Networks, Probabilistic Reasoning,
and their integration with the Enhanced Cognitive Architecture.
"""

import unittest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import json
import uuid
import numpy as np

# Add the core directory to the path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the advanced cognitive modules
try:
    from core.reasoning.advanced_cognitive_modules import (
        TransformerNLPModule, GraphNeuralNetworkModule, ProbabilisticReasoningModule,
        create_advanced_cognitive_modules
    )
    from core.reasoning.enhanced_cognitive_architecture import (
        CognitiveTask, CognitiveModuleType, ProcessingPriority
    )
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Advanced cognitive modules not available for testing: {e}")
    MODULES_AVAILABLE = False


class TestTransformerNLPModule(unittest.TestCase):
    """Test the TransformerNLPModule."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not MODULES_AVAILABLE:
            self.skipTest("Advanced cognitive modules not available")
        
        self.nlp_module = TransformerNLPModule()
    
    def test_text_understanding(self):
        """Test text understanding capabilities."""
        test_text = "The neural symbolic integration system combines logic with pattern recognition for advanced reasoning."
        
        task = CognitiveTask(
            task_id="nlp_test_001",
            task_type="text_analysis",
            input_data={'operation': 'understand', 'text': test_text},
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result = self.nlp_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('tokens', result)
        self.assertIn('key_concepts', result)
        self.assertIn('semantic_meaning', result)
        self.assertIn('emotional_tone', result)
        self.assertGreater(len(result['tokens']), 0)
    
    def test_text_generation(self):
        """Test text generation capabilities."""
        prompt = "The future of artificial intelligence"
        
        task = CognitiveTask(
            task_id="nlp_test_002",
            task_type="text_generation",
            input_data={'operation': 'generate', 'prompt': prompt},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result = self.nlp_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('generated_text', result)
        self.assertIn('total_tokens', result)
        self.assertGreater(len(result['generated_text']), 0)
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis capabilities."""
        positive_text = "This is an amazing and wonderful achievement in artificial intelligence!"
        negative_text = "This is terrible and awful, I hate this implementation."
        neutral_text = "The system processes information according to specified parameters."
        
        # Test positive sentiment
        task_pos = CognitiveTask(
            task_id="nlp_sentiment_pos",
            task_type="sentiment_analysis",
            input_data={'operation': 'analyze_sentiment', 'text': positive_text},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result_pos = self.nlp_module.process(task_pos)
        self.assertTrue(result_pos['success'])
        self.assertEqual(result_pos['sentiment'], 'positive')
        
        # Test negative sentiment
        task_neg = CognitiveTask(
            task_id="nlp_sentiment_neg",
            task_type="sentiment_analysis",
            input_data={'operation': 'analyze_sentiment', 'text': negative_text},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result_neg = self.nlp_module.process(task_neg)
        self.assertTrue(result_neg['success'])
        self.assertEqual(result_neg['sentiment'], 'negative')
        
        # Test neutral sentiment
        task_neutral = CognitiveTask(
            task_id="nlp_sentiment_neutral",
            task_type="sentiment_analysis",
            input_data={'operation': 'analyze_sentiment', 'text': neutral_text},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result_neutral = self.nlp_module.process(task_neutral)
        self.assertTrue(result_neutral['success'])
        self.assertEqual(result_neutral['sentiment'], 'neutral')
    
    def test_concept_extraction(self):
        """Test concept extraction from text."""
        text = "Machine learning algorithms use neural networks to understand complex patterns in data."
        
        task = CognitiveTask(
            task_id="nlp_concept_test",
            task_type="concept_extraction",
            input_data={'operation': 'extract_concepts', 'text': text},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result = self.nlp_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('raw_concepts', result)
        self.assertIn('concept_clusters', result)
        self.assertGreater(result['concept_count'], 0)
    
    def test_semantic_similarity(self):
        """Test semantic similarity calculation."""
        text1 = "Neural networks learn from data patterns"
        text2 = "Machine learning systems recognize data structures"
        text3 = "The cat sat on the mat"
        
        # Test similar texts
        task_similar = CognitiveTask(
            task_id="nlp_similarity_similar",
            task_type="similarity_analysis",
            input_data={
                'operation': 'semantic_similarity',
                'text1': text1,
                'text2': text2
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result_similar = self.nlp_module.process(task_similar)
        self.assertTrue(result_similar['success'])
        self.assertGreater(result_similar['combined_similarity'], 0.1)
        
        # Test dissimilar texts
        task_dissimilar = CognitiveTask(
            task_id="nlp_similarity_dissimilar",
            task_type="similarity_analysis",
            input_data={
                'operation': 'semantic_similarity',
                'text1': text1,
                'text2': text3
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        result_dissimilar = self.nlp_module.process(task_dissimilar)
        self.assertTrue(result_dissimilar['success'])
        self.assertLess(result_dissimilar['combined_similarity'], 
                       result_similar['combined_similarity'])


class TestGraphNeuralNetworkModule(unittest.TestCase):
    """Test the GraphNeuralNetworkModule."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not MODULES_AVAILABLE:
            self.skipTest("Advanced cognitive modules not available")
        
        self.gnn_module = GraphNeuralNetworkModule()
    
    def test_add_node(self):
        """Test adding nodes to the knowledge graph."""
        task = CognitiveTask(
            task_id="gnn_test_001",
            task_type="graph_modification",
            input_data={
                'operation': 'add_node',
                'node_id': 'test_concept',
                'features': {'type': 'test', 'importance': 0.8}
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.GRAPH_NEURAL_NET]
        )
        
        result = self.gnn_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['node_id'], 'test_concept')
        self.assertGreater(result['total_nodes'], 0)
    
    def test_add_edge(self):
        """Test adding edges to the knowledge graph."""
        # First add nodes
        self.gnn_module._add_node('source_node', {'type': 'test'})
        self.gnn_module._add_node('target_node', {'type': 'test'})
        
        task = CognitiveTask(
            task_id="gnn_test_002",
            task_type="graph_modification",
            input_data={
                'operation': 'add_edge',
                'source': 'source_node',
                'target': 'target_node',
                'edge_type': 'test_relationship'
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.GRAPH_NEURAL_NET]
        )
        
        result = self.gnn_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('edge', result)
        self.assertGreater(result['total_edges'], 0)
    
    def test_query_relationships(self):
        """Test querying relationships in the graph."""
        # Use existing node from initialization
        task = CognitiveTask(
            task_id="gnn_test_003",
            task_type="graph_query",
            input_data={
                'operation': 'query_relationships',
                'node_id': 'learning',
                'max_depth': 2
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.GRAPH_NEURAL_NET]
        )
        
        result = self.gnn_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['node_id'], 'learning')
        self.assertIn('relationships', result)
        self.assertIn('relationship_count', result)
    
    def test_find_path(self):
        """Test finding paths between nodes."""
        task = CognitiveTask(
            task_id="gnn_test_004",
            task_type="graph_pathfinding",
            input_data={
                'operation': 'find_path',
                'source': 'learning',
                'target': 'memory',
                'max_length': 5
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.GRAPH_NEURAL_NET]
        )
        
        result = self.gnn_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['source'], 'learning')
        self.assertEqual(result['target'], 'memory')
        self.assertIn('path', result)
        self.assertIn('found', result)
    
    def test_graph_reasoning(self):
        """Test graph-based reasoning capabilities."""
        # Test associative reasoning
        task_assoc = CognitiveTask(
            task_id="gnn_reasoning_assoc",
            task_type="graph_reasoning",
            input_data={
                'operation': 'graph_reasoning',
                'query': 'learning patterns',
                'reasoning_type': 'associative'
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.GRAPH_NEURAL_NET]
        )
        
        result_assoc = self.gnn_module.process(task_assoc)
        self.assertTrue(result_assoc['success'])
        self.assertEqual(result_assoc['reasoning_type'], 'associative')
        self.assertIn('associations', result_assoc)
        
        # Test causal reasoning
        task_causal = CognitiveTask(
            task_id="gnn_reasoning_causal",
            task_type="graph_reasoning",
            input_data={
                'operation': 'graph_reasoning',
                'query': 'causal relationships',
                'reasoning_type': 'causal'
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.GRAPH_NEURAL_NET]
        )
        
        result_causal = self.gnn_module.process(task_causal)
        self.assertTrue(result_causal['success'])
        self.assertEqual(result_causal['reasoning_type'], 'causal')
        self.assertIn('causal_chains', result_causal)


class TestProbabilisticReasoningModule(unittest.TestCase):
    """Test the ProbabilisticReasoningModule."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not MODULES_AVAILABLE:
            self.skipTest("Advanced cognitive modules not available")
        
        self.prob_module = ProbabilisticReasoningModule()
    
    def test_bayesian_inference(self):
        """Test Bayesian inference capabilities."""
        task = CognitiveTask(
            task_id="prob_test_001",
            task_type="probabilistic_inference",
            input_data={
                'operation': 'inference',
                'query_variable': 'learning_success',
                'evidence': {'attention_level': 'focused', 'prior_knowledge': 'moderate'}
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.PROBABILISTIC_REASONING]
        )
        
        result = self.prob_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['query_variable'], 'learning_success')
        self.assertIn('posterior_distribution', result)
        self.assertIn('most_likely_state', result)
        self.assertIn('uncertainty', result)
        
        # Check that probabilities sum to approximately 1
        posterior = result['posterior_distribution']
        prob_sum = sum(posterior.values())
        self.assertAlmostEqual(prob_sum, 1.0, places=2)
    
    def test_uncertainty_assessment(self):
        """Test uncertainty assessment capabilities."""
        situation = {
            'attention_level': 'focused',
            'confidence': 0.8,
            'available_information': 0.6
        }
        
        task = CognitiveTask(
            task_id="prob_test_002",
            task_type="uncertainty_analysis",
            input_data={
                'operation': 'uncertainty_assessment',
                'situation': situation,
                'required_information': ['attention_level', 'prior_knowledge', 'difficulty']
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.PROBABILISTIC_REASONING]
        )
        
        result = self.prob_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('total_uncertainty', result)
        self.assertIn('uncertainty_factors', result)
        self.assertIn('confidence_level', result)
        self.assertIn('recommendation', result)
        
        # Uncertainty should be between 0 and 1
        self.assertGreaterEqual(result['total_uncertainty'], 0.0)
        self.assertLessEqual(result['total_uncertainty'], 1.0)
    
    def test_decision_making(self):
        """Test probabilistic decision making."""
        options = ['option_a', 'option_b', 'option_c']
        utilities = {
            'option_a': {'success': 0.8, 'failure': 0.2},
            'option_b': {'success': 0.6, 'failure': 0.4},
            'option_c': {'success': 0.9, 'failure': 0.1}
        }
        probabilities = {
            'option_a': {'success': 0.7, 'failure': 0.3},
            'option_b': {'success': 0.8, 'failure': 0.2},
            'option_c': {'success': 0.6, 'failure': 0.4}
        }
        
        task = CognitiveTask(
            task_id="prob_test_003",
            task_type="decision_analysis",
            input_data={
                'operation': 'decision_making',
                'options': options,
                'utilities': utilities,
                'probabilities': probabilities
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.PROBABILISTIC_REASONING]
        )
        
        result = self.prob_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('expected_utilities', result)
        self.assertIn('recommended_option', result)
        self.assertIn(result['recommended_option'], options)
    
    def test_belief_updates(self):
        """Test belief updating with new evidence."""
        new_evidence = {'attention_level': 'distracted'}
        
        task = CognitiveTask(
            task_id="prob_test_004",
            task_type="belief_update",
            input_data={
                'operation': 'update_beliefs',
                'variable': 'learning_success',
                'new_evidence': new_evidence
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.PROBABILISTIC_REASONING]
        )
        
        result = self.prob_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['variable'], 'learning_success')
        self.assertIn('updated_posterior', result)
        self.assertIn('evidence_impact', result)
    
    def test_monte_carlo_simulation(self):
        """Test Monte Carlo simulation capabilities."""
        task = CognitiveTask(
            task_id="prob_test_005",
            task_type="monte_carlo_analysis",
            input_data={
                'operation': 'monte_carlo',
                'query_variable': 'learning_success',
                'num_samples': 100
            },
            priority=ProcessingPriority.LOW,
            required_modules=[CognitiveModuleType.PROBABILISTIC_REASONING]
        )
        
        result = self.prob_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['query_variable'], 'learning_success')
        self.assertIn('empirical_distribution', result)
        self.assertGreater(result['num_samples'], 0)


class TestModuleFactory(unittest.TestCase):
    """Test the module factory function."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not MODULES_AVAILABLE:
            self.skipTest("Advanced cognitive modules not available")
    
    def test_create_advanced_modules(self):
        """Test creating all advanced cognitive modules."""
        modules = create_advanced_cognitive_modules()
        
        self.assertIsInstance(modules, dict)
        
        # Check that expected modules are created
        expected_modules = [
            CognitiveModuleType.TRANSFORMER_NLP,
            CognitiveModuleType.GRAPH_NEURAL_NET,
            CognitiveModuleType.PROBABILISTIC_REASONING
        ]
        
        for module_type in expected_modules:
            self.assertIn(module_type, modules)
            self.assertIsNotNone(modules[module_type])
    
    def test_module_status(self):
        """Test that modules report their status correctly."""
        modules = create_advanced_cognitive_modules()
        
        for module_type, module in modules.items():
            status = module.get_status()
            
            self.assertIn('module_type', status)
            self.assertIn('is_active', status)
            self.assertIn('resource_usage', status)
            self.assertEqual(status['module_type'], module_type.value)


class TestAdvancedModuleIntegration(unittest.TestCase):
    """Test integration of advanced modules with the main architecture."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not MODULES_AVAILABLE:
            self.skipTest("Advanced cognitive modules not available")
    
    def test_multi_modal_processing(self):
        """Test processing tasks that require multiple advanced modules."""
        # This would test the enhanced cognitive architecture with advanced modules
        # For now, we test individual module capabilities
        
        nlp_module = TransformerNLPModule()
        gnn_module = GraphNeuralNetworkModule()
        prob_module = ProbabilisticReasoningModule()
        
        # Test that modules can be used together
        text = "Learning requires memory and attention"
        
        # NLP processing
        nlp_task = CognitiveTask(
            task_id="integration_nlp",
            task_type="text_analysis",
            input_data={'operation': 'extract_concepts', 'text': text},
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.TRANSFORMER_NLP]
        )
        
        nlp_result = nlp_module.process(nlp_task)
        self.assertTrue(nlp_result['success'])
        
        # Graph processing using concepts from NLP
        concepts = nlp_result.get('raw_concepts', [])
        if 'learning' in concepts:
            gnn_task = CognitiveTask(
                task_id="integration_gnn",
                task_type="graph_query",
                input_data={
                    'operation': 'query_relationships',
                    'node_id': 'learning'
                },
                priority=ProcessingPriority.HIGH,
                required_modules=[CognitiveModuleType.GRAPH_NEURAL_NET]
            )
            
            gnn_result = gnn_module.process(gnn_task)
            self.assertTrue(gnn_result['success'])
        
        # Probabilistic reasoning about learning success
        prob_task = CognitiveTask(
            task_id="integration_prob",
            task_type="probabilistic_inference",
            input_data={
                'operation': 'inference',
                'query_variable': 'learning_success',
                'evidence': {'attention_level': 'focused'}
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.PROBABILISTIC_REASONING]
        )
        
        prob_result = prob_module.process(prob_task)
        self.assertTrue(prob_result['success'])


def run_advanced_cognitive_module_tests():
    """Run all tests for the advanced cognitive modules."""
    
    if not MODULES_AVAILABLE:
        print("❌ Advanced Cognitive Modules not available for testing")
        print("   Please ensure all dependencies are installed and modules are accessible")
        return False
    
    print("🚀 Running Advanced Cognitive Modules Test Suite")
    print("=" * 65)
    
    # Create test suite
    test_classes = [
        TestTransformerNLPModule,
        TestGraphNeuralNetworkModule,
        TestProbabilisticReasoningModule,
        TestModuleFactory,
        TestAdvancedModuleIntegration
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n🔬 Running {test_class.__name__}...")
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        
        class_total = result.testsRun
        class_passed = class_total - len(result.failures) - len(result.errors)
        class_failed = len(result.failures) + len(result.errors)
        
        total_tests += class_total
        passed_tests += class_passed
        failed_tests += class_failed
        
        if class_failed == 0:
            print(f"   ✅ {class_passed}/{class_total} tests passed")
        else:
            print(f"   ⚠️  {class_passed}/{class_total} tests passed ({class_failed} failed)")
            
            # Show failure details
            for failure in result.failures:
                print(f"      FAIL: {failure[0]}")
            for error in result.errors:
                print(f"      ERROR: {error[0]}")
    
    # Test Summary
    print(f"\n📊 ADVANCED MODULES TEST SUMMARY:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {failed_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "   Success Rate: 0%")
    
    if failed_tests == 0:
        print(f"\n🎉 ALL ADVANCED MODULE TESTS PASSED!")
        print("✅ Transformer NLP Module operational")
        print("✅ Graph Neural Network Module operational")
        print("✅ Probabilistic Reasoning Module operational")
        print("✅ Multi-modal integration validated")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Please review and fix issues before deployment.")
        return False


if __name__ == "__main__":
    success = run_advanced_cognitive_module_tests()
    sys.exit(0 if success else 1)
