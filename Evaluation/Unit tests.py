# tests/test_validate.py
import pandas as pd
from eval.validate import validate_all, validate_events

def _mk_runs():
    return pd.DataFrame([{
        "run_id":"r1","seed":123,"topic":"tech_launch","start_strategy":"influencer",
        "backend":"baseline","n_ticks":10,"persona_mix":"{\"friendly\":0.6,\"skeptical\":0.3,\"influencer\":0.1}",
        "graph_hash":"abc"
    }])

def _mk_posts():
    return pd.DataFrame([{
        "post_id":"p1","run_id":"r1","backend":"baseline","variant_id":"baseline_fixed",
        "text":"Community meetup this weekend.","features_json":None,"judge_score":None
    }])

def _mk_summary():
    return pd.DataFrame([{
        "run_id":"r1","reach_rate":0.35,"cascade_size":5,"cascade_depth":3,
        "time_to_peak":2,"peak_reshare_count":3,"unique_reshares":5,
        "cost_calls":0,"cost_tokens":0
    }])

def _mk_events_ok():
    return pd.DataFrame([
        {"run_id":"r1","tick":1,"event_type":"exposure","src":1,"dst":2,"src_is_influencer":True,"dst_persona":"friendly","seen_count_before":0},
        {"run_id":"r1","tick":2,"event_type":"reshare","src":2,"dst":3,"src_is_influencer":False,"dst_persona":"friendly","seen_count_before":1},
    ])

def _mk_events_bad():
    return pd.DataFrame([
        {"run_id":"r1","tick":2,"event_type":"reshare","src":2,"dst":3,"src_is_influencer":False,"dst_persona":"friendly","seen_count_before":0},
    ])

def test_validate_all_ok():
    runs, posts, summary, events = _mk_runs(), _mk_posts(), _mk_summary(), _mk_events_ok()
    assert validate_all(runs, events, posts, summary)

def test_validate_events_fail():
    runs = _mk_runs()
    events = _mk_events_bad()
    try:
        validate_events(events, runs)
        assert False, "should fail"
    except AssertionError:
        assert True
