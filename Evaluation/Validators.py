# eval/validate.py — validators for logs & metadata
import pandas as pd

ALLOWED_TOPICS = {"tech_launch", "health_tips", "community_event"}
ALLOWED_STARTS = {"influencer", "random"}
ALLOWED_BACKENDS = {"baseline", "model_a", "model_b", "model_c", "model_d", "model_e"}
ALLOWED_PERSONAS = {"friendly", "skeptical", "influencer"}

def _check_required(df, cols, name: str):
    missing = [c for c in cols if c not in df.columns]
    assert not missing, f"{name}: missing columns {missing}"

def validate_runs(df):
    _check_required(df, ["run_id","seed","topic","start_strategy","backend","n_ticks","persona_mix","graph_hash"], "runs")
    assert df["backend"].isin(ALLOWED_BACKENDS).all()
    assert df["start_strategy"].isin(ALLOWED_STARTS).all()
    assert df["topic"].isin(ALLOWED_TOPICS).all()
    assert df["run_id"].is_unique

def validate_posts(df_posts, df_runs):
    _check_required(df_posts, ["post_id","run_id","backend","variant_id","text","features_json","judge_score"], "posts")
    # one post per run
    counts = df_posts.groupby("run_id").size()
    assert (counts == 1).all()
    # backend match
    merged = df_posts[["run_id","backend"]].merge(df_runs[["run_id","backend"]], on="run_id", suffixes=("_p","_r"))
    assert (merged["backend_p"] == merged["backend_r"]).all()

def validate_events(df_events, df_runs):
    _check_required(df_events, ["run_id","tick","event_type","src","dst","src_is_influencer","dst_persona","seen_count_before"], "events")
    assert df_events["event_type"].isin(["exposure","reshare"]).all()
    assert df_events["dst_persona"].isin(ALLOWED_PERSONAS).all()
    # tick ≤ n_ticks
    mx = df_events.groupby("run_id")["tick"].max().reset_index().merge(df_runs[["run_id","n_ticks"]])
    assert (mx["tick"] <= mx["n_ticks"]).all()
    # reshare must follow exposure
    for rid, g in df_events.sort_values("tick").groupby("run_id"):
        exposures = set(g[g.event_type=="exposure"]["dst"])
        for dst in g[g.event_type=="reshare"]["dst"]:
            assert dst in exposures, f"reshare without exposure in run {rid}"
        # at most 1 reshare/user
        assert not (g[g.event_type=="reshare"].groupby("dst").size() > 1).any()

def validate_summary(df_summary, df_runs, df_events):
    _check_required(df_summary, ["run_id","reach_rate","cascade_size","cascade_depth","time_to_peak","peak_reshare_count","unique_reshares","cost_calls","cost_tokens"], "summary")
    assert df_summary["reach_rate"].between(0,1).all()
    mx = df_summary.merge(df_runs[["run_id","n_ticks"]])
    assert (mx["time_to_peak"] <= mx["n_ticks"]).all()
    # unique_reshares matches events
    calc = df_events[df_events.event_type=="reshare"].groupby("run_id")["dst"].nunique().reset_index(name="calc")
    merged = df_summary.merge(calc, on="run_id", how="left").fillna({"calc":0})
    assert (merged["unique_reshares"] == merged["calc"]).all()

def validate_all(runs, events, posts, summary):
    validate_runs(runs)
    validate_posts(posts, runs)
    validate_events(events, runs)
    validate_summary(summary, runs, events)
    return True
