"""
Section 5 - Algorithm Implementation Testing
CS301 2024-2025 Summer Project - Group 145

This module implements comprehensive testing for both brute force and heuristic algorithms
as required by CS301 template sections 5.1 and 5.2.
"""

import sys
import os
sys.path.append('../src')

import json
import time
from typing import Dict, List, Any
from subset_sum import SubsetSumSolver
from instance_generator import SubsetSumInstanceGenerator

def section5_1_brute_force_testing():
    """
    Section 5.1: Brute Force Algorithm Testing
    Tests the brute force implementation on various sized instances
    """
    print("="*80)
    print("SECTION 5.1 - BRUTE FORCE ALGORITHM TESTING")
    print("="*80)

    generator = SubsetSumInstanceGenerator(seed=42)
    test_results = []

    # Test different sizes from 5 to 15 elements
    test_sizes = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    total_tests = 0
    total_failures = 0

    for size in test_sizes:
        print(f"\nTesting size {size}:")

        # Generate multiple instances per size
        instances_per_size = 15 if size <= 10 else 10

        for i in range(instances_per_size):
            # Generate test instance
            multiset, target = generator.generate_uniform_random(
                size, min_val=1, max_val=20, target_ratio=0.5
            )

            solver = SubsetSumSolver(multiset, target)

            try:
                # Test decision version
                start_time = time.time()
                exists, decision_solution, decision_time = solver.brute_force_decision()

                # Test optimization version
                opt_solution, opt_sum, opt_time = solver.brute_force_optimization()

                # Validate solutions
                decision_valid = solver.validate_solution(decision_solution)
                opt_valid = solver.validate_solution(opt_solution)

                test_results.append({
                    'size': size,
                    'instance': i + 1,
                    'multiset': multiset,
                    'target': target,
                    'decision_exists': exists,
                    'decision_solution': decision_solution,
                    'decision_time': decision_time,
                    'decision_valid': decision_valid,
                    'opt_solution': opt_solution,
                    'opt_sum': opt_sum,
                    'opt_time': opt_time,
                    'opt_valid': opt_valid,
                    'status': 'PASSED' if decision_valid and opt_valid else 'FAILED'
                })

                total_tests += 1
                if not (decision_valid and opt_valid):
                    total_failures += 1
                    print(f"  ❌ Instance {i+1}: Validation failed")
                else:
                    print(f"  ✅ Instance {i+1}: {decision_time:.6f}s + {opt_time:.6f}s")

            except Exception as e:
                test_results.append({
                    'size': size,
                    'instance': i + 1,
                    'error': str(e),
                    'status': 'ERROR'
                })
                total_tests += 1
                total_failures += 1
                print(f"  ❌ Instance {i+1}: Error - {e}")

    # Generate report
    summary = {
        'total_tests': total_tests,
        'total_failures': total_failures,
        'success_rate': ((total_tests - total_failures) / total_tests * 100) if total_tests > 0 else 0,
        'tested_sizes': test_sizes,
        'max_size_tested': max(test_sizes),
        'avg_time_per_test': sum(r.get('decision_time', 0) + r.get('opt_time', 0)
                                for r in test_results if 'decision_time' in r) / total_tests
    }

    report = {
        'section': '5.1',
        'description': 'Brute Force Algorithm Testing',
        'summary': summary,
        'detailed_results': test_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Save results
    os.makedirs('../results', exist_ok=True)
    with open('../results/section5_1_brute_force_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*80}")
    print("SECTION 5.1 SUMMARY")
    print(f"{'='*80}")
    print(f"Total tests: {total_tests}")
    print(f"Successful tests: {total_tests - total_failures}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    print(f"Max size tested: {summary['max_size_tested']} elements")
    print(f"Average time per test: {summary['avg_time_per_test']:.6f}s")

    return report

def section5_2_heuristic_testing():
    """
    Section 5.2: Heuristic Algorithm Testing
    Tests 15-20 samples using heuristic algorithms
    """
    print("\n" + "="*80)
    print("SECTION 5.2 - HEURISTIC ALGORITHM TESTING")
    print("="*80)

    generator = SubsetSumInstanceGenerator(seed=123)
    algorithms = ['GREEDY', 'IMPROVED_GREEDY', 'DP_APPROXIMATION']
    test_results = []

    # Generate 20 diverse test samples
    samples = []
    sample_configs = [
        {'type': 'uniform', 'size': 25, 'target_ratio': 0.4},
        {'type': 'uniform', 'size': 30, 'target_ratio': 0.5},
        {'type': 'uniform', 'size': 35, 'target_ratio': 0.6},
        {'type': 'clustered', 'size': 20, 'clusters': 3},
        {'type': 'clustered', 'size': 25, 'clusters': 4},
        {'type': 'high_density', 'size': 15, 'target_ratio': 0.8},
        {'type': 'high_density', 'size': 20, 'target_ratio': 0.75},
        {'type': 'low_density', 'size': 30, 'target_ratio': 0.3},
        {'type': 'low_density', 'size': 35, 'target_ratio': 0.25},
        {'type': 'uniform', 'size': 40, 'target_ratio': 0.45},
        {'type': 'uniform', 'size': 45, 'target_ratio': 0.55},
        {'type': 'clustered', 'size': 30, 'clusters': 5},
        {'type': 'high_density', 'size': 25, 'target_ratio': 0.7},
        {'type': 'low_density', 'size': 40, 'target_ratio': 0.35},
        {'type': 'uniform', 'size': 50, 'target_ratio': 0.5},
        {'type': 'uniform', 'size': 28, 'target_ratio': 0.42},
        {'type': 'clustered', 'size': 35, 'clusters': 4},
        {'type': 'high_density', 'size': 18, 'target_ratio': 0.85},
        {'type': 'low_density', 'size': 45, 'target_ratio': 0.28},
        {'type': 'uniform', 'size': 32, 'target_ratio': 0.48}
    ]

    for i, config in enumerate(sample_configs):
        if config['type'] == 'uniform':
            multiset, target = generator.generate_uniform_random(
                config['size'], min_val=1, max_val=50, target_ratio=config['target_ratio']
            )
        elif config['type'] == 'clustered':
            multiset, target = generator.generate_clustered_values(
                config['size'], num_clusters=config['clusters'], cluster_width=10, target_ratio=0.5
            )
        elif config['type'] == 'high_density':
            multiset, target = generator.generate_high_density(
                config['size'], target_ratio=config['target_ratio']
            )
        else:  # low_density
            multiset, target = generator.generate_low_density(
                config['size'], target_ratio=config['target_ratio']
            )

        samples.append({
            'id': i + 1,
            'type': config['type'],
            'multiset': multiset,
            'target': target,
            'size': len(multiset)
        })

    total_tests = 0
    total_failures = 0

    for sample in samples:
        print(f"\nSample {sample['id']} ({sample['type']}, size={sample['size']}):")

        solver = SubsetSumSolver(sample['multiset'], sample['target'])
        sample_results = {'sample_info': sample}

        for algorithm in algorithms:
            try:
                if algorithm == 'GREEDY':
                    solution, sum_result, exec_time = solver.greedy_heuristic()
                elif algorithm == 'IMPROVED_GREEDY':
                    solution, sum_result, exec_time = solver.improved_greedy_heuristic()
                elif algorithm == 'DP_APPROXIMATION':
                    solution, sum_result, exec_time = solver.dynamic_programming_approximation()

                # Validate solution
                is_valid = solver.validate_solution(solution)

                sample_results[algorithm] = {
                    'solution': solution,
                    'sum': sum_result,
                    'execution_time': exec_time,
                    'valid': is_valid,
                    'target_ratio': sum_result / sample['target'] if sample['target'] > 0 else 0
                }

                total_tests += 1
                if not is_valid:
                    total_failures += 1
                    print(f"  ❌ {algorithm}: Invalid solution")
                else:
                    print(f"  ✅ {algorithm}: {sum_result}/{sample['target']} ({sum_result/sample['target']*100:.1f}%) in {exec_time:.6f}s")

            except Exception as e:
                sample_results[algorithm] = {
                    'error': str(e),
                    'valid': False
                }
                total_tests += 1
                total_failures += 1
                print(f"  ❌ {algorithm}: Error - {e}")

        test_results.append(sample_results)

    # Generate summary
    algorithm_stats = {}
    for algorithm in algorithms:
        valid_tests = [r for r in test_results if algorithm in r and r[algorithm].get('valid', False)]
        algorithm_stats[algorithm] = {
            'total_tests': len([r for r in test_results if algorithm in r]),
            'valid_tests': len(valid_tests),
            'avg_target_ratio': sum(r[algorithm]['target_ratio'] for r in valid_tests) / len(valid_tests) if valid_tests else 0,
            'avg_execution_time': sum(r[algorithm]['execution_time'] for r in valid_tests) / len(valid_tests) if valid_tests else 0
        }

    summary = {
        'total_samples': len(samples),
        'total_tests': total_tests,
        'total_failures': total_failures,
        'success_rate': ((total_tests - total_failures) / total_tests * 100) if total_tests > 0 else 0,
        'algorithms_tested': algorithms,
        'algorithm_statistics': algorithm_stats
    }

    report = {
        'section': '5.2',
        'description': 'Heuristic Algorithm Testing on 20 Samples',
        'summary': summary,
        'samples': samples,
        'detailed_results': test_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Save results
    with open('../results/section5_2_heuristic_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*80}")
    print("SECTION 5.2 SUMMARY")
    print(f"{'='*80}")
    print(f"Total samples: {summary['total_samples']}")
    print(f"Total algorithm tests: {total_tests}")
    print(f"Successful tests: {total_tests - total_failures}")
    print(f"Success rate: {summary['success_rate']:.1f}%")

    for algorithm, stats in algorithm_stats.items():
        print(f"\n{algorithm}:")
        print(f"  Valid tests: {stats['valid_tests']}/{stats['total_tests']}")
        print(f"  Avg target achievement: {stats['avg_target_ratio']*100:.1f}%")
        print(f"  Avg execution time: {stats['avg_execution_time']:.6f}s")

    return report

if __name__ == "__main__":
    # Run both sections
    section5_1_report = section5_1_brute_force_testing()
    section5_2_report = section5_2_heuristic_testing()

    print(f"\n{'='*80}")
    print("SECTION 5 COMPLETE - ALL ALGORITHM IMPLEMENTATIONS TESTED")
    print(f"{'='*80}")