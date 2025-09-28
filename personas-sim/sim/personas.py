import numpy as np
from .config import SimConfig

PERSONA_TYPES = ["friendly", "skeptical", "neutral"]

def assign_personas(G, cfg: SimConfig):
    rng = np.random.default_rng(cfg.seed)
    n = G.number_of_nodes()
    n_influencers = max(1, int(n * cfg.influencer_ratio))
    influencers = set(rng.choice(n, size=n_influencers, replace=False))

    # 依 mix 抽樣人格
    probs = np.array([cfg.persona_mix[p] for p in PERSONA_TYPES])
    probs = probs / probs.sum()
    personas = list(rng.choice(PERSONA_TYPES, size=n, replace=True, p=probs))

    for i in range(n):
        G.nodes[i]["persona"] = personas[i]
        G.nodes[i]["is_influencer"] = (i in influencers)
