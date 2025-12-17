from src.validation_pipelines import build_pipelines, run_pipeline
from src.data_sources import fetch_jiras
from src.config import get_config
import pandas as pd
import re

def clean_illegal_chars(df):
    """Return a new dataframe with illegal characters removed."""
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010\013\014\016-\037]')
    
    # Create a copy and transform each column
    df_clean = df.copy()
    for col in df_clean.select_dtypes(include=['object']):
        df_clean[col] = df_clean[col].astype(str).apply(lambda x: ILLEGAL_CHARACTERS_RE.sub('', x))
    return df_clean


def main(input_csv: str = None, 
         output_excel: str = None, 
         chunk_size: int = None,
         config: dict = None):
    """
    Main validation function.
    
    Args:
        input_csv: Path to input CSV file (overrides config if provided)
        output_excel: Path to output Excel file (overrides config if provided)
        chunk_size: Chunk size for processing (overrides config if provided)
        config: Configuration dictionary (loads from file if not provided)
    """
    # Load config if not provided
    if config is None:
        config = get_config()
    
    # Use provided parameters or fall back to config
    jira_config = config['jira']
    filename = input_csv or jira_config['filename']
    output_file = output_excel or "jira_issues_validated.xlsx"
    chunk_size = chunk_size or jira_config['chunk_size']
    
    # Build pipelines from config
    pipelines = build_pipelines(config['pipelines'], config['validations'])
    validate = run_pipeline(pipelines)
    
    # Process issues in chunks
    with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
        startrow = 0
        for df_chunk in fetch_jiras(filename, chunk_size):
            # Create new dataframe with error column
            df_chunk = (
                df_chunk
                .assign(error=df_chunk.apply(lambda row: validate(row), axis=1))
                .assign(error=lambda df: df['error'].apply(lambda errs: '; '.join(errs) if errs else ''))
            )
            df_chunk = clean_illegal_chars(df_chunk)

            df_chunk.to_excel(writer, index=False, header=(startrow==0), startrow=startrow)
            startrow += len(df_chunk)

if __name__ == "__main__":
    main()


