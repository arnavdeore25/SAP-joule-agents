# Financial Closing Escalation Extension – Stonebridge Equipment Group

Agent extension for the SAP Financial Closing Assistant that introduces company-specific escalation rules to accelerate critical issue identification during period-end closing.

## Business challenge

Stonebridge Equipment Group's finance team currently requires up to two hours to manually identify and escalate critical financial closing issues during each period-end close. The existing SAP Financial Closing Assistant handles core closing activities but does not apply company-specific escalation rules. The team needs an extension that automatically retrieves and analyzes closing tasks, closing documents, posting errors, scheduled completion times, period-end deadlines, and task dependencies — then classifies and prioritizes issues using three escalation rules:

- **Critical – Immediate Action Required:** Closing documents with posting errors involving amounts exceeding €100,000.
- **Urgent – Deadline Imminent:** Incomplete closing tasks with fewer than four hours remaining before the official period-end deadline.
- **Flag – Schedule Risk:** Closing tasks that have passed their scheduled completion time and are blocking downstream task dependencies.

The extension must operate strictly in read-only advisory mode, never posting documents, completing tasks, approving journal entries, modifying closing schedules, or performing any financial transactions. All existing Financial Closing Assistant capabilities must be fully preserved.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to identify & escalate critical closing issues | 2 hours | 15 minutes | Per period-end close | Financial Closing Escalation | user |
| Escalation Rule Coverage | — | 100% | Ongoing | All 3 escalation conditions | user |
| Escalation Classification Accuracy | — | ≥95% | Ongoing | Critical / Urgent / Flag classification | user |
| Read-Only Compliance | — | 100% (0 modifications) | Ongoing | Financial record integrity | user |
| Missed Critical Issues per close cycle | — | 0 | Per period-end close | Financial Closing Escalation | user |

## Key Milestones

- **Escalation rules defined:** All three escalation conditions (Critical, Urgent, Flag) are fully specified and confirmed with the finance team.
- **Extension instructions authored:** Extension instructions implementing all three rules are validated against the base agent's extension capability.
- **Escalation summary validated:** Consolidated escalation summary output is reviewed against realistic period-end scenarios covering all three rule types.
- **Read-only compliance confirmed:** Zero financial transactions or record modifications occur during any test run.
- **Existing functionality preserved:** All base Financial Closing Assistant capabilities remain operational and unaffected.

## Business Architecture (RBA)

### End-to-End Process

Record to Report

### Process Hierarchy

```
Record to Report
└── Record to Report
    └── Perform accounting and financial close (BPS-413_002)
        └── Perform financial closing
        └── Monitor closing task status and deadlines
        └── Identify and escalate posting errors
        └── Manage period-end task dependencies
```

### Summary

The business challenge maps directly to the "Perform accounting and financial close" sub-process (BPS-413_002) within the Record to Report end-to-end process. The escalation rules address monitoring, error detection, and dependency management activities that are part of standard financial close execution.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|---|---|---|---|---|---|---|---|---|
| Retrieve and analyze closing tasks with deadlines | SAP Advanced Financial Closing, SAP S/4HANA Cloud | `sap.s4:apiResource:CE_STATUTORYREPORTINGTASK_0001:v1` | — | — | — | — | No | Statutory Reporting Task API available; no MCP server found |
| Identify posting errors on high-value documents (>€100K) | SAP S/4HANA Cloud | `sap.s4:apiResource:API_JOURNALENTRYITEMBASIC_SRV:v1` | — | — | — | — | No | Journal Entry Item Read API available; no MCP server found |
| Read financial document data for error context | SAP S/4HANA Cloud | `sap.s4:apiResource:C_TRIALBALANCE_CDS:v1` | — | — | — | — | No | Trial Balance Read API available; no MCP server found |
| Read ledger and period data | SAP S/4HANA Cloud | `sap.s4:apiResource:API_LEDGER_SRV:v1` | — | — | — | — | No | Ledger Read API available; no MCP server found |
| Company-specific escalation rule engine (3 rules) | None | — | — | — | — | — | Yes | No standard product applies all three rules; custom instructions required |
| Consolidated escalation summary with prioritization | None | — | — | — | — | — | Yes | No out-of-box prioritized escalation report; custom instruction output required |
| Scheduling service for AFC tasks | SAP Advanced Financial Closing | `sap.afc:apiResource:SSPIV1:v1` | — | — | — | — | Maybe | API marked unavailable in tenant; base agent may provide access |
| Read-only advisory enforcement | SAP Advanced Financial Closing | — | — | — | — | — | No | Enforced via extension instruction constraints |

