# SAP Joule Agents

A collection of AI agents and agent extensions developed using **SAP Joule Studio**, focused on solving practical enterprise business problems through conversational AI, intelligent automation and agent-based workflows.

This repository currently contains two SAP Joule projects:

- **Customer Billing Review Agent** – A conversational agent that retrieves customer billing and contractual payment information, compares records, identifies discrepancies and generates review summaries.
- **Financial Closing Assistant Extension** – An extension of SAP's existing Financial Closing Assistant that introduces company-specific financial closing escalation rules while preserving the existing assistant capabilities.

The projects include their business intent, product requirements, Joule Studio assets, specifications, configuration files and supporting documentation.

---

## Table of Contents

- [Projects Overview](#projects-overview)
- [1. Customer Billing Review Agent](#1-customer-billing-review-agent)
- [2. Financial Closing Assistant Extension](#2-financial-closing-assistant-extension)
- [Repository Structure](#repository-structure)
- [Technologies and Concepts](#technologies-and-concepts)
- [Governance and Safety](#governance-and-safety)
- [Getting Started](#getting-started)
- [Author](#author)

---

## Projects Overview

| Project | Business Domain | Agent Type | Primary Objective |
|---|---|---|---|
| Customer Billing Review Agent | Invoice to Cash | Conversational Agent | Compare customer billing records with contractual payment terms |
| Financial Closing Assistant Extension | Record to Report | Agent Extension | Identify, classify and prioritise financial closing issues |

---

## 1. Customer Billing Review Agent

**Business:** Barton Industrial Supply  
**Domain:** Finance / Billing Operations  
**Platform:** SAP Joule Studio

### Business Problem

Billing specialists often need to retrieve customer billing documents and contractual payment information from different sources and manually compare them.

This process takes time and makes it difficult to identify payment discrepancies, overdue invoices and differences between actual billing behaviour and agreed contract terms.

### Agent Capabilities

The Customer Billing Review Agent understands the user's request and selects the appropriate capability.

| Request Type | Agent Behaviour |
|---|---|
| Billing-only request | Retrieves and presents customer billing information |
| Contract-only request | Retrieves and presents contractual payment information |
| Complete billing review | Retrieves both datasets, compares records and identifies discrepancies |
| Out-of-scope request | Politely declines and explains its limitations |

### Key Features

- Customer billing information retrieval.
- Contractual payment information retrieval.
- Comparison of billing amounts and due dates.
- Identification of matching and mismatching records.
- Detection of overdue payments.
- Structured Customer Billing Review Summary.
- Recommendations based on retrieved information.
- Intent-based capability selection.

### Business Outcomes

The project defines the following target outcomes:

- Reduce average customer billing review time by **30% within three months**.
- Identify payment differences in at least **95% of reviewed customer accounts**.
- Reduce manual effort for billing specialists by **40%**.

### Read-Only Restrictions

The agent operates strictly in read-only mode. It cannot modify invoices or contracts, apply credits or write-offs, change payment arrangements or initiate collection actions.

### Documentation

- [Agent Documentation, Prompts and Test Cases](Customer%20Billing%20Review%20Agent/Customer_Billing_Review_Agent_Documentation.md)
- [Intent](Customer%20Billing%20Review%20Agent/intent.md)
- [Product Requirements Document](Customer%20Billing%20Review%20Agent/product-requirements-document.md)
- [Assets](Customer%20Billing%20Review%20Agent/assets/)
- [Specifications](Customer%20Billing%20Review%20Agent/specification/)

---

## 2. Financial Closing Assistant Extension

**Business:** Stonebridge Equipment Group  
**Domain:** Record to Report / Financial Close  
**Platform:** SAP Joule Studio  
**Extension Type:** Existing SAP Agent Extension

### Business Problem

During period-end closing, finance teams need to identify critical posting errors, incomplete tasks approaching their deadlines and overdue tasks that are blocking other activities.

Manually reviewing these issues can delay escalation and affect the efficiency of the financial closing process.

The objective of this project is to extend the existing SAP Financial Closing Assistant with company-specific escalation logic.

### Escalation Rules

The extension introduces three escalation categories.

| Priority | Category | Business Rule |
|---|---|---|
| 1 | Critical | Closing documents with posting errors involving amounts greater than €100,000 |
| 2 | Urgent | Incomplete closing tasks with fewer than four hours remaining before the official period-end deadline |
| 3 | Flag | Overdue closing tasks that are actively blocking downstream task dependencies |

### Key Features

- Retrieval and analysis of relevant financial closing information.
- Detection of high-value posting errors.
- Identification of incomplete tasks approaching deadlines.
- Detection of overdue tasks actively blocking downstream activities.
- Foreign-currency conversion to EUR using approved exchange rates.
- Identification of cases requiring manual verification.
- Multiple escalation conditions reported for the same item.
- Consolidated Financial Closing Escalation Summary.
- Priority-based reporting: Critical → Urgent → Flag.
- Recommended next steps for the finance team.

### Read-Only Advisory Mode

The new escalation workflow is strictly read-only.

It must never:

- Post financial documents.
- Complete closing tasks.
- Approve journal entries.
- Modify closing schedules.
- Perform financial transactions.

The extension preserves the existing Financial Closing Assistant capabilities. Its read-only restrictions apply specifically to the new escalation workflow.

### Architecture Approach

The extension builds on the existing SAP Financial Closing Assistant rather than creating a completely independent agent.

It uses the supported instruction-extension capability to introduce company-specific escalation rules and relies on the base assistant's existing integrations and data access.

No additional MCP servers or n8n hooks are introduced in this release.

### Business Outcomes

The project defines the following targets:

| Metric | Target |
|---|---|
| Overall business process time to identify and escalate issues | Reduce from 2 hours to 15 minutes |
| Assistant response time | Within 3 minutes |
| Escalation rule coverage | 100% |
| Classification accuracy | At least 95% |
| Read-only compliance | 100% |

These are intended project targets, not verified production results.

### Documentation

- [Extension Documentation](Extend%20the%20Financial%20Closing%20Assistant/Finanaial_Closing_Assistant_Documentation_Extension.md)
- [Extension Intent](Extend%20the%20Financial%20Closing%20Assistant/intent.md)
- [Product Requirements Document](Extend%20the%20Financial%20Closing%20Assistant/product-requirements-document.md)
- [Assets](Extend%20the%20Financial%20Closing%20Assistant/assets/)
- [Specifications](Extend%20the%20Financial%20Closing%20Assistant/specification/)

---

## Repository Structure

```text
SAP-joule-agents/
│
├── Customer Billing Review Agent/
│   ├── assets/
│   ├── specification/
│   ├── Customer_Billing_Review_Agent_Documentation.md
│   ├── intent.md
│   ├── product-requirements-document.md
│   └── solution.yaml
│
├── Extend the Financial Closing Assistant/
│   ├── assets/
│   ├── specification/
│   ├── Finanaial_Closing_Assistant_Documentation_Extension.md
│   ├── intent.md
│   ├── product-requirements-document.md
│   └── solution.yaml
│
├── .gitattributes
├── .gitignore
└── README.md
```

Each project is maintained in its own directory to keep its assets, specifications, requirements and supporting documentation organised.

---

## Technologies and Concepts

The projects involve the following SAP and AI concepts:

- SAP Joule Studio
- SAP Joule Agents and Agent Extensions
- Conversational AI and Autonomous Agents
- Intent-based capability routing
- Agent instructions and business rules
- Enterprise business process automation
- Read-only data retrieval and advisory workflows
- Agent testing and validation
- AI governance and responsible AI
- SAP solution configuration

---

## Governance and Safety

Responsible AI usage and business guardrails are important aspects of both projects.

The implementations emphasise:

- Clearly defined agent responsibilities and scope.
- Intent-based capability selection.
- Controlled access to business information.
- Read-only restrictions where required.
- Recommendations supported by retrieved business data.
- Human review for decisions and actions requiring business authorisation.
- Test scenarios for validating expected agent behaviour.

The objective is to build useful enterprise AI solutions without compromising business processes, financial data integrity or organisational controls.

---

## Author

**Arnav Deore**

MCA Student | SAP Technology Enthusiast | AI Agent Development

- GitHub: [@arnavdeore25](https://github.com/arnavdeore25)
- Repository: [SAP Joule Agents](https://github.com/arnavdeore25/SAP-joule-agents)

---

*Exploring enterprise AI through SAP Joule Agents, business process automation and intelligent agent extensions.*
