INTENT

Extend the existing SAP Financial Closing Assistant for Stonebridge Equipment Group by introducing company-specific financial closing escalation rules while preserving all existing assistant capabilities and functionality.
The extended assistant should retrieve and analyze relevant financial closing tasks, closing documents, posting errors, scheduled completion times, period-end deadlines, and task dependencies.
Identify and classify critical closing issues using the following rules:
Critical – Immediate Action Required: Identify closing documents with posting errors involving amounts exceeding €100,000. Highlight the affected document, error details, and amount.
Urgent – Deadline Imminent: Identify incomplete closing tasks with fewer than four hours remaining before the official period-end closing deadline. Highlight the task reference, remaining time, and deadline.
Flag – Schedule Risk: Identify closing tasks that have passed their scheduled completion time and are blocking downstream task dependencies. Highlight the overdue task, delay, and affected dependencies.
Generate a consolidated Financial Closing Escalation Summary, prioritizing issues in the following order: Critical, Urgent, and Flag.
For each identified issue, provide:
Task or closing document reference.
Escalation category and reason.
Relevant amount, deadline, or overdue duration.
Affected downstream dependencies, where applicable.
Recommended next steps for the finance team.
If multiple escalation rules apply to the same task or document, identify and report all applicable conditions.
The assistant must operate strictly in read-only mode. It must never post financial documents, complete tasks, approve journal entries, modify closing schedules, or perform any financial transactions. All recommendations must remain advisory.
The extension must preserve the existing Financial Closing Assistant capabilities and aim to reduce the time required to identify and escalate critical closing issues from two hours to 15 minutes.

Enhancement of Intent (Follow up question)
Strengthen read-only restrictions
Your summary mentions read-only advisory mode, which is good. Explicitly add:
Never post financial documents.
Never complete closing tasks.
Never approve journal entries.
Never modify closing schedules.

Preserve existing functionality 


Enhancement of PRD (Follow up question)
The PRD looks good overall. Please make the following refinements:
Clarify that strict read-only restrictions apply specifically to the new escalation workflow, while preserving all existing Financial Closing Assistant capabilities.
For Flag escalation, ensure that an overdue task must actually be blocking at least one downstream task, rather than simply having a dependency relationship.
Clarify the performance targets: 15 minutes is the overall business process target, while 3 minutes is the assistant's response-time target.
Add currency handling for the €100,000 threshold. Convert foreign-currency amounts to EUR using an approved exchange rate and flag missing conversion data for manual verification.
Define how escalation coverage and classification accuracy will be validated through test scenarios.
Keep the existing scope, three escalation rules, architecture, and read-only requirements unchanged otherwise. Please update the PRD accordingly.
