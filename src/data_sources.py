from src.logger import get_logger
from typing import Iterator
import pandas as pd

logger = get_logger()

def fetch_jiras(chunk_size: int = 1000) -> Iterator[pd.DataFrame]:
    # Placeholder implementation: In a real scenario, this would fetch data from a JIRA API or database. 
    logger.info(f"Fetching JIRA issues in chunks of size {chunk_size}")
    #dataset from Kaggle: https://www.kaggle.com/datasets/antonyjr/jira-issue-reports-v1
    return pd.read_csv('jira_issues.csv', 
                       chunksize=chunk_size)