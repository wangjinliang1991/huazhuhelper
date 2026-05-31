"""华住OpenAPI认证模块 - 获取access_token"""

import base64
import time
import requests


class HuazhuhelperAuth:
    """华住认证客户端"""

    def __init__(self, client_id: str, client_secret: str,
                 distributor_id: str = "MEITUAN", is_test: bool = True):
        """
        Args:
            client_id: 客户端ID（从华住申请）
            client_secret: 客户端密钥（从华住申请）
            distributor_id: 渠道Code（如 MEITUAN）
            is_test: 是否测试环境
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.distributor_id = distributor_id
        self.is_test = is_test
        self.auth_domain = "https://test-oauth2-api.huazhu.com" if is_test else "https://openapi.huazhu.com"
        self._token = None
        self._expires_at = 0

    def _basic_auth(self) -> str:
        """将 clientId:clientSecret 进行Base64编码"""
        raw = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(raw.encode()).decode()
        return f"Basic {encoded}"

    def get_token(self) -> str:
        """获取access_token（自动缓存，到期前120秒刷新）"""
        if self._token and time.time() < self._expires_at - 120:
            return self._token

        headers = {
            "Authorization": self._basic_auth(),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if self.is_test:
            headers["X-Lane-Tag"] = "preview"

        resp = requests.post(
            f"{self.auth_domain}/oauth/token",
            params={"scope": "ALL", "grant_type": "client_credentials"},
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        if "access_token" not in data:
            raise Exception(f"获取token失败: {data}")

        self._token = data["access_token"]
        self._expires_at = time.time() + data.get("expires_in", 3600)
        return self._token
