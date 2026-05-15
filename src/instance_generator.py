"""
Random Instance Generator for Subset Sum Problem
CS301 2024-2025 Summer Project - Group 145 - Section 4

Implements parametric algorithm to produce random sample inputs.
"""

import random
from typing import List, Tuple, Dict
import math


class SubsetSumInstanceGenerator:
    """
    Parametric random instance generator for Subset Sum problem.
    Generates instances with different characteristics and difficulty levels.
    """

    def __init__(self, seed: int = None):
        """
        Initialize the instance generator.

        Args:
            seed: Random seed for reproducible results
        """
        if seed is not None:
            random.seed(seed)

    def generate_uniform_random(self, n: int, min_val: int = 1, max_val: int = 100,
                               target_ratio: float = 0.5) -> Tuple[List[int], int]:
        """
        Generate uniform random instance.

        Args:
            n: Number of elements in multiset
            min_val: Minimum value for elements
            max_val: Maximum value for elements
            target_ratio: Target as ratio of total sum

        Returns:
            Tuple of (multiset, target)
        """
        multiset = [random.randint(min_val, max_val) for _ in range(n)]
        total_sum = sum(multiset)
        target = max(1, int(total_sum * target_ratio))
        return multiset, target

    def generate_with_duplicates(self, n: int, unique_values: int,
                                target_ratio: float = 0.5) -> Tuple[List[int], int]:
        """
        Generate instance with intentional duplicate values.

        Args:
            n: Total number of elements
            unique_values: Number of unique values
            target_ratio: Target as ratio of total sum

        Returns:
            Tuple of (multiset, target)
        """
        if unique_values > n:
            unique_values = n

        # Create unique values
        unique_vals = [random.randint(1, 50) for _ in range(unique_values)]

        # Create multiset with duplicates
        multiset = []
        for _ in range(n):
            multiset.append(random.choice(unique_vals))

        total_sum = sum(multiset)
        target = max(1, int(total_sum * target_ratio))
        return multiset, target

    def generate_hard_instance(self, n: int, density: str = "dense") -> Tuple[List[int], int]:
        """
        Generate deliberately hard instances for testing algorithm limits.

        Args:
            n: Number of elements
            density: "sparse", "medium", or "dense"

        Returns:
            Tuple of (multiset, target)
        """
        if density == "sparse":
            # Large range, low target
            multiset = [random.randint(1, n*10) for _ in range(n)]
            target = max(1, sum(multiset) // 4)
        elif density == "dense":
            # Small range, high target
            multiset = [random.randint(1, 20) for _ in range(n)]
            target = max(1, int(sum(multiset) * 0.8))
        else:  # medium
            multiset = [random.randint(1, n*2) for _ in range(n)]
            target = max(1, sum(multiset) // 2)

        return multiset, target

    def generate_exact_solution_instance(self, n: int) -> Tuple[List[int], int]:
        """
        Generate instance guaranteed to have exact solution.

        Args:
            n: Number of elements

        Returns:
            Tuple of (multiset, target)
        """
        # Create multiset
        multiset = [random.randint(1, 50) for _ in range(n)]

        # Choose random subset for exact solution
        subset_size = random.randint(1, min(n, 4))  # Small subset for feasibility
        subset_indices = random.sample(range(n), subset_size)
        target = sum(multiset[i] for i in subset_indices)

        return multiset, target

    def generate_no_solution_instance(self, n: int) -> Tuple[List[int], int]:
        """
        Generate instance guaranteed to have no exact solution.

        Args:
            n: Number of elements

        Returns:
            Tuple of (multiset, target)
        """
        multiset = [random.randint(2, 20) * 2 for _ in range(n)]  # All even
        target = random.randint(1, 10) * 2 + 1  # Odd target
        return multiset, target

    def generate_benchmark_suite(self, sizes: List[int], samples_per_size: int = 5) -> List[Dict]:
        """
        Generate comprehensive benchmark suite.

        Args:
            sizes: List of problem sizes to test
            samples_per_size: Number of instances per size

        Returns:
            List of benchmark instances
        """
        instances = []
        instance_id = 1

        for size in sizes:
            for sample in range(samples_per_size):
                # Generate different types of instances
                instance_types = [
                    ("uniform_easy", lambda: self.generate_uniform_random(size, 1, 20, 0.4)),
                    ("uniform_medium", lambda: self.generate_uniform_random(size, 1, 50, 0.5)),
                    ("uniform_hard", lambda: self.generate_uniform_random(size, 1, 100, 0.7)),
                    ("duplicates", lambda: self.generate_with_duplicates(size, max(2, size//3))),
                    ("hard_sparse", lambda: self.generate_hard_instance(size, "sparse")),
                    ("hard_dense", lambda: self.generate_hard_instance(size, "dense")),
                    ("exact_solution", lambda: self.generate_exact_solution_instance(size)),
                    ("no_solution", lambda: self.generate_no_solution_instance(size))
                ]

                for type_name, generator in instance_types:
                    multiset, target = generator()

                    instances.append({
                        'id': instance_id,
                        'type': type_name,
                        'size': size,
                        'multiset': multiset.copy(),
                        'target': target,
                        'total_sum': sum(multiset),
                        'density': len(set(multiset)) / len(multiset),  # Uniqueness ratio
                        'max_value': max(multiset),
                        'min_value': min(multiset)
                    })
                    instance_id += 1

        return instances

    def generate_realistic_distribution(self, n: int, distribution_type: str = "normal") -> Tuple[List[int], int]:
        """
        Generate instances with realistic distributions.

        Args:
            n: Number of elements
            distribution_type: "normal", "exponential", "power_law", "bimodal"

        Returns:
            Tuple of (multiset, target)
        """
        import math

        if distribution_type == "normal":
            # Normal distribution around mean=20, std=8
            mean, std = 20, 8
            multiset = []
            for _ in range(n):
                val = max(1, int(random.normalvariate(mean, std)))
                multiset.append(val)
            target_ratio = random.uniform(0.4, 0.6)
            target = max(1, int(sum(multiset) * target_ratio))

        elif distribution_type == "exponential":
            # Exponential distribution (many small values, few large)
            lambd = 0.2
            multiset = []
            for _ in range(n):
                val = max(1, int(random.expovariate(lambd)))
                multiset.append(val)
            target_ratio = random.uniform(0.3, 0.7)
            target = max(1, int(sum(multiset) * target_ratio))

        elif distribution_type == "power_law":
            # Power law distribution (scale-free)
            alpha = 2.5
            multiset = []
            for _ in range(n):
                u = random.random()
                val = max(1, int((1 - u) ** (-1/(alpha-1))))
                multiset.append(min(val, 100))  # Cap at 100
            target_ratio = random.uniform(0.4, 0.6)
            target = max(1, int(sum(multiset) * target_ratio))

        elif distribution_type == "bimodal":
            # Two-peak distribution
            multiset = []
            for _ in range(n):
                if random.random() < 0.6:
                    val = max(1, int(random.normalvariate(10, 3)))
                else:
                    val = max(1, int(random.normalvariate(40, 5)))
                multiset.append(val)
            target_ratio = random.uniform(0.45, 0.55)
            target = max(1, int(sum(multiset) * target_ratio))

        else:
            # Default to uniform
            return self.generate_uniform_random(n)

        return multiset, target

    def generate_correlated_instance(self, n: int, correlation_strength: float = 0.7) -> Tuple[List[int], int]:
        """
        Generate instance where element values are correlated.

        Args:
            n: Number of elements
            correlation_strength: 0=no correlation, 1=strong correlation

        Returns:
            Tuple of (multiset, target)
        """
        base_value = random.randint(5, 25)
        multiset = [base_value]

        for _ in range(n - 1):
            if random.random() < correlation_strength:
                # Correlated value (close to previous)
                variation = random.randint(-3, 3)
                new_val = max(1, multiset[-1] + variation)
            else:
                # Random value
                new_val = random.randint(1, 50)
            multiset.append(new_val)

        target_ratio = random.uniform(0.4, 0.6)
        target = max(1, int(sum(multiset) * target_ratio))
        return multiset, target

    def generate_adversarial_instance(self, n: int, adversarial_type: str = "greedy_worst") -> Tuple[List[int], int]:
        """
        Generate adversarial instances that challenge specific algorithms.

        Args:
            n: Number of elements
            adversarial_type: "greedy_worst", "dp_memory_intensive", "backtrack_deep"

        Returns:
            Tuple of (multiset, target)
        """
        if adversarial_type == "greedy_worst":
            # Large elements that don't fit well together (bad for greedy)
            multiset = []
            target = 100
            # Add elements slightly larger than target/2
            for i in range(n//2):
                multiset.append(target//2 + random.randint(1, 5))
            # Add small elements that could combine well
            for i in range(n - n//2):
                multiset.append(random.randint(1, target//4))

        elif adversarial_type == "dp_memory_intensive":
            # Large target relative to element values (memory intensive for DP)
            max_element = 10
            multiset = [random.randint(1, max_element) for _ in range(n)]
            target = sum(multiset) * 2  # Unreachable target

        elif adversarial_type == "backtrack_deep":
            # Elements that require deep exploration
            multiset = []
            target = 50
            # Add elements that sum to just under target in many combinations
            for _ in range(n):
                multiset.append(target // n + random.randint(-2, 2))
            target = sum(multiset[:n//2])  # Target achievable by half the elements

        else:
            return self.generate_uniform_random(n)

        return multiset, max(1, target)

    def generate_scaled_benchmark_suite(self, base_sizes: List[int],
                                       scale_factors: List[int] = [1, 2, 5, 10]) -> List[Dict]:
        """
        Generate scalable benchmark suite with multiple difficulty levels.

        Args:
            base_sizes: Base problem sizes
            scale_factors: Scaling factors for each size

        Returns:
            List of benchmark instances
        """
        instances = []
        instance_id = 1

        for base_size in base_sizes:
            for scale in scale_factors:
                size = base_size * scale

                # Generate multiple instance types at each scaled size
                instance_types = [
                    ("uniform_easy", lambda: self.generate_uniform_random(size, 1, 20, 0.4)),
                    ("uniform_hard", lambda: self.generate_uniform_random(size, 1, 100, 0.7)),
                    ("realistic_normal", lambda: self.generate_realistic_distribution(size, "normal")),
                    ("realistic_exponential", lambda: self.generate_realistic_distribution(size, "exponential")),
                    ("realistic_power_law", lambda: self.generate_realistic_distribution(size, "power_law")),
                    ("correlated_weak", lambda: self.generate_correlated_instance(size, 0.3)),
                    ("correlated_strong", lambda: self.generate_correlated_instance(size, 0.8)),
                    ("adversarial_greedy", lambda: self.generate_adversarial_instance(size, "greedy_worst")),
                    ("adversarial_dp", lambda: self.generate_adversarial_instance(size, "dp_memory_intensive")),
                    ("adversarial_backtrack", lambda: self.generate_adversarial_instance(size, "backtrack_deep")),
                    ("exact_solution", lambda: self.generate_exact_solution_instance(size)),
                    ("no_solution", lambda: self.generate_no_solution_instance(size))
                ]

                for type_name, generator in instance_types:
                    try:
                        multiset, target = generator()

                        instances.append({
                            'id': instance_id,
                            'type': type_name,
                            'size': size,
                            'base_size': base_size,
                            'scale_factor': scale,
                            'multiset': multiset.copy(),
                            'target': target,
                            'total_sum': sum(multiset),
                            'density': len(set(multiset)) / len(multiset),
                            'max_value': max(multiset),
                            'min_value': min(multiset),
                            'target_ratio': target / sum(multiset) if sum(multiset) > 0 else 0,
                            'difficulty_estimate': self._estimate_difficulty(multiset, target)
                        })
                        instance_id += 1
                    except Exception as e:
                        print(f"Warning: Failed to generate {type_name} instance of size {size}: {e}")
                        continue

        return instances

    def _estimate_difficulty(self, multiset: List[int], target: int) -> str:
        """
        Estimate difficulty level of an instance.

        Args:
            multiset: Problem multiset
            target: Target value

        Returns:
            Difficulty level: "trivial", "easy", "medium", "hard", "extreme"
        """
        n = len(multiset)
        total_sum = sum(multiset)
        unique_ratio = len(set(multiset)) / n
        target_ratio = target / total_sum if total_sum > 0 else 0

        # Calculate difficulty score based on various factors
        difficulty_score = 0

        # Size factor
        if n <= 5:
            difficulty_score += 1
        elif n <= 10:
            difficulty_score += 2
        elif n <= 15:
            difficulty_score += 3
        else:
            difficulty_score += 4

        # Target ratio factor (extremes are harder)
        if 0.4 <= target_ratio <= 0.6:
            difficulty_score += 2  # Medium difficulty
        elif 0.2 <= target_ratio < 0.4 or 0.6 < target_ratio <= 0.8:
            difficulty_score += 3  # Harder
        else:
            difficulty_score += 4  # Very hard

        # Uniqueness factor (more unique = potentially harder)
        if unique_ratio > 0.8:
            difficulty_score += 2
        elif unique_ratio > 0.6:
            difficulty_score += 1

        # Value range factor
        value_range = max(multiset) - min(multiset)
        if value_range > 50:
            difficulty_score += 1

        # Classify based on total score
        if difficulty_score <= 3:
            return "trivial"
        elif difficulty_score <= 5:
            return "easy"
        elif difficulty_score <= 7:
            return "medium"
        elif difficulty_score <= 9:
            return "hard"
        else:
            return "extreme"

    def save_instances_to_file(self, instances: List[Dict], filename: str):
        """
        Save generated instances to file.

        Args:
            instances: List of instances to save
            filename: Output filename
        """
        import json

        with open(filename, 'w') as f:
            json.dump(instances, f, indent=2)

        print(f"Saved {len(instances)} instances to {filename}")

    def load_instances_from_file(self, filename: str) -> List[Dict]:
        """
        Load instances from file.

        Args:
            filename: Input filename

        Returns:
            List of loaded instances
        """
        import json

        with open(filename, 'r') as f:
            instances = json.load(f)

        print(f"Loaded {len(instances)} instances from {filename}")
        return instances


# Algorithm implementation for generator pseudocode documentation
def generate_random_subset_sum_instance_pseudocode():
    """
    Pseudocode for random instance generation algorithm.

    Algorithm RandomSubsetSumInstance(n, min_val, max_val, target_ratio)
    Input:
        n - number of elements
        min_val, max_val - value range
        target_ratio - target as fraction of total sum
    Output:
        (multiset S, target t)

    BEGIN
        S = empty list
        FOR i = 1 TO n DO
            value = Random(min_val, max_val)
            S.append(value)
        END FOR

        total_sum = Sum(S)
        t = max(1, floor(total_sum * target_ratio))

        RETURN (S, t)
    END
    """
    pass


if __name__ == "__main__":
    # Example usage and testing
    print("Subset Sum Instance Generator")
    print("=" * 40)

    generator = SubsetSumInstanceGenerator(seed=42)

    # Generate various types of instances
    print("1. Uniform Random Instance:")
    multiset, target = generator.generate_uniform_random(8, 1, 20, 0.5)
    print(f"   S = {multiset}, t = {target}")

    print("\n2. Instance with Duplicates:")
    multiset, target = generator.generate_with_duplicates(10, 4, 0.6)
    print(f"   S = {multiset}, t = {target}")

    print("\n3. Hard Instance (dense):")
    multiset, target = generator.generate_hard_instance(6, "dense")
    print(f"   S = {multiset}, t = {target}")

    print("\n4. Exact Solution Instance:")
    multiset, target = generator.generate_exact_solution_instance(7)
    print(f"   S = {multiset}, t = {target}")

    print("\n5. No Solution Instance:")
    multiset, target = generator.generate_no_solution_instance(5)
    print(f"   S = {multiset}, t = {target}")

    # Generate benchmark suite
    print("\n6. Benchmark Suite Generation:")
    instances = generator.generate_benchmark_suite([3, 4, 5], samples_per_size=2)
    print(f"   Generated {len(instances)} benchmark instances")

    # Show sample instance
    sample = instances[0]
    print(f"   Sample: {sample['type']} - S={sample['multiset']}, t={sample['target']}")