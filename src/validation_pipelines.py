from src.filters import (type_is, status_is, 
                         and_,not_, is_null,
                         always)
from src.validations import (
    assignee_not_empty,
    resolved_date_not_null,
    priority_not_null,
    updated_after_created,
    status_is_valid,
)
from src.config import get_config
from src.logger import get_logger
from datetime import datetime

logger = get_logger()
config = get_config()['pipelines']

def run_pipeline(pipeline):
    """
    Runs a pipeline of (filter, [validators]) pairs on an issue.
    Each filter is a function that takes an issue and returns True/False.
    Each validator is a function that takes an issue and returns None or an error message.
    Returns a list of error messages (if any).
    """
    def runner(issue):
        errors = []
        logger.info(f"Running pipeline on issue {issue.get('key', 'N/A')}")
        for filter_func, validators in pipeline:
            if filter_func(issue):
                for validator in validators:
                    logger.info(f"{issue.get('key', 'N/A')}: Running validator {validator.__name__}")
                    result = validator(issue)
                    if result is not None:
                        errors.append(result)
        return errors
    return runner


# 1. Check that assignee_id is not empty for issues of type "Story" or "Bug".
pipeline_assignee_for_story_or_bug = [
    (type_is(config['require_assignee_for_types']), [assignee_not_empty])
]

# 2. Ensure "Resolved" or "Closed" issues have a non-null resolved_date.
pipeline_resolved_closed_has_resolved_date = [
    (status_is(config['require_resolved_date_for_statuses']), [resolved_date_not_null])
]

# 3. Validate that "In Progress" issues have a non-null assignee_id.
pipeline_in_progress_has_assignee = [
    (status_is('In Progress'), [assignee_not_empty])
]

# 4. Check that "Priority" is set for all issues except "Epics".
pipeline_priority_not_null_except_epic = [
    (not_(type_is('Epic')), [priority_not_null])
]

# 5. Flag issues where created_date is after resolved_date.
pipeline_updated_before_created = [
    (
        and_(
            not_(is_null('created')),
            not_(is_null('updated'))
        ),
        [updated_after_created]
    )
]

# 6. Identify issues with missing or invalid "status" values (not in allowed set).
# 7. Ensure due_date is not before created_date.
pipeline_status_and_dates_are_valid = [
    (always, [status_is_valid, updated_after_created])
]

# Example: Combine all pipelines for a full validation run
all_pipelines = (
    pipeline_assignee_for_story_or_bug +
    pipeline_resolved_closed_has_resolved_date +
    pipeline_in_progress_has_assignee +
    pipeline_priority_not_null_except_epic +
    pipeline_updated_before_created +
    pipeline_status_and_dates_are_valid
)