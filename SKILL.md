---
name: huazhuhelper
description: 查询华住酒店列表。通过华住OpenAPI获取酒店数据，需要用户提供clientId和clientSecret进行OAuth2认证。当用户提到华住酒店、酒店列表、华住API、查酒店时使用。
---

# 华住酒店列表查询

查询华住OpenAPI的酒店列表，自动处理OAuth2认证和Token管理。

## 前置条件

向用户询问以下信息（必需）：
- **clientId**: 华住分配的客户端ID
- **clientSecret**: 华住分配的客户端密钥
- **distributorId**: 渠道Code（如 MEITUAN），默认 MEITUAN

## 工作流程

### Step 1: 安装依赖

```bash
pip install requests
```

### Step 2: 确认环境

- 测试环境（默认）: `https://test-oauth2-api.huazhu.com`
- 生产环境: `https://openapi.huazhu.com`

### Step 3: 运行查询脚本

在用户项目根目录执行以下 Python 代码（将凭证替换为用户提供的真实值）：

```python
import base64, time, uuid, requests

# === 用户凭证 ===
CLIENT_ID = "用户提供的clientId"
CLIENT_SECRET = "用户提供的clientSecret"
DISTRIBUTOR_ID = "MEITUAN"
IS_TEST = True

# === Step 1: 获取 Token ===
auth_domain = "https://test-oauth2-api.huazhu.com" if IS_TEST else "https://openapi.huazhu.com"
biz_domain = "http://test-crs-distributor.huazhu.com" if IS_TEST else "https://openapi.huazhu.com"

raw_cred = f"{CLIENT_ID}:{CLIENT_SECRET}"
basic_auth = f"Basic {base64.b64encode(raw_cred.encode()).decode()}"

headers = {
    "Authorization": basic_auth,
    "Content-Type": "application/x-www-form-urlencoded",
}
if IS_TEST:
    headers["X-Lane-Tag"] = "preview"

resp = requests.post(
    f"{auth_domain}/oauth/token",
    params={"scope": "ALL", "grant_type": "client_credentials"},
    headers=headers,
    timeout=10,
)
resp.raise_for_status()
token = resp.json()["access_token"]
print(f"Token: {token[:20]}...")

# === Step 2: 查询酒店列表 ===
hotel_headers = {
    "Authorization": f"Bearer {token}",
    "distributorId": DISTRIBUTOR_ID,
    "timestamp": str(int(time.time() * 1000)),
    "traceId": str(uuid.uuid4()),
}

resp = requests.get(f"{biz_domain}/hotels", headers=hotel_headers, timeout=10)
resp.raise_for_status()
data = resp.json()

hotels = data if isinstance(data, list) else data.get("content", data.get("data", []))
print(f"共 {len(hotels)} 个酒店:")
for i, h in enumerate(hotels[:20], 1):
    print(f"  {i}. {h.get('hotelName','')} (ID: {h.get('hotelId','')})")
if len(hotels) > 20:
    print(f"  ... 还有 {len(hotels)-20} 个")
```

## 使用本项目模块

本 Skill 安装后，脚本位于 `{baseDir}/scripts/` 目录下：

```python
import sys
sys.path.insert(0, "{baseDir}/scripts")

from huazhuhelper_auth import HuazhuhelperAuth
from huazhuhelper_hotel import HuazhuhelperHotel

auth = HuazhuhelperAuth(
    client_id="用户的clientId",
    client_secret="用户的clientSecret",
    distributor_id="MEITUAN",
    is_test=True,
)
hotel = HuazhuhelperHotel(auth)
hotels = hotel.get_hotel_list()
for h in hotels:
    print(h.get("hotelName"), h.get("hotelId"))
```

其中 `{baseDir}` 是 Skill 安装后的根目录，通常为 `~/.openclaw/skills/huazhuhelper`。

## API 请求头说明

### 获取 Token
| 头 | 值 | 说明 |
|---|---|---|
| Authorization | `Basic {base64(clientId:secret)}` | clientId:secret 的 Base64 编码 |
| Content-Type | `application/x-www-form-urlencoded` | - |
| X-Lane-Tag | `preview` | 仅测试环境需要 |

### 查询酒店
| 头 | 值 | 说明 |
|---|---|---|
| Authorization | `Bearer {token}` | 上一步获取的token |
| distributorId | 渠道Code | 如 MEITUAN |
| timestamp | 毫秒时间戳 | 自动生成 |
| traceId | UUID | 自动生成 |

## 错误处理

- **401**: clientId 或 clientSecret 错误
- **403**: IP 不在白名单，需联系华住添加
- **Token过期**: 重新执行 Step 1 获取新 token
