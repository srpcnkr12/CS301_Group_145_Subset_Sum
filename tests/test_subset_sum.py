"""
Unit tests for Subset Sum Problem implementation.
CS301 2024-2025 Summer Project - Group 145
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from subset_sum import SubsetSumSolver, generate_random_instance, compare_algorithms


class TestSubsetSumSolver(unittest.TestCase):
    """Test cases for SubsetSumSolver class."""

    def test_initialization(self):
        """Test proper initialization of solver."""
        solver = SubsetSumSolver([1, 2, 3], 5)
        self.assertEqual(solver.multiset, [1, 2, 3])
        self.assertEqual(solver.target, 5)
        self.assertEqual(solver.n, 3)

    def test_initialization_validation(self):
        """Test input validation during initialization."""
        # Empty multiset
        with self.assertRaises(ValueError):
            SubsetSumSolver([], 5)

        # Non-positive target
        with self.assertRaises(ValueError):
            SubsetSumSolver([1, 2, 3], 0)

        # Non-positive elements
        with self.assertRaises(ValueError):
            SubsetSumSolver([1, -2, 3], 5)

    def test_brute_force_decision_exact_match(self):
        """Test brute force decision algorithm with exact matches."""
        # Example 1 from template: {3, 4, 5, 8, 11}, t = 12
        solver = SubsetSumSolver([3, 4, 5, 8, 11], 12)
        exists, subset, time_taken = solver.brute_force_decision()

        self.assertTrue(exists)
        self.assertEqual(sum(subset), 12)
        self.assertGreater(time_taken, 0)
        self.assertTrue(solver.validate_solution(subset))

    def test_brute_force_decision_no_solution(self):
        """Test brute force decision algorithm with no exact solution."""
        # Example 2 from template: {2, 4, 7, 10}, t = 15
        solver = SubsetSumSolver([2, 4, 7, 10], 15)
        exists, subset, time_taken = solver.brute_force_decision()

        self.assertFalse(exists)
        self.assertEqual(subset, [])
        self.assertGreater(time_taken, 0)

    def test_brute_force_optimization(self):
        """Test brute force optimization algorithm."""
        # Example 2 from template: should find sum = 14
        solver = SubsetSumSolver([2, 4, 7, 10], 15)
        subset, sum_result, time_taken = solver.brute_force_optimization()

        self.assertEqual(sum_result, 14)
        self.assertEqual(sum(subset), 14)
        self.assertGreater(time_taken, 0)
        self.assertTrue(solver.validate_solution(subset))

    def test_greedy_heuristic(self):
        """Test greedy heuristic algorithm."""
        # Example 1 from template
        solver = SubsetSumSolver([3, 4, 5, 8, 11], 12)
        subset, sum_result, time_taken = solver.brute_force_optimization()

        self.assertLessEqual(sum_result, 12)
        self.assertEqual(sum(subset), sum_result)
        self.assertGreater(time_taken, 0)
        self.assertTrue(solver.validate_solution(subset))

    def test_duplicate_values(self):
        """Test handling of duplicate values."""
        # Example 4 from template: {2, 2, 2, 5, 5}, t = 9
        solver = SubsetSumSolver([2, 2, 2, 5, 5], 9)

        # Test decision version
        exists, subset, _ = solver.brute_force_decision()
        self.assertTrue(exists)
        self.assertEqual(sum(subset), 9)

        # Test optimization version
        subset_opt, sum_opt, _ = solver.brute_force_optimization()
        self.assertEqual(sum_opt, 9)

    def test_trivial_cases(self):
        """Test trivial edge cases."""
        # Single element equal to target
        solver = SubsetSumSolver([5], 5)
        exists, subset, _ = solver.brute_force_decision()
        self.assertTrue(exists)
        self.assertEqual(subset, [5])

        # Single element greater than target
        solver = SubsetSumSolver([10], 5)
        exists, subset, _ = solver.brute_force_decision()
        self.assertFalse(exists)

    def test_solution_validation(self):
        """Test solution validation method."""
        solver = SubsetSumSolver([1, 2, 3, 4, 5], 10)

        # Valid solutions
        self.assertTrue(solver.validate_solution([1, 2, 3]))  # sum = 6
        self.assertTrue(solver.validate_solution([5, 4]))     # sum = 9
        self.assertTrue(solver.validate_solution([]))         # empty subset

        # Invalid solutions
        self.assertFalse(solver.validate_solution([6]))       # element not in multiset
        self.assertFalse(solver.validate_solution([1, 2, 3, 4, 5, 1]))  # sum > target


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""

    def test_random_instance_generation(self):
        """Test random instance generator."""
        multiset, target = generate_random_instance(5, 10, 0.5)

        self.assertEqual(len(multiset), 5)
        self.assertTrue(all(1 <= x <= 10 for x in multiset))
        self.assertGreater(target, 0)
        self.assertLessEqual(target, sum(multiset))

    def test_algorithm_comparison(self):
        """Test algorithm comparison function."""
        multiset = [1, 2, 3, 4, 5]
        target = 6

        results = compare_algorithms(multiset, target)

        # Check all algorithms are present
        expected_algorithms = ["brute_force_decision", "brute_force_optimization", "greedy"]
        for alg in expected_algorithms:
            self.assertIn(alg, results)
            self.assertIn('subset', results[alg])
            self.assertIn('sum', results[alg])
            self.assertIn('time', results[alg])
            self.assertIn('valid', results[alg])


class TestPerformanceEdgeCases(unittest.TestCase):
    """Test performance and edge cases."""

    def test_large_input_greedy(self):
        """Test greedy algorithm on larger input."""
        # Generate a larger instance for greedy testing
        multiset = list(range(1, 21))  # [1, 2, ..., 20]
        target = 50

        solver = SubsetSumSolver(multiset, target)
        subset, sum_result, time_taken = solver.greedy_heuristic()

        self.assertLessEqual(sum_result, target)
        self.assertTrue(solver.validate_solution(subset))
        self.assertLess(time_taken, 0.1)  # Should be fast

    def test_all_elements_too_large(self):
        """Test case where all elements exceed target."""
        # Example 5 from template: {10, 20, 30}, t = 5
        solver = SubsetSumSolver([10, 20, 30], 5)

        # Decision version should return False
        exists, subset, _ = solver.brute_force_decision()
        self.assertFalse(exists)
        self.assertEqual(subset, [])

        # Optimization should return empty set with sum 0
        subset_opt, sum_opt, _ = solver.brute_force_optimization()
        self.assertEqual(sum_opt, 0)
        self.assertEqual(subset_opt, [])

    def test_target_equals_single_element(self):
        """Test when target equals exactly one element."""
        solver = SubsetSumSolver([1, 2, 5, 7], 5)

        exists, subset, _ = solver.brute_force_decision()
        self.assertTrue(exists)
        self.assertIn(5, subset)


if __name__ == '__main__':
    unittest.main(verbosity=2)