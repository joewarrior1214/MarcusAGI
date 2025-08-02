#!/usr/bin/env python3
"""
Test Suite for Enhanced Cognitive Architecture
==============================================

Comprehensive testing of the enhanced cognitive architecture system
including all cognitive modules and integration capabilities.
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

# Add the core directory to the path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the enhanced cognitive architecture
try:
    from core.reasoning.enhanced_cognitive_architecture import (
        EnhancedCognitiveArchitecture, CognitiveTask, CognitiveModuleType,
        ProcessingPriority, WorkingMemoryModule, EpisodicMemoryModule,
        MetacognitiveMonitor, ExecutiveController, MemoryTrace, AttentionState,
        demonstrate_enhanced_cognitive_architecture
    )
    ARCHITECTURE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Enhanced cognitive architecture not available for testing: {e}")
    ARCHITECTURE_AVAILABLE = False


class TestCognitiveTask(unittest.TestCase):
    """Test the CognitiveTask data structure."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
    
    def test_cognitive_task_creation(self):
        """Test creating a cognitive task."""
        task = CognitiveTask(
            task_id="test_task_001",
            task_type="reasoning",
            input_data={'problem': 'test problem'},
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.NEUROSYMBOLIC_CORE]
        )
        
        self.assertEqual(task.task_id, "test_task_001")
        self.assertEqual(task.task_type, "reasoning")
        self.assertEqual(task.priority, ProcessingPriority.HIGH)
        self.assertIsInstance(task.created, datetime)
        self.assertIsNone(task.started)
        self.assertIsNone(task.completed)


