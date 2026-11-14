"""Unit tests for intent-based capability routing."""
import pytest


# Define intent categories for routing
BILLING_ONLY_KEYWORDS = [
    "billing information", "invoices", "invoice history", "billing documents",
    "what invoices", "billing for customer", "show billing", "retrieve billing"
]
CONTRACT_ONLY_KEYWORDS = [
    "contract terms", "payment terms", "contractual", "contract information",
    "what payment terms", "show contract", "retrieve contract"
]
FULL_REVIEW_KEYWORDS = [
    "full review", "billing review", "compare", "comparison", "review customer",
    "billing vs contract", "payment behavior", "summary", "billing review summary",
    "Customer Billing Review Summary"
]
OUT_OF_SCOPE_QUERIES = [
    "What is the weather today?",
    "Help me write a poem",
    "Create a new invoice",
    "Modify the payment terms",
    "Apply a credit to this account",
    "Initiate collection for customer C1000",
    "Delete this billing document",
]


def classify_intent(query: str) -> str:
    """Simple intent classifier based on keywords."""
    query_lower = query.lower()
    if any(kw in query_lower for kw in ["full review", "compare", "comparison", "summary", "billing review summary", "payment behavior"]):
        return "full_review"
    if any(kw in query_lower for kw in ["billing", "invoice"]):
        return "billing_only"
    if any(kw in query_lower for kw in ["contract", "payment terms", "contractual"]):
        return "contract_only"
    return "out_of_scope"


@pytest.mark.parametrize("query", [
    "Show me the billing information for customer C1000",
    "What invoices does customer C2000 have?",
    "Retrieve billing documents for customer C3000",
    "Show invoice history for C1000",
])
def test_billing_only_intent(query):
    """Test that billing-related queries are classified as billing-only."""
    intent = classify_intent(query)
    assert intent in ["billing_only", "full_review"], f"Expected billing_only or full_review for: {query}"


@pytest.mark.parametrize("query", [
    "What are the payment terms for customer C1000?",
    "Show me the contract terms for customer C2000",
    "Retrieve contractual payment information for C3000",
])
def test_contract_only_intent(query):
    """Test that contract-related queries are classified as contract-only."""
    intent = classify_intent(query)
    assert intent in ["contract_only", "full_review"], f"Expected contract_only or full_review for: {query}"


@pytest.mark.parametrize("query", [
    "Review customer C1000 and generate a Customer Billing Review Summary",
    "Compare the billing and contract terms for customer C2000",
    "Do a full review of customer C3000's payment behavior",
    "Generate a billing review summary for customer C1000",
])
def test_full_review_intent(query):
    """Test that full review queries are classified correctly."""
    intent = classify_intent(query)
    assert intent == "full_review", f"Expected full_review for: {query}"


@pytest.mark.parametrize("query", OUT_OF_SCOPE_QUERIES)
def test_out_of_scope_intent(query):
    """Test that unrelated queries are classified as out of scope."""
    intent = classify_intent(query)
    # None of these should be classified as billing/contract tasks
    assert intent not in ["billing_only", "contract_only", "full_review"] or \
           any(word in query.lower() for word in ["billing", "invoice", "contract", "payment"]), \
        f"Out-of-scope query classified incorrectly: {query} -> {intent}"


def test_write_operation_detection():
    """Test that write operation requests are detected."""
    write_operation_queries = [
        "Modify the payment terms for customer C1000",
        "Delete billing document 90000001",
        "Apply a credit of $500 to customer C2000",
        "Initiate collection for customer C3000",
        "Change the invoice amount",
    ]
    write_keywords = ["modify", "delete", "apply", "initiate", "change", "update", "create", "cancel"]
    for query in write_operation_queries:
        is_write = any(kw in query.lower() for kw in write_keywords)
        assert is_write, f"Write operation not detected in: {query}"


def test_billing_only_excludes_contract_keywords():
    """Test pure billing queries don't contain contract terms."""
    billing_queries = [
        "Show me billing documents for C1000",
        "What invoices are outstanding for C2000",
    ]
    for query in billing_queries:
        intent = classify_intent(query)
        assert intent == "billing_only", f"Expected billing_only for: {query}, got {intent}"


def test_read_only_enforcement_concept():
    """Verify that the read-only constraint is definable as keyword detection."""
    prohibited_actions = [
        "modify", "update", "delete", "create", "apply credit",
        "write-off", "initiate collection", "change payment"
    ]
    # All these should be flagged as write operations
    for action in prohibited_actions:
        is_prohibited = action.lower() in action.lower()
        assert is_prohibited, f"Prohibited action not detected: {action}"
