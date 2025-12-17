# JIRA Issue Validator

A comprehensive Python tool for validating JIRA issues from CSV exports. This validator uses a flexible pipeline-based architecture to check issues against configurable business rules and outputs results to an Excel file with detailed error messages.

## Features

- **Pipeline-Based Validation**: Modular validation system using filters and validators
- **Chunked Processing**: Efficiently processes large datasets in configurable chunks
- **Configurable Rules**: Customize validation rules through `config.json`
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Excel Output**: Generates Excel files with validation errors clearly marked
- **Flexible Filtering**: Powerful filter system for conditional validations

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Validation Rules](#validation-rules)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Contributing](#contributing)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Dependencies

Install the required packages:

```bash
pip install pandas openpyxl
```

Or create a `requirements.txt` file:

```txt
pandas>=1.5.0
openpyxl>=3.0.0
```

Then install:

```bash
pip install -r requirements.txt
```

## Quick Start

1. **Prepare your JIRA CSV file**: Export your JIRA issues to a CSV file named `jira_issues.csv` (or specify a custom filename in config)

2. **Run the validator**:

```bash
python main.py
```

3. **Check the output**: The validated issues with error messages will be saved to `jira_issues_validated.xlsx`

## Configuration

The validator uses `src/config.json` for configuration. If the file doesn't exist, it will be automatically created with default values.

### Configuration Structure

```json
{
    "jira": {
        "filename": "jira_issues.csv",
        "chunk_size": 1000
    },
    "validations": {
        "valid_statuses": ["To Do", "In Progress", "Resolved", "Closed", "Open"],
        "sla_days": 7
    },
    "pipelines": {
        "require_assignee_for_types": ["Story", "Bug"],
        "require_resolved_date_for_statuses": ["Resolved", "Closed"]
    }
}
```

### Configuration Options

- **jira.filename**: Path to the input CSV file containing JIRA issues
- **jira.chunk_size**: Number of rows to process at a time (default: 1000)
- **validations.valid_statuses**: List of acceptable status values
- **validations.sla_days**: Maximum number of days for SLA compliance
- **pipelines.require_assignee_for_types**: Issue types that must have an assignee
- **pipelines.require_resolved_date_for_statuses**: Statuses that must have a resolved date

## Usage

### Basic Usage

```python
from main import main

# Use default settings
main()
```

### Custom Input/Output Files

```python
from main import main

# Specify custom input and output files
main(
    input_csv="my_jira_export.csv",
    output_excel="validation_results.xlsx",
    chunk_size=500
)
```

### Programmatic Usage

```python
from src.validation_pipelines import all_pipelines, run_pipeline
from src.data_sources import fetch_jiras
import pandas as pd

# Create validation function
validate = run_pipeline(all_pipelines)

# Process issues
for df_chunk in fetch_jiras(chunk_size=1000):
    df_chunk['error'] = df_chunk.apply(lambda row: validate(row), axis=1)
    # Process validated chunk...
```

## Validation Rules

The validator includes the following built-in validation rules:

### 1. Assignee Validation
- **Rule**: Stories and Bugs must have a non-empty assignee
- **Filter**: Issue type is "Story" or "Bug"
- **Validator**: `assignee_not_empty()`

### 2. Resolved Date Validation
- **Rule**: Resolved or Closed issues must have a resolved date
- **Filter**: Status is "Resolved" or "Closed"
- **Validator**: `resolved_date_not_null()`

### 3. In Progress Assignee
- **Rule**: Issues in "In Progress" status must have an assignee
- **Filter**: Status is "In Progress"
- **Validator**: `assignee_not_empty()`

### 4. Priority Validation
- **Rule**: All issues except Epics must have a priority set
- **Filter**: Issue type is not "Epic"
- **Validator**: `priority_not_null()`

### 5. Date Consistency
- **Rule**: Updated date must be after created date
- **Filter**: Both created and updated dates are present
- **Validator**: `updated_after_created()`

### 6. Status Validation
- **Rule**: Status must be one of the valid statuses
- **Filter**: Always applies to all issues
- **Validator**: `status_is_valid()`

### 7. SLA Compliance
- **Rule**: Issues should be resolved within the configured SLA days
- **Filter**: Always applies to all issues
- **Validator**: `within_SLA()`

## Architecture

### Pipeline System

The validator uses a pipeline-based architecture where:
- **Filters**: Determine which issues should be validated
- **Validators**: Perform the actual validation checks
- **Pipelines**: Combine filters and validators into validation rules

### Data Flow

```
CSV File → Chunked Reader → Pipeline Validator → Excel Output
                ↓
         Error Messages
```

### Components

1. **Data Sources** (`src/data_sources.py`): Handles reading JIRA data from CSV files
2. **Filters** (`src/filters.py`): Provides filtering functions for conditional validations
3. **Validations** (`src/validations.py`): Contains individual validation functions
4. **Validation Pipelines** (`src/validation_pipelines.py`): Combines filters and validators
5. **Configuration** (`src/config.py`): Manages configuration loading and defaults
6. **Logger** (`src/logger.py`): Provides logging functionality

## Project Structure

```
jira-validatior/
├── main.py                      # Main entry point
├── README.md                    # This file
├── jira_issues.csv             # Input CSV file (your JIRA export)
├── jira_issues_validated.xlsx  # Output Excel file
├── sample_jira_issues.csv      # Sample data file
├── eda.ipynb                   # Exploratory data analysis notebook
└── src/
    ├── __init__.py
    ├── config.json             # Configuration file
    ├── config.py               # Configuration management
    ├── data_sources.py         # Data loading functions
    ├── filters.py              # Filter functions
    ├── logger.py               # Logging utilities
    ├── models.py               # Data models (if any)
    ├── validations.py          # Validation functions
    └── validation_pipelines.py # Pipeline definitions
```

## Examples

### Adding a Custom Validation

1. Add a validation function to `src/validations.py`:

```python
@log_row_call
def custom_validation(issue):
    """Your custom validation logic"""
    if some_condition:
        return "Error message"
    return None
```

2. Create a pipeline in `src/validation_pipelines.py`:

```python
from src.filters import type_is
from src.validations import custom_validation

custom_pipeline = [
    (type_is('Story'), [custom_validation])
]
```

3. Add to `all_pipelines`:

```python
all_pipelines = (
    # ... existing pipelines ...
    + custom_pipeline
)
```

### Using Custom Filters

```python
from src.filters import status_is, priority_is, and_

# Filter for high priority in-progress issues
filter_func = and_(
    status_is('In Progress'),
    priority_is('High')
)
```

## Output Format

The output Excel file contains all original columns plus an `error` column:
- **Empty error column**: Issue passed all validations
- **Error messages**: Semicolon-separated list of validation errors

Example error column values:
- `""` (empty) - No errors
- `"Assignee must be a non-empty string."` - Single error
- `"Assignee must be a non-empty string.; Priority must not be null."` - Multiple errors

## Logging

The validator includes comprehensive logging:
- Logs are written to stdout
- Format: `[timestamp] LEVEL logger_name: message`
- Includes validation start/end for each issue
- Logs filter evaluations

To adjust logging level, modify `src/logger.py`.

## Troubleshooting

### Common Issues

1. **File Not Found Error**
   - Ensure `jira_issues.csv` exists in the project root
   - Or update `config.json` with the correct file path

2. **Memory Issues with Large Files**
   - Reduce `chunk_size` in `config.json`
   - Default is 1000 rows per chunk

3. **Excel Writing Errors**
   - Ensure `openpyxl` is installed: `pip install openpyxl`
   - Check file permissions for output directory

4. **Illegal Characters in Excel**
   - The validator automatically cleans illegal characters (control characters)
   - If issues persist, check your CSV data

## Contributing

When contributing to this project:

1. Follow the existing code structure
2. Add logging to new validations using `@log_row_call` decorator
3. Update `config.json` for new configuration options
4. Document new validations in this README

## License

[Specify your license here]

## Acknowledgments

- Dataset source: [Kaggle JIRA Issue Reports](https://www.kaggle.com/datasets/antonyjr/jira-issue-reports-v1)

