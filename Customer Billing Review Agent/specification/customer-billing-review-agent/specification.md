# Specification: customer-billing-review-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` from the solution root before starting implementation.
- [x] Bootstrap agent code in `assets/customer-billing-review-agent/` using instructions from the `sap-agent-bootstrap` section. Invoke from inside `assets/customer-billing-review-agent/`, using copy commands — do NOT create files manually.
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`.

---

## Runtime Skills

The agent has a well-defined capability routing requirement with conditional multi-step logic (billing-only, contract-only, full review, out-of-scope handling). Create the following runtime skill:

- [ ] Create `assets/customer-billing-review-agent/app/skills/billing-review/SKILL.md` with:
  - YAML frontmatter: `name: billing-review`, `description: Customer billing review workflow — routes between billing-only, contract-only, full comparative review, and out-of-scope handling based on user intent`
  - **Intent Detection section**: rules for identifying billing-only vs. contract-only vs. full review vs. out-of-scope requests.
  - **Billing-Only Mode**: retrieve billing documents for the customer, present in clear structured format.
  - **Contract-Only Mode**: retrieve contractual payment information for the customer, present in clear structured format.
  - **Full Review Mode**: retrieve both billing and contract data, compare, identify and explain meaningful differences, highlight areas requiring attention, generate a Customer Billing Review Summary (customer overview, billing findings, contract findings, identified differences, areas requiring attention, justified recommendations).
  - **Out-of-Scope Handling**: politely decline, explain the agent's defined capabilities (billing retrieval, contract retrieval, full review), and invite the user to ask within scope.
  - **Read-Only Constraint**: explicit rule — the agent MUST NEVER modify invoices, contracts, or payment arrangements; MUST NEVER apply credits, write-offs, or initiate collection actions. If asked to do so, decline politely.

---

## Project-Specific Tasks

### Agent System Prompt & Persona

- [ ] Open `assets/customer-billing-review-agent/app/agent.py`.
- [ ] Set the agent name to `Customer Billing Review Agent` and the company context to `Barton Industrial Supply`.
- [ ] In the `@prompt_section` / `get_system_prompt()` body, include:
  - Agent role: assists billing specialists at Barton Industrial Supply in reviewing customer billing and contractual payment information.
  - Capability modes: billing-only retrieval, contract-only retrieval, full comparative review.
  - Read-only enforcement: NEVER modify invoices, contracts, or payment arrangements; NEVER apply credits or write-offs; NEVER initiate collection actions.
  - Instruction to use tools to retrieve live data only — never fabricate or invent data.
  - Instruction to load the `billing-review` skill for all billing and contract review tasks.
  - Page size limit: when calling tools that support pagination, always set the page size parameter (`top`, `$top`, etc.) to a maximum of 100 items.
  - Error handling: relay tool errors verbatim without adding suggestions.

### Billing Document Capability

- [ ] The agent must use MCP tools to retrieve billing documents from SAP S/4HANA:
  - API: `CE_BILLINGDOCUMENT_0001` (Billing Document OData API, v1)
  - API spec file: `specification/customer-billing-review-agent/api-specs/CE_BILLINGDOCUMENT_0001.edmx`
  - Operation: read-only retrieval of billing documents and invoice history for a given customer.
  - Resources in scope: `BillingDocument`, `BillingDocumentItem`
- [ ] Implement agent logic to:
  - Accept a customer identifier from the billing specialist.
  - Call the billing document MCP tool to retrieve billing documents for that customer.
  - Present results in a structured, human-readable format (invoice date, invoice number, amount, payment status).

### Contract Accounting Payment Capability

- [ ] The agent must use MCP tools to retrieve contractual payment terms from SAP S/4HANA:
  - API: `API_CABUSPARTPAYMENT_0002` (Contract Accounting Business Partner Payment, v2)
  - API spec file: `specification/customer-billing-review-agent/api-specs/API_CABUSPARTPAYMENT_0002.edmx`
  - Operation: read-only retrieval of contract accounting payment information for a given customer.
  - Resources in scope: `BusPartPayment`, `BusPartPaymentItem`
- [ ] Implement agent logic to:
  - Accept a customer identifier from the billing specialist.
  - Call the contract payment MCP tool to retrieve contractual payment terms for that customer.
  - Present results in a structured, human-readable format (payment terms, due dates, schedules).

### Intent-Based Capability Routing

- [ ] Implement routing logic in the agent (via the `billing-review` skill) so that:
  - Billing-only requests → call only the billing document MCP tool, present billing findings.
  - Contract-only requests → call only the contract payment MCP tool, present contract findings.
  - Full review requests → call both tools, perform comparative analysis, identify differences, generate Customer Billing Review Summary.
  - Out-of-scope requests → politely decline with explanation of agent capabilities.

### Customer Billing Review Summary

- [ ] For full review mode, the agent must produce a structured Customer Billing Review Summary containing:
  1. **Customer Overview**: customer identifier and context.
  2. **Billing Findings**: summary of retrieved billing documents (invoice dates, amounts, payment statuses).
  3. **Contract Findings**: summary of contractual payment terms.
  4. **Identified Differences**: clear explanation of any meaningful differences between actual payment behavior and contracted terms.
  5. **Areas Requiring Attention**: flagged items that deviate significantly or require specialist action.
  6. **Recommendations**: justified recommendations based solely on retrieved data (read-only — no actions taken).

### Read-Only Enforcement

- [ ] Add an explicit guardrail in the system prompt and in the `billing-review` skill: if the user requests any write operation (modify invoice, apply credit, change payment terms, initiate collection), the agent MUST decline and explain it operates in read-only mode.

---

## MCP Tool Integration (Path A — API Spec Files)

MCP tool scope for billing document API:
```
MCP API: sap.s4:apiResource:CE_BILLINGDOCUMENT_0001:v1
MCP tool scope: read-only
Resources in scope: BillingDocument, BillingDocumentItem
```

MCP tool scope for contract accounting payment API:
```
MCP API: sap.s4:apiResource:API_CABUSPARTPAYMENT_0002:v2
MCP tool scope: read-only
Resources in scope: BusPartPayment, BusPartPaymentItem
```

- [ ] Invoke `mcp-translation-file` skill for `specification/customer-billing-review-agent/api-specs/CE_BILLINGDOCUMENT_0001.edmx` (OData, ORD ID: `sap.s4:apiResource:CE_BILLINGDOCUMENT_0001:v1`, read-only, resources: BillingDocument, BillingDocumentItem).
- [ ] Invoke `mcp-translation-file` skill for `specification/customer-billing-review-agent/api-specs/API_CABUSPARTPAYMENT_0002.edmx` (OData, ORD ID: `sap.s4:apiResource:API_CABUSPARTPAYMENT_0002:v2`, read-only, resources: BusPartPayment, BusPartPaymentItem).
- [ ] Invoke `setup-solution` skill to create MCP server assets for both translation files.
- [ ] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module (bootstrap-generated) — never import directly from `sap_cloud_sdk.agentgateway`, never create direct HTTP clients for SAP APIs.
- [ ] Add MCP server dependencies to `asset.yaml` under `requires` — one entry per MCP server, using the exact ORD IDs from the generated MCP server assets (read from `asset.yaml` of each MCP server after generation with `grep '^ordId:' assets/<mcp-server-asset-name>/asset.yaml`).
- [ ] Generate `mcp-mock.json` using the `mcp-mock-config` skill after both MCP servers are set up.

---

## Business Instrumentation

- [ ] Implement business step instrumentation for each milestone from the PRD using structured logging (pattern: `[MILESTONE_ID].[achieved|missed]: [description]`) and OpenTelemetry custom spans:
  - **M1** — Customer Identified: `M1.achieved: customer identified and confirmed in scope` / `M1.missed: customer identifier not found or out of scope`
  - **M2** — Billing Data Retrieved: `M2.achieved: billing documents retrieved successfully` / `M2.missed: billing document retrieval failed or returned no results`
  - **M3** — Contract Terms Retrieved: `M3.achieved: contract payment terms retrieved successfully` / `M3.missed: contract terms retrieval failed or returned no results`
  - **M4** — Comparison and Analysis Completed: `M4.achieved: billing vs. contract comparison completed` / `M4.missed: comparison could not be completed due to missing or incomplete data`
  - **M5** — Customer Billing Review Summary Generated: `M5.achieved: customer billing review summary generated and delivered` / `M5.missed: summary generation failed or was incomplete`
- [ ] Use the decorator form (`@tracer.start_as_current_span("name")`) on regular async methods. For `stream()`, extract business logic into a plain async helper `_run_agent()` and instrument that method — never use `with tracer.start_as_current_span(...)` inside an async generator.
- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`.

---

## Testing

- [ ] `conftest.py` only sets `IBD_TESTING=true` — the fixture monkey-patches `mcp_tools.get_mcp_tools` before any agent code runs.
- [ ] Write unit tests in `assets/customer-billing-review-agent/tests/`:
  - One test for the billing document retrieval tool call.
  - One test for the contract payment retrieval tool call.
  - One test for intent routing (billing-only, contract-only, full review, out-of-scope).
  - Run each immediately after writing.
- [ ] Write one integration test executing the full agent flow (customer identification → billing retrieval → contract retrieval → comparison → summary) with mocked LLM responses and mocked MCP tools.
- [ ] Run `pytest` from `assets/customer-billing-review-agent/` (no args) — if coverage < 70%, add tests until threshold met.
- [ ] Run `pytest` again from `assets/customer-billing-review-agent/` (no args) to generate final `test_report.json`.
- [ ] Verify `test_report.json` exists in `assets/customer-billing-review-agent/` — if not, run pytest again until it does.
