# Product Requirements Document (PRD)

**Title:** Financial Closing Escalation Extension – Stonebridge Equipment Group  
**Date:** 2026-11-14  
**Owner:** Stonebridge Equipment Group – Finance  
**Solution Category:** Agent Extension

---

## Product Purpose & Value Proposition

**Elevator Pitch:**  
During period-end close, the Stonebridge finance team spends up to two hours manually scanning closing tasks, documents, and error logs to identify issues that need escalation. This extension automates that process — applying three company-specific escalation rules to deliver a prioritized summary in under 15 minutes, while preserving all existing Financial Closing Assistant capabilities.

**Business Need:**  
The existing SAP Financial Closing Assistant handles core closing activities but does not apply company-specific escalation logic. Issues — such as posting errors on high-value documents, tasks approaching deadlines, or schedule blockages — are discovered manually, increasing risk of missed deadlines and unresolved errors during the close cycle.

**Expected Value:**  
The extension reduces critical issue identification from 2 hours to 15 minutes per close cycle. It ensures 100% coverage of the three escalation conditions, targets ≥95% classification accuracy, and enforces zero unauthorized financial modifications — directly improving close quality and team responsiveness.

**Product Objectives (Prioritized):**
1. Automatically identify and classify all closing issues matching the three escalation rules (Critical, Urgent, Flag) during each period-end close cycle.
2. Generate a consolidated, prioritized Financial Closing Escalation Summary with actionable context for the finance team.
3. Enforce strict read-only advisory mode — never perform any financial transaction or record modification.
4. Preserve all existing Financial Closing Assistant capabilities without interruption.

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to identify & escalate critical closing issues | 2 hours | 15 minutes | Per period-end close | Financial Closing Escalation | user |
| Escalation Rule Coverage | — | 100% | Ongoing | All 3 escalation conditions | user |
| Escalation Classification Accuracy | — | ≥95% | Ongoing | Critical / Urgent / Flag classification | user |
| Read-Only Compliance | — | 100% (0 modifications) | Ongoing | Financial record integrity | user |
| Missed Critical Issues per close cycle | — | 0 | Per period-end close | Financial Closing Escalation | user |

---

## User Profiles & Personas

### Primary Persona: Maria – Finance Controller

Maria is a 38-year-old Finance Controller at Stonebridge Equipment Group, responsible for the integrity of the period-end close. She manages 60–80 closing tasks per cycle and reviews financial documents for posting errors. During close, she works under significant time pressure — late errors can delay reporting, trigger audit findings, or cause restatements. She is proficient with SAP but frustrated by the need to manually aggregate status from multiple screens and systems. She needs fast, reliable visibility into what is broken and what needs her attention right now.

### Secondary Persona: Thomas – Period-End Close Manager

Thomas is a 45-year-old Period-End Close Manager who oversees the closing schedule for all entities within Stonebridge. He tracks task completion against the official period-end deadline and manages escalations upward to finance leadership. His biggest pain point is being caught off-guard by overdue tasks that silently block downstream work. He needs a tool that surfaces scheduling risks early, before they cascade into a missed close deadline.

### Other User Types

- **Financial Closing Team Lead:** Coordinates day-to-day execution of closing tasks, receives escalation summaries to direct team action.
- **SAP System Administrator:** Manages the base Financial Closing Assistant and the extension deployment.

---

## User Goals & Tasks

### For Maria – Finance Controller:

**Goals:**
- Identify all posting errors on high-value documents within minutes of starting the escalation review.
- Know immediately which tasks are at risk of missing the period-end deadline.

**Key Tasks:**
- Trigger the Financial Closing Escalation Summary via the Financial Closing Assistant.
- Review Critical escalations (posting errors >€100K) with document reference and error detail.
- Review Urgent escalations (tasks <4h to deadline) with task reference and time remaining.
- Forward the consolidated summary to the close manager or relevant task owners.

### For Thomas – Period-End Close Manager:

