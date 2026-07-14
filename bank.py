def transfer_funds(from_account, to_account, amount):
    """
    Transfer amount from from_account to to_account.

    Each account is a dict: {"id": int, "balance": float, "owner": str}

    Returns a transaction dict on success.
    Raises ValueError for invalid inputs.
    """
    if not isinstance(from_account, dict) or not isinstance(to_account, dict):
        raise ValueError("Accounts must be dictionaries")

    required_keys = {"id", "balance", "owner"}
    if not required_keys.issubset(from_account.keys()) or not required_keys.issubset(to_account.keys()):
        raise ValueError("Accounts must include id, balance, and owner")

    if from_account is to_account or from_account.get("id") == to_account.get("id"):
        raise ValueError("Source and destination accounts must be different")

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a positive number")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    if not isinstance(from_account["balance"], (int, float)) or not isinstance(to_account["balance"], (int, float)):
        raise ValueError("Account balances must be numeric")

    if from_account["balance"] < amount:
        raise ValueError("Insufficient funds")

    from_account["balance"] -= amount
    to_account["balance"] += amount

    return {
        "from_id": from_account["id"],
        "to_id": to_account["id"],
        "amount": amount,
        "from_balance_after": from_account["balance"],
        "to_balance_after": to_account["balance"],
    }
