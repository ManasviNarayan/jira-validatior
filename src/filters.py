import pandas as pd

def status_is(value: str|list):
    '''
    Filter issues by their status.
    Check if the issue's status matches the given value or is in the given list of values.
    
    :param value: Description
    :type value: str | list
    '''
    return lambda issue: issue['status'] == value if isinstance(value, str) else issue['status'] in value

def priority_is(value: str|list):
    '''
    Filter issues by their priority.
    Check if the issue's priority matches the given value or is in the given list of values.

    :param value: Description
    :type value: str | list
    '''
    return lambda issue: issue['priority'] == value if isinstance(value, str) else issue['priority'] in value

def type_is(value: str|list):
    '''
    Filter issues by their type.
    Check if the issue's type matches the given value or is in the given list of values.

    :param value: Description
    :type value: str | list
    '''
    return lambda issue: issue['type'] == value if isinstance(value, str) else issue['type'] in value

def is_assigned(to:str = ""):
    '''
    Filter issues by their assignee_id.
    If 'to' is provided, check if the issue's assignee matches 'to'. If 'to' is not provided, check if the issue has any assignee.
    
    :param to: Description
    :type to: str
    '''
    if to:
        return lambda issue: issue['assignee_id'] == to
    else:
        return lambda issue: pd.notna(issue['assignee_id']) and issue['assignee_id'].strip() != ''

def created_before(date):
    '''
    Filter issues by their creation date.
    Check if the issue was created before the given date.

    :param date: Description
    :type date: datetime
    '''
    return lambda issue: issue['created'] < date

def created_after(date):
    '''
    Filter issues by their creation date.
    Check if the issue was created after the given date.

    :param date: Description
    :type date: datetime
    '''
    return lambda issue: issue['created'] > date

def is_null(field):
    '''
    Filter issues by checking if a specific field is null.

    :param field: Description
    :type field: str
    '''
    return lambda issue: pd.isna(issue[field])

def and_(*filters):
    return lambda issue: all(f(issue) for f in filters)

def or_(*filters):
    return lambda issue: any(f(issue) for f in filters)

def not_(filter_func):
    return lambda issue: not filter_func(issue)

def always(issue):
    return True

