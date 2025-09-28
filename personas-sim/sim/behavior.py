import math

# 可調參數（之後能放到 config 或 sweep）
PARAMS = {
    "bias": -1.2,                 # 全域偏置（越低越保守）
    "friendly_boost": 1.0,
    "skeptical_penalty": -0.8,
    "influencer_source_boost": 0.8,
    "prior_exposure_gain": 0.25,  # 每多看一次，輕微上升
    "cap": 4                      # prior_exposure 計算上限
}

def logistic(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def reshare_prob(persona: str, seen_times: int, from_influencer: bool) -> float:
    z = PARAMS["bias"]
    if persona == "friendly":
        z += PARAMS["friendly_boost"]
    elif persona == "skeptical":
        z += PARAMS["skeptical_penalty"]
    # neutral 不加成

    if from_influencer:
        z += PARAMS["influencer_source_boost"]

    z += min(seen_times, PARAMS["cap"]) * PARAMS["prior_exposure_gain"]
    return logistic(z)
