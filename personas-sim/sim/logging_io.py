import pandas as pd
from pathlib import Path

def save_run(events_df: pd.DataFrame, summary: dict, outdir="runs", run_id="seed42"):
    Path(outdir).mkdir(parents=True, exist_ok=True)
    events_path = Path(outdir) / f"events_{run_id}.parquet"
    events_df.to_parquet(events_path, index=False)
    return str(events_path)

def summarize_to_df(summaries: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(summaries)
