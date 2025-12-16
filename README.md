## Plan: Data Hygiene Validations for Jira Issues

This plan outlines complex, conditional data hygiene checks to ensure the Jira issues dataset is clean and ready for reporting. These validations focus on business logic and field dependencies.

### Steps
1. Check that `assignee_id` is not empty for issues of type "Story" or "Bug".
2. Ensure "Resolved" or "Closed" issues have a non-null `resolved_date`.
3. Validate that "In Progress" issues have a non-null `assignee_id`.
4. Confirm that "Epic" issues do not have a parent issue set.
5. Ensure "Sub-task" issues have a valid, non-null parent issue key.
6. Check that "Priority" is set for all issues except "Epics".
7. Flag issues where `created_date` is after `resolved_date`.
8. Identify issues with missing or invalid "status" values (not in allowed set).
9. Detect issues with duplicate summaries within the same project.
10. Ensure "Due Date" is not before "Created Date" for any issue.

### Further Considerations
1. Should we include checks for custom fields or project-specific rules?
2. What is the allowed set of statuses and priorities for validation?
3. Should we flag issues with excessive time in a single status?