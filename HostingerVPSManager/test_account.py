from hostinger_vps_manager.api import HostingerAPIClient
from hostinger_vps_manager.resources.account import AccountManager

def test_get_balance():
    client = HostingerAPIClient()
    account = AccountManager(client)
    balance = account.get_balance()
    print(f"当前余额: ${balance:.2f}")
    assert balance >= 0