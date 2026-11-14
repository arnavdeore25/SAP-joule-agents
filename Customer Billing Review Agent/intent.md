# Customer Billing Review Agent — Barton Industrial Supply

## Business challenge

Billing specialists at Barton Industrial Supply need a conversational AI agent that retrieves and analyzes customer billing information alongside contractual payment terms, enabling them to quickly determine whether a customer's payment behavior aligns with their agreed contract. The agent must intelligently select between billing-only, contract-only, or full comparative review modes based on the user's request, and must operate strictly in read-only mode.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Average time to complete customer billing review | To be measured | -30% reduction | 3 months post-deployment | Billing & Contract Information Retrieval | user |
| Payment difference identification rate | To be measured | ≥95% of reviewed accounts | 3 months post-deployment | Billing vs. Contract Comparison | user |
| Manual effort reduction for billing specialists | To be measured | -40% reduction | 3 months post-deployment | Consolidated Billing Review & Summary Generation | user |

## Key Milestones

1. **Customer Identified** — Billing specialist provides a customer identifier; agent confirms the customer exists and is in scope.
2. **Billing Data Retrieved** — Agent successfully fetches billing documents and invoice history for the customer.
3. **Contract Terms Retrieved** — Agent successfully fetches contractual payment terms for the customer.
4. **Comparison & Analysis Completed** — Agent identifies differences between actual payment behavior and contracted terms, flags areas of concern.
5. **Customer Billing Review Summary Generated** — Agent produces a structured summary with findings and justified recommendations for the billing specialist.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash Standard B2B

### Process Hierarchy

```
Lead to Cash Standard B2B (E2E)
└── Invoice to Cash (physical products and services)
    └── Manage customer invoices (physical products and services) (BPS-363_002)
        └── Prepare billing data
```

### Summary

The agent maps to the Invoice to Cash phase of Lead to Cash, specifically the sub-process for managing customer invoices — covering billing data retrieval, contract payment term comparison, and compliance review for accounts receivable specialists.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Retrieve customer billing documents and invoice history | SAP S/4HANA Cloud — Customer Invoice Processing (SC1129/SC5331), Billing Data Management | `sap.s4:apiResource:CE_BILLINGDOCUMENT_0001:v1` | — | — | — | — | Maybe | No MCP server found; custom tool wrapper required |
| Retrieve subsequent billing documents | SAP S/4HANA Cloud — Billing Data Management | `sap.s4:apiResource:API_SUBSQNT_BILLG_DOC_SBI_SRV:v1` | — | — | — | — | Maybe | No MCP server found; custom tool wrapper required |
| Retrieve contractual payment terms per customer | SAP S/4HANA Cloud — Contract Accounting | `sap.s4:apiResource:API_CABUSPARTPAYMENT_0002:v2` | — | — | — | — | Maybe | No MCP server found; custom tool wrapper required |
| Compare billing behavior vs. contract terms | SAP S/4HANA + SAP Analytics Cloud (optional) | — | — | — | — | — | Yes | Agent reasoning layer handles comparison; no standard asset covers automated diff analysis |
| Generate Customer Billing Review Summary | Custom agent capability | — | — | — | — | — | Yes | LLM-generated structured summary with recommendations — no standard SAP asset covers this |
| Customer payment data (Payment Terms, Open Items) | — | — | — | — | — | — | Yes | `Payment Terms`, `Accounts Receivable Open Items`, `Customer Payment` APIs are unavailable in landscape |

### Key findings

- SAP S/4HANA Cloud is the primary standard asset covering billing document management and customer invoice processing.
- Three relevant APIs are available (`CE_BILLINGDOCUMENT_0001`, `API_SUBSQNT_BILLG_DOC_SBI_SRV`, `API_CABUSPARTPAYMENT_0002`), but none have pre-built MCP servers — custom OData tool wrappers are required.
- Several highly relevant APIs (Customer Payment, Payment Terms, Accounts Receivable Open Items) are marked unavailable in the customer landscape — the agent scope must be constrained accordingly.
- The comparative analysis and Customer Billing Review Summary are genuine gaps — no standard SAP asset covers automated contract-vs-billing diff analysis; this is delivered via the agent's reasoning layer.
- The agent must operate strictly in read-only mode (GET operations only); no invoice modification, credit application, or collection actions.

## Recommendations

### Customer Billing Review Agent — Python AI Agent (A2A)

#### Executive Summary

Pro-code Python A2A agent with targeted SAP S/4HANA API tool calls for read-only billing and contract review.

#### Recommended Solution

A conversational Python AI agent built on the A2A protocol, deployed on SAP BTP. The agent exposes three capability modes: billing-only retrieval, contract-only retrieval, and full comparative review. It calls SAP S/4HANA OData APIs directly as MCP tools (custom wrappers) to retrieve billing documents and contract accounting payment data. For out-of-scope requests, the agent politely declines.

#### Recommended solution category

AI Agent

#### Intent fit
95%