### Key findings

- The base Financial Closing Assistant (`sap.agtcloass:agent:financial-closing-assistant:v1`, v1.0.0) is registered as extensible and supports instructions additions (`instructionSupported: true`), making it the correct target.
- MCP tool additions are supported by the agent but the `enable_agent_extension_mcp_server` feature flag is `false`; tools capability is therefore disabled and the extension relies on enhanced instructions only.
- n8n hooks are supported by the agent but the `enable_agent_extension_n8n_hooks` feature flag is `false`; hooks are excluded from scope.
- The three escalation rules (Critical, Urgent, Flag) have no standard SAP product equivalent and must be implemented as custom instructions within the extension.
- Available APIs (Statutory Reporting Task, Journal Entry Item Read, Trial Balance Read, Ledger Read) provide the data foundation; the base agent's existing tool access covers these data sources.
- The SAP Advanced Financial Closing scheduling API (`sap.afc:apiResource:SSPIV1:v1`) is marked unavailable in the tenant but may be accessible via the base agent's existing integrations.

## Recommendations

### Extend Financial Closing Assistant with Company-Specific Escalation Rules

#### Executive Summary

Add escalation instruction layer to existing Financial Closing Assistant.

#### Recommended Solution

Extend the SAP Financial Closing Assistant (`sap.agtcloass:agent:financial-closing-assistant:v1`) with a custom instruction set that implements Stonebridge Equipment Group's three escalation rules. The extension uses the agent's `instructionSupported` capability to inject detailed guidance for retrieving closing data, evaluating each escalation condition, and generating a prioritized consolidation escalation summary. The extension is strictly advisory and read-only, preserving all base agent capabilities.

#### Problem Statement

Finance controllers at Stonebridge Equipment Group spend up to two hours per period-end close manually scanning tasks, documents, and error logs to identify issues requiring escalation. This delay risks missed deadlines and unresolved posting errors impacting financial close quality.

#### Affected User Roles

- Finance Controller
- Period-End Close Manager
- Financial Closing Team Lead

#### Important factors

##### Reduces manual effort through automation
The extension automates the identification and classification of all closing issues matching the three escalation rules, reducing a 2-hour manual process to approximately 15 minutes.

##### Strictly advisory and read-only
The extension enforces hard read-only constraints: it never posts documents, completes tasks, approves journal entries, modifies schedules, or performs transactions. All outputs are recommendations only.

##### Preserves existing capabilities
By extending rather than replacing the base agent, all existing Financial Closing Assistant capabilities (journal entry, accruals, clearing, insights) remain fully operational.

##### Multi-condition escalation detection
If multiple escalation rules apply to the same task or document, all applicable conditions are reported — preventing underreporting of compound issues.

#### Potential risks

##### Scheduling API availability
The SAP AFC Scheduling Service Provider Interface is marked as unavailable in the tenant. If the base agent cannot provide access to scheduling data, deadline-based (Urgent) escalations may require alternative data sourcing.

##### Instruction-only scope limitation
Because MCP tools are disabled, the extension cannot add new API connections. It relies entirely on the base agent's existing data access, which may limit the depth of escalation data available.

#### Recommended solution category

Agent Extension

#### Intent fit
93%
