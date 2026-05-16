"""
Section 7 - Quality Analysis
CS301 2024-2025 Summer Project - Group 145

This module implements quality analysis comparing heuristic algorithms
against optimal brute force solutions as required by CS301 template section 7.
"""

import sys
import os
sys.path.append('../src')

import json
import time
import numpy as np
from typing import Dict, List, Any
from subset_sum import SubsetSumSolver
from instance_generator import SubsetSumInstanceGenerator

def run_section7_quality_analysis():
    """
    Section 7: Quality Analysis of Heuristic Algorithms
    Compares heuristic solutions against optimal brute force solutions
    """
    print("="*80)
    print("SECTION 7 - QUALITY ANALYSIS")
    print("CS301 2024-2025 Summer Project - Group 145")
    print("="*80)
    print("Comparing heuristic algorithms against optimal brute force solutions")
    print("Analyzing solution quality across various problem sizes and types")
    print()

    generator = SubsetSumInstanceGenerator(seed=456)

    # Algorithms to compare
    heuristic_algorithms = ['GREEDY', 'IMPROVED_GREEDY', 'DP_APPROXIMATION']

    # Test configuration
    test_instances = []

    # Generate diverse test instances
    print("Generating test instances...")

    # Small instances for brute force comparison (size 8-14)
    for size in range(8, 15):
        for instance_type in ['uniform', 'clustered', 'high_density', 'low_density']:
            for trial in range(6):  # 6 instances per size per type
                if instance_type == 'uniform':
                    multiset, target = generator.generate_uniform_random(
                        size, min_val=1, max_val=20, target_ratio=0.4 + trial * 0.1
                    )
                elif instance_type == 'clustered':
                    multiset, target = generator.generate_correlated_instance(
                        size, correlation_strength=0.7
                    )
                elif instance_type == 'high_density':
                    multiset, target = generator.generate_hard_instance(
                        size, "dense"
                    )
                else:  # low_density
                    multiset, target = generator.generate_hard_instance(
                        size, "sparse"
                    )

                test_instances.append({
                    'id': len(test_instances) + 1,
                    'size': size,
                    'type': instance_type,
                    'trial': trial + 1,
                    'multiset': multiset,
                    'target': target
                })

    print(f"Generated {len(test_instances)} test instances")

    # Run quality analysis
    quality_results = []
    total_instances = len(test_instances)

    print(f"\nRunning quality analysis on {total_instances} instances...")

    for i, instance in enumerate(test_instances):
        if (i + 1) % 50 == 0:
            print(f"Progress: {i + 1}/{total_instances} instances processed")

        solver = SubsetSumSolver(instance['multiset'], instance['target'])

        # Get optimal solution using brute force
        try:
            optimal_solution, optimal_sum, bf_time = solver.brute_force_optimization()

            instance_result = {
                'instance_info': instance,
                'optimal_sum': optimal_sum,
                'optimal_solution': optimal_solution,
                'brute_force_time': bf_time,
                'heuristic_results': {}
            }

            # Test each heuristic algorithm
            for algorithm in heuristic_algorithms:
                try:
                    if algorithm == 'GREEDY':
                        solution, sum_result, exec_time = solver.greedy_heuristic()
                    elif algorithm == 'IMPROVED_GREEDY':
                        solution, sum_result, exec_time = solver.improved_greedy_heuristic()
                    elif algorithm == 'DP_APPROXIMATION':
                        solution, sum_result, exec_time = solver.dynamic_programming_approximation()

                    # Calculate quality metrics
                    target_ratio = sum_result / instance['target'] if instance['target'] > 0 else 0
                    optimality_ratio = sum_result / optimal_sum if optimal_sum > 0 else 0
                    optimality_gap = (optimal_sum - sum_result) / optimal_sum if optimal_sum > 0 else 0
                    is_optimal = (sum_result == optimal_sum)

                    instance_result['heuristic_results'][algorithm] = {
                        'solution': solution,
                        'sum': sum_result,
                        'execution_time': exec_time,
                        'target_ratio': target_ratio,
                        'optimality_ratio': optimality_ratio,
                        'optimality_gap': optimality_gap,
                        'is_optimal': is_optimal,
                        'valid': solver.validate_solution(solution)
                    }

                except Exception as e:
                    instance_result['heuristic_results'][algorithm] = {
                        'error': str(e),
                        'valid': False
                    }

            quality_results.append(instance_result)

        except Exception as e:
            print(f"Error processing instance {instance['id']}: {e}")
            continue

    print(f"Completed analysis on {len(quality_results)} instances")

    # Generate quality metrics summary
    print(f"\n{'='*60}")
    print("QUALITY METRICS ANALYSIS")
    print('='*60)

    algorithm_metrics = {}

    for algorithm in heuristic_algorithms:
        valid_results = [
            r['heuristic_results'][algorithm] for r in quality_results
            if algorithm in r['heuristic_results'] and
               r['heuristic_results'][algorithm].get('valid', False)
        ]

        if valid_results:
            target_ratios = [r['target_ratio'] for r in valid_results]
            optimality_ratios = [r['optimality_ratio'] for r in valid_results]
            optimality_gaps = [r['optimality_gap'] for r in valid_results]
            perfect_solutions = sum(1 for r in valid_results if r['is_optimal'])
            execution_times = [r['execution_time'] for r in valid_results]

            algorithm_metrics[algorithm] = {
                'total_instances': len(valid_results),
                'avg_target_ratio': np.mean(target_ratios),
                'avg_optimality_ratio': np.mean(optimality_ratios),
                'avg_optimality_gap': np.mean(optimality_gaps),
                'perfect_solution_rate': perfect_solutions / len(valid_results),
                'avg_execution_time': np.mean(execution_times),
                'target_ratio_std': np.std(target_ratios),
                'optimality_ratio_std': np.std(optimality_ratios)
            }
        else:
            algorithm_metrics[algorithm] = {
                'total_instances': 0,
                'error': 'No valid results'
            }

    # Print detailed analysis
    for algorithm, metrics in algorithm_metrics.items():
        if 'error' not in metrics:
            print(f"\n{algorithm} QUALITY ANALYSIS:")
            print("-" * 40)
            print(f"✓ Total instances analyzed: {metrics['total_instances']}")
            print(f"✓ Average target achievement: {metrics['avg_target_ratio']*100:.1f}%")
            print(f"✓ Average optimality ratio: {metrics['avg_optimality_ratio']*100:.1f}%")
            print(f"✓ Average optimality gap: {metrics['avg_optimality_gap']*100:.1f}%")
            print(f"✓ Perfect solution rate: {metrics['perfect_solution_rate']*100:.1f}%")
            print(f"✓ Average execution time: {metrics['avg_execution_time']:.6f}s")

            # Quality assessment
            if metrics['perfect_solution_rate'] >= 0.9:
                quality_level = "EXCELLENT"
            elif metrics['perfect_solution_rate'] >= 0.7:
                quality_level = "GOOD"
            elif metrics['perfect_solution_rate'] >= 0.5:
                quality_level = "FAIR"
            else:
                quality_level = "POOR"
            print(f"✓ Quality level: {quality_level}")
        else:
            print(f"\n{algorithm}: {metrics['error']}")

    # Instance type analysis
    print(f"\n{'='*60}")
    print("QUALITY BY INSTANCE TYPE")
    print('='*60)

    instance_types = ['uniform', 'clustered', 'high_density', 'low_density']
    type_analysis = {}

    for inst_type in instance_types:
        type_results = [r for r in quality_results if r['instance_info']['type'] == inst_type]
        type_analysis[inst_type] = {
            'total_instances': len(type_results),
            'algorithms': {}
        }

        for algorithm in heuristic_algorithms:
            valid_type_results = [
                r['heuristic_results'][algorithm] for r in type_results
                if algorithm in r['heuristic_results'] and
                   r['heuristic_results'][algorithm].get('valid', False)
            ]

            if valid_type_results:
                perfect_rate = sum(1 for r in valid_type_results if r['is_optimal']) / len(valid_type_results)
                avg_optimality = np.mean([r['optimality_ratio'] for r in valid_type_results])

                type_analysis[inst_type]['algorithms'][algorithm] = {
                    'perfect_rate': perfect_rate,
                    'avg_optimality': avg_optimality
                }

        print(f"\n{inst_type.upper()} instances ({type_analysis[inst_type]['total_instances']} total):")
        for algorithm, stats in type_analysis[inst_type]['algorithms'].items():
            print(f"  {algorithm}: {stats['perfect_rate']*100:.1f}% perfect, {stats['avg_optimality']*100:.1f}% avg optimality")

    # Generate final report
    best_algorithm = max(algorithm_metrics.keys(),
                        key=lambda k: algorithm_metrics[k].get('perfect_solution_rate', 0)
                        if 'error' not in algorithm_metrics[k] else 0)

    summary = {
        'total_instances_analyzed': len(quality_results),
        'algorithms_tested': heuristic_algorithms,
        'instance_types_tested': instance_types,
        'best_algorithm': best_algorithm,
        'best_algorithm_perfect_rate': algorithm_metrics[best_algorithm].get('perfect_solution_rate', 0) * 100
    }

    report = {
        'section': '7',
        'description': 'Quality Analysis of Heuristic vs Optimal Solutions',
        'summary': summary,
        'quality_metrics': algorithm_metrics,
        'instance_type_analysis': type_analysis,
        'detailed_results': quality_results[:100],  # Store first 100 for space
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Save results
    os.makedirs('../results', exist_ok=True)
    with open('../results/section7_quality_analysis.json', 'w') as f:
        json.dump(report, f, indent=2)

    # Final summary
    print(f"\n{'='*80}")
    print("SECTION 7 QUALITY ANALYSIS - FINAL SUMMARY")
    print('='*80)

    print(f"\nKEY FINDINGS:")
    print(f"✓ Total instances analyzed: {summary['total_instances_analyzed']}")
    print(f"✓ Best performing algorithm: {best_algorithm}")
    print(f"✓ Best algorithm perfect solution rate: {summary['best_algorithm_perfect_rate']:.1f}%")

    print(f"\nALGORITHM RANKING (by perfect solution rate):")
    sorted_algorithms = sorted(
        [(alg, metrics.get('perfect_solution_rate', 0) * 100)
         for alg, metrics in algorithm_metrics.items() if 'error' not in metrics],
        key=lambda x: x[1], reverse=True
    )

    for i, (alg, rate) in enumerate(sorted_algorithms, 1):
        print(f"  {i}. {alg}: {rate:.1f}% perfect solutions")

    print(f"\nFILE GENERATED:")
    print(f"✓ Quality analysis report: ../results/section7_quality_analysis.json")

    print(f"\n🎯 SECTION 7 QUALITY ANALYSIS COMPLETE!")

    return report

if __name__ == "__main__":
    run_section7_quality_analysis()