import time
import requests
from typing import Dict, Any, Optional
from .exceptions import HostingerAPIError
from dotenv import load_dotenv
import os

load_dotenv()  # 加载.env文件
API_KEY = os.getenv("HOSTINGER_API_KEY")


class HostingerAPIClient:
    BASE_URL = "https://developers.hostinger.com"
    USER_AGENT = "HostingerVPSManager/1.0 (+https://github.com/IsZongjie)"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HOSTINGER_API_KEY")
        if not self.api_key:
            raise ValueError("API密钥未配置")

        self.session = requests.Session()
        self._configure_session()

    def _configure_session(self):
        """配置会话参数"""
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": self.USER_AGENT
        })
        self.session.timeout = (10, 30)  # 连接/读取超时

    def _request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict] = None,
            json_data: Optional[Dict] = None,
            retries: int = 3
    ) -> Dict[str, Any]:
        """统一请求处理"""
        for attempt in range(retries):
            try:
                response = self.session.request(
                    method,
                    f"{self.BASE_URL}{endpoint}",
                    params=params,
                    json=json_data
                )
                response.raise_for_status()
                return self._parse_response(response)
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise HostingerAPIError(
                        code=getattr(e.response, "status_code", 500),
                        message=str(e),
                        raw_error=e
                    ) from e
                # 指数退避重试
                wait_time = 2 ** attempt
                print(f"请求失败，{wait_time}秒后重试...")
                time.sleep(wait_time)

    @staticmethod
    def _parse_response(response: requests.Response) -> Dict[str, Any]:
        """解析响应数据"""
        try:
            return response.json()
        except ValueError:
            return {"error": "无效的JSON响应"}