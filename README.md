# huazhuhelper

华住OpenAPI酒店列表查询 Skill for OpenClaw。

## 安装

```bash
# ClawHub 安装（推荐）
clawhub install huazhuhelper

# 或在 OpenClaw 中直接
openclaw skills install huazhuhelper
```

## 项目结构

```
huazhuhelper/
├── SKILL.md                    # Skill 定义（OpenClaw Agent 读取此文件）
├── scripts/                    # 脚本目录
│   ├── huazhuhelper_auth.py    # 认证模块（获取Token）
│   └── huazhuhelper_hotel.py   # 酒店查询模块
└── requirements.txt          # 依赖：requests
```

## 发布到 ClawHub

### 方式一：Web 界面（推荐新手）

1. 访问 https://clawhub.ai/import
2. 选择 **Import from GitHub**
3. 填入仓库地址，点击 Detect
4. 确认信息后发布

### 方式二：CLI 命令

```bash
# 1. 安装 ClawHub CLI
npm install -g clawhub

# 2. 登录（GitHub 账号）
clawhub login

# 3. 发布
clawhub publish . \
  --slug huazhuhelper \
  --name "华住酒店查询" \
  --version 1.0.0 \
  --tags latest
```

## 本地开发

```python
import sys
sys.path.insert(0, "scripts")

from huazhuhelper_auth import HuazhuhelperAuth
from huazhuhelper_hotel import HuazhuhelperHotel

auth = HuazhuhelperAuth(client_id="你的ID", client_secret="你的Secret")
hotels = HuazhuhelperHotel(auth).get_hotel_list()
for h in hotels:
    print(h["hotelName"], h["hotelId"])
```

## 依赖

```bash
pip install requests
```