**Goals:**
- Identify tasks that are overdue and blocking downstream dependencies before they affect the close deadline.
- Receive a prioritized, consolidated view of all active escalations.

**Key Tasks:**
- Request the escalation summary and review Flag escalations (overdue tasks with dependency impact).
- Use the recommended next steps to direct team resources to unblocked critical paths.

---

## Product Principles

1. **Read-Only for Escalation, Always:** The escalation workflow introduced by this extension is strictly read-only and advisory — it never posts, completes, approves, or modifies anything. This constraint applies exclusively to the new escalation logic and does not restrict the base Financial Closing Assistant's existing write-capable operations (journal entry, accruals, clearing).
2. **Preserve First:** The extension augments the base Financial Closing Assistant. No existing capability is modified, constrained, or replaced.
3. **Prioritized Clarity:** The escalation summary is structured to deliver the most critical information first (Critical → Urgent → Flag), enabling fast decisions under time pressure.
4. **Complete Coverage:** If multiple escalation rules apply to the same task or document, all are reported. Underreporting is never acceptable.
5. **Actionable Output:** Every escalation must include a recommended next step. Identification without guidance is insufficient.

---

## Business Context

**Current State:**  
Finance controllers and close managers manually review closing dashboards, error logs, and task lists across SAP Advanced Financial Closing and SAP S/4HANA to identify issues. This process is fragmented, time-consuming (up to 2 hours per cycle), and reliant on individual knowledge of escalation thresholds. Issues can be missed or identified too late to resolve before the period-end deadline.

**Strategic Alignment:**  
This extension supports Stonebridge Equipment Group's objective to accelerate and de-risk the financial close process. It is consistent with SAP's Record to Report best practices for financial close automation and positions the finance team to handle close cycles with greater confidence and less manual overhead.

**Success Criteria:**  
See the Business Metrics section above.

---

## Goals and Non-Goals

### Goals (In Scope)

- Retrieve and analyze closing tasks, closing documents, posting errors, scheduled completion times, period-end deadlines, and task dependencies using the base agent's existing data access.
- Apply three escalation rules and classify each identified issue as Critical, Urgent, or Flag.
- Detect and report all applicable escalation categories for a single task or document (multi-condition detection).
- Generate a consolidated Financial Closing Escalation Summary, prioritized Critical → Urgent → Flag.
- For each issue, provide: task/document reference, escalation category and reason, relevant amount/deadline/duration, affected downstream dependencies, and recommended next steps.
- Enforce strict read-only advisory mode throughout all operations.
- Preserve all existing Financial Closing Assistant capabilities without modification.

### Non-Goals (Out of Scope)

- Posting financial documents, creating journal entries, or performing any financial transaction.
- Completing closing tasks, approving journal entries, or modifying closing schedules.
- Adding new API connections or MCP tool integrations (feature flag disabled in current environment).
- Configuring n8n hooks or automated pre/post-processing workflows.
- Replacing or modifying the base Financial Closing Assistant's core logic.
- Predictive or forecasting capabilities (e.g., predicting future deadline breaches).

---

## Requirements

### Must-Have Requirements

**REQ-01: Closing Data Retrieval**

- **Problem to Solve:** The finance team cannot escalate issues it cannot see. The extension must gather all relevant closing data before applying escalation rules.
- **User Story:** As a Finance Controller, I need the assistant to retrieve closing tasks, closing documents, posting errors, scheduled completion times, period-end deadlines, and task dependencies so that I have a complete data picture for escalation analysis.
- **Acceptance Criteria:**
  - Given a period-end close cycle is active, when the escalation summary is requested, then the assistant retrieves all closing tasks with their status, scheduled times, and deadlines.
  - Given a period-end close cycle is active, when the escalation summary is requested, then the assistant retrieves closing documents with associated posting errors and amounts.
  - Given closing tasks exist, when the escalation summary is requested, then task dependencies (downstream relationships) are identified and carried into the analysis.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 1

**REQ-02: Critical Escalation – Posting Errors on High-Value Documents**

