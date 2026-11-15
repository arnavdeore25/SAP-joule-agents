# Specification: financial-closing-escalation-agent-extension

> **Guidelines**: Read [guidelines.md](../guidelines.md) and [guidelines-agent-extension.md](../guidelines-agent-extension.md) before executing ANY tasks below. Follow all constraints described there throughout execution.

## Basic Setup

- [x] Read the project input (`product-requirements-document.md`, `intent.md`)
- [x] Confirm the base agent to extend:
  - **ordId:** `sap.agtcloass:agent:financial-closing-assistant:v1`
  - **version:** `1.0.0`
  - **Extension capability:** `default` (`capabilityId: default`, `instructionSupported: true`)
  - **Feature flags (pre-confirmed):** `enable_agent_extension_mcp_server = false`, `enable_agent_extension_n8n_hooks = false`
  - Tools and hooks are **out of scope** — instruction-only extension

## Feature Flags Verification

- [x] Re-run feature flag checks to confirm current state:
  ```bash
  jl feature-flags get enable_agent_extension_mcp_server
  jl feature-flags get enable_agent_extension_n8n_hooks
  ```
- [x] Confirm both return `false`; if either has changed to `true`, re-evaluate scope with the user before proceeding

## Extension Instructions — Escalation Rule Engine

The extension instruction must implement all three escalation rules, the consolidated summary format, currency handling, and read-only guardrails. The instruction is injected via the `default` capability's `instruction` field in `extension.yaml`.

### REQ-01: Closing Data Retrieval Instructions

- [x] Write instructions directing the agent to retrieve, at the start of any escalation analysis request:
  - All closing tasks for the active period-end close cycle, including: task reference/ID, completion status, scheduled completion time, and official period-end deadline
  - All closing documents with associated posting errors, including: document reference, error detail, original amount, and original currency
  - Task dependency relationships: for each closing task, which downstream tasks depend on it and their current status (not started / started / complete)
- [x] Write instructions specifying that all data retrieval uses the base agent's existing read-only tools — no write operations during data collection
- [x] Write fallback instructions: if any data category cannot be retrieved, the agent must note the gap explicitly in the escalation summary and proceed with the data it has (no silent failures)

### REQ-02: Critical Escalation Rule — Posting Errors on High-Value Documents

- [x] Write instructions for the Critical escalation check:
  - For each closing document with a posting error:
    - If the document currency is EUR: compare the amount directly against the €100,000 threshold
    - If the document currency is not EUR: convert the amount to EUR using the approved exchange rate available through the base agent's SAP S/4HANA data access
    - If no approved exchange rate is available for conversion: include the document in the summary as a "Conversion Unavailable – Manual Verification Required" item; do NOT exclude it silently
    - If the EUR amount is strictly greater than €100,000: classify the document as **Critical – Immediate Action Required**
    - If the EUR amount is exactly €100,000: do NOT classify as Critical (strict greater-than threshold)
- [x] Write instructions for the Critical issue output format — each entry must include:
  - Document reference
  - Error detail description
  - Original amount and currency
  - EUR-equivalent amount (with exchange rate applied, or "conversion unavailable" where applicable)
  - Recommended next step (e.g. "Contact the responsible accountant to resolve the posting error before period-end close")

### REQ-03: Urgent Escalation Rule — Imminent Period-End Deadline

- [x] Write instructions for the Urgent escalation check:
  - For each incomplete closing task:
    - Calculate the time remaining until the official period-end deadline (current timestamp vs. deadline timestamp)
    - If the remaining time is strictly less than four hours: classify the task as **Urgent – Deadline Imminent**
    - If the remaining time is exactly four hours or more: do NOT classify as Urgent
    - If the task is already complete: do NOT classify as Urgent regardless of remaining time
- [x] Write instructions for the Urgent issue output format — each entry must include:
  - Task reference/ID
  - Remaining time to deadline (expressed in hours and minutes, e.g. "2h 45m")
  - Official period-end deadline timestamp
  - Recommended next step (e.g. "Escalate to task owner immediately and verify resource availability to complete before deadline")

### REQ-04: Flag Escalation Rule — Overdue Tasks Actively Blocking Dependencies

