import numpy as np
import networkx as nx
from .config import SimConfig

def build_graph(cfg: SimConfig) -> nx.Graph:
    np.random.seed(cfg.seed)
    sizes = list(cfg.community_sizes)
    # 社群內連結機率高、社群間較低
    p_in, p_out = 0.08, 0.005
    p = [[p_in if i==j else p_out for j in range(len(sizes))] for i in range(len(sizes))]
    G = nx.stochastic_block_model(sizes, p, seed=cfg.seed)
    # 確保節點 id 連號 0..N-1
    G = nx.convert_node_labels_to_integers(G, first_label=0, ordering="default")
    return G