- **Problem to Solve:** Posting errors on large-value documents can cause material misstatements if not resolved before close. These must be surfaced immediately, regardless of the document's original currency.
- **User Story:** As a Finance Controller, I need the assistant to identify all closing documents with posting errors where the affected amount exceeds €100,000 (after EUR conversion where necessary) and classify them as Critical so that I can prioritize their resolution.
- **Acceptance Criteria:**
  - Given closing documents with posting errors exist, when the escalation analysis runs, then any document with a posting error and an EUR amount exceeding €100,000 is classified as Critical.
  - Given a document is denominated in EUR, then the stated amount is used directly for threshold comparison.
  - Given a document is denominated in a foreign currency, then the amount is converted to EUR using the approved exchange rate available through the base agent's data access before applying the threshold.
  - Given a foreign-currency document exists but no approved exchange rate is available for conversion, then the document is flagged for manual verification and included in the summary with a note stating the conversion could not be completed; it is NOT silently excluded.
  - Given a Critical issue is identified, then the output includes: the document reference, the specific error detail, the original amount and currency, and the EUR-equivalent amount used for threshold comparison.
  - Given a document's EUR-equivalent amount is exactly €100,000, then it is NOT classified as Critical (the threshold is strictly greater than €100,000).
- **Maps to Objective:** Objectives 1 and 2
- **Priority Rank:** 2

**REQ-03: Urgent Escalation – Imminent Period-End Deadline**

- **Problem to Solve:** Incomplete tasks that are close to the period-end deadline need immediate human attention to avoid a missed close.
- **User Story:** As a Period-End Close Manager, I need the assistant to identify incomplete closing tasks with fewer than four hours remaining before the official period-end closing deadline and classify them as Urgent so that I can mobilize resources in time.
- **Acceptance Criteria:**
  - Given incomplete closing tasks exist with a known period-end deadline, when the escalation analysis runs, then any incomplete task with fewer than four hours remaining before the deadline is classified as Urgent.
  - Given an Urgent issue is identified, then the output includes: the task reference, the remaining time to deadline (in hours and minutes), and the official deadline timestamp.
  - Given a task is complete, then it is NOT classified as Urgent regardless of the time remaining.
- **Maps to Objective:** Objectives 1 and 2
- **Priority Rank:** 3

**REQ-04: Flag Escalation – Overdue Tasks Actively Blocking Dependencies**

- **Problem to Solve:** Overdue tasks that block downstream work silently hold up the entire close schedule. These must be visible before they cause cascading delays.
- **User Story:** As a Period-End Close Manager, I need the assistant to identify closing tasks that have passed their scheduled completion time and are actively preventing at least one downstream task from starting or completing so that I can unblock the critical path before the deadline is breached.
- **Acceptance Criteria:**
  - Given closing tasks with scheduled completion times exist, when the escalation analysis runs, then a task is classified as Flag only if it is both (a) past its scheduled completion time AND (b) directly blocking at least one downstream task that cannot proceed until this task is complete.
  - Given a task is overdue but all dependent downstream tasks have already started or completed independently, then it is NOT classified as Flag (the dependency must be actively blocking, not merely recorded).
  - Given a task is overdue but has no downstream dependency relationships defined, then it is NOT classified as Flag under this rule (it may still qualify under other rules).
  - Given a Flag issue is identified, then the output includes: the overdue task reference, the duration of the overdue period, and the list of downstream tasks that are actively blocked by this overdue task.
- **Maps to Objective:** Objectives 1 and 2
- **Priority Rank:** 4

**REQ-05: Consolidated Escalation Summary with Prioritized Output**

