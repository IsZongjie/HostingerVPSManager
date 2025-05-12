import time
from typing import List, Optional
from ..api import HostingerAPIClient
from ..models import VPSPlan, VPSInstance


class VPSManager:
    def __init__(self, client: HostingerAPIClient):
        self.client = client

    def get_prices(
            self,
            region: Optional[str] = None,
            currency: str = "USD"
    ) -> List[VPSPlan]:
        """获取VPS价格列表

        Args:
            region: 区域代码（如us/eu）
            currency: 货币类型（USD/EUR等）

        Returns:
            List[VPSPlan]: 价格计划列表
        """
        params = {
            "location": region,
            "currency": currency
        } if region else {"currency": currency}

        response = self.client._request("GET", "/vps/plans", params=params)
        return [VPSPlan(**plan) for plan in response["plans"]]

    def list_instances(self) -> List["VPSInstance"]:
        """列出所有VPS实例"""
        response = self.client._request("GET", "/vps")
        return [VPSInstance(**vps) for vps in response["vps"]]

    def create_instance(
            self,
            plan_id: str,
            os: str,
            region: str,
            hostname: str = None,
            auto_renew: bool = True
    ) -> str:
        """创建新VPS实例

        Args:
            plan_id: 套餐ID（如kvm1）
            os: 操作系统（如ubuntu_22_04）
            region: 区域代码
            hostname: 主机名（可选）
            auto_renew: 是否自动续费

        Returns:
            str: 订单ID
        """
        payload = {
            "product": "vps",
            "plan": plan_id,
            "billing_cycle": "monthly",  # 固定按月计费
            "config": {
                "os": os,
                "datacenter": region,
                "hostname": hostname or f"vps-{int(time.time())}"
            },
            "auto_renew": auto_renew
        }

        response = self.client._request("POST", "/orders", json_data=payload)
        return response["order_id"]

    def power_control(self, instance_id: str, action: str) -> bool:
        """控制VPS电源状态

        Args:
            instance_id: 实例ID
            action: 操作类型（start/stop/restart）

        Returns:
            bool: 操作是否成功
        """
        valid_actions = ["start", "stop", "restart"]
        if action not in valid_actions:
            raise ValueError(f"无效操作，必须是：{', '.join(valid_actions)}")

        self.client._request("POST", f"/vps/{instance_id}/power", json_data={"action": action})
        return True

    def destroy_instance(self, instance_id: str) -> bool:
        """销毁VPS实例

        Args:
            instance_id: 实例ID

        Returns:
            bool: 操作是否成功
        """
        self.client._request("DELETE", f"/vps/{instance_id}")
        return True