class TestWorkingMemoryModule(unittest.TestCase):
    """Test the WorkingMemoryModule."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
        
        self.memory_module = WorkingMemoryModule()
    
    def test_store_item(self):
        """Test storing an item in working memory."""
        test_item = {'concept': 'neural_network', 'importance': 0.8}
        
        task = CognitiveTask(
            task_id="mem_test_001",
            task_type="memory_store",
            input_data={'operation': 'store', 'item': test_item},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        result = self.memory_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('item_id', result)
        self.assertEqual(result['buffer_size'], 1)
    
    def test_retrieve_item(self):
        """Test retrieving items from working memory."""
        # First store an item
        test_item = {'concept': 'symbolic_reasoning', 'domain': 'AI'}
        
        store_task = CognitiveTask(
            task_id="mem_test_002",
            task_type="memory_store",
            input_data={'operation': 'store', 'item': test_item},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        store_result = self.memory_module.process(store_task)
        self.assertTrue(store_result['success'])
        
        # Now retrieve it
        retrieve_task = CognitiveTask(
            task_id="mem_test_003",
            task_type="memory_retrieve",
            input_data={'operation': 'retrieve', 'query': {'concept': 'symbolic'}},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        retrieve_result = self.memory_module.process(retrieve_task)
        
        self.assertTrue(retrieve_result['success'])
        self.assertGreater(len(retrieve_result['retrieved_items']), 0)
    
    def test_buffer_capacity_limit(self):
        """Test that working memory respects capacity limits."""
        # Store items beyond capacity
        for i in range(10):  # More than buffer capacity of 7
            test_item = {'concept': f'concept_{i}', 'value': i}
            
            task = CognitiveTask(
                task_id=f"mem_test_{i+10}",
                task_type="memory_store",
                input_data={'operation': 'store', 'item': test_item},
                priority=ProcessingPriority.MEDIUM,
                required_modules=[CognitiveModuleType.WORKING_MEMORY]
            )
            
            result = self.memory_module.process(task)
            self.assertTrue(result['success'])
        
        # Buffer should not exceed capacity
        self.assertLessEqual(len(self.memory_module.current_buffer), 
                           self.memory_module.buffer_capacity)


class TestEpisodicMemoryModule(unittest.TestCase):
    """Test the EpisodicMemoryModule."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
        
        self.memory_module = EpisodicMemoryModule()
    
    def test_store_episode(self):
        """Test storing an episodic memory."""
        episode_data = {
            'event': 'problem_solving_success',
            'context': {'domain': 'mathematics', 'difficulty': 'medium'},
            'emotional_valence': 0.7,
            'importance': 0.8
        }
        
        task = CognitiveTask(
            task_id="ep_test_001",
            task_type="episode_store",
            input_data={'operation': 'store', 'episode': episode_data},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.EPISODIC_MEMORY]
        )
        
        result = self.memory_module.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('episode_id', result)
        self.assertEqual(len(self.memory_module.episodes), 1)
    
    def test_retrieve_episodes(self):
        """Test retrieving episodic memories."""
        # Store several episodes
        episodes = [
            {
                'event': 'learning_session',
                'context': {'subject': 'mathematics', 'duration': 60},
                'emotional_valence': 0.5,
                'importance': 0.6
            },
            {
                'event': 'problem_solving',
                'context': {'subject': 'physics', 'success': True},
                'emotional_valence': 0.8,
                'importance': 0.9
            }
        ]
        
        for i, episode in enumerate(episodes):
            task = CognitiveTask(
                task_id=f"ep_store_{i}",
                task_type="episode_store",
                input_data={'operation': 'store', 'episode': episode},
                priority=ProcessingPriority.MEDIUM,
                required_modules=[CognitiveModuleType.EPISODIC_MEMORY]
            )
            
            result = self.memory_module.process(task)
            self.assertTrue(result['success'])
        
        # Retrieve by context
        retrieve_task = CognitiveTask(
            task_id="ep_retrieve_001",
            task_type="episode_retrieve",
            input_data={
                'operation': 'retrieve',
                'query': {
                    'context': {'subject': 'mathematics'}
                }
            },
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.EPISODIC_MEMORY]
        )
        
        result = self.memory_module.process(retrieve_task)
        
        self.assertTrue(result['success'])
        self.assertGreater(len(result['episodes']), 0)
    
    def test_memory_consolidation(self):
        """Test episodic memory consolidation."""
        # Store an episode and access it multiple times
        episode_data = {
            'event': 'important_discovery',
            'context': {'domain': 'science'},
            'emotional_valence': 0.9,
            'importance': 0.9
        }
        
        store_task = CognitiveTask(
            task_id="ep_consolidate_001",
            task_type="episode_store",
            input_data={'operation': 'store', 'episode': episode_data},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.EPISODIC_MEMORY]
        )
        
        result = self.memory_module.process(store_task)
        episode_id = result['episode_id']
        
        # Access it multiple times
        for _ in range(5):
            retrieve_task = CognitiveTask(
                task_id="ep_access",
                task_type="episode_retrieve",
                input_data={
                    'operation': 'retrieve',
                    'query': {'context': {'domain': 'science'}}
                },
                priority=ProcessingPriority.MEDIUM,
                required_modules=[CognitiveModuleType.EPISODIC_MEMORY]
            )
            self.memory_module.process(retrieve_task)
        
        # Test consolidation
        consolidate_task = CognitiveTask(
            task_id="ep_consolidate_002",
            task_type="memory_consolidate",
            input_data={'operation': 'consolidate'},
            priority=ProcessingPriority.LOW,
            required_modules=[CognitiveModuleType.EPISODIC_MEMORY]
        )
        
        result = self.memory_module.process(consolidate_task)
        
        self.assertTrue(result['success'])
        self.assertGreater(result['consolidated_episodes'], 0)


