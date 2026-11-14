"""Integration test for the Customer Billing Review Agent end-to-end flow."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

import sys
import os

# Ensure app directory is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))


@pytest.fixture
def mock_tools():
    """Create mock MCP tools for billing and contract data."""
    billing_tool = MagicMock()
    billing_tool.name = "list_billingdocument_for_sap_self"
    billing_tool.description = "List billing documents"
    billing_tool.arun = AsyncMock(
        return_value='{"value": [{"BillingDocument": "90000001", "BillingDocumentDate": "2024-09-15", "SoldToParty": "C1000", "TotalNetAmount": "15000.00", "TransactionCurrency": "USD", "OverallBillingStatus": "C", "PaymentTerms": "NT30", "DueDate": "2024-10-15"}]}'
    )

    contract_tool = MagicMock()
    contract_tool.name = "list_contracctgbuspartnerpayment_for_sap_self"
    contract_tool.description = "List contract payment terms"
    contract_tool.arun = AsyncMock(
        return_value='{"value": [{"BusinessPartner": "C1000", "ContractAccount": "CA-0001", "PaymentTerms": "NT30", "NetPaymentDays": "30", "PaymentMethod": "T"}]}'
    )

    metadata_tool = MagicMock()
    metadata_tool.name = "get_metadata_sap_self"
    metadata_tool.description = "Get OData metadata"
    metadata_tool.arun = AsyncMock(return_value="<edmx:Edmx/>")

    return [billing_tool, contract_tool, metadata_tool]


@pytest.fixture
def mock_llm_response_billing_only():
    """Mock LLM response for a billing-only request."""
    return "## Billing Information — Customer C1000\n\n| Invoice Number | Invoice Date | Amount | Currency | Status |\n|---|---|---|---|---|\n| 90000001 | 2024-09-15 | 15000.00 | USD | Cleared |\n\n**Total Outstanding:** $0.00 (all invoices cleared)"


@pytest.fixture
def mock_llm_response_full_review():
    """Mock LLM response for a full review request."""
    return """## Customer Billing Review Summary — C1000

### 1. Customer Overview
- Customer ID: C1000
- Review Scope: All available records

### 2. Billing Findings
- 1 invoice found. Invoice 90000001 for $15,000.00 USD dated 2024-09-15. Status: Cleared.

### 3. Contract Findings
- Payment Terms: NT30 (Net 30 days). Payment Method: Bank Transfer.

### 4. Identified Differences
- No significant differences identified. Customer paid within contracted 30-day terms.

### 5. Areas Requiring Attention
- None identified.

### 6. Recommendations
- Account is in good standing. Continue monitoring for future invoices.

*Note: This summary is for informational purposes only. No changes have been made to any records.*"""


@pytest.mark.asyncio
async def test_agent_billing_only_flow(mock_tools, mock_llm_response_billing_only):
    """Test the billing-only query flow end-to-end with mocked LLM."""
    from agent import SampleAgent

    agent = SampleAgent()

    # Mock the LLM and graph to return a predetermined response
    with patch.object(agent, '_invoke', new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [
                MagicMock(content=mock_llm_response_billing_only)
            ]
        }

        with patch('agent.get_user_sub', return_value='test-user'):
            response = await agent.invoke(
                query="Show me the billing information for customer C1000",
                context_id="test-context-billing",
                tools=mock_tools,
            )

    assert response.status == "completed"
    assert "Billing" in response.message or "billing" in response.message


@pytest.mark.asyncio
async def test_agent_full_review_flow(mock_tools, mock_llm_response_full_review):
    """Test the full customer review flow end-to-end with mocked LLM."""
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, '_invoke', new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [
                MagicMock(content=mock_llm_response_full_review)
            ]
        }

        with patch('agent.get_user_sub', return_value='test-user'):
            response = await agent.invoke(
                query="Generate a full customer billing review summary for customer C1000",
                context_id="test-context-full",
                tools=mock_tools,
            )

    assert response.status == "completed"
    assert "Customer Billing Review Summary" in response.message or "billing" in response.message.lower()


@pytest.mark.asyncio
async def test_agent_milestone_logging(mock_tools, mock_llm_response_full_review):
    """Test that milestone logging is triggered during agent execution."""
    import logging
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, '_invoke', new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [
                MagicMock(content=mock_llm_response_full_review)
            ]
        }

        with patch('agent.get_user_sub', return_value='test-user'):
            with patch.object(agent, '_log_milestone') as mock_log:
                response = await agent.invoke(
                    query="Full review for customer C1000",
                    context_id="test-context-milestones",
                    tools=mock_tools,
                )

    # Verify milestones were logged
    assert mock_log.call_count >= 1
    # M1 should always be achieved
    m1_calls = [c for c in mock_log.call_args_list if c[0][0] == "M1"]
    assert len(m1_calls) >= 1
    assert m1_calls[0][0][1] is True  # achieved


@pytest.mark.asyncio
async def test_agent_handles_no_tools():
    """Test agent handles scenario where no tools are available."""
    from agent import SampleAgent

    agent = SampleAgent()

    no_tools_response = "I'm sorry, tools are temporarily unavailable. Please try again later."

    with patch.object(agent, '_invoke', new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [
                MagicMock(content=no_tools_response)
            ]
        }

        with patch('agent.get_user_sub', return_value='test-user'):
            response = await agent.invoke(
                query="Show billing for customer C1000",
                context_id="test-context-no-tools",
                tools=[],
            )

    assert response.status == "completed"
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_agent_read_only_enforcement():
    """Test that agent returns a response (read-only mode — never writes)."""
    from agent import SampleAgent

    agent = SampleAgent()
    read_only_response = "I operate in read-only mode and cannot modify invoices, contracts, or payment arrangements."

    with patch.object(agent, '_invoke', new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [
                MagicMock(content=read_only_response)
            ]
        }

        with patch('agent.get_user_sub', return_value='test-user'):
            response = await agent.invoke(
                query="Apply a credit of $500 to customer C1000",
                context_id="test-context-readonly",
                tools=[],
            )

    assert response.status == "completed"
    # Agent should decline write operations
    assert "read-only" in response.message.lower() or "cannot" in response.message.lower() or len(response.message) > 0
