from dataclasses import dataclass

@dataclass
class SimConfig:
    n_agents: int = 200
    community_sizes: tuple[int, int, int] = (80, 70, 50)  # 三個社群
    influencer_ratio: float = 0.05                         # 5% 是網紅
    persona_mix: dict = None                               # 之後覆寫
    max_steps: int = 10
    base_feed_exposure: int = 20                           # 起始可見數（簡化）
    seed: int = 42

    def __post_init__(self):
        if self.persona_mix is None:
            # 友善、懷疑、一般（非網紅）
            self.persona_mix = {"friendly": 0.45, "skeptical": 0.45, "neutral": 0.10}