- [x] Write instructions for the Flag escalation check:
  - For each closing task that has passed its scheduled completion time:
    - Check whether the task has at least one downstream dependent task that is currently in a "not started" state
    - A task qualifies as Flag **only if** it meets both conditions: (a) past scheduled completion time AND (b) at least one downstream task is blocked (status: not started) because of this task's incomplete state
    - If all dependent downstream tasks have already started or completed independently: do NOT classify as Flag (the blockage must be active, not historical)
    - If the overdue task has no downstream dependency relationships: do NOT classify as Flag under this rule
- [x] Write instructions for the Flag issue output format — each entry must include:
  - Overdue task reference/ID
  - Duration of the overdue period (e.g. "Overdue by 3h 20m")
  - List of downstream tasks actively blocked (task reference and current status for each)
  - Recommended next step (e.g. "Prioritize completion of this task to unblock downstream closing activities and prevent deadline breach")

### REQ-05: Consolidated Escalation Summary — Prioritized Output

- [x] Write instructions for generating the Financial Closing Escalation Summary:
  - The summary must be structured in the following section order: **Critical**, then **Urgent**, then **Flag**
  - Each section lists all identified issues in that category, each with: task/document reference, escalation category and reason, relevant amount/deadline/overdue duration, affected downstream dependencies (where applicable), and recommended next steps
  - If no issues are found in a given category: omit that category's section entirely (no empty sections)
  - If no issues are found in any category: output a single statement — "No escalation items identified for the current period-end close cycle."
  - The summary header must identify: the period-end close cycle date/reference, the timestamp of the analysis run, and a total count of issues by category (e.g. "Critical: 2 | Urgent: 1 | Flag: 3")

### REQ-06: Multi-Condition Detection

- [x] Write instructions specifying that a single task or document is evaluated against ALL three escalation rules independently
- [x] Write instructions that if a task or document qualifies under more than one rule, ALL applicable categories are reported for that item — it appears under each relevant section of the summary
- [x] Add an explicit example in the instructions: a document with a posting error >€100K that belongs to an incomplete task with <4h to deadline should appear under both Critical and Urgent

### REQ-07: Read-Only Advisory Mode Guardrails (Escalation Workflow)

- [x] Write explicit prohibitions in the instructions, scoped to the escalation workflow:
  - Never post, create, or modify financial documents
  - Never complete closing tasks or change their status
  - Never approve journal entries
  - Never modify closing schedules or deadline timestamps
  - Never perform any financial transaction
- [x] Write instructions clarifying that these restrictions apply exclusively to the escalation workflow; the base agent's existing capabilities (journal entry creation, accruals, clearing, analytics) are unaffected and must not be constrained by the escalation instructions
- [x] Write a default-safe fallback: if the agent encounters an ambiguous instruction during escalation analysis, it must default to read-only advisory behavior

### REQ-08: Preservation of Existing Capabilities

- [x] Write instructions that explicitly scope all escalation guidance to escalation-specific requests only
- [x] Ensure the escalation instructions do not include any language that would override, suppress, or interfere with the base agent's capabilities for journal entry creation, accruals processing, receivables/payables clearing, or financial analytics
- [x] Include a clarification statement in the instructions: "These instructions extend the agent's capabilities for financial closing escalation analysis only. All other capabilities of the Financial Closing Assistant remain active and unmodified."

### REQ-09: Boundary Condition and Accuracy Validation

