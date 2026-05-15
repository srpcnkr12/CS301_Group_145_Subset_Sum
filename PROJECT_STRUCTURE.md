# CS301 Group 145 Subset Sum Project Structure

```
CS301_Group_145_Subset_Sum_Final/
├── README.md                           # Project overview and documentation
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore rules
├── run_analysis.py                    # Complete analysis runner script
├── PROJECT_STRUCTURE.md               # This file
│
├── src/                               # Source code
│   ├── subset_sum.py                  # Main algorithm implementations (563 lines)
│   └── instance_generator.py          # Random instance generator
│
├── tests/                             # Test suite
│   └── test_subset_sum.py             # Unit tests for algorithms
│
├── analysis/                          # Analysis scripts (CS301 sections)
│   ├── section5_testing.py           # Section 5: Algorithm testing
│   ├── section6_performance.py       # Section 6: Performance analysis
│   ├── section7_quality.py           # Section 7: Quality analysis
│   └── section8_functional.py        # Section 8: Functional testing
│
├── docs/                              # Documentation
│   ├── report.tex                     # Complete LaTeX report
│   └── performance_report.md          # Performance analysis summary
│
└── results/                           # Generated results (after running analysis)
    ├── section5_1_brute_force_report.json
    ├── section5_2_heuristic_report.json
    ├── section6_performance_results.csv
    ├── section6_performance_report.json
    ├── section7_quality_analysis.json
    ├── section8_functional_testing.json
    └── performance_plots.png
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run complete analysis:**
   ```bash
   python run_analysis.py
   ```

3. **Run individual sections:**
   ```bash
   cd analysis/
   python section6_performance.py  # For performance testing
   python section7_quality.py      # For quality analysis
   ```

4. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

## Key Files

- **`src/subset_sum.py`** - Core implementation with 5 algorithms
- **`analysis/section6_performance.py`** - Statistical performance analysis
- **`docs/report.tex`** - Complete CS301 LaTeX report
- **`run_analysis.py`** - One-click complete analysis runner

## GitHub Ready Features

✅ Professional directory structure
✅ Complete documentation
✅ Requirements.txt for dependencies
✅ .gitignore for clean repository
✅ Executable analysis scripts
✅ Academic-quality code organization