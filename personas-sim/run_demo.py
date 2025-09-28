from sim.config import SimConfig
from sim.graph import build_graph
from sim.personas import assign_personas
from sim.engine import run_sim
from sim.logging_io import save_run, summarize_to_df
import numpy as np
from pathlib import Path

def main():
    cfg = SimConfig(seed=42)
    G = build_graph(cfg)
    assign_personas(G, cfg)

    seeds = [11,12,13,14,15,16,17,18,19,20]
    summaries = []
    for s in seeds:
        origin = np.random.default_rng(s).integers(0, G.number_of_nodes())
        result = run_sim(G, max_steps=cfg.max_steps, origin=origin, seed=s, post_text="[baseline msg]")
        save_run(result.events, result.summary, outdir="runs", run_id=f"seed{s}")
        summaries.append(result.summary)

    df = summarize_to_df(summaries)
    out_path = Path("runs") / "runs_summary.parquet"
    df.to_parquet(out_path, index=False)
    print("Done. Summaries:\n", df.head())
    print(f"Saved to: {out_path}")

if __name__ == "__main__":
    main()
