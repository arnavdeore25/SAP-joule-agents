"""Unit tests for contract accounting payment MCP tool usage."""
import pytest
from unittest.mock import AsyncMock

# Tool names from the contract accounting payment MCP server
LIST_CONTRACT_TOOL = "list_contracctgbuspartnerpayment_for_sap_self"
GET_CONTRACT_TOOL = "get_contracctgbuspartnerpayment_for_sap_self"
COUNT_CONTRACT_TOOL = "count_contracctgbuspartnerpayment_for_sap_self"
LIST_CONTRACT_ENHANCED_TOOL = "list_cabppaytenhcdfordspcrcy_for_sap_self"


@pytest.fixture
def mock_contract_payment_response():
    return {
        "value": [
            {
                "BusinessPartner": "C1000",
                "ContractAccount": "CA-0001",
                "PaymentTerms": "NT30",
                "DueCalculationBaseDate": "2024-09-15",
                "CashDiscount1Days": "10",
                "CashDiscount1Percent": "2.000",
                "NetPaymentDays": "30",
                "PaymentMethod": "T",
                "PaymentBlockingReason": "",
            }
        ]
    }


@pytest.fixture
def mock_contract_single_response():
    return {
        "BusinessPartner": "C1000",
        "ContractAccount": "CA-0001",
        "PaymentTerms": "NT30",
        "NetPaymentDays": "30",
        "PaymentMethod": "T",
    }


def test_contract_list_tool_name():
    """Verify the contract list tool name matches expected format."""
    assert LIST_CONTRACT_TOOL.startswith("list_")
    assert "contracctg" in LIST_CONTRACT_TOOL.lower()


def test_contract_get_tool_name():
    """Verify the contract get tool name matches expected format."""
    assert GET_CONTRACT_TOOL.startswith("get_")
    assert "contracctg" in GET_CONTRACT_TOOL.lower()


def test_contract_count_tool_name():
    """Verify the contract count tool name matches expected format."""
    assert COUNT_CONTRACT_TOOL.startswith("count_")
    assert "contracctg" in COUNT_CONTRACT_TOOL.lower()


def test_contract_list_response_structure(mock_contract_payment_response):
    """Verify contract payment list response has expected structure."""
    assert "value" in mock_contract_payment_response
    items = mock_contract_payment_response["value"]
    assert len(items) >= 1
    item = items[0]
    assert "BusinessPartner" in item
    assert "PaymentTerms" in item
    assert "NetPaymentDays" in item


def test_contract_response_payment_terms(mock_contract_payment_response):
    """Verify contract payment response contains payment term details."""
    item = mock_contract_payment_response["value"][0]
    assert item["PaymentTerms"] == "NT30"
    assert item["NetPaymentDays"] == "30"
    assert item["BusinessPartner"] == "C1000"


def test_contract_single_response_structure(mock_contract_single_response):
    """Verify single contract payment record has expected structure."""
    assert "BusinessPartner" in mock_contract_single_response
    assert "PaymentTerms" in mock_contract_single_response
    assert "NetPaymentDays" in mock_contract_single_response


@pytest.mark.asyncio
async def test_contract_tool_invocation():
    """Test that contract payment tool can be invoked with correct parameters."""
    mock_tool = AsyncMock()
    mock_tool.name = LIST_CONTRACT_TOOL
    mock_tool.arun = AsyncMock(
        return_value='{"value": [{"BusinessPartner": "C1000", "PaymentTerms": "NT30", "NetPaymentDays": "30"}]}'
    )

    result = await mock_tool.arun(
        input={"$filter": "BusinessPartner eq 'C1000'", "$top": "100"}
    )
    assert "BusinessPartner" in result
    assert "PaymentTerms" in result
    mock_tool.arun.assert_called_once()
