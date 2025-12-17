from src.logger import log_row_call, get_logger
from datetime import datetime
import pandas as pd

logger = get_logger()

@log_row_call
def assignee_not_empty(issue):
    '''
    Validate that the assignee_id is a non-empty string.
    '''
    assignee = issue.get('assignee_id', '')
    if pd.isna(assignee) or not isinstance(assignee, str) or not assignee.strip():
        return "Assignee must be a non-empty string."
    return None

@log_row_call
def resolved_date_not_null(issue):
    '''
    Validate that the resolved date is not null.
    '''
    resolved_date = issue.get('resolved', None)
    if pd.isna(resolved_date):
        return "Resolved date must not be null."
    return None

@log_row_call
def priority_not_null(issue):
    '''
    Validate that the priority is not null.
    '''
    priority = issue.get('priority', None)
    if pd.isna(priority):
        return "Priority must not be null."
    return None

@log_row_call
def updated_after_created(issue):
    '''
    Validate that the updated date is after the created date.
    '''
    created = issue.get('created', None)
    updated = issue.get('updated', None)
    if pd.isna(created) or pd.isna(updated):
        return "Created and updated dates must not be null."
    if updated < created:
        return "Updated date must be after created date."
    return None

def status_is_valid(issue, 
                    valid_statuses= None):
    '''
    Validate that the issue's status is within the set of valid statuses.
    '''
    status = issue.get('status', '')
    if pd.isna(status) or status not in valid_statuses:
        return f"Status '{status}' is not valid. Must be one of {valid_statuses}."
    return None

def within_SLA(issue, sla_days=None):
    '''
    Validate that the issue was resolved within the SLA days.
    '''
    created = issue.get('created', None)
    resolved = issue.get('resolved', None)
    if pd.isna(created):
        return "Created date must not be null."
    end_date = resolved if not pd.isna(resolved) else datetime.today()
    delta = end_date - created
    if delta.days > sla_days:
        if not pd.isna(resolved):
            return f"Issue resolution time {delta.days} days exceeds SLA of {sla_days} days."
        else:
            return f"Issue open for {delta.days} days exceeds SLA of {sla_days} days."
    return None