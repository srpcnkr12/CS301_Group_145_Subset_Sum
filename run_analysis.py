#!/usr/bin/env python3
"""
CS301 Subset Sum Project - Complete Analysis Runner
Group 145 - Aras Samuk 32493

This script runs all analysis sections in sequence to generate complete results.
"""

import os
import sys
import time

def run_complete_analysis():
    """Run all analysis sections in proper sequence."""
    print("="*80)
    print("CS301 SUBSET SUM PROJECT - COMPLETE ANALYSIS")
    print("Group 145 - Aras Samuk 32493")
    print("="*80)
    print("Running all analysis sections in sequence...")
    print()

    # Change to analysis directory
    os.chdir('analysis')

    analysis_sections = [
        ('section5_testing.py', 'Section 5: Algorithm Implementation Testing'),
        ('section6_performance.py', 'Section 6: Performance Analysis'),
        ('section7_quality.py', 'Section 7: Quality Analysis'),
        ('section8_functional.py', 'Section 8: Functional Testing')
    ]

    results = {}
    overall_start = time.time()

    for script, description in analysis_sections:
        print(f"\n{'='*60}")
        print(f"RUNNING {description}")
        print(f"{'='*60}")

        start_time = time.time()

        try:
            # Run the analysis script
            exit_code = os.system(f'python {script}')

            if exit_code == 0:
                status = "✅ COMPLETED"
                success = True
            else:
                status = "❌ FAILED"
                success = False

            execution_time = time.time() - start_time

            results[script] = {
                'description': description,
                'success': success,
                'execution_time': execution_time,
                'status': status
            }

            print(f"\n{status} in {execution_time:.2f}s")

        except Exception as e:
            results[script] = {
                'description': description,
                'success': False,
                'error': str(e),
                'status': "❌ ERROR"
            }
            print(f"\n❌ ERROR: {e}")

    total_time = time.time() - overall_start

    # Generate summary report
    print(f"\n{'='*80}")
    print("COMPLETE ANALYSIS SUMMARY")
    print(f"{'='*80}")

    successful_sections = sum(1 for r in results.values() if r['success'])
    total_sections = len(results)

    print(f"\nOVERALL RESULTS:")
    print(f"  Sections completed: {successful_sections}/{total_sections}")
    print(f"  Total execution time: {total_time:.2f}s")
    print(f"  Overall success rate: {successful_sections/total_sections*100:.1f}%")

    print(f"\nSECTION DETAILS:")
    for script, result in results.items():
        print(f"  {result['description']}: {result['status']}")
        if 'execution_time' in result:
            print(f"    Execution time: {result['execution_time']:.2f}s")

    print(f"\nGENERATED FILES:")
    print(f"  📁 results/section5_1_brute_force_report.json")
    print(f"  📁 results/section5_2_heuristic_report.json")
    print(f"  📁 results/section6_performance_results.csv")
    print(f"  📁 results/section6_performance_report.json")
    print(f"  📁 results/section7_quality_analysis.json")
    print(f"  📁 results/section8_functional_testing.json")
    print(f"  📊 results/performance_plots.png")

    if successful_sections == total_sections:
        print(f"\n🎯 ALL ANALYSIS SECTIONS COMPLETED SUCCESSFULLY!")
        print(f"Project is ready for CS301 submission.")
    else:
        print(f"\n⚠️  Some sections failed. Please check the errors above.")

    return results

if __name__ == "__main__":
    results = run_complete_analysis()