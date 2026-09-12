FORBIDDEN_CAPABILITIES = {
    "orders_create", "orders_edit", "orders_cancel", "orders_close_position",
    "transfer", "send", "withdraw", "portfolios_create", "portfolios_edit",
    "portfolios_delete", "convert_execute", "delegated_sign", "wallet_sign",
    "private_key", "cdp_spend"
}

READ_HINTS = {
    "accounts", "balance", "balances", "portfolios_list", "portfolios_get",
    "orders_list", "orders_get", "orders_fills", "fees", "transactions",
    "statements", "reports", "exports", "ledger", "activity", "history"
}

def classify_capability(name: str) -> str:
    n = name.lower()
    if any(token in n for token in FORBIDDEN_CAPABILITIES):
        return "FORBIDDEN_MUTATION"
    if any(token in n for token in READ_HINTS):
        return "READ_CANDIDATE"
    return "HOLD_REVIEW"
