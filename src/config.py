# config.py
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
print(CONFIG_FILE)

DEFAULT_CONFIG = {
    "jira": {
        'filename': 'jira_issues.csv',
        'chunk_size': 1000
    },
    'validations': {
        'valid_statuses': ['To Do', 'In Progress', 'Resolved', 'Closed', 'Open'],
        'sla_days': 7
    },
    'pipelines': {
        'require_assignee_for_types': ['Story', 'Bug'],
        'require_resolved_date_for_statuses': ['Resolved', 'Closed']
    }
}

_config = None  # private module state


def get_config():
    global _config

    if _config is None:
        _config = _load_config()

    return _config


def _load_config():
    if not CONFIG_FILE.exists():
        _initialize_config()

    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _initialize_config():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)
