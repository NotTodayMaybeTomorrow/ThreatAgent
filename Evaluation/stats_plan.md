# Stats Plan (Week 1 · Day 1)

**Created:** 2025-09-29

## 1. Objectives & Endpoints
- **Primary endpoint**: Δ *reach_rate* (LLM − Baseline) under **influencer-start**. Report per-topic and overall.
- **Secondary endpoints**: `cascade_size`, `cascade_depth`, `time_to_peak`, `cost_per_success`, `persona_reshare_rate`, and Δ *reach_rate* under **random-start**.

### Metric definitions
- **reach_rate** = unique agents exposed / N (N=200).
- **cascade_size** = number of unique resharers.
- **cascade_depth** = maximum depth in the reshare propagation tree.
- **time_to_peak** = tick index with maximal #reshares (argmax over ticks).
- **cost_per_success** = (# LLM calls used in runs with reach_rate ≥ threshold) / (# successful runs).

Success threshold default: **35%** (configurable).

## 2. Study Factors
- Topics: 3 (`tech_launch`, `health_tips`, `community_event`)
- Start strategies: 2 (`influencer`, `random`)
- Backends: baseline + 5 LLM models (`model_a`..`model_e`)
- Seeds: **15** (fixed list; see `configs/experiment.yaml`)

## 3. Statistical Methods
### 3.1 Confidence intervals
- **BCa bootstrap** (10k resamples, CI=95%). Use seed=12345 for determinism.
- Report median (or mean for reach_rate) with 95% CI.

### 3.2 Hypothesis testing
- **Primary**: permutation test (50k permutations, seed=23456) comparing mean *reach_rate* between LLM and Baseline under influencer-start. Two-sided p-value.
- **Secondary**: permutation test on median for scale-like metrics (`cascade_size`, `depth`, `time_to_peak`); mean for rates as appropriate.

### 3.3 Effect sizes
- **Cliff’s δ** for pairwise LLM vs Baseline comparisons; interpret using thresholds:
  - negligible < 0.147; small < 0.33; medium < 0.474; large ≥ 0.474
- **Rate ratio** for `cost_per_success` (bootstrap CI).

### 3.4 Multiple comparisons
- Control false discovery rate using **Benjamini–Hochberg** at **q=0.05** across all secondary tests (and exploratory persona comparisons).

## 4. Analysis Sets
- **Per-topic** analyses: stratify by topic.
- **Overall** analysis: pool across topics using equal weights per seed (or mixed-effects as future extension).

## 5. Reporting
- For each comparison, report: point estimate, 95% CI, p-value (permutation), effect size (Cliff’s δ) and interpretation bucket.
- Provide both CSV tables and publication-ready figures (PNG + SVG).

## 6. Reproducibility
- Fix seeds for bootstrap/permutation.
- Save analysis manifest (config hash, code version, artifact paths).
- Ensure deterministic reading order and sorting by `run_id`.

## 7. Deviation Handling
- Any change to endpoints, thresholds, or N seeds must be recorded in `docs/change_log.md` with rationale.
