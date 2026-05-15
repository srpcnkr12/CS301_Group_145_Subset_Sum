# Results Directory

This directory contains all generated results from CS301 Subset Sum project analysis.

## Files Generated

### Section 5: Algorithm Implementation Testing
- **`section5_1_brute_force_report.json`** - Brute force algorithm testing results (162 test instances)
- **`section5_2_heuristic_report.json`** - Heuristic algorithm testing results (20 validation samples)

### Section 6: Performance Analysis
- **`section6_performance_results.csv`** - Statistical performance measurements (360 data points)
- **`section6_performance_report.json`** - Performance analysis summary with curve fitting
- **`performance_plots.png`** - 4-plot performance visualization (602KB)

### Section 7: Quality Analysis
- **`section7_quality_analysis.json`** - Heuristic vs optimal quality comparison (344 instances)

### Section 8: Functional Testing
- **`section8_functional_testing.json`** - Implementation correctness validation (44 tests)

## Statistics Summary

| Metric | Value |
|--------|-------|
| Total tests executed | 568 |
| Success rate | 100% |
| Statistical quality | GOOD (87.5% narrow intervals) |
| Implementation reliability | 100% |

## Usage

These files are automatically generated when running:
```bash
python run_analysis.py
```

Or individually:
```bash
cd analysis/
python section6_performance.py  # Generates section 6 files
python section7_quality.py      # Generates section 7 files
```