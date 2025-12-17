import pandas as pd
from src.logger import log_filter_call

def status_is(value: str|list):
    @log_filter_call(f"status_is({value})")
    def _filter(issue):
        # Pattern matching: match on value type to determine comparison method
        match value:
            # Pattern 1: Single string value - exact match
            case str():
                return issue.get('status') == value
            
            # Pattern 2: List of strings - membership check
            case list():
                return issue.get('status') in value
            
            # Pattern 3: Default case (invalid type)
            case _:
                return False
    return _filter

def priority_is(value: str|list):
    @log_filter_call(f"priority_is({value})")
    def _filter(issue):
        # Pattern matching: match on value type to determine comparison method
        match value:
            # Pattern 1: Single string value - exact match
            case str():
                return issue.get('priority') == value
            
            # Pattern 2: List of strings - membership check
            case list():
                return issue.get('priority') in value
            
            # Pattern 3: Default case (invalid type)
            case _:
                return False
    return _filter

def type_is(value: str|list):
    @log_filter_call(f"type_is({value})")
    def _filter(issue):
        # Pattern matching: match on value type to determine comparison method
        match value:
            # Pattern 1: Single string value - exact match
            case str():
                return issue.get('type') == value
            
            # Pattern 2: List of strings - membership check
            case list():
                return issue.get('type') in value
            
            # Pattern 3: Default case (invalid type)
            case _:
                return False
    return _filter

def is_assigned(to:str = ""):
    # Pattern matching: match on 'to' parameter to determine filter behavior
    match to:
        # Pattern 1: Empty string or None - check if any assignee exists
        case "" | None:
            @log_filter_call("is_assigned(any)")
            def _filter(issue):
                assignee = issue.get('assignee_id')
                # Nested pattern matching on assignee value
                match assignee:
                    # Pattern 1a: None value - no assignee
                    case None:
                        return False
                    # Pattern 1b: Check for pandas NaN - no assignee
                    case _ if pd.isna(assignee):
                        return False
                    # Pattern 1c: Non-empty string - has assignee
                    case str() if assignee.strip():
                        return True
                    # Pattern 1d: Empty string or whitespace - no valid assignee
                    case str() if not assignee.strip():
                        return False
                    # Pattern 1e: Default case
                    case _:
                        return False
            return _filter
        
        # Pattern 2: Non-empty string - check for specific assignee
        case str() if to:
            @log_filter_call(f"is_assigned(to = {to})")
            def _filter(issue):
                return issue.get('assignee_id') == to
            return _filter
        
        # Pattern 3: Default case (invalid input)
        case _:
            raise ValueError(f"Invalid assignee value: {to}")

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

