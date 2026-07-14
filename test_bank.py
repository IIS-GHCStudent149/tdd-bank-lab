import pytest

from bank import transfer_funds


@pytest.fixture
def checking_account():
    return {"id": 1001, "balance": 500.0, "owner": "Alice Johnson"}


@pytest.fixture
def savings_account():
    return {"id": 1002, "balance": 250.0, "owner": "Bob Smith"}


def test_transfer_funds_updates_balances_and_returns_transaction_details(
    checking_account, savings_account
):
    transaction = transfer_funds(checking_account, savings_account, 150.0)

    assert transaction["from_id"] == checking_account["id"]
    assert transaction["to_id"] == savings_account["id"]
    assert transaction["amount"] == 150.0
    assert transaction["from_balance_after"] == 350.0
    assert transaction["to_balance_after"] == 400.0
    assert set(transaction.keys()) >= {"from_id", "to_id", "amount", "from_balance_after", "to_balance_after"}

    assert checking_account["balance"] == 350.0
    assert savings_account["balance"] == 400.0


@pytest.mark.parametrize("amount", [0, -10.0])
def test_transfer_funds_rejects_non_positive_amount(checking_account, savings_account, amount):
    with pytest.raises(ValueError, match="greater than zero"):
        transfer_funds(checking_account, savings_account, amount)


def test_transfer_funds_rejects_when_source_balance_is_too_low(checking_account, savings_account):
    with pytest.raises(ValueError, match="sufficient funds"):
        transfer_funds(checking_account, savings_account, 600.0)


def test_transfer_funds_rejects_when_source_and_destination_are_the_same(checking_account):
    with pytest.raises(ValueError, match="different"):
        transfer_funds(checking_account, checking_account, 50.0)