- **Problem to Solve:** Individual issue detection is only useful if the finance team receives a clear, prioritized summary that enables fast decision-making.
- **User Story:** As a Finance Controller or Close Manager, I need a consolidated Financial Closing Escalation Summary that lists all identified issues in order of priority (Critical first, then Urgent, then Flag) so that I can act on the most important items first.
- **Acceptance Criteria:**
  - Given one or more escalation issues are identified, when the summary is generated, then issues are listed in the order: Critical, Urgent, Flag.
  - Given an issue is identified, then the summary entry includes: task or document reference, escalation category and reason, relevant amount/deadline/overdue duration, affected downstream dependencies (where applicable), and recommended next steps.
  - Given no issues are identified in a given category, then that category is omitted from the summary (no empty sections).
  - Given no issues are identified in any category, then the summary clearly states that no escalation items were found.
- **Maps to Objective:** Objectives 1 and 2
- **Priority Rank:** 5

**REQ-06: Multi-Condition Escalation Detection**

- **Problem to Solve:** A single task or document may satisfy more than one escalation rule simultaneously. Reporting only one condition would lead to underreporting.
- **User Story:** As a Finance Controller, I need the assistant to report all applicable escalation categories for a given task or document so that I have the complete escalation picture without missing any condition.
- **Acceptance Criteria:**
  - Given a closing document qualifies as both Critical (posting error >€100K) and Urgent (appears in an incomplete task with <4h to deadline), then both conditions are reported for that item in the escalation summary.
  - Given a closing task qualifies as both Urgent and Flag, then both conditions are reported.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 6

**REQ-07: Strict Read-Only Advisory Mode for the Escalation Workflow**

- **Problem to Solve:** The escalation workflow introduced by this extension must never interfere with financial records or closing processes. All escalation outputs must be advisory. The base Financial Closing Assistant's existing write-capable capabilities (journal entry creation, accruals, clearing) are unaffected by this constraint.
- **User Story:** As a Finance System Administrator, I need the escalation extension to be strictly read-only so that, within the escalation workflow, no financial document is posted, no task is completed, no journal entry is approved, no schedule is modified, and no financial transaction is performed.
- **Acceptance Criteria:**
  - Given any escalation scenario, when the assistant processes the escalation rules, then no write operation, posting, approval, completion, or schedule modification is performed as part of the escalation workflow.
  - Given the escalation summary is delivered, then it is presented as advisory recommendations, not executed actions.
  - Given an edge case or ambiguous instruction within the escalation workflow, then the assistant defaults to read-only and advisory behavior.
  - Given a user invokes a base agent capability outside the escalation workflow (e.g., journal entry creation), then that capability operates normally and is not restricted by the escalation read-only constraint.
- **Maps to Objective:** Objective 3
- **Priority Rank:** 7

**REQ-08: Preservation of Existing Financial Closing Assistant Capabilities**

- **Problem to Solve:** The extension must not degrade or disable any existing capability of the base Financial Closing Assistant.
- **User Story:** As a Finance Controller, I need all existing Financial Closing Assistant capabilities — including journal entry creation, accruals processing, clearing, and analytics — to remain fully available after the extension is deployed.
- **Acceptance Criteria:**
  - Given the extension is deployed, when a user invokes any base agent capability (journal entry, accruals, clearing, insights), then it operates identically to its pre-extension behavior.
  - Given the extension adds instructions, then these instructions are scoped to escalation analysis and do not conflict with or override base agent instructions.
- **Maps to Objective:** Objective 4
- **Priority Rank:** 8

**REQ-09: Escalation Coverage and Classification Accuracy Validation**