- [x] Document the following mandatory test scenarios to be verified after the extension is deployed (record in a `test-scenarios.md` file alongside the extension):
  - **TC-01 (Critical – EUR):** Document with EUR posting error of €100,001 → must be classified Critical
  - **TC-02 (Critical – boundary):** Document with EUR posting error of exactly €100,000 → must NOT be classified Critical
  - **TC-03 (Critical – FX conversion):** Document with USD posting error; converted EUR equivalent exceeds €100,000 → must be classified Critical, EUR amount shown
  - **TC-04 (Critical – FX no rate):** Document with posting error in a currency with no approved exchange rate → must appear as "Conversion Unavailable – Manual Verification Required", NOT excluded
  - **TC-05 (Urgent – threshold):** Incomplete task with 3h 59m remaining → must be classified Urgent
  - **TC-06 (Urgent – boundary):** Incomplete task with exactly 4h 00m remaining → must NOT be classified Urgent
  - **TC-07 (Urgent – complete task):** Completed task with 1h remaining → must NOT be classified Urgent
  - **TC-08 (Flag – active blockage):** Overdue task with downstream task in "not started" status → must be classified Flag
  - **TC-09 (Flag – no active blockage):** Overdue task where all downstream tasks have already started → must NOT be classified Flag
  - **TC-10 (Flag – no dependencies):** Overdue task with no downstream dependency relationships → must NOT be classified Flag
  - **TC-11 (Multi-condition):** Document with posting error >€100K AND associated incomplete task with <4h remaining → must appear under both Critical AND Urgent
  - **TC-12 (Multi-condition):** Overdue task that is also incomplete with <4h to deadline → must appear under both Urgent AND Flag
  - **TC-13 (No issues):** Close cycle with no qualifying issues → summary must state "No escalation items identified"
  - **TC-14 (Read-only compliance):** Any escalation analysis run → zero financial record modifications must occur; verify via system audit log
  - **TC-15 (Partial data):** Analysis run where deadline data is missing for some tasks → summary delivered with explicit data gap noted, not silent failure
  - **TC-16 through TC-22 (Additional edge cases):** Multi-currency mix, multi-entity, compound all-three-rules, summary ordering, empty section omission, FX conversion boundary, missing dependency status
- [x] Confirm test scenarios cover all three escalation categories, boundary conditions, currency conversion, multi-condition detection, no-issue scenario, read-only compliance, and partial data fallback
- [x] Record expected results for all test scenarios in `test-scenarios.md`

## Extension File Generation

- [x] Run `setup-solution` skill from the **solution root** to create `solution.yaml` and register the extension asset; if `solution.yaml` already exists, only add the agent-extension entry — do NOT overwrite
- [x] Invoke the `create-agent-extension` skill from `assets/financial-closing-escalation-agent-extension/` to generate `extension.yaml` and `asset.yaml`:
  - Extension name: `financial-closing-escalation`
  - Target agent ordId: `sap.agtcloass:agent:financial-closing-assistant:v1`
  - Target agent version: `1.0.0`
  - Capability: `default` (capabilityId)
  - Include `instruction` field (instructionSupported: true)
  - Do NOT include `tools` section (enable_agent_extension_mcp_server = false)
  - Do NOT include `hooks` section (enable_agent_extension_n8n_hooks = false)
- [x] Populate `extension.yaml` `capabilityImplementations[0].instruction` with the full escalation instruction text derived from all requirement tasks above (REQ-01 through REQ-08 content)
- [x] Ensure `asset.yaml` `requires` references the base agent with:
  - `name: financial-closing-assistant`
  - `kind: agent`
  - `ordId: sap.agtcloass:agent:financial-closing-assistant:v1`
  - `version: "1.0.0"`

## Final Validation

- [x] Verify `assets/financial-closing-escalation-agent-extension/extension.yaml` exists and is well-formed YAML
- [x] Verify `assets/financial-closing-escalation-agent-extension/asset.yaml` exists and is well-formed YAML
- [x] Verify `extension.yaml` contains:
  - `agent.ordId: sap.agtcloass:agent:financial-closing-assistant:v1`
  - `capabilityImplementations[0].capabilityId: default`
  - `capabilityImplementations[0].instruction` is populated (non-empty)
  - No `tools` section (feature flag disabled)
  - No `hooks` section (feature flag disabled)
- [x] Verify `asset.yaml` contains:
  - `type: agent-extension`
  - `requires` entry with `kind: agent` referencing the base agent ordId and version
  - No MCP server or n8n workflow `requires` entries (none in scope)
- [x] Verify `solution.yaml` includes `./assets/financial-closing-escalation-agent-extension/asset.yaml` in the `assets:` list
- [x] Verify `test-scenarios.md` exists alongside the extension with all 20+ test scenarios and expected results documented
- [x] Confirm the instruction text implements all six content requirements: data retrieval (REQ-01), Critical rule with currency handling (REQ-02), Urgent rule (REQ-03), Flag rule with active-blockage condition (REQ-04), prioritized summary format (REQ-05), multi-condition detection (REQ-06), read-only guardrails scoped to escalation only (REQ-07), and capability preservation statement (REQ-08)
