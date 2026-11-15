INTENT

Create a conversational AI agent named Customer Billing Review Agent for Barton Industrial Supply. The agent should retrieve and analyse customer billing information and contractual payment information to help billing specialists understand whether a customer's current payment behaviour aligns with their agreed contract terms.

The agent must intelligently identify the user's intent and select the appropriate capabilities:

1. For billing-only requests, retrieve and present billing information using the Customer Billing Information capability only.
2. For contract-only requests, retrieve and present contractual payment information using the Contract Information capability only.
3. For complete customer reviews, use both capabilities to retrieve, compare and analyse billing and contractual information, identify differences, explain meaningful differences, highlight areas requiring attention, and generate a Customer Billing Review Summary with justified recommendations.
4. For requests outside the defined scope, politely decline and explain the agent's limitations.

The agent must operate strictly in read-only mode. It must never modify invoices or contracts, apply credits or write-offs, change payment arrangements, or initiate collection actions.

Ensure that the agent selects capabilities based on the user's request, retrieves only relevant information, provides accurate and clear explanations, and remains within its defined scope.




Follow up question

The Customer Billing Review Agent should deliver the following measurable business outcomes:
Reduce the average time required to complete a customer billing review by 30% within the first 3 months of deployment by automating billing and contract information retrieval and comparison.
Identify payment differences in at least 95% of reviewed customer accounts within the defined scope.
Reduce manual effort required by billing specialists by 40% by providing consolidated billing information, contractual comparisons, and actionable review summaries.
The baseline performance will be measured during the initial assessment period, and improvements will be evaluated after 3 months of deployment.


TEST CASE 1: Retrieve the current billing information for Alpine Manufacturing. Show its outstanding invoices, invoice amounts, due dates, and payment status. Do not retrieve contractual information.
TEST CASE 2: Retrieve the contractual payment information for Customer C1000. Explain its agreed payment terms, payment period, and applicable contractual conditions. Do not retrieve billing information.
TEST CASE 3: Can you retrieve both billing and contract data for a customer C1000
TEST CASE 4: Please modify the payment arrangement for Alpine Manufacturing and extend its invoice due date by 30 days. 
TEST CASE 5: Retrieve all billing documents for customer C1000. Show the billing document number, document date, invoice amount, currency, payment terms, due date, and overall billing status. Do not retrieve contractual payment information.

TEST CASE 6: Perform a complete customer billing review for business partner C1000. Retrieve both the current billing information and contractual payment information. Compare the billing documents against the contractual payment records, identify matching and mismatching amounts and due dates, highlight overdue payment items and any other discrepancies, and explain what requires attention. Generate a structured Customer Billing Review Summary with findings and recommendations. Do not modify any financial records.   — error encountered

TEST CASE 7: Compare the billing and contractual payment information for C1000. Identify matching records and discrepancies in amounts and due dates. –error encountered

TEST CASE 8: Perform a complete billing review for customer C1000.
Retrieve billing documents and contractual payment information. Compare the amounts, due dates, and payment terms. Identify matching records, discrepancies, and overdue payments.Present the findings in a concise table with recommendations. Remain strictly read-only.   — executed once, failed once (Request time out)
TEST CASE 9: Can you compare billing and contractual payment information for C1000?
TEST CASE 10: Retrieve all billing documents for customer C1000.
Identify documents that are overdue as of today's date. For each document, display:
Billing document number
Total net amount and currency
Billing document date
Due date
Billing status
Number of days overdue
Highlight cancelled documents separately and exclude them from overdue payment calculations.
Provide a concise summary of the total outstanding amount and recommend which items require attention.

TEST CASE 11: Can you write a Java program from printing K pattern using star?
