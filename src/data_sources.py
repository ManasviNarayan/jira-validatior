from typing import Iterator
import pandas as pd

def fetch_jiras(chunk_size: int = 1000) -> Iterator[pd.DataFrame]:
    # Reads JIRA issues in chunks
    return pd.read_csv('jira_issues.csv', 
                       chunksize=chunk_size)