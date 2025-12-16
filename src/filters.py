import pandas as pd
from src.logger import log_filter_call

def status_is(value: str|list):
    @log_filter_call(f"status_is({value})")
    def _filter(issue):
        return issue['status'] == value if isinstance(value, str) else issue['status'] in value
    return _filter

def priority_is(value: str|list):
    @log_filter_call(f"priority_is({value})")
    def _filter(issue):
        return issue['priority'] == value if isinstance(value, str) else issue['priority'] in value
    return _filter

def type_is(value: str|list):
    @log_filter_call(f"type_is({value})")
    def _filter(issue):
        return issue['type'] == value if isinstance(value, str) else issue['type'] in value
    return _filter

def is_assigned(to:str = ""):
    if to:
        @log_filter_call(f"is_assigned(to = {to})")
        def _filter(issue):
            return issue['assignee_id'] == to
        return _filter
    else:
        @log_filter_call("is_assigned(any)")
        def _filter(issue):
            return pd.notna(issue['assignee_id']) and issue['assignee_id'].strip() != ''
        return _filter

def created_before(date):
    @log_filter_call(f"created_before({date})")
    def _filter(issue):
        return issue['created'] < date
    return _filter

def created_after(date):
    @log_filter_call(f"created_after({date})")
    def _filter(issue):
        return issue['created'] > date
    return _filter

def is_null(field):
    @log_filter_call(f"is_null({field})")
    def _filter(issue):
        return bool(issue.get(field))
    return _filter

def and_(*filters):
    @log_filter_call("and_ filter")
    def _filter(issue):
        return all(f(issue) for f in filters)
    return _filter

def or_(*filters):
    @log_filter_call("or_ filter")
    def _filter(issue):
        return any(f(issue) for f in filters)
    return _filter

def not_(filter_func):
    @log_filter_call("not_ filter")
    def _filter(issue):
        return not filter_func(issue)
    return _filter

@log_filter_call("always filter")
def always(issue):
    return True