- **Problem to Solve:** The business metrics target 100% escalation rule coverage and ≥95% classification accuracy. There must be a defined, repeatable method to verify these targets are being met.
- **User Story:** As a Finance Controller, I need confidence that the assistant correctly identifies all qualifying issues and classifies them accurately so that I can rely on the escalation summary without manual double-checking.
- **Acceptance Criteria:**
  - **Coverage validation:** A set of test scenarios must be defined covering all three escalation rules, including boundary conditions (e.g., a document at exactly €100,000, a task at exactly 4 hours to deadline, an overdue task with no active downstream blocker). For each scenario, the assistant's output is compared against the expected result. 100% coverage is achieved when all qualifying test cases produce an escalation entry.
  - **Classification accuracy validation:** A set of at minimum 20 diverse test scenarios must be defined, spanning all three escalation categories (Critical, Urgent, Flag), multi-condition cases, no-escalation cases, and edge cases (foreign-currency amounts requiring conversion, missing exchange rate data, tasks with dependency records but no active blockage). Accuracy is measured as the ratio of correctly classified scenarios to total scenarios. The target is ≥95%.
  - **Boundary condition tests must include:**
    - Document with EUR amount of exactly €100,000 → NOT Critical.
    - Document with EUR amount of €100,001 → Critical.
    - Foreign-currency document where converted EUR amount exceeds €100,000 → Critical (with conversion shown).
    - Foreign-currency document with no exchange rate available → flagged for manual verification, not excluded.
    - Incomplete task with exactly 4 hours remaining → Urgent.
    - Incomplete task with 4 hours and 1 minute remaining → NOT Urgent.
    - Overdue task with a dependency relationship but downstream task already started → NOT Flag.
    - Overdue task actively blocking an unstarted downstream task → Flag.
  - **Read-only compliance test:** At least one test scenario must verify that no write operation, posting, or modification occurs during escalation analysis. This test passes only if zero financial record changes are detected.
  - Test scenario definitions and expected results must be documented and available for each release.
- **Maps to Objective:** Objectives 1 and 2
- **Priority Rank:** 9

---

## Non-Functional Requirements

### Performance
- **Business Process Target:** The end-to-end time for a finance team member to identify and escalate critical closing issues must not exceed 15 minutes per period-end close cycle (inclusive of requesting the summary, reviewing it, and initiating escalation actions).
- **Assistant Response Target:** The escalation summary must be delivered within 3 minutes of the user's request under normal period-end close conditions. This covers data retrieval, rule evaluation, and summary generation by the assistant.
- **Throughput:** The extension must handle a full period-end closing task set (up to 200 tasks and 500 documents) within a single analysis run.

### Reliability
- **Fallback:** If closing data cannot be fully retrieved, the assistant must clearly state which data was unavailable and deliver a partial escalation summary for the data it could access, rather than failing silently.

### Explainability
- **Traceability:** Each escalation entry must reference the specific source data (document number, task ID, timestamp) that triggered the classification.
- **Uncertainty Communication:** If the assistant cannot determine whether a condition is met (e.g., deadline data is missing), it must flag the item as requiring manual verification rather than silently excluding it.

---

## Solution Architecture

**Architecture Overview:**  
The solution is an Agent Extension deployed against the SAP Financial Closing Assistant (`sap.agtcloass:agent:financial-closing-assistant:v1`). It uses the `instructionSupported` extension capability to inject escalation logic as structured instructions. No new API connections or MCP servers are added. The base agent's existing integrations with SAP Advanced Financial Closing and SAP S/4HANA provide data access.

**Key Components:**

- **Agent Extension (instruction layer):** Custom instructions implementing the three escalation rules, prioritization logic, summary format, and read-only guardrails.
- **Base Agent – Financial Closing Assistant:** Existing orchestrator that coordinates journal entry, accruals, clearing, and insights sub-agents. Provides data access to closing systems.
- **SAP Advanced Financial Closing:** Source of closing task data, schedules, deadlines, and task dependency information.
- **SAP S/4HANA Finance:** Source of financial documents, posting errors, journal entry items, and ledger data.

**Integration Points:**

- The extension integrates exclusively via the base agent's instruction extension capability — no direct API calls from the extension.
- The base agent's existing connections to SAP AFC and SAP S/4HANA are the data path.

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
- The extension targets the `default` capability of the Financial Closing Assistant, using `instructionSupported: true`.
- MCP tool additions and n8n hooks are out of scope for this release (feature flags disabled). The extension is designed so that tools could be added in a future release when the feature flag is enabled.

**Business Step Instrumentation:**
All five escalation business steps are instrumented with milestone log statements to support observability and monitoring of the extension's execution.

### Automation & Agent Behaviour

