import pytest
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID
from models.account import Account


def test_account_defaults():
    """Test that defaults are correctly applied when creating an Account."""
    account = Account(label="Savings")

    assert account.id is None
    assert isinstance(account.uuid, UUID)
    assert account.balance == Decimal("0.00")
    assert account.created_at.tzinfo == timezone.utc
    assert account.label == "Savings"


def test_account_balance_cannot_be_negative():
    """Ensure that negative balances are not allowed by model definition."""
    with pytest.raises(ValueError):
        error_data = {"label": "Invalid", "balance": "-10.00"}
        Account.model_validate(error_data)


def test_account_custom_balance():
    """Test that a valid positive balance can be set."""
    acc = Account(label="Checking", balance=Decimal("150.75"))
    assert acc.balance == Decimal("150.75")


def test_account_created_at_is_timezone_aware():
    """Ensure created_at is set with UTC timezone."""
    acc = Account(label="Investment")
    assert isinstance(acc.created_at, datetime)
    assert acc.created_at.tzinfo == timezone.utc


def test_account_user_id_assignment():
    """Test that user_id can be assigned properly (foreign key placeholder)."""
    acc = Account(label="Joint", user_id=123)
    assert acc.user_id == 123


def test_account_uuid_uniqueness():
    """UUID should be unique across instances."""
    acc1 = Account(label="Wallet")
    acc2 = Account(label="Savings")
    assert acc1.uuid != acc2.uuid
