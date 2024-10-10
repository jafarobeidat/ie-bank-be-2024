from iebank_api.models import Account
import pytest

def test_create_account():
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check that the fields (name, account_number, balance, currency, status, country, and created_at) are set correctly
    """
    # Creating a new account with name, currency, and country
    account = Account('John Doe', '€', country='Jordan')  # 'Jordan' is set as the country

    # Asserting the account's properties are correctly initialized
    assert account.name == 'John Doe'  # Name should be 'John Doe'
    assert account.currency == '€'  # Currency should be set to '€'
    assert account.account_number is not None  # Account number should be automatically generated
    assert account.balance == 0.0  # Initial balance should be 0.0
    assert account.status == 'Active'  # Status should default to 'Active'
    assert account.country == 'Jordan'  # Country should be 'Jordan'