**Automation Level:** Rule-based within an autonomous agent framework (the base agent is autonomous; the escalation logic applied by the extension is deterministic rule evaluation).

**Actions the system performs without human approval:**
- Retrieves closing task data, document data, posting errors, deadlines, and dependencies.
- Evaluates each escalation condition against retrieved data.
- Generates and delivers the consolidated escalation summary.

**Actions that require human review or approval:**
- All recommended next steps (resolution actions) require explicit human decision and execution.
- No action in the extension's scope is self-executing.

**Model or engine used:** SAP Generative AI Hub (inherited from the base Financial Closing Assistant).

**Knowledge & data sources accessed:**
- SAP Advanced Financial Closing: closing tasks, schedules, deadlines, task dependencies, completion status.
- SAP S/4HANA Finance: closing documents, posting errors, journal entry items, ledger data, document amounts.

**Tools or connectors invoked:**
- Base agent's existing closing task retrieval tools (read-only).
- Base agent's existing financial document and journal entry retrieval tools (read-only).
- No additional tools or connectors introduced by this extension.

**Guardrails & fail-safes:**
- Within the escalation workflow: never post financial documents, create journal entries, or perform write operations of any kind. This read-only constraint is scoped to the escalation logic and does not restrict the base agent's existing write-capable operations.
- Within the escalation workflow: never complete closing tasks, approve journal entries, or modify closing schedules.
- All escalation outputs are advisory recommendations only.
- For foreign-currency documents: always convert to EUR using an approved exchange rate before applying the €100,000 threshold. If no approved rate is available, flag the document for manual verification — never exclude it silently.
- If closing data is incomplete or unavailable, deliver a partial summary with explicit data gaps noted.
- If an escalation condition cannot be evaluated due to missing data, flag the item for manual verification rather than silently excluding it.

---

## Milestones

### M1: Closing Data Retrieved

- **Description:** The assistant has successfully retrieved all relevant closing data required for escalation analysis: closing tasks with status, scheduled completion times, and deadlines; closing documents with posting errors and amounts; and task dependency relationships.
- **Achieved when:** All available closing data has been retrieved from the connected systems and is ready for rule evaluation.
- **Log on achievement:** `M1.achieved: closing data retrieved — tasks: {task_count}, documents: {doc_count}, errors: {error_count}`
- **Log on miss:** `M1.missed: closing data retrieval incomplete — {reason}; partial data available: {available_data_summary}`

### M2: Critical Issues Identified

- **Description:** The assistant has evaluated all closing documents for the Critical escalation condition (posting errors on documents with EUR amounts exceeding €100,000, with foreign-currency conversion applied where necessary).
- **Achieved when:** All documents with posting errors have been checked against the €100,000 threshold — including currency conversion for non-EUR documents — and Critical issues and manual-verification flags have been classified.
- **Log on achievement:** `M2.achieved: critical escalation check complete — critical issues found: {critical_count}, conversion flags: {conversion_flag_count}`
- **Log on miss:** `M2.missed: critical escalation check could not complete — {reason}`

### M3: Urgent Issues Identified

- **Description:** The assistant has evaluated all incomplete closing tasks for the Urgent escalation condition (fewer than four hours remaining before the period-end deadline).
- **Achieved when:** All incomplete tasks have been checked against the 4-hour deadline threshold and Urgent issues have been classified.
- **Log on achievement:** `M3.achieved: urgent escalation check complete — urgent issues found: {urgent_count}`
- **Log on miss:** `M3.missed: urgent escalation check could not complete — {reason}`

### M4: Flag Issues Identified

- **Description:** The assistant has evaluated all closing tasks for the Flag escalation condition (overdue tasks blocking downstream dependencies).
- **Achieved when:** All overdue tasks have been cross-referenced with their dependency relationships and Flag issues have been classified.
- **Log on achievement:** `M4.achieved: flag escalation check complete — flag issues found: {flag_count}`
- **Log on miss:** `M4.missed: flag escalation check could not complete — {reason}`

