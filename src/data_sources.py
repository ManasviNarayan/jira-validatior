from src.logger import get_logger
from src.config import get_config
from typing import Iterator
import pandas as pd

logger = get_logger()
config = get_config()['jira']

def fetch_jiras(chunk_size: int = config['chunk_size']) -> Iterator[pd.DataFrame]:
    # Placeholder implementation: In a real scenario, this would fetch data from a JIRA API or database. 
    logger.info(f"Fetching JIRA issues in chunks of size {chunk_size}")
    #dataset from Kaggle: https://www.kaggle.com/datasets/antonyjr/jira-issue-reports-v1
    return pd.read_csv(config['filename'], 
                       chunksize=chunk_size)