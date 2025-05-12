from ..api import HostingerAPIClient
from typing import List


class RegionManager:
    def __init__(self, client: HostingerAPIClient):
        self.client = client

    def list_regions(self) -> List[str]:
        """获取支持的区域列表

        Returns:
            List[str]: 可用区域代码列表（如['us', 'eu']）
        """
        # 从价格端点提取所有唯一区域
        response = self.client._request("GET", "/vps/plans")
        return list({plan["datacenter"] for plan in response["plans"]})