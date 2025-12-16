## Plan: Data Hygiene Validations for Jira Issues

This plan outlines complex, conditional data hygiene checks to ensure the Jira issues dataset is clean and ready for reporting. These validations focus on business logic and field dependencies.

### Steps
1. Check that `assignee_id` is not empty for issues of type "Story" or "Bug".
2. Ensure "Resolved" or "Closed" issues have a non-null `resolved_date`.
3. Validate that "In Progress" issues have a non-null `assignee_id`.
4. Check that "Priority" is set for all issues except "Epics".
5. Flag issues where `created_date` is after `resolved_date`.
6. Identify issues with missing or invalid "status" values (not in allowed set).
7. Validate that updated date is after created date


### Further Considerations
1. Should we include checks for custom fields or project-specific rules?
2. What is the allowed set of statuses and priorities for validation?
3. Should we flag issues with excessive time in a single status?