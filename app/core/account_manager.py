class AccountManager:
    def __init__(self):
        self.connected_accounts = {}

    def add_account(self, provider: str, account_id: str, scopes: list[str]):
        self.connected_accounts[provider + ":" + account_id] = {
            "provider": provider,
            "account_id": account_id,
            "scopes": scopes,
            "enabled": True,
        }

    def get_account(self, provider: str, account_id: str):
        return self.connected_accounts.get(provider + ":" + account_id)
