# Data Contracts 

**Created:** 2025-09-29

This document defines the **schemas**, **valid values**, and **invariants** for all logs and metadata the
Evaluation pipeline consumes. Producers (Simulation & Threat Agent) MUST conform to these contracts.

---

## Common definitions
- **N agents**: 200 (from `configs/experiment.yaml`)
- **Ticks**: 0..n_ticks (inclusive of 0 for injection; events must have tick ∈ [0, n_ticks])
- **Backends**: `baseline`, `model_a`, `model_b`, `model_c`, `model_d`, `model_e`
- **Start strategies**: `influencer`, `random`
- **Personas**: `friendly`, `skeptical`, `influencer`

### Identifiers
- `run_id`: unique string per (seed × topic × start_strategy × backend)
- `post_id`: unique string for the injected post of a given run
- `variant_id`: backend-specific identifier; `null`/`"baseline_fixed"` for baseline

---

## Table: `runs.parquet`
| Column            | Type    | Required | Notes |
|-------------------|---------|----------|-------|
| run_id            | string  | yes      | unique |
| seed              | int32   | yes      | from experiment seeds |
| topic             | string  | yes      | ∈ {tech_launch, health_tips, community_event} |
| start_strategy    | string  | yes      | ∈ {influencer, random} |
| backend           | string  | yes      | ∈ {baseline, model_a..model_e} |
| chosen_variant_id | string  | nullable | baseline may use `"baseline_fixed"` or `null` |
| n_ticks           | int32   | yes      | ≤ value in config |
| persona_mix       | string  | yes      | JSON string like {"friendly":0.6,"skeptical":0.3,"influencer":0.1} |
| graph_hash        | string  | yes      | checksum of graph structure |

**Invariants**
- `backend` must be in allowed set.
- `n_ticks` must match config (or be ≤ config n_ticks).

---

## Table: `events.parquet`
| Column            | Type    | Required | Notes |
|-------------------|---------|----------|-------|
| run_id            | string  | yes      | FK to runs.run_id |
| tick              | int32   | yes      | 0..n_ticks |
| event_type        | string  | yes      | ∈ {exposure, reshare} |
| src               | int32   | yes      | node id (poster/resharer) |
| dst               | int32   | yes      | node id (viewer/recipient) |
| src_is_influencer | bool    | yes      | whether src has influencer role |
| dst_persona       | string  | yes      | ∈ {friendly, skeptical, influencer} |
| seen_count_before | int32   | yes      | how many prior exposures dst had before this event |

**Invariants**
- Ticks non-decreasing within a run and `max(tick) ≤ runs.n_ticks`.
- For every `reshare` event by `dst`, there must exist at least one prior `exposure` to `dst` with a smaller tick.
- Each `dst` can `reshare` at most once per run.

---

## Table: `posts.parquet`
| Column       | Type    | Required | Notes |
|--------------|---------|----------|-------|
| post_id      | string  | yes      | unique |
| run_id       | string  | yes      | FK to runs.run_id |
| backend      | string  | yes      | as above |
| variant_id   | string  | nullable | baseline may use `"baseline_fixed"`/`null` |
| text         | string  | yes      | selected/injected content |
| features_json| string  | nullable | JSON of features (length, sentiment, cta flags, etc.) |
| judge_score  | float64 | nullable | null for baseline |

**Invariants**
- Exactly **one** row per `run_id` (one injected post per run).

---

## Table: `summary.parquet`
| Column             | Type    | Required | Notes |
|--------------------|---------|----------|-------|
| run_id             | string  | yes      | FK to runs.run_id |
| reach_rate         | float64 | yes      | unique_exposed / 200 |
| cascade_size       | int32   | yes      | # unique resharers |
| cascade_depth      | int32   | yes      | max path length |
| time_to_peak       | int32   | yes      | tick with max reshares |
| peak_reshare_count | int32   | yes      | max #reshare on a tick |
| unique_reshares    | int32   | yes      | same as cascade_size |
| cost_calls         | int32   | yes      | 0 for baseline |
| cost_tokens        | int32   | yes      | 0 for baseline |

---

## Table: `config.parquet`
| Column      | Type   | Required | Notes |
|-------------|--------|----------|-------|
| run_id      | string | yes      | FK |
| config_json | string | yes      | Frozen parameters used by simulation |

---

## Cross-table rules
- A `run_id` present in `events`/`posts`/`summary` **must** exist in `runs`.
- For a given run, `posts.backend == runs.backend`.
- Counts must be consistent: `unique_reshares == number of distinct dst with reshare`.

---
