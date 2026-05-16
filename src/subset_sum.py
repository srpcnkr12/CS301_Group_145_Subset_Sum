"""
Subset Sum Problem Implementation
CS301 2024-2025 Summer Project - Group 145

Implements both brute force and heuristic algorithms for the Subset Sum problem.
"""

import time
from typing import List, Tuple, Optional, Set


class SubsetSumSolver:
    """
    Solver for the Subset Sum problem with both exact and heuristic algorithms.
    """

    def __init__(self, multiset: List[int], target: int):
        """
        Initialize the Subset Sum solver.

        Args:
            multiset: List of positive integers
            target: Target sum to achieve
        """
        if not multiset:
            raise ValueError("Multiset cannot be empty")
        if target <= 0:
            raise ValueError("Target must be positive")
        if any(x <= 0 for x in multiset):
            raise ValueError("All elements in multiset must be positive")

        self.multiset = multiset.copy()
        self.target = target
        self.n = len(multiset)

    def brute_force_decision(self) -> Tuple[bool, List[int], float]:
        """
        Optimized brute force solution for decision version using advanced pruning.

        Returns:
            Tuple of (exists_solution, solution_subset, execution_time)
        """
        start_time = time.time()

        # Preprocessing: sort in descending order for better pruning
        sorted_items = sorted([(self.multiset[i], i) for i in range(self.n)], reverse=True)
        sorted_multiset = [item[0] for item in sorted_items]

        # Precompute suffix sums for pruning
        suffix_sums = [0] * (self.n + 1)
        for i in range(self.n - 1, -1, -1):
            suffix_sums[i] = suffix_sums[i + 1] + sorted_multiset[i]

        def optimized_backtrack(index: int, current_sum: int, current_subset: List[int]) -> Optional[List[int]]:
            # Base Case 1: Target reached exactly
            if current_sum == self.target:
                return current_subset.copy()

            # Base Case 2: Out of bounds or sum exceeded
            if index >= self.n or current_sum > self.target:
                return None

            # Advanced Pruning: Check if remaining elements can reach target
            remaining_needed = self.target - current_sum
            if remaining_needed > suffix_sums[index]:
                return None

            # Advanced Pruning: Check if current element alone exceeds what's needed
            current_element = sorted_multiset[index]

            # Recursive Step 1: Include the current element (try larger elements first)
            if current_sum + current_element <= self.target:
                current_subset.append(current_element)
                result = optimized_backtrack(index + 1, current_sum + current_element, current_subset)
                if result is not None:
                    return result
                current_subset.pop()

            # Recursive Step 2: Exclude the current element
            # Additional pruning: skip if excluding would make target unreachable
            if remaining_needed <= suffix_sums[index + 1]:
                result = optimized_backtrack(index + 1, current_sum, current_subset)
                if result is not None:
                    return result

            return None

        solution = optimized_backtrack(0, 0, [])
        execution_time = time.time() - start_time

        if solution is not None:
            return True, solution, execution_time
        else:
            return False, [], execution_time

    def brute_force_optimization(self) -> Tuple[List[int], int, float]:
        """
        Memory-optimized brute force solution for optimization version with advanced pruning.
        Finds subset with maximum sum <= target.

        Returns:
            Tuple of (best_subset, best_sum, execution_time)
        """
        start_time = time.time()

        # Preprocessing: sort for better pruning
        sorted_items = sorted([(self.multiset[i], i) for i in range(self.n)], reverse=True)
        sorted_multiset = [item[0] for item in sorted_items]

        # Precompute suffix sums
        suffix_sums = [0] * (self.n + 1)
        for i in range(self.n - 1, -1, -1):
            suffix_sums[i] = suffix_sums[i + 1] + sorted_multiset[i]

        best_subset = []
        best_sum = 0

        def optimized_backtrack(index: int, current_sum: int, current_subset: List[int]):
            nonlocal best_subset, best_sum

            # Early termination: if we found target, we're done
            if current_sum == self.target:
                best_subset = current_subset.copy()
                best_sum = current_sum
                return True  # Signal to stop searching

            # Update best solution if current is better
            if current_sum <= self.target and current_sum > best_sum:
                best_subset = current_subset.copy()
                best_sum = current_sum

            # Base case: out of bounds
            if index >= self.n:
                return False

            # Advanced Pruning 1: Check if we can improve best_sum with remaining elements
            max_possible = current_sum + suffix_sums[index]
            if max_possible <= best_sum:
                return False

            # Advanced Pruning 2: If current element alone exceeds target, skip inclusion
            current_element = sorted_multiset[index]

            # Try including current element first (larger elements have priority)
            if current_sum + current_element <= self.target:
                current_subset.append(current_element)
                if optimized_backtrack(index + 1, current_sum + current_element, current_subset):
                    return True  # Found optimal solution
                current_subset.pop()

            # Advanced Pruning 3: Check if excluding current element can still beat best
            if current_sum + suffix_sums[index + 1] > best_sum:
                if optimized_backtrack(index + 1, current_sum, current_subset):
                    return True

            return False

        optimized_backtrack(0, 0, [])
        execution_time = time.time() - start_time

        return best_subset, best_sum, execution_time

    def greedy_heuristic(self) -> Tuple[List[int], int, float]:
        """
        Greedy heuristic algorithm.
        Sorts elements in descending order and greedily selects items.

        Returns:
            Tuple of (subset, sum, execution_time)
        """
        start_time = time.time()

        # Sort multiset in descending order with original indices
        indexed_multiset = [(self.multiset[i], i) for i in range(self.n)]
        indexed_multiset.sort(key=lambda x: x[0], reverse=True)

        current_sum = 0
        selected_subset = []

        for value, original_index in indexed_multiset:
            if current_sum + value <= self.target:
                current_sum += value
                selected_subset.append(value)

        execution_time = time.time() - start_time
        return selected_subset, current_sum, execution_time

    def improved_greedy_heuristic(self) -> Tuple[List[int], int, float]:
        """
        Improved greedy heuristic with better selection strategy.
        Uses value-to-remaining-space ratio for smarter selection.

        Returns:
            Tuple of (subset, sum, execution_time)
        """
        start_time = time.time()

        # Sort by value descending as base
        indexed_multiset = [(self.multiset[i], i) for i in range(self.n)]
        indexed_multiset.sort(key=lambda x: x[0], reverse=True)

        current_sum = 0
        selected_subset = []
        remaining_target = self.target

        for value, original_index in indexed_multiset:
            if current_sum + value <= self.target:
                # Calculate efficiency: value / remaining_space
                remaining_space = self.target - current_sum
                efficiency = value / remaining_space if remaining_space > 0 else 0

                # Be more selective as we approach target
                # Use theoretical threshold: include if efficiency > 1/remaining_elements
                remaining_elements = len([x for x in indexed_multiset if x not in selected_subset])
                efficiency_threshold = 1.0 / max(1, remaining_elements)
                if efficiency >= efficiency_threshold or remaining_space >= value * 2:
                    current_sum += value
                    selected_subset.append(value)

        # If we have remaining space, try to fill with smaller items
        if current_sum < self.target:
            remaining_items = [x for x in indexed_multiset
                             if x[0] not in selected_subset and x[0] <= self.target - current_sum]
            remaining_items.sort(key=lambda x: x[0])  # Small to large for remaining

            for value, _ in remaining_items:
                if current_sum + value <= self.target:
                    current_sum += value
                    selected_subset.append(value)

        execution_time = time.time() - start_time
        return selected_subset, current_sum, execution_time

    def dynamic_programming_approximation(self,
                                        max_target: int = None,
                                        max_items: int = None) -> Tuple[List[int], int, float]:
        """
        DP-based approximation for better quality (polynomial space).
        Uses pruned dynamic programming approach.

        Args:
            max_target: Maximum target value for which DP is feasible (default: n^2)
            max_items: Maximum number of items for which DP is feasible (default: log2(target))

        Returns:
            Tuple of (subset, sum, execution_time)
        """
        start_time = time.time()

        # Set reasonable defaults based on problem size
        if max_target is None:
            max_target = self.n * self.n  # O(n^2) space complexity
        if max_items is None:
            max_items = max(10, int(self.target.bit_length()))  # log-based on target

        # For small instances, DP is feasible
        if self.target <= max_target and self.n <= max_items:
            # Classic DP table approach
            dp = [[False for _ in range(self.target + 1)] for _ in range(self.n + 1)]
            dp[0][0] = True

            # Fill DP table
            for i in range(1, self.n + 1):
                for w in range(self.target + 1):
                    # Don't include current item
                    dp[i][w] = dp[i-1][w]

                    # Include current item if possible
                    if w >= self.multiset[i-1]:
                        dp[i][w] = dp[i][w] or dp[i-1][w - self.multiset[i-1]]

            # Find maximum achievable sum
            max_sum = 0
            for w in range(self.target, -1, -1):
                if dp[self.n][w]:
                    max_sum = w
                    break

            # Reconstruct solution
            subset = []
            w = max_sum
            for i in range(self.n, 0, -1):
                if w >= self.multiset[i-1] and dp[i-1][w - self.multiset[i-1]]:
                    subset.append(self.multiset[i-1])
                    w -= self.multiset[i-1]

            execution_time = time.time() - start_time
            return subset, max_sum, execution_time
        else:
            # Fall back to improved greedy for large instances
            return self.improved_greedy_heuristic()

    def fptas_approximation(self, epsilon: float) -> Tuple[List[int], int, float]:
        """
        Fully Polynomial-Time Approximation Scheme (FPTAS) for Subset Sum.
        Provides (1-ε) approximation ratio in O(n²/ε) time.

        Args:
            epsilon: Approximation parameter (0 < ε < 1, smaller = better approximation, longer time)

        Returns:
            Tuple of (subset, sum, execution_time)

        Raises:
            ValueError: If epsilon is not in valid range (0, 1)
        """
        start_time = time.time()

        if epsilon <= 0 or epsilon >= 1:
            raise ValueError(f"Epsilon must be in range (0, 1), got {epsilon}")

        # Determine threshold based on theoretical complexity bounds
        exact_dp_threshold = max(10, int(1 / epsilon))  # When exact DP becomes more efficient
        high_precision_threshold = 0.001  # When exact solution is required

        # For very small instances or high precision requirement, use exact DP
        if self.n <= exact_dp_threshold or epsilon < high_precision_threshold:
            return self.dynamic_programming_approximation()

        # FPTAS scaling technique
        max_element = max(self.multiset)
        scaling_factor = max(1, (epsilon * max_element) / self.n)

        # Scale down the multiset
        scaled_multiset = [max(1, int(x / scaling_factor)) for x in self.multiset]
        scaled_target = max(1, int(self.target / scaling_factor))

        # Run DP on scaled problem
        n = len(scaled_multiset)
        dp = [[False for _ in range(scaled_target + 1)] for _ in range(n + 1)]
        dp[0][0] = True

        # Fill DP table
        for i in range(1, n + 1):
            for w in range(scaled_target + 1):
                # Don't include current item
                dp[i][w] = dp[i-1][w]

                # Include current item if possible
                if w >= scaled_multiset[i-1]:
                    dp[i][w] = dp[i][w] or dp[i-1][w - scaled_multiset[i-1]]

        # Find maximum achievable scaled sum
        max_scaled_sum = 0
        for w in range(scaled_target, -1, -1):
            if dp[n][w]:
                max_scaled_sum = w
                break

        # Reconstruct solution using original multiset
        subset = []
        w = max_scaled_sum
        for i in range(n, 0, -1):
            if w >= scaled_multiset[i-1] and dp[i-1][w - scaled_multiset[i-1]]:
                subset.append(self.multiset[i-1])  # Use original values
                w -= scaled_multiset[i-1]

        actual_sum = sum(subset)

        # Verify and potentially improve solution
        if actual_sum <= self.target:
            # Try to add more elements to improve the solution
            remaining_elements = [x for x in self.multiset if x not in subset or subset.count(x) < self.multiset.count(x)]
            for element in sorted(remaining_elements, reverse=True):
                if actual_sum + element <= self.target:
                    subset.append(element)
                    actual_sum += element

        execution_time = time.time() - start_time
        return subset, actual_sum, execution_time

    def advanced_greedy_approximation(self) -> Tuple[List[int], int, float]:
        """
        Advanced greedy with multiple strategies and best result selection.

        Returns:
            Tuple of (subset, sum, execution_time)
        """
        start_time = time.time()

        strategies = []

        # Strategy 1: Standard greedy (largest first)
        subset1, sum1, _ = self.greedy_heuristic()
        strategies.append((subset1, sum1, "largest_first"))

        # Strategy 2: Smallest first (sometimes better for tight targets)
        sorted_elements = sorted([(self.multiset[i], i) for i in range(self.n)])
        current_sum = 0
        subset2 = []
        for value, _ in sorted_elements:
            if current_sum + value <= self.target:
                current_sum += value
                subset2.append(value)
        strategies.append((subset2, current_sum, "smallest_first"))

        # Strategy 3: Density-based (value per "space used")
        density_sorted = sorted([(self.multiset[i], i) for i in range(self.n)],
                               key=lambda x: x[0] / max(1, self.target - x[0]), reverse=True)
        current_sum = 0
        subset3 = []
        for value, _ in density_sorted:
            if current_sum + value <= self.target:
                current_sum += value
                subset3.append(value)
        strategies.append((subset3, current_sum, "density_based"))

        # Strategy 4: Balanced approach (mix of large and fitting elements)
        remaining_capacity = self.target
        subset4 = []
        current_sum = 0
        available = self.multiset.copy()

        while available and remaining_capacity > 0:
            # Choose element that maximizes value while considering remaining space
            best_element = None
            best_score = -1
            best_idx = -1

            for i, element in enumerate(available):
                if element <= remaining_capacity:
                    # Score based on value and how well it uses remaining space
                    score = element + (element / remaining_capacity) * 10
                    if score > best_score:
                        best_score = score
                        best_element = element
                        best_idx = i

            if best_element is not None:
                subset4.append(best_element)
                current_sum += best_element
                remaining_capacity -= best_element
                available.pop(best_idx)
            else:
                break

        strategies.append((subset4, current_sum, "balanced"))

        # Select best strategy
        best_subset, best_sum, best_strategy = max(strategies, key=lambda x: x[1])

        execution_time = time.time() - start_time
        return best_subset, best_sum, execution_time

    def solve(self, algorithm: str = "brute_force_optimization") -> Tuple[List[int], int, float]:
        """
        Solve using specified algorithm.

        Args:
            algorithm: "brute_force_decision", "brute_force_optimization", "greedy",
                      "improved_greedy", "dp_approximation", "fptas", or "advanced_greedy"

        Returns:
            Tuple of (subset, sum, execution_time)
        """
        if algorithm == "brute_force_decision":
            exists, subset, time_taken = self.brute_force_decision()
            return subset, sum(subset) if exists else 0, time_taken
        elif algorithm == "brute_force_optimization":
            return self.brute_force_optimization()
        elif algorithm == "greedy":
            return self.greedy_heuristic()
        elif algorithm == "improved_greedy":
            return self.improved_greedy_heuristic()
        elif algorithm == "dp_approximation":
            return self.dynamic_programming_approximation()
        elif algorithm == "fptas":
            return self.fptas_approximation()
        elif algorithm == "advanced_greedy":
            return self.advanced_greedy_approximation()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def validate_solution(self, subset: List[int]) -> bool:
        """
        Validate if a subset is a valid solution.

        Args:
            subset: Proposed solution subset

        Returns:
            True if subset is valid (all elements in multiset and sum <= target)
        """
        if not subset:
            return True  # Empty subset is always valid

        # Check if all elements in subset exist in multiset
        multiset_copy = self.multiset.copy()
        for element in subset:
            if element not in multiset_copy:
                return False
            multiset_copy.remove(element)

        # Check if sum is within target
        return sum(subset) <= self.target


