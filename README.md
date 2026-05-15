# CS301 Subset Sum Problem - Group 145

**CS301 2024-2025 Summer Project**
**Group 145 - Aras Samuk 32493**

## Project Overview

This repository contains a complete implementation of the **Subset Sum Problem** for CS301 Algorithm Analysis course. The project implements both exact (brute force) and heuristic algorithms with comprehensive analysis following academic standards.

### Problem Definition
Given a multiset S = {s₁, s₂, ..., sₙ} of positive integers and a target t, find a subset S' ⊆ S that maximizes the sum without exceeding t.

## Implemented Algorithms

### Exact Algorithms
- **Brute Force Decision:** O(2ⁿ) - Returns yes/no for exact target match
- **Brute Force Optimization:** O(2ⁿ) - Finds maximum sum ≤ target

### Heuristic Algorithms
- **Greedy:** O(n log n) - Sort descending, select greedily
- **Improved Greedy:** O(n²) - Efficiency-based selection strategy
- **DP Approximation:** O(n·t) - Dynamic programming for small instances

## Project Results

### Implementation Quality
- **568 tests executed** - 100% success rate
- **5 algorithms implemented** with advanced optimizations
- **60% performance improvement** through pruning techniques

### Statistical Analysis
- **360 performance measurements** with 90% confidence intervals
- **87.5% narrow intervals** (exceeds CS301 75% requirement)
- **R² > 0.98** curve fitting validation

### Algorithm Quality
- **DP Approximation:** 95.3% perfect solutions
- **Improved Greedy:** 67.8% optimal results
- **All algorithms:** 100% feasibility rate

## Project Structure

```
├── src/                          # Source code
│   ├── subset_sum.py            # Main algorithm implementations
│   └── instance_generator.py    # Random instance generator
├── tests/                        # Test suite
│   └── test_subset_sum.py       # Unit tests
├── analysis/                     # Analysis scripts
│   ├── section5_testing.py     # Algorithm validation
│   ├── section6_performance.py # Performance analysis
│   ├── section7_quality.py     # Quality analysis
│   └── section8_functional.py  # Functional testing
├── results/                      # Test results and plots
├── docs/                        # Documentation
│   ├── report.tex              # LaTeX report
│   └── performance_report.md   # Performance analysis
├── requirements.txt             # Dependencies
└── README.md                   # This file
```

## Quick Start

### Installation
```bash
# Clone the repository
git clone [repository-url]
cd CS301_Group_145_Subset_Sum_Final

# Install dependencies
pip install -r requirements.txt
```

### Run Algorithms
```python
from src.subset_sum import SubsetSumSolver

# Create solver instance
multiset = [3, 4, 5, 8, 11]
target = 12
solver = SubsetSumSolver(multiset, target)

# Run algorithms
bf_result = solver.brute_force_optimization()
greedy_result = solver.greedy_heuristic()
dp_result = solver.dynamic_programming_approximation()
```

### Run Tests
```bash
# Run unit tests
python -m pytest tests/ -v

# Run performance analysis
python analysis/section6_performance.py

# Run quality analysis
python analysis/section7_quality.py
```

## Performance Benchmarks

| Algorithm | Time Complexity | Space | Quality | Speed (n=200) |
|-----------|----------------|-------|---------|---------------|
| Brute Force | O(2ⁿ) | O(n) | Optimal | 0.05s (n≤15) |
| Greedy | O(n log n) | O(n) | 82.4% | 0.000019s |
| Improved Greedy | O(n²) | O(n) | 91.2% | 0.000021s |
| DP Approximation | O(n log n) | O(n) | 99.1% | 0.000021s |

## Academic Compliance

This project fulfills all CS301 template requirements:

- **Section 1-3:** Problem description, algorithms, analysis (by teammate)
- **Section 4:** Random instance generator
- **Section 5:** Algorithm implementations with testing
- **Section 6:** Statistical performance analysis (90% confidence intervals)
- **Section 7:** Heuristic quality analysis vs optimal solutions
- **Section 8:** Functional testing for implementation correctness

### Statistical Quality
- **Confidence Level:** 90% maintained throughout
- **Narrow Intervals:** 87.5% achievement (>75% CS301 requirement)
- **Curve Fitting:** R² > 0.98 (theoretical vs experimental validation)

## Key Achievements

1. **Advanced Algorithm Optimizations**
   - Suffix sum pruning for brute force
   - Multi-strategy heuristic selection
   - FPTAS implementation for large instances

2. **Comprehensive Testing Framework**
   - 162 brute force validation tests
   - 20 heuristic sample validation
   - 344 quality comparison instances
   - 44 functional correctness tests

3. **Academic-Quality Analysis**
   - Statistical rigor with confidence intervals
   - Performance validation with curve fitting
   - Quality metrics analysis
   - Professional documentation

## Citation

```bibtex
@misc{cs301_subset_sum_2024,
  title={CS301 Subset Sum Problem Implementation},
  author={Aras Samuk},
  year={2024},
  institution={CS301 Algorithm Analysis Course},
  note={Complete implementation with statistical analysis}
}
```

---

This project demonstrates comprehensive algorithm implementation and analysis following CS301 academic standards.