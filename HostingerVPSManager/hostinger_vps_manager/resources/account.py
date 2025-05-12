from ..api import HostingerAPIClient
from ..exceptions import HostingerAPIError


class AccountManager:
    def __init__(self, client: HostingerAPIClient):
        self.client = client

    def get_balance(self) -> float:
        """获取账户余额

        Returns:
            float: 账户余额（精确到小数点后2位）

        Raises:
            HostingerAPIError: 当API返回错误时
        """
        response = self.client._request("GET", "/user/balance")
        return round(response["balance"], 2)