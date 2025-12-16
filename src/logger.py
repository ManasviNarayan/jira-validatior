
from functools import wraps

def get_logger(name="jira_validator"):
    """
    Returns a singleton logger instance for the given name.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def log_row_call(func):
    """
    Decorator to log function calls for each row (issue).
    Logs the function name, issue key (if present), and result.
    """
    logger = get_logger()

    @wraps(func)
    def wrapper(issue, *args, **kwargs):
        issue_key = issue.get('key', 'N/A') if isinstance(issue, pd.Series) else 'N/A'
        logger.info(f"{issue_key}: {func.__name__} start")
        result = func(issue, *args, **kwargs)
        logger.info(f"{issue_key}: {func.__name__} end")
        return result
    return wrapper

def log_filter_call(name):
    """
    Decorator to log filter function calls for each row (issue).
    Logs the filter name, issue key (if present), and result.
    """
    logger = get_logger()
    def decorator(func):
        @wraps(func)
        def wrapper(issue, *args, **kwargs):
            issue_key = issue.get('key', 'N/A') if isinstance(issue, pd.Series) else 'N/A'
            result = func(issue, *args, **kwargs)
            logger.info(f"{issue_key}: {name} -> {result}")
            return result
        return wrapper
    return decorator
import logging
import pandas as pd