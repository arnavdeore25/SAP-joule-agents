# Financial Closing Escalation Extension — Test Scenarios

**Purpose:** Validate escalation rule coverage (target: 100%) and classification accuracy (target: ≥95%) as defined in REQ-09 of the Product Requirements Document.

**Minimum scenarios required:** 20  
**Total scenarios defined:** 22

---

## Test Scenario Reference

| ID | Category | Description | Expected Result |
|---|---|---|---|
| TC-01 | Critical – EUR | Document with EUR posting error of €100,001 | Classified as Critical; EUR amount shown |
| TC-02 | Critical – boundary | Document with EUR posting error of exactly €100,000 | NOT classified as Critical (strict greater-than) |
| TC-03 | Critical – FX conversion | Document in USD; converted EUR equivalent = €105,000 | Classified as Critical; EUR amount and exchange rate shown |
| TC-04 | Critical – FX no rate | Document in a currency with no approved exchange rate | Appears as "Conversion Unavailable – Manual Verification Required"; NOT excluded |
| TC-05 | Urgent – threshold | Incomplete task with 3h 59m remaining to deadline | Classified as Urgent; time remaining shown as "3h 59m" |
| TC-06 | Urgent – boundary | Incomplete task with exactly 4h 00m remaining | NOT classified as Urgent |
| TC-07 | Urgent – complete task | Completed task with 1h remaining to deadline | NOT classified as Urgent |
| TC-08 | Flag – active blockage | Overdue task; one downstream task has status "not started" | Classified as Flag; blocked task listed |
| TC-09 | Flag – no active blockage | Overdue task; all downstream tasks have already started | NOT classified as Flag |
| TC-10 | Flag – no dependencies | Overdue task with no downstream dependency relationships | NOT classified as Flag |
| TC-11 | Multi-condition: Critical + Urgent | Document with posting error >€100K; associated task has <4h to deadline | Document appears under Critical AND associated task appears under Urgent |
| TC-12 | Multi-condition: Urgent + Flag | Incomplete task with <4h to deadline AND overdue, blocking an unstarted downstream task | Task appears under both Urgent AND Flag |
| TC-13 | No issues | Close cycle with no qualifying issues in any category | Summary states "No escalation items identified for the current period-end close cycle." |
| TC-14 | Read-only compliance | Execute any escalation analysis run | Zero financial record modifications occur; verified via system audit log |
| TC-15 | Partial data – missing deadlines | Analysis run where deadline data is missing for some tasks | Summary delivered with explicit data gap noted; no silent failure |
| TC-16 | Multi-currency mix | Close cycle with EUR, USD, GBP, and JPY documents; some above threshold after conversion | Correct Critical classifications for all converted amounts above €100K; correct exclusions for those at or below |
| TC-17 | Multi-entity close | Close cycle spanning two company codes; each with independent tasks and deadlines | Escalation rules applied correctly per task/document regardless of company code |
| TC-18 | Compound – all three rules | One task qualifies under all three rules (overdue, <4h to deadline, actively blocking downstream) | Task appears under Critical (if it has an associated high-value error), Urgent, and Flag; or Urgent and Flag if no associated document error |
| TC-19 | Summary section ordering | Close cycle with Critical, Urgent, and Flag issues present | Summary sections appear in order: Critical, Urgent, Flag — no reordering |
| TC-20 | Empty section omission | Close cycle with only Urgent issues; no Critical or Flag issues | Summary contains only the Urgent section; Critical and Flag sections are not present |
| TC-21 | FX conversion – boundary | Document in USD; converted EUR equivalent = exactly €100,000 | NOT classified as Critical (boundary applies after conversion) |
| TC-22 | Partial data – missing dependency status | Analysis run where some downstream task statuses are unavailable | Flag rule can only be evaluated for tasks with known dependency statuses; items with missing status flagged for manual verification |

---

## Boundary Condition Summary

| Rule | Condition | Expected Classification |
|---|---|---|
| Critical | EUR amount > €100,000 | Critical |
| Critical | EUR amount = €100,000 | NOT Critical |
| Critical | EUR amount < €100,000 | NOT Critical |
| Critical | Foreign currency, converted EUR > €100,000 | Critical (with conversion shown) |
| Critical | Foreign currency, converted EUR = €100,000 | NOT Critical |
| Critical | Foreign currency, no approved exchange rate | Conversion Unavailable – Manual Verification Required |
| Urgent | Time remaining < 4h (incomplete task) | Urgent |
| Urgent | Time remaining = 4h (incomplete task) | NOT Urgent |
| Urgent | Time remaining > 4h (incomplete task) | NOT Urgent |
| Urgent | Task complete, any time remaining | NOT Urgent |
| Flag | Overdue + downstream task "not started" | Flag |
| Flag | Overdue + all downstream tasks "started" or "complete" | NOT Flag |
| Flag | Overdue + no downstream dependencies | NOT Flag |
| Flag | Not overdue + downstream task "not started" | NOT Flag |

---

## Read-Only Compliance Verification

**TC-14 procedure:**
1. Execute a full escalation analysis run against a period-end close cycle with qualifying issues.
2. After the run completes, query the SAP S/4HANA financial audit log and SAP Advanced Financial Closing change log.
3. Verify that zero document postings, task completions, journal entry approvals, schedule modifications, or any other write operations were recorded during the analysis run.
4. Test passes only if zero modifications are detected.

---

## Accuracy Measurement

Classification accuracy is measured as:

```
Accuracy = (Number of correctly classified scenarios) / (Total scenarios evaluated) × 100%
```

Target: ≥ 95% (at least 21 of 22 scenarios must produce the expected result).

Coverage target: 100% — all 22 scenarios must be executed during each validation cycle.
