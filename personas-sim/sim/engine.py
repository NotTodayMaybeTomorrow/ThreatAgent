from collections import defaultdict, deque
import numpy as np
import pandas as pd
from .behavior import reshare_prob

class SimRunResult:
    def __init__(self, events_df: pd.DataFrame, summary: dict):
        self.events = events_df
        self.summary = summary

def run_sim(G, max_steps=10, origin=0, seed=0, post_text=""):
    rng = np.random.default_rng(seed)

    # 狀態
    seen_count = defaultdict(int)     # node -> 次數
    reshared = set()                  # 已轉發者
    events = []                       # 日誌

    # 佇列： (step, source_node, target_node, depth_from_origin)
    q = deque()

    # Step 0：起始者發文 → 其鄰居看到
    origin_neighbors = list(G.neighbors(origin))
    for v in origin_neighbors:
        q.append((1, origin, v, 1))  # 第一步被看見的深度為1

    events.append({"step": 0, "actor": origin, "event": "post", "depth": 0})

    max_depth = 0
    reached_set = set(origin_neighbors) | {origin}
    step_peak = 0
    step_reach_counts = defaultdict(int)
    step_reach_counts[0] = 1  # origin 自己

    # BFS 式傳播
    while q:
        step, src, tgt, depth = q.popleft()
        if step > max_steps:
            continue
        max_depth = max(max_depth, depth)

        # 看到貼文
        seen_count[tgt] += 1
        step_reach_counts[step] += 1
        events.append({"step": step, "actor": tgt, "event": "see", "from": src, "depth": depth})
        reached_set.add(tgt)

        # 決定是否轉發
        persona = G.nodes[tgt]["persona"]
        from_influencer = G.nodes[src]["is_influencer"]
        p = reshare_prob(persona, seen_count[tgt], from_influencer)

        if (tgt not in reshared) and (rng.random() < p):
            reshared.add(tgt)
            events.append({"step": step, "actor": tgt, "event": "reshare", "from": src, "depth": depth})

            # 推播給尚未看過的鄰居（簡化：廣播所有鄰居）
            for w in G.neighbors(tgt):
                if w == src:
                    continue
                q.append((step + 1, tgt, w, depth + 1))

    # 摘要
    time_to_peak = max(step_reach_counts, key=lambda s: step_reach_counts[s])
    summary = {
        "origin": origin,
        "reached": len(reached_set),
        "cascade_depth": max_depth,
        "time_to_peak": time_to_peak,
        "post_text": post_text
    }
    events_df = pd.DataFrame(events)
    return SimRunResult(events_df, summary)
