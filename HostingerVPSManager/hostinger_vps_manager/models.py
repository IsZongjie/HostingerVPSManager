from typing import TypedDict, Optional

class VPSPlan(TypedDict):
    id: str
    name: str
    cpu: int
    memory: str  # 示例: "4GB"
    storage: str  # 示例: "50GB NVMe"
    bandwidth: str  # 示例: "1TB"
    price: float
    discounted_price: Optional[float]
    currency: str

class VPSInstance(TypedDict):
    id: str
    status: str  # running/stopped/pending
    ip: str
    plan: str
    datacenter: str
    created_at: str  # ISO 8601格式时间戳