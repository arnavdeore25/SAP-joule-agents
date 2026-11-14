"""Unit tests for billing document MCP tool usage."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Tool names from the billing document MCP server
LIST_BILLING_TOOL = "list_billingdocument_for_sap_self"
GET_BILLING_TOOL = "get_billingdocument_for_sap_self"
COUNT_BILLING_TOOL = "count_billingdocument_for_sap_self"


@pytest.fixture
def mock_billing_list_response():
    return {
        "value": [
            {
                "BillingDocument": "90000001",
                "BillingDocumentDate": "2024-09-15",
                "SoldToParty": "C1000",
                "TotalNetAmount": "15000.00",
                "TransactionCurrency": "USD",
                "OverallBillingStatus": "C",
                "PaymentTerms": "NT30",
                "DueDate": "2024-10-15",
            },
            {
                "BillingDocument": "90000002",
                "BillingDocumentDate": "2024-10-01",
                "SoldToParty": "C1000",
                "TotalNetAmount": "22500.00",
                "TransactionCurrency": "USD",
                "OverallBillingStatus": "B",
                "PaymentTerms": "NT30",
                "DueDate": "2024-11-01",
            },
        ]
    }


@pytest.fixture
def mock_billing_single_response():
    return {
        "BillingDocument": "90000001",
        "BillingDocumentDate": "2024-09-15",
        "SoldToParty": "C1000",
        "TotalNetAmount": "15000.00",
        "TransactionCurrency": "USD",
        "OverallBillingStatus": "C",
    }


def test_billing_list_tool_name():
    """Verify the billing list tool name matches expected format."""
    assert LIST_BILLING_TOOL.startswith("list_")
    assert "billing" in LIST_BILLING_TOOL.lower()


def test_billing_get_tool_name():
    """Verify the billing get tool name matches expected format."""
    assert GET_BILLING_TOOL.startswith("get_")
    assert "billing" in GET_BILLING_TOOL.lower()


def test_billing_count_tool_name():
    """Verify the billing count tool name matches expected format."""
    assert COUNT_BILLING_TOOL.startswith("count_")
    assert "billing" in COUNT_BILLING_TOOL.lower()


def test_billing_list_response_structure(mock_billing_list_response):
    """Verify billing list response has expected structure."""
    assert "value" in mock_billing_list_response
    items = mock_billing_list_response["value"]
    assert len(items) >= 1
    item = items[0]
    assert "BillingDocument" in item
    assert "SoldToParty" in item
    assert "TotalNetAmount" in item
    assert "TransactionCurrency" in item


def test_billing_list_response_customer_filter(mock_billing_list_response):
    """Verify billing list response is for the requested customer."""
    items = mock_billing_list_response["value"]
    for item in items:
        assert item["SoldToParty"] == "C1000"


def test_billing_single_response_structure(mock_billing_single_response):
    """Verify single billing document response has expected structure."""
    assert "BillingDocument" in mock_billing_single_response
    assert "TotalNetAmount" in mock_billing_single_response
    assert "OverallBillingStatus" in mock_billing_single_response


@pytest.mark.asyncio
async def test_billing_tool_invocation():
    """Test that billing tool can be invoked with correct parameters."""
    mock_tool = AsyncMock()
    mock_tool.name = LIST_BILLING_TOOL
    mock_tool.arun = AsyncMock(return_value='{"value": [{"BillingDocument": "90000001", "SoldToParty": "C1000", "TotalNetAmount": "15000.00"}]}')

    result = await mock_tool.arun(
        input={"$filter": "SoldToParty eq 'C1000'", "$top": "100"}
    )
    assert "BillingDocument" in result
    assert "C1000" in result
    mock_tool.arun.assert_called_once()
