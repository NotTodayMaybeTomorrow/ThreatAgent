# schema.py — Arrow schemas for evaluation inputs
import pyarrow as pa

ALLOWED_TOPICS = {"tech_launch", "health_tips", "community_event"}
ALLOWED_STARTS = {"influencer", "random"}
ALLOWED_BACKENDS = {"baseline", "model_a", "model_b", "model_c", "model_d", "model_e"}
ALLOWED_PERSONAS = {"friendly", "skeptical", "influencer"}

runs_schema = pa.schema([
    ("run_id", pa.string()),
    ("seed", pa.int32()),
    ("topic", pa.string()),
    ("start_strategy", pa.string()),
    ("backend", pa.string()),
    ("chosen_variant_id", pa.string()),   # nullable allowed
    ("n_ticks", pa.int32()),
    ("persona_mix", pa.string()),         # JSON string
    ("graph_hash", pa.string()),
])

events_schema = pa.schema([
    ("run_id", pa.string()),
    ("tick", pa.int32()),
    ("event_type", pa.string()),          # "exposure" | "reshare"
    ("src", pa.int32()),
    ("dst", pa.int32()),
    ("src_is_influencer", pa.bool_()),
    ("dst_persona", pa.string()),
    ("seen_count_before", pa.int32()),
])

posts_schema = pa.schema([
    ("post_id", pa.string()),
    ("run_id", pa.string()),
    ("backend", pa.string()),
    ("variant_id", pa.string()),          # nullable ok
    ("text", pa.string()),
    ("features_json", pa.string()),       # nullable ok
    ("judge_score", pa.float64()),        # nullable ok
])

summary_schema = pa.schema([
    ("run_id", pa.string()),
    ("reach_rate", pa.float64()),
    ("cascade_size", pa.int32()),
    ("cascade_depth", pa.int32()),
    ("time_to_peak", pa.int32()),
    ("peak_reshare_count", pa.int32()),
    ("unique_reshares", pa.int32()),
    ("cost_calls", pa.int32()),
    ("cost_tokens", pa.int32()),
])

config_schema = pa.schema([
    ("run_id", pa.string()),
    ("config_json", pa.string()),
])