def generate_random_instance(n: int, max_value: int, target_ratio: float = 0.5) -> Tuple[List[int], int]:
    """
    Generate a random instance of Subset Sum problem.

    Args:
        n: Number of elements in multiset
        max_value: Maximum value for elements
        target_ratio: Target as ratio of total sum

    Returns:
        Tuple of (multiset, target)
    """
    import random

    multiset = [random.randint(1, max_value) for _ in range(n)]
    total_sum = sum(multiset)
    target = int(total_sum * target_ratio)

    # Ensure target is at least 1
    target = max(1, target)

    return multiset, target


def compare_algorithms(multiset: List[int], target: int) -> dict:
    """
    Compare all algorithms on the same instance.

    Args:
        multiset: Input multiset
        target: Target sum

    Returns:
        Dictionary with results for each algorithm
    """
    solver = SubsetSumSolver(multiset, target)
    results = {}

    # Test all algorithms
    algorithms = ["brute_force_decision", "brute_force_optimization", "greedy"]

    for alg in algorithms:
        try:
            subset, sum_result, time_taken = solver.solve(alg)
            results[alg] = {
                'subset': subset,
                'sum': sum_result,
                'time': time_taken,
                'valid': solver.validate_solution(subset)
            }
        except Exception as e:
            results[alg] = {
                'error': str(e),
                'subset': [],
                'sum': 0,
                'time': 0,
                'valid': False
            }

    return results


if __name__ == "__main__":
    # Example usage from template
    print("Subset Sum Problem Solver")
    print("=" * 40)

    # Test examples from template
    test_cases = [
        ([3, 4, 5, 8, 11], 12),  # Example 1: Standard Yes Instance
        ([2, 4, 7, 10], 15),     # Example 2: No Exact Match
        ([1, 2, 3, 4, 5], 5),    # Example 3: Multiple Valid Subsets
        ([2, 2, 2, 5, 5], 9),    # Example 4: Duplicate Values
        ([10, 20, 30], 5)        # Example 5: Trivial Zero
    ]

    for i, (multiset, target) in enumerate(test_cases, 1):
        print(f"\nExample {i}: S = {multiset}, t = {target}")
        print("-" * 30)

        results = compare_algorithms(multiset, target)

        for alg, result in results.items():
            if 'error' not in result:
                print(f"{alg.upper():<20}: {result['subset']} -> {result['sum']} "
                      f"({result['time']:.6f}s)")
            else:
                print(f"{alg.upper():<20}: ERROR - {result['error']}")