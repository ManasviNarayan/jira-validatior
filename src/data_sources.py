from src.logger import get_logger
from typing import Iterator
import pandas as pd

logger = get_logger()

def fetch_jiras(filename: str, chunk_size: int) -> Iterator[pd.DataFrame]:
    """
    Fetch JIRA issues from a CSV file in chunks.
    
    Args:
        filename: Path to the CSV file containing JIRA issues
        chunk_size: Number of rows to process per chunk
    
    Returns:
        Iterator of DataFrames, each containing up to chunk_size rows
    """
    # Placeholder implementation: In a real scenario, this would fetch data from a JIRA API or database. 
    logger.info(f"Fetching JIRA issues from {filename} in chunks of size {chunk_size}")
    #dataset from Kaggle: https://www.kaggle.com/datasets/antonyjr/jira-issue-reports-v1
    return pd.read_csv(filename, chunksize=chunk_size)