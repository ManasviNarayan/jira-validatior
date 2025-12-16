from datetime import datetime

def assignee_not_empty(issue):
    '''
    Validate that the assignee_id is a non-empty string.
    
    :param issue: Description
    '''
    assignee = issue.get('assignee_id', '')
    if not isinstance(assignee, str) or not assignee.strip():
        return "Assignee must be a non-empty string."
    return None

def resolved_date_not_null(issue):
    '''
    Validate that the resolved date is not null.
    :param issue: Description
    '''
    resolved_date = issue.get('resolved', None)
    if resolved_date is None:
        return "Resolved date must not be null."
    return None

def priority_not_null(issue):
    '''
    Validate that the priority is not null.
    
    :param issue: Description
    '''
    priority = issue.get('priority', None)
    if priority is None:
        return "Priority must not be null."
    return None

def updated_after_created(issue):
    '''
    Validate that the updated date is after the created date.
    
    :param issue: Description
    '''
    created = issue.get('created', None)
    updated = issue.get('updated', None)
    if created is None or updated is None:
        return "Created and updated dates must not be null."
    if updated < created:
        return "Updated date must be after created date."
    return None

def status_is_valid(issue, 
                    valid_statuses= {'Open', 'In Progress', 'Resolved', 'Closed'}):
    '''
    Validate that the issue's status is within the set of valid statuses.

    :param issue: Description
    :param valid_statuses: Set of valid statuses,
    default is {'Open', 'In Progress', 'Resolved', 'Closed'}
    '''
    status = issue.get('status', '')
    if status not in valid_statuses:
        return f"Status '{status}' is not valid. Must be one of {valid_statuses}."
    return None

def within_SLA(issue, sla_days=7):
    '''
    Validate that the issue was resolved within the SLA days.

    :param issue: Description
    :param sla_days: Number of days for SLA, default is 7
    '''
    created = issue.get('created', None)
    resolved = issue.get('resolved', None)
    if created is None:
        return "Created date must not be null."
    end_date = resolved if resolved is not None else datetime.today()
    delta = end_date - created
    if delta.days > sla_days:
        if resolved is not None:
            return f"Issue resolution time {delta.days} days exceeds SLA of {sla_days} days."
        else:
            return f"Issue open for {delta.days} days exceeds SLA of {sla_days} days."
    return None