class TestMetacognitiveMonitor(unittest.TestCase):
    """Test the MetacognitiveMonitor."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
        
        self.monitor = MetacognitiveMonitor()
    
    def test_monitor_cognitive_state(self):
        """Test monitoring cognitive state."""
        system_state = {
            'working_memory_load': 0.6,
            'attention_focus': ['task_1', 'task_2'],
            'processing_speed': 1.2,
            'error_rate': 0.1,
            'confidence_level': 0.8
        }
        
        task = CognitiveTask(
            task_id="meta_test_001",
            task_type="state_monitor",
            input_data={'operation': 'monitor', 'system_state': system_state},
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.METACOGNITIVE_MONITOR]
        )
        
        result = self.monitor.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('current_state', result)
        self.assertIn('issues_detected', result)
        self.assertIn('recommendations', result)
    
    def test_performance_evaluation(self):
        """Test performance evaluation."""
        task_results = [
            {'task_type': 'reasoning', 'success': True, 'confidence': 0.8, 'completion_time': 1.2},
            {'task_type': 'reasoning', 'success': True, 'confidence': 0.7, 'completion_time': 1.5},
            {'task_type': 'memory', 'success': False, 'confidence': 0.4, 'completion_time': 2.0},
            {'task_type': 'creative', 'success': True, 'confidence': 0.9, 'completion_time': 0.8}
        ]
        
        task = CognitiveTask(
            task_id="meta_test_002",
            task_type="performance_eval",
            input_data={'operation': 'evaluate_performance', 'task_results': task_results},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.METACOGNITIVE_MONITOR]
        )
        
        result = self.monitor.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('performance_metrics', result)
        self.assertIn('improvement_suggestions', result)
        
        # Check that performance metrics are calculated
        metrics = result['performance_metrics']
        self.assertIn('overall_success_rate', metrics)
        self.assertIn('strengths', metrics)
        self.assertIn('weaknesses', metrics)
    
    def test_strategy_recommendation(self):
        """Test strategy recommendation."""
        problem_context = {
            'type': 'complex_reasoning',
            'complexity': 'high',
            'requires_creativity': True,
            'has_uncertainty': True
        }
        
        task = CognitiveTask(
            task_id="meta_test_003",
            task_type="strategy_recommend",
            input_data={'operation': 'recommend_strategy', 'problem_context': problem_context},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.METACOGNITIVE_MONITOR]
        )
        
        result = self.monitor.process(task)
        
        self.assertTrue(result['success'])
        self.assertIn('recommended_strategies', result)
        self.assertIn('confidence', result)
        self.assertGreater(len(result['recommended_strategies']), 0)


class TestExecutiveController(unittest.TestCase):
    """Test the ExecutiveController."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
        
        # Create mock cognitive modules
        self.mock_modules = {
            CognitiveModuleType.WORKING_MEMORY: Mock(),
            CognitiveModuleType.EPISODIC_MEMORY: Mock(),
            CognitiveModuleType.METACOGNITIVE_MONITOR: Mock()
        }
        
        # Configure mock returns
        for module in self.mock_modules.values():
            module.process.return_value = {'success': True, 'result': 'mock_result'}
        
        self.controller = ExecutiveController(self.mock_modules)
    
    def test_coordinate_processing(self):
        """Test coordinating processing across modules."""
        task = CognitiveTask(
            task_id="exec_test_001",
            task_type="multi_module_task",
            input_data={'problem': 'test coordination'},
            priority=ProcessingPriority.HIGH,
            required_modules=[
                CognitiveModuleType.WORKING_MEMORY,
                CognitiveModuleType.EPISODIC_MEMORY
            ]
        )
        
        result = self.controller.coordinate_processing(task)
        
        self.assertIn('success', result)
        self.assertIn('module_contributions', result)
        self.assertIn('coordination_success_rate', result)
        
        # Verify that required modules were called
        self.mock_modules[CognitiveModuleType.WORKING_MEMORY].process.assert_called_once()
        self.mock_modules[CognitiveModuleType.EPISODIC_MEMORY].process.assert_called_once()
    
    def test_resource_allocation(self):
        """Test resource allocation to modules."""
        required_modules = [
            CognitiveModuleType.WORKING_MEMORY,
            CognitiveModuleType.METACOGNITIVE_MONITOR
        ]
        
        self.controller._allocate_resources(required_modules)
        
        self.assertEqual(len(self.controller.resource_allocation), 2)
        for module_type in required_modules:
            self.assertIn(module_type, self.controller.resource_allocation)
            self.assertGreater(self.controller.resource_allocation[module_type], 0)
    
    def test_get_status(self):
        """Test getting controller status."""
        # Process a task to populate history
        task = CognitiveTask(
            task_id="exec_status_test",
            task_type="status_test",
            input_data={},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        self.controller.coordinate_processing(task)
        
        status = self.controller.get_status()
        
        self.assertIn('total_coordinations', status)
        self.assertIn('recent_success_rate', status)
        self.assertIn('average_processing_time', status)
        self.assertGreater(status['total_coordinations'], 0)


class TestEnhancedCognitiveArchitecture(unittest.TestCase):
    """Test the complete Enhanced Cognitive Architecture."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
        
        # Create temporary database for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test_cognitive.db")
        
        # Initialize architecture
        self.architecture = EnhancedCognitiveArchitecture()
        self.architecture.db_path = self.test_db_path
        self.architecture.setup_database()
    
    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_architecture_initialization(self):
        """Test that the architecture initializes correctly."""
        self.assertIsNotNone(self.architecture.cognitive_modules)
        self.assertIsNotNone(self.architecture.executive_control)
        self.assertIn(CognitiveModuleType.WORKING_MEMORY, self.architecture.cognitive_modules)
        self.assertIn(CognitiveModuleType.EPISODIC_MEMORY, self.architecture.cognitive_modules)
        self.assertIn(CognitiveModuleType.METACOGNITIVE_MONITOR, self.architecture.cognitive_modules)
    
    def test_process_cognitive_task(self):
        """Test processing a cognitive task through the architecture."""
        task = CognitiveTask(
            task_id="arch_test_001",
            task_type="memory_reasoning_task",
            input_data={
                'problem': 'Store and retrieve information about neural networks',
                'context': {'domain': 'AI', 'complexity': 'medium'}
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        result = self.architecture.process_cognitive_task(task)
        
        self.assertIn('success', result)
        self.assertIsNotNone(task.completed)
        self.assertIsNotNone(task.result)
    
    def test_determine_required_modules(self):
        """Test automatic determination of required modules."""
        # Memory task
        memory_task = CognitiveTask(
            task_id="module_test_001",
            task_type="remember_information",
            input_data={'query': 'recall previous learning'},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[]
        )
        
        modules = self.architecture._determine_required_modules(memory_task)
        
        self.assertIn(CognitiveModuleType.NEUROSYMBOLIC_CORE, modules)
        self.assertIn(CognitiveModuleType.WORKING_MEMORY, modules)
        self.assertIn(CognitiveModuleType.EPISODIC_MEMORY, modules)
        
        # Creative task
        creative_task = CognitiveTask(
            task_id="module_test_002",
            task_type="creative_problem_solving",
            input_data={'challenge': 'innovative solution needed'},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[]
        )
        
        modules = self.architecture._determine_required_modules(creative_task)
        
        self.assertIn(CognitiveModuleType.NEUROSYMBOLIC_CORE, modules)
        self.assertIn(CognitiveModuleType.DIVERGENT_THINKING, modules)
        self.assertIn(CognitiveModuleType.ASSOCIATIVE_NETWORK, modules)
    
    def test_get_system_status(self):
        """Test getting comprehensive system status."""
        status = self.architecture.get_system_status()
        
        self.assertIn('system_status', status)
        self.assertIn('performance_metrics', status)
        self.assertIn('module_statuses', status)
        self.assertIn('executive_control_status', status)
        self.assertIn('timestamp', status)
        
        # Check performance metrics structure
        metrics = status['performance_metrics']
        self.assertIn('tasks_processed', metrics)
        self.assertIn('average_processing_time', metrics)
        self.assertIn('success_rate', metrics)
    
    def test_learning_from_task(self):
        """Test that the system learns from completed tasks."""
        # Create a successful task
        task = CognitiveTask(
            task_id="learn_test_001",
            task_type="learning_task",
            input_data={'lesson': 'test learning'},
            priority=ProcessingPriority.MEDIUM,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        # Process the task
        result = self.architecture.process_cognitive_task(task)
        
        # Verify learning occurred
        self.assertIsNotNone(task.result)
        self.assertGreater(self.architecture.performance_metrics['tasks_processed'], 0)
    
    @patch('core.reasoning.enhanced_cognitive_architecture.logger')
    def test_error_handling(self, mock_logger):
        """Test error handling in task processing."""
        # Create a task that will cause an error
        task = CognitiveTask(
            task_id="error_test_001",
            task_type="invalid_task_type",
            input_data={'invalid': 'data'},
            priority=ProcessingPriority.LOW,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        # Process the task
        result = self.architecture.process_cognitive_task(task)
        
        # Verify error was handled gracefully
        self.assertIsNotNone(result)
        self.assertIsNotNone(task.completed)


class TestDemonstration(unittest.TestCase):
    """Test the demonstration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
    
    def test_demonstrate_enhanced_capabilities(self):
        """Test the demonstration of enhanced capabilities."""
        architecture = EnhancedCognitiveArchitecture()
        
        results = architecture.demonstrate_enhanced_capabilities()
        
        self.assertIn('demonstration_results', results)
        self.assertIn('system_status', results)
        self.assertIn('capabilities_validated', results)
        
        # Check that key capabilities were demonstrated
        capabilities = results['capabilities_validated']
        expected_capabilities = [
            'working_memory_management',
            'episodic_memory_formation',
            'metacognitive_monitoring',
            'executive_control',
            'modular_architecture'
        ]
        
        for capability in expected_capabilities:
            self.assertIn(capability, capabilities)
    
    @patch('builtins.print')
    def test_full_demonstration_function(self, mock_print):
        """Test the complete demonstration function."""
        architecture, results = demonstrate_enhanced_cognitive_architecture()
        
        if architecture and results:
            self.assertIsInstance(architecture, EnhancedCognitiveArchitecture)
            self.assertIn('demonstration_results', results)
            
            # Verify that demonstration output was printed
            mock_print.assert_called()


class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios combining multiple modules."""
    
    def setUp(self):
        """Set up test fixtures."""
        if not ARCHITECTURE_AVAILABLE:
            self.skipTest("Enhanced cognitive architecture not available")
        
        self.architecture = EnhancedCognitiveArchitecture()
    
    def test_memory_reasoning_integration(self):
        """Test integration between memory and reasoning modules."""
        # Store information first
        store_task = CognitiveTask(
            task_id="integration_001",
            task_type="memory_store",
            input_data={
                'operation': 'store',
                'item': {'concept': 'integration_test', 'value': 'important_data'}
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.WORKING_MEMORY]
        )
        
        store_result = self.architecture.process_cognitive_task(store_task)
        self.assertTrue(store_result.get('success', False))
        
        # Retrieve and reason about the information
        reasoning_task = CognitiveTask(
            task_id="integration_002",
            task_type="remember_and_reason",
            input_data={
                'query': 'integration_test',
                'reasoning_type': 'analytical'
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[
                CognitiveModuleType.WORKING_MEMORY,
                CognitiveModuleType.NEUROSYMBOLIC_CORE
            ]
        )
        
        reasoning_result = self.architecture.process_cognitive_task(reasoning_task)
        self.assertIn('success', reasoning_result)
    
    def test_metacognitive_performance_monitoring(self):
        """Test metacognitive monitoring of performance across tasks."""
        # Process several tasks
        task_results = []
        
        for i in range(5):
            task = CognitiveTask(
                task_id=f"performance_test_{i}",
                task_type="test_task",
                input_data={'test_data': f'data_{i}'},
                priority=ProcessingPriority.MEDIUM,
                required_modules=[CognitiveModuleType.WORKING_MEMORY]
            )
            
            result = self.architecture.process_cognitive_task(task)
            task_results.append({
                'task_type': task.task_type,
                'success': result.get('success', False),
                'confidence': 0.8,
                'completion_time': 1.0
            })
        
        # Monitor performance
        monitor_task = CognitiveTask(
            task_id="performance_monitor",
            task_type="performance_evaluation",
            input_data={
                'operation': 'evaluate_performance',
                'task_results': task_results
            },
            priority=ProcessingPriority.HIGH,
            required_modules=[CognitiveModuleType.METACOGNITIVE_MONITOR]
        )
        
        monitor_result = self.architecture.process_cognitive_task(monitor_task)
        self.assertTrue(monitor_result.get('success', False))
        self.assertIn('performance_metrics', monitor_result)


def run_enhanced_cognitive_tests():
    """Run all tests for the enhanced cognitive architecture."""
    
    if not ARCHITECTURE_AVAILABLE:
        print("❌ Enhanced Cognitive Architecture not available for testing")
        print("   Please ensure all dependencies are installed and modules are accessible")
        return False
    
    print("🧠 Running Enhanced Cognitive Architecture Test Suite")
    print("=" * 65)
    
    # Create test suite
    test_classes = [
        TestCognitiveTask,
        TestWorkingMemoryModule,
        TestEpisodicMemoryModule,
        TestMetacognitiveMonitor,
        TestExecutiveController,
        TestEnhancedCognitiveArchitecture,
        TestDemonstration,
        TestIntegrationScenarios
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
    print(f"\n📊 TEST SUMMARY:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {failed_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "   Success Rate: 0%")
    
    if failed_tests == 0:
        print(f"\n🎉 ALL TESTS PASSED! Enhanced Cognitive Architecture is ready for use.")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Please review and fix issues before deployment.")
        return False


if __name__ == "__main__":
    success = run_enhanced_cognitive_tests()
    
    if success:
        print(f"\n🚀 Running demonstration...")
        demonstrate_enhanced_cognitive_architecture()
    
    sys.exit(0 if success else 1)
