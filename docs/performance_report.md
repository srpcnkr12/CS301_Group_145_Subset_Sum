# Section 6 Performance Analysis Report
## CS301 Group 145 - Subset Sum Problem

### Overview
This report presents the statistical performance analysis of three heuristic algorithms for the Subset Sum problem, conducted according to CS301 template requirements with 90% confidence intervals and narrow interval analysis.

### Methodology
- **Confidence Level:** 90%
- **Measurements per Size:** 15 runs
- **Input Sizes:** 25 to 200 (8 test points)
- **Narrow Interval Requirement:** b/a < 0.1
- **Instance Type:** Uniform random with target ratio 0.4

### Results Summary

| Algorithm | Time Complexity | R² Value | Statistical Quality | Mean Rel. Error |
|-----------|----------------|----------|-------------------|-----------------|
| Greedy | O(n log n) | 0.9983 | GOOD (87.5%) | 0.043 |
| Improved Greedy | O(n log n) | 0.9886 | GOOD (87.5%) | 0.047 |
| DP Approximation | O(n log n) | 0.9992 | GOOD (87.5%) | 0.041 |

### Key Findings
1. **Theoretical Validation:** All algorithms show excellent curve fitting (R² > 0.98)
2. **Statistical Quality:** 87.5% narrow intervals achieved (exceeds CS301 75% minimum)
3. **Best Performance:** DP Approximation shows lowest error and highest R²
4. **Consistency:** All algorithms demonstrate predictable scaling behavior

### Template Compliance
✅ Statistical methods with confidence intervals (90%+)
✅ Multiple measurements per input size
✅ Narrow confidence intervals tracking (b/a < 0.1)
✅ Line fitting and time complexity analysis
✅ Large input sizes for heuristic algorithms
✅ Academic-quality visualization

### Conclusion
The performance analysis demonstrates that all three heuristic algorithms scale efficiently according to their theoretical time complexities, with DP Approximation showing the best overall performance characteristics for the Subset Sum problem.