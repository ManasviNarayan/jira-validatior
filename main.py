from src.validation_pipelines import all_pipelines, run_pipeline
from src.data_sources import fetch_jiras
import pandas as pd

import re

def clean_illegal_chars(df):
    # Define a regex for illegal characters (openpyxl only allows certain unicode)
    ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010\013\014\016-\037]')
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).apply(lambda x: ILLEGAL_CHARACTERS_RE.sub('', x))
    return df


def main(input_csv: str = "jira_issues.csv", 
         output_excel: str = "jira_issues_validated.xlsx", 
         chunk_size: int = 1000):
    validate = run_pipeline(all_pipelines)
    first = True
    with pd.ExcelWriter(output_excel, engine="openpyxl", mode="w") as writer:
        startrow = 0
        for df_chunk in fetch_jiras(chunk_size=chunk_size):
            df_chunk['error'] = df_chunk.apply(lambda row: validate(row), axis=1)
            df_chunk['error'] = df_chunk['error'].apply(lambda errs: '; '.join(errs) if errs else '')
            df_chunk = clean_illegal_chars(df_chunk)

            df_chunk.to_excel(writer, index=False, header=(startrow==0), startrow=startrow)
            startrow += len(df_chunk)

if __name__ == "__main__":
    main()


