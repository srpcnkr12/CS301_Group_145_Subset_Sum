"""
Section 8 - Functional Testing
CS301 2024-2025 Summer Project - Group 145

This module implements functional testing to verify implementation correctness
as required by CS301 template section 8.
"""

import sys
import os
sys.path.append('../src')

import json
import time
from typing import Dict, List, Any
from subset_sum import SubsetSumSolver
from instance_generator import SubsetSumInstanceGenerator

def run_section8_functional_testing():
    """
    Section 8: Functional Testing for Implementation Correctness
    Tests implementation correctness using various testing methods
    """
    print("="*80)
    print("SECTION 8 - FUNCTIONAL TESTING")
    print("CS301 2024-2025 Summer Project - Group 145")
    print("="*80)
    print("Testing implementation correctness using comprehensive testing methods")
    print("Following CS301 testing methodologies for algorithm validation")
    print()

    test_results = {
        'edge_cases': [],
        'boundary_tests': [],
        'consistency_tests': [],
        'validation_tests': [],
        'comparison_tests': []
    }

    total_tests = 0
    passed_tests = 0

    # Edge Case Testing
    print("1. EDGE CASE TESTING")
    print("-" * 30)

    edge_cases = [
        ([1], 1, "single_element_exact"),
        ([1], 2, "single_element_impossible"),
        ([5, 5, 5], 5, "duplicates_simple"),
        ([1, 2, 3], 0, "zero_target"),
        ([100], 50, "large_element_partial"),
        ([1, 1, 1, 1], 4, "all_same_exact"),
        ([10, 20, 30], 5, "all_too_large"),
        ([2, 4, 6, 8], 1, "all_even_odd_target"),
        ([1, 3, 5, 7], 8, "all_odd_even_target"),
        ([], 10, "empty_multiset"),
        ([50, 25, 75], 100, "exact_sum_two"),
        ([1, 2, 4, 8], 15, "powers_of_two")
    ]

    for multiset, target, test_name in edge_cases:
        print(f"Testing {test_name}...", end=" ")
        total_tests += 1

        try:
            if not multiset:  # Empty multiset case
                try:
                    solver = SubsetSumSolver(multiset, target)
                    test_passed = False  # Should raise an error
                except ValueError:
                    test_passed = True  # Correctly rejected empty multiset
            else:
                solver = SubsetSumSolver(multiset, target)

                # Test all algorithms
                algorithms = [
                    'brute_force_decision',
                    'brute_force_optimization',
                    'greedy_heuristic',
                    'improved_greedy_heuristic',
                    'dynamic_programming_approximation'
                ]

                results = {}
                all_valid = True

                for alg in algorithms:
                    try:
                        if 'decision' in alg:
                            exists, subset, time_taken = getattr(solver, alg)()
                            results[alg] = {
                                'exists': exists,
                                'subset': subset,
                                'time': time_taken,
                                'valid': solver.validate_solution(subset)
                            }
                            if not results[alg]['valid']:
                                all_valid = False
                        else:
                            subset, sum_result, time_taken = getattr(solver, alg)()
                            is_valid = solver.validate_solution(subset)
                            results[alg] = {
                                'subset': subset,
                                'sum': sum_result,
                                'time': time_taken,
                                'valid': is_valid
                            }
                            if not is_valid:
                                all_valid = False
                    except Exception as e:
                        results[alg] = {'error': str(e), 'valid': False}
                        all_valid = False

                test_passed = all_valid

            test_results['edge_cases'].append({
                'test_name': test_name,
                'multiset': multiset,
                'target': target,
                'passed': test_passed,
                'results': results if multiset else None
            })

            if test_passed:
                passed_tests += 1
                print("✅ PASSED")
            else:
                print("❌ FAILED")

        except Exception as e:
            test_results['edge_cases'].append({
                'test_name': test_name,
                'error': str(e),
                'passed': False
            })
            print(f"❌ ERROR: {e}")

    # Boundary Testing
    print(f"\n2. BOUNDARY TESTING")
    print("-" * 30)

    boundary_cases = [
        ([1, 2, 3, 4, 5], 15, "target_equals_sum"),
        ([1, 2, 3, 4, 5], 16, "target_exceeds_sum"),
        ([10, 10, 10], 30, "target_equals_sum_duplicates"),
        ([1, 2, 3, 4, 5], 1, "target_equals_min"),
        ([1, 2, 3, 4, 5], 5, "target_equals_max"),
        ([2, 4, 6, 8], 2, "target_equals_smallest"),
        ([2, 4, 6, 8], 8, "target_equals_largest"),
        ([1, 1, 1, 1, 1], 3, "many_duplicates")
    ]

    for multiset, target, test_name in boundary_cases:
        print(f"Testing {test_name}...", end=" ")
        total_tests += 1

        try:
            solver = SubsetSumSolver(multiset, target)

            # Test consistency between decision and optimization
            exists, decision_subset, _ = solver.brute_force_decision()
            opt_subset, opt_sum, _ = solver.brute_force_optimization()

            # Validation checks
            decision_valid = solver.validate_solution(decision_subset)
            opt_valid = solver.validate_solution(opt_subset)

            # Consistency check
            if exists and sum(decision_subset) == target:
                consistency_check = (opt_sum >= target or opt_sum == sum(decision_subset))
            else:
                consistency_check = (opt_sum < target)

            test_passed = decision_valid and opt_valid and consistency_check

            test_results['boundary_tests'].append({
                'test_name': test_name,
                'multiset': multiset,
                'target': target,
                'decision_exists': exists,
                'decision_subset': decision_subset,
                'opt_sum': opt_sum,
                'consistency_check': consistency_check,
                'passed': test_passed
            })

            if test_passed:
                passed_tests += 1
                print("✅ PASSED")
            else:
                print("❌ FAILED")

        except Exception as e:
            test_results['boundary_tests'].append({
                'test_name': test_name,
                'error': str(e),
                'passed': False
            })
            total_tests += 1
            print(f"❌ ERROR: {e}")

    # Consistency Testing
    print(f"\n3. CONSISTENCY TESTING")
    print("-" * 30)

    generator = SubsetSumInstanceGenerator(seed=789)

    for i in range(10):
        print(f"Consistency test {i+1}...", end=" ")
        total_tests += 1

        try:
            # Generate random instance
            multiset, target = generator.generate_uniform_random(
                8, min_val=1, max_val=15, target_ratio=0.6
            )

            solver = SubsetSumSolver(multiset, target)

            # Run same algorithm multiple times
            results_greedy = []
            results_improved = []

            for run in range(5):
                subset1, sum1, _ = solver.greedy_heuristic()
                subset2, sum2, _ = solver.improved_greedy_heuristic()

                results_greedy.append((subset1, sum1))
                results_improved.append((subset2, sum2))

            # Check deterministic behavior
            greedy_consistent = all(r[1] == results_greedy[0][1] for r in results_greedy)
            improved_consistent = all(r[1] == results_improved[0][1] for r in results_improved)

            test_passed = greedy_consistent and improved_consistent

            test_results['consistency_tests'].append({
                'test_id': i + 1,
                'multiset': multiset,
                'target': target,
                'greedy_consistent': greedy_consistent,
                'improved_consistent': improved_consistent,
                'passed': test_passed
            })

            if test_passed:
                passed_tests += 1
                print("✅ PASSED")
            else:
                print("❌ FAILED")

        except Exception as e:
            test_results['consistency_tests'].append({
                'test_id': i + 1,
                'error': str(e),
                'passed': False
            })
            print(f"❌ ERROR: {e}")

    # Input Validation Testing
    print(f"\n4. INPUT VALIDATION TESTING")
    print("-" * 30)

    invalid_inputs = [
        ([-1, 2, 3], 5, "negative_elements"),
        ([1, 2, 3], -5, "negative_target"),
        ([0, 1, 2], 3, "zero_element"),
        ([1.5, 2, 3], 4, "float_elements"),
        ([1, 2, 3], 2.5, "float_target"),
        (None, 5, "none_multiset")
    ]

    for multiset, target, test_name in invalid_inputs:
        print(f"Testing {test_name}...", end=" ")
        total_tests += 1

        try:
            solver = SubsetSumSolver(multiset, target)
            test_passed = False  # Should raise an error
            print("❌ FAILED (no error raised)")
        except (ValueError, TypeError) as e:
            test_passed = True  # Correctly rejected invalid input
            print("✅ PASSED (correctly rejected)")
        except Exception as e:
            test_passed = False
            print(f"❌ FAILED (wrong error type: {e})")

        test_results['validation_tests'].append({
            'test_name': test_name,
            'multiset': multiset,
            'target': target,
            'passed': test_passed
        })

        if test_passed:
            passed_tests += 1

    # Algorithm Comparison Testing
    print(f"\n5. ALGORITHM COMPARISON TESTING")
    print("-" * 30)

    for i in range(8):
        print(f"Comparison test {i+1}...", end=" ")
        total_tests += 1

        try:
            # Generate small instance for brute force comparison
            multiset, target = generator.generate_uniform_random(
                10, min_val=1, max_val=12, target_ratio=0.5
            )

            solver = SubsetSumSolver(multiset, target)

            # Get optimal solution
            opt_subset, opt_sum, _ = solver.brute_force_optimization()

            # Test heuristics don't exceed optimal
            greedy_subset, greedy_sum, _ = solver.greedy_heuristic()
            improved_subset, improved_sum, _ = solver.improved_greedy_heuristic()
            dp_subset, dp_sum, _ = solver.dynamic_programming_approximation()

            # Validation checks
            greedy_valid = greedy_sum <= opt_sum and solver.validate_solution(greedy_subset)
            improved_valid = improved_sum <= opt_sum and solver.validate_solution(improved_subset)
            dp_valid = dp_sum <= opt_sum and solver.validate_solution(dp_subset)

            test_passed = greedy_valid and improved_valid and dp_valid

            test_results['comparison_tests'].append({
                'test_id': i + 1,
                'multiset': multiset,
                'target': target,
                'optimal_sum': opt_sum,
                'greedy_sum': greedy_sum,
                'improved_sum': improved_sum,
                'dp_sum': dp_sum,
                'greedy_valid': greedy_valid,
                'improved_valid': improved_valid,
                'dp_valid': dp_valid,
                'passed': test_passed
            })

            if test_passed:
                passed_tests += 1
                print("✅ PASSED")
            else:
                print("❌ FAILED")

        except Exception as e:
            test_results['comparison_tests'].append({
                'test_id': i + 1,
                'error': str(e),
                'passed': False
            })
            print(f"❌ ERROR: {e}")

    # Generate final report
    print(f"\n{'='*80}")
    print("SECTION 8 FUNCTIONAL TESTING - FINAL SUMMARY")
    print('='*80)

    summary_stats = {}
    for category, tests in test_results.items():
        passed = sum(1 for test in tests if test.get('passed', False))
        total = len(tests)
        summary_stats[category] = {
            'total_tests': total,
            'passed_tests': passed,
            'success_rate': (passed / total * 100) if total > 0 else 0
        }

    print(f"\nTEST CATEGORY RESULTS:")
    for category, stats in summary_stats.items():
        print(f"  {category.replace('_', ' ').title()}: {stats['passed_tests']}/{stats['total_tests']} ({stats['success_rate']:.1f}%)")

    overall_success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"\nOVERALL RESULTS:")
    print(f"  Total tests executed: {total_tests}")
    print(f"  Tests passed: {passed_tests}")
    print(f"  Overall success rate: {overall_success_rate:.1f}%")

    if overall_success_rate >= 95:
        implementation_quality = "EXCELLENT"
    elif overall_success_rate >= 85:
        implementation_quality = "GOOD"
    elif overall_success_rate >= 70:
        implementation_quality = "ACCEPTABLE"
    else:
        implementation_quality = "NEEDS IMPROVEMENT"

    print(f"  Implementation quality: {implementation_quality}")

    # Save detailed report
    report = {
        'section': '8',
        'description': 'Functional Testing for Implementation Correctness',
        'overall': {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': overall_success_rate,
            'implementation_quality': implementation_quality
        },
        'category_summary': summary_stats,
        'detailed_results': test_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    os.makedirs('../results', exist_ok=True)
    with open('../results/section8_functional_testing.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nFILE GENERATED:")
    print(f"✓ Functional testing report: ../results/section8_functional_testing.json")

    print(f"\n🎯 SECTION 8 FUNCTIONAL TESTING COMPLETE!")

    return report

if __name__ == "__main__":
    run_section8_functional_testing()