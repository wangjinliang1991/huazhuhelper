"""华住OpenAPI酒店查询模块"""

import time
import uuid
import requests
from huazhuhelper_auth import HuazhuhelperAuth


class HuazhuhelperHotel:
    """华住酒店查询客户端"""

    def __init__(self, auth: HuazhuhelperAuth,
                 biz_domain: str = "http://test-crs-distributor.huazhu.com"):
        self.auth = auth
        self.biz_domain = biz_domain

    def get_hotel_list(self) -> list:
        """
        获取酒店列表

        Returns:
            list[dict]，每个元素包含 hotelId、hotelName 等字段
        """
        token = self.auth.get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "distributorId": self.auth.distributor_id,
            "timestamp": str(int(time.time() * 1000)),
            "traceId": str(uuid.uuid4()),
        }

        resp = requests.get(f"{self.biz_domain}/hotels", headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list):
            return data

        code = data.get("code")
        if code and code != 1000:
            raise Exception(f"API错误 [code={code}]: {data.get('message', '未知错误')}")

        return data.get("content", data.get("data", []))