### M5: Escalation Summary Delivered

- **Description:** The consolidated Financial Closing Escalation Summary has been generated, prioritized (Critical → Urgent → Flag), and delivered to the user.
- **Achieved when:** The summary has been presented to the user with all identified issues, their escalation categories, relevant details, and recommended next steps.
- **Log on achievement:** `M5.achieved: escalation summary delivered — total issues: {total_count} (critical: {c}, urgent: {u}, flag: {f})`
- **Log on miss:** `M5.missed: escalation summary could not be generated — {reason}`

---

## Risks, Assumptions, and Dependencies

### Risks

- **AFC Scheduling API Availability:** The SAP AFC Scheduling Service Provider Interface is marked as unavailable in the tenant. If the base agent cannot access scheduling data through its existing integrations, Urgent and Flag escalation evaluations may be incomplete.
- **Instruction Scope Limitation:** Because MCP tools are disabled, the extension cannot establish new data connections. Escalation depth is bounded by what the base agent can already access.
- **Data Quality:** Escalation accuracy depends on the quality and completeness of closing task and document data in the connected systems. Missing scheduled completion times or amounts may reduce coverage.

### Assumptions

- The base Financial Closing Assistant has sufficient data access to closing tasks, documents, posting errors, deadlines, and dependencies to support all three escalation rules.
- The base agent's `instructionSupported` capability accepts detailed, structured escalation instructions of sufficient length to implement all three rules.
- The period-end deadline is a defined, retrievable data point accessible through the base agent.
- Task dependency relationships are maintained and retrievable within SAP Advanced Financial Closing, including the status of downstream tasks (started / not started / complete).
- Approved exchange rates for foreign-currency-to-EUR conversion are accessible through the base agent's existing SAP S/4HANA data access. Where rates are unavailable, the document is flagged for manual verification.

### Dependencies

- Availability and deployment of the base Financial Closing Assistant (`sap.agtcloass:agent:financial-closing-assistant:v1`, version 1.0.0).
- Access to SAP Advanced Financial Closing data (tasks, schedules, deadlines, dependencies) through the base agent.
- Access to SAP S/4HANA Finance data (documents, posting errors, amounts) through the base agent.

---

## Appendix

### Glossary

- **Period-End Close:** The process of finalizing all financial transactions for an accounting period before producing financial statements.
- **Critical Escalation:** A closing document with a posting error where the affected EUR amount exceeds €100,000. Foreign-currency amounts are converted to EUR using an approved exchange rate before the threshold is applied.
- **Urgent Escalation:** An incomplete closing task with fewer than four hours remaining before the official period-end deadline.
- **Flag Escalation:** A closing task that has passed its scheduled completion time and is actively blocking at least one downstream task that cannot proceed until this task is complete. A task with a dependency record where the downstream task has already started or completed does not qualify.
- **Consolidated Escalation Summary:** The prioritized report generated by the extension, listing all identified issues in order: Critical, Urgent, Flag.
- **Read-Only Advisory Mode:** An operational constraint under which the assistant only retrieves and analyzes data; it never performs any write, post, approve, or modify action.
- **Task Dependency:** A relationship in which one closing task cannot begin or complete until a prerequisite task is finished.
- **Approved Exchange Rate:** The official exchange rate maintained in SAP S/4HANA and used by Stonebridge Equipment Group for financial reporting purposes. Used for converting foreign-currency document amounts to EUR before applying the €100,000 Critical escalation threshold.
- **Active Blockage:** A state in which a downstream task cannot proceed because its prerequisite (an overdue task) has not been completed and the downstream task has not started or been independently resolved.

### References

- SAP Advanced Financial Closing: https://help.sap.com/docs/advanced-financial-closing
- SAP S/4HANA Financial Close: https://help.sap.com/docs/SAP_S4HANA_CLOUD/financials
- Record to Report – SAP Reference Business Architecture (BPS-413_002)
- Financial Closing Assistant base agent: `sap.agtcloass:agent:financial-closing-assistant:v1`
