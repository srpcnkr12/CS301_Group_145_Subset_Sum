"""
Section 6 - Performance Testing
CS301 2024-2025 Summer Project - Group 145

This module implements statistical performance analysis with confidence intervals
as required by CS301 template section 6.
"""

import sys
import os
sys.path.append('../src')

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import pandas as pd
import time
import json
from typing import Dict, List, Tuple

from subset_sum import SubsetSumSolver
from instance_generator import SubsetSumInstanceGenerator

class PerformanceAnalyzer:
    """Statistical performance analyzer with CS301 template compliance."""

    def __init__(self, confidence_level: float = 0.90):
        self.confidence_level = confidence_level
        self.generator = SubsetSumInstanceGenerator(seed=42)

    def measure_algorithm_performance(self, algorithm_name: str, sizes: List[int],
                                   runs_per_size: int = 15) -> List[Dict]:
        """
        Measure algorithm performance with statistical rigor.

        Args:
            algorithm_name: Name of algorithm to test
            sizes: List of input sizes to test
            runs_per_size: Number of measurements per size

        Returns:
            List of performance measurement results
        """
        print(f"\nTesting {algorithm_name}...")
        results = []
        narrow_intervals = 0

        for size in sizes:
            print(f"Testing size {size}...", end=" ")
            times = []

            # Multiple measurements per size
            for run in range(runs_per_size):
                # Generate test instance
                multiset, target = self.generator.generate_uniform_random(
                    size, min_val=1, max_val=50, target_ratio=0.4
                )

                solver = SubsetSumSolver(multiset, target)

                # Measure execution time
                start_time = time.perf_counter()

                if algorithm_name == 'GREEDY':
                    result = solver.greedy_heuristic()
                elif algorithm_name == 'IMPROVED_GREEDY':
                    result = solver.improved_greedy_heuristic()
                elif algorithm_name == 'DP_APPROXIMATION':
                    result = solver.dynamic_programming_approximation()

                end_time = time.perf_counter()
                times.append(end_time - start_time)

            # Statistical analysis
            mean_time = np.mean(times)
            std_time = np.std(times, ddof=1)
            n = len(times)

            # Calculate confidence interval
            se = std_time / np.sqrt(n)
            t_value = stats.t.ppf((1 + self.confidence_level) / 2, df=n-1)
            margin_error = t_value * se

            # Check narrow interval requirement (b/a < 0.1)
            relative_error = margin_error / mean_time if mean_time > 0 else float('inf')
            is_narrow = bool(relative_error < 0.1)

            if is_narrow:
                narrow_intervals += 1

            result_data = {
                'algorithm': algorithm_name,
                'size': size,
                'mean_time': mean_time,
                'std_time': std_time,
                'margin_error': margin_error,
                'relative_error': relative_error,
                'is_narrow': is_narrow,
                'runs': runs_per_size,
                'confidence_level': self.confidence_level
            }

            results.append(result_data)
            print(f"Mean: {mean_time:.6f}s, Relative error: {relative_error:.3f}")

        total_intervals = len(sizes)
        print(f"Narrow intervals: {narrow_intervals}/{total_intervals} ({narrow_intervals/total_intervals*100:.1f}%)")

        return results

    def analyze_time_complexity(self, results: List[Dict]) -> Dict:
        """Analyze time complexity with curve fitting."""
        sizes = np.array([r['size'] for r in results])
        times = np.array([r['mean_time'] for r in results])

        # Define fitting functions
        def linear(x, a, b):
            return a * x + b

        def quadratic(x, a, b, c):
            return a * x**2 + b * x + c

        def nlogn(x, a, b):
            return a * x * np.log(x) + b

        fits = {}

        # Try different complexity fits
        try:
            # Linear O(n)
            popt, _ = curve_fit(linear, sizes, times)
            predicted = linear(sizes, *popt)
            r2 = 1 - np.sum((times - predicted)**2) / np.sum((times - np.mean(times))**2)
            fits['Linear O(n)'] = {'params': popt, 'r2': r2, 'func': linear}
        except:
            pass

        try:
            # Quadratic O(n²)
            popt, _ = curve_fit(quadratic, sizes, times)
            predicted = quadratic(sizes, *popt)
            r2 = 1 - np.sum((times - predicted)**2) / np.sum((times - np.mean(times))**2)
            fits['Quadratic O(n²)'] = {'params': popt, 'r2': r2, 'func': quadratic}
        except:
            pass

        try:
            # N log N O(n log n)
            popt, _ = curve_fit(nlogn, sizes, times)
            predicted = nlogn(sizes, *popt)
            r2 = 1 - np.sum((times - predicted)**2) / np.sum((times - np.mean(times))**2)
            fits['N log N O(n log n)'] = {'params': popt, 'r2': r2, 'func': nlogn}
        except:
            pass

        # Find best fit
        if fits:
            best_fit_name = max(fits.keys(), key=lambda k: fits[k]['r2'])
            best_fit = fits[best_fit_name]
            return {
                'best_fit': best_fit_name,
                'r2': best_fit['r2'],
                'params': best_fit['params'].tolist(),
                'all_fits': {name: {'r2': fit['r2'], 'params': fit['params'].tolist()}
                           for name, fit in fits.items()}
            }
        else:
            return {'best_fit': 'None', 'r2': 0.0, 'params': [], 'all_fits': {}}

    def generate_performance_plots(self, all_results: Dict[str, List[Dict]],
                                 output_path: str = '../results/performance_plots.png'):
        """Generate comprehensive performance visualization."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

        algorithms = list(all_results.keys())

        # Plot 1: Performance comparison (linear scale)
        for i, (algorithm, results) in enumerate(all_results.items()):
            sizes = [r['size'] for r in results]
            times = [r['mean_time'] for r in results]
            errors = [r['margin_error'] for r in results]

            ax1.errorbar(sizes, times, yerr=errors, label=algorithm,
                        color=colors[i], marker='o', linewidth=2)

        ax1.set_xlabel('Problem Size (n)', fontweight='bold')
        ax1.set_ylabel('Execution Time (seconds)', fontweight='bold')
        ax1.set_title('Performance Comparison - Linear Scale', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Performance comparison (log scale)
        for i, (algorithm, results) in enumerate(all_results.items()):
            sizes = [r['size'] for r in results]
            times = [r['mean_time'] for r in results]

            ax2.loglog(sizes, times, label=algorithm, color=colors[i],
                      marker='o', linewidth=2)

        ax2.set_xlabel('Problem Size (n)', fontweight='bold')
        ax2.set_ylabel('Execution Time (seconds)', fontweight='bold')
        ax2.set_title('Performance Comparison - Log-Log Scale', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        # Plot 3: Statistical quality
        algorithm_names = []
        narrow_percentages = []

        for algorithm, results in all_results.items():
            narrow_count = sum(1 for r in results if r['is_narrow'])
            total_count = len(results)
            narrow_percentage = narrow_count / total_count * 100

            algorithm_names.append(algorithm)
            narrow_percentages.append(narrow_percentage)

        bars = ax3.bar(algorithm_names, narrow_percentages, color=colors[:len(algorithm_names)], alpha=0.7)
        ax3.axhline(y=90, color='red', linestyle='--', label='90% Target')
        ax3.set_xlabel('Algorithm', fontweight='bold')
        ax3.set_ylabel('Narrow Intervals (%)', fontweight='bold')
        ax3.set_title('Statistical Quality (b/a < 0.1)', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')

        # Add percentage labels
        for bar, percentage in zip(bars, narrow_percentages):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{percentage:.1f}%', ha='center', va='bottom', fontweight='bold')

        # Plot 4: Relative error distribution
        for i, (algorithm, results) in enumerate(all_results.items()):
            rel_errors = [r['relative_error'] for r in results]
            sizes = [r['size'] for r in results]

            ax4.scatter(sizes, rel_errors, label=algorithm, color=colors[i], alpha=0.7, s=50)

        ax4.axhline(y=0.1, color='red', linestyle='--', label='Target (0.1)')
        ax4.set_xlabel('Problem Size (n)', fontweight='bold')
        ax4.set_ylabel('Relative Error (b/a)', fontweight='bold')
        ax4.set_title('Confidence Interval Quality', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_yscale('log')

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Performance plots saved to: {output_path}")

def run_section6_performance_testing():
    """Run complete Section 6 performance testing."""
    print("="*80)
    print("SECTION 6 - PERFORMANCE TESTING")
    print("CS301 2024-2025 Summer Project - Group 145")
    print("="*80)
    print("Template Requirements Implementation:")
    print("✓ Statistical methods with 90% confidence intervals")
    print("✓ Multiple measurements per input size")
    print("✓ Narrow intervals requirement (b/a < 0.1)")
    print("✓ Line fitting for time complexity analysis")
    print("✓ Large input sizes for scalability testing")
    print("✓ Academic-quality visualization")
    print()

    analyzer = PerformanceAnalyzer(confidence_level=0.90)

    # Test parameters
    sizes = list(range(25, 201, 25))  # 25, 50, 75, 100, 125, 150, 175, 200
    algorithms = ['GREEDY', 'IMPROVED_GREEDY', 'DP_APPROXIMATION']
    runs_per_size = 15

    all_results = {}
    complexity_analysis = {}

    # Test each algorithm
    for algorithm in algorithms:
        print(f"\n{'='*60}")
        print(f"TESTING {algorithm} ALGORITHM")
        print('='*60)

        # Measure performance
        results = analyzer.measure_algorithm_performance(algorithm, sizes, runs_per_size)
        all_results[algorithm] = results

        # Analyze time complexity
        complexity = analyzer.analyze_time_complexity(results)
        complexity_analysis[algorithm] = complexity

        print(f"\nCOMPLEXITY ANALYSIS FOR {algorithm}:")
        print("-" * 40)
        print(f"✓ Best fitting curve: {complexity['best_fit']}")
        print(f"✓ R² = {complexity['r2']:.4f}")

        # Print equation based on best fit
        if complexity['best_fit'] != 'None' and complexity['params']:
            params = complexity['params']
            if 'Quadratic' in complexity['best_fit'] and len(params) >= 3:
                a, b, c = params[:3]
                print(f"✓ Equation: T(n) = {a:.2e}*n² + {b:.2e}*n + {c:.2e}")
            elif 'Linear' in complexity['best_fit'] and len(params) >= 2:
                a, b = params[:2]
                print(f"✓ Equation: T(n) = {a:.2e}*n + {b:.2e}")
            elif 'N log N' in complexity['best_fit'] and len(params) >= 2:
                a, b = params[:2]
                print(f"✓ Equation: T(n) = {a:.2e}*n*log(n) + {b:.2e}")

        # Statistical quality assessment
        narrow_count = sum(1 for r in results if r['is_narrow'])
        total_count = len(results)
        mean_rel_error = np.mean([r['relative_error'] for r in results])

        print(f"\nSTATISTICAL QUALITY:")
        print("-" * 30)
        print(f"✓ Total measurements: {sum(r['runs'] for r in results)}")
        print(f"✓ Narrow intervals: {narrow_count}/{total_count} ({narrow_count/total_count*100:.1f}%)")
        print(f"✓ Mean relative error: {mean_rel_error:.3f}")

        if narrow_count/total_count >= 0.9:
            quality = "EXCELLENT"
        elif narrow_count/total_count >= 0.75:
            quality = "GOOD"
        else:
            quality = "NEEDS IMPROVEMENT"
        print(f"✓ Statistical quality: {quality}")

    # Generate visualization
    print(f"\n{'='*80}")
    print("GENERATING PERFORMANCE VISUALIZATION")
    print('='*80)

    os.makedirs('../results', exist_ok=True)
    analyzer.generate_performance_plots(all_results)

    # Save detailed CSV results
    csv_data = []
    for algorithm, results in all_results.items():
        for result in results:
            csv_data.append({
                'Algorithm': result['algorithm'],
                'Size': result['size'],
                'Mean_Time': result['mean_time'],
                'Std_Time': result['std_time'],
                'Margin_Error': result['margin_error'],
                'Relative_Error': result['relative_error'],
                'Is_Narrow_Interval': result['is_narrow'],
                'Runs_Per_Size': result['runs'],
                'Confidence_Level': result['confidence_level']
            })

    df = pd.DataFrame(csv_data)
    df.to_csv('../results/section6_performance_results.csv', index=False)

    # Generate comprehensive report
    overall_narrow = sum(len([r for r in results if r['is_narrow']]) for results in all_results.values())
    overall_total = sum(len(results) for results in all_results.values())

    report = {
        'section': '6',
        'description': 'Performance Testing with Statistical Analysis',
        'parameters': {
            'confidence_level': 0.90,
            'runs_per_size': runs_per_size,
            'tested_sizes': sizes,
            'algorithms': algorithms
        },
        'results': all_results,
        'complexity_analysis': complexity_analysis,
        'summary': {
            'total_measurements': sum(len(results) * runs_per_size for results in all_results.values()),
            'narrow_intervals_achieved': f"{overall_narrow}/{overall_total} ({overall_narrow/overall_total*100:.1f}%)",
            'project_statistical_quality': 'EXCELLENT' if overall_narrow/overall_total >= 0.9
                                         else 'GOOD' if overall_narrow/overall_total >= 0.75
                                         else 'NEEDS IMPROVEMENT'
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    with open('../results/section6_performance_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    # Final summary
    print(f"\n{'='*80}")
    print("SECTION 6 PERFORMANCE TESTING - FINAL SUMMARY")
    print('='*80)

    print(f"\nOVERALL PROJECT STATISTICS:")
    print(f"  Total narrow intervals: {overall_narrow}/{overall_total} ({overall_narrow/overall_total*100:.1f}%)")
    print(f"  Project statistical quality: {report['summary']['project_statistical_quality']}")

    print(f"\nFILES GENERATED:")
    print(f"✓ Performance plots: ../results/performance_plots.png")
    print(f"✓ Detailed results: ../results/section6_performance_results.csv")
    print(f"✓ Complete report: ../results/section6_performance_report.json")

    print(f"\n🎯 SECTION 6 PERFORMANCE TESTING COMPLETE!")

    return report

if __name__ == "__main__":
    run_section6_performance_testing()