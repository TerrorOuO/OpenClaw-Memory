# MEMORY.md - 渡的记忆

> 我叫渡，是哥的私人助手。名字取自"渡口"——你带着问题来，我帮你找到方向渡过去。

---

## 关于哥（用户）

- **称呼：** 哥
- **职业：** 主策划
- **背景：** 系统策划出身，涵盖立项、系统设计、数值，正在学习数值方向
- **时区：** UTC+8（东八区）
- **沟通风格偏好：**
  - 希望我能自我反思、有创造力
  - 能自己思考解决方案，不要总是抛问题回去
  - 被否认或出错时要主动复盘并记录问题，避免重蹈覆辙
  - 哥在学数值，遇到数值相关问题多解释原理，帮助理解

---

## 分区群说明

| 分区 | 群 | cron | GitHub 分区 |
|---|---|---|---|
| 代码排查 | 代码排查群 | 每晚 21:30 归档推送 | [代码排查] |
| 配表编辑 | 配置编辑群 | 每晚 21:30 归档推送 | [配置编辑群] |
| 数值讨论 | 数值讨论群 | 每晚 21:30 归档推送 | [数值讨论] |
| 系统设计 | 系统设计群 | 每晚 21:30 归档推送 | [系统设计] |
| 主 session | 主群 | 每晚 22:00 整理各群推送并统一归档 | 全局管理 |

**主 session 职责：**
- 统筹规划，不处理具体业务问题
- 未明确分区或准备新建分区的内容，先在主群讨论
- 归档时发现新分区内容，直接整理建立新分区
- 每晚 22:00 整理各分区群 21:30 推送的内容，统一写入 MEMORY.md 并 push GitHub
- 每早 9:30 自动 git pull 确保本地是最新版本

---

## [代码排查]

### 环境信息
- **SSH Host:** 172.20.160.68 | User: xieyuntian | Port: 22 | OS: Windows
- **代码仓库:** E:\A2\X3_client
- **项目：** X3（A2系列），Unity 客户端 + C# 服务端
- **仓库结构：** `client/`（Unity）、`server/`（GameServer / GameServer.Hotfix / CenterServer / MapServer）

### 已排查问题

**2026-03-19：付费玩家联盟推荐弹窗（1700服）不弹**
- 事件名：`pop_window_guild_rec_bi_pay_invite`
- 核心文件：`server/GameServer.Hotfix/PlayerMeta/Union/UnionMeta.cs` → `PayInviteAsync()`
- 根因：开服时间限制 `GuildSuggestForPurchaseDuation` 到期后永久停止触发
- 结论：设计行为，非 bug。延长需调整该配置值
- 待确认：1700服开服时间 + 配置值是否刚好卡在2月23号

### 复盘
- Property.xlsx 有保护无法直接读取，遇到连续2次读取失败应立即告知哥，不要继续无效尝试

---

## [系统设计]

### 立项 / 设计决策记录

**2026-03-19：OpenClaw 分区群架构设计**
- 用多个钉钉群做功能分区，每个群专职一个方向
- 各群 cron 每晚 21:30 归档到 MEMORY.md 对应分区并 push GitHub
- 主 session cron 每晚 22:00 做全量归档
- 早上 9:30 检查是否为最新版本，落后则自动 pull
- GitHub 仓库：https://github.com/TerrorOuO/OpenClaw-Memory

### 复盘
- 跨 session 通信：sessions_list 查不到其他 session，label="main" 路由待验证
- 两个 session 都显示 key 为 main，真实唯一 key 暂未确认，后续需要测试

---

## [配置编辑群]

### 群说明
- 专职处理配表编辑需求，每晚 21:30 自动归档到此分区并 push GitHub
- 配置表路径：E:\x3\design\data_dev_siren（当前版本 data_dev_siren）

### 关键内容记录

**2026-03-19：FunctionUnlock 1096 海妖开服第14天解锁**
- 需求：开服第14天才能解锁海妖（机甲）系统（SirenMecha）
- 方案：
  1. TimeCycle 表新增一行：TriggerType=2, Attribution=4, StartTime=`13d 00:00:00`，IsOn=1
  2. FunctionUnlock 表 1096 行 TimeLimit 填新增的 TimeCycle ID
- 注意：StartTime 格式 `Nd 00:00:00`，N = 目标天数 - 1

**表结构速查**
- **FunctionUnlock：** ID / EnumName / IsOn / SeverLimit / TimeLimit(→TimeCycle.ID) / PlayerLvLimit / ChapterTaskLimit / TaskLimit
- **TimeCycle：** ID / IsOn / Attribution / TriggerType / StartTime / DurationType / Duration / CycleType / ReOpenTime
  - TriggerType=2（开服时间）+ Attribution=4（服务器）是最常用的开服天数配置
- **SoldierEquipLevel：** ID / EquipType / SoldierType / EquipLevel / PropType(→属性ID,数值) / UpdateCondition / CostMaterial
  - SoldierType: 1=猎人 2=射手 3=斗士
  - PropType 格式：`属性ID,数值|属性ID,数值`

### 复盘
- 暂无

---

## [数值讨论]

### 群说明
- 专职讨论数值问题，每晚 21:30 自动归档讨论结果到此分区并 push GitHub
- 哥正在学习数值，讨论时多解释原理

### 讨论记录

**2026-03-19：射手武器属性 120022（single archer soldiers attack）**
- 蓝隼火铳（Azure Falcon Firearm）Lv.1 PropType = `120022,1 | 11007,36800`
- 120022 = 射手单体攻击属性
- +1 的数值单位待确认（Property.xlsx 读取失败，推测为万分比，即 +0.01%）
- 待确认：Property.xlsx 是否有密码保护，120022 的单位定义

### 复盘
- 暂无

---

## 全局工具权限

### Google Sheets 访问
- **token 路径：** `/root/.openclaw/workspace/google_token.json`
- **账号：** xieyuntian@nibirutech.com
- **权限范围：** spreadsheets.readonly
- **client_secret 路径：** `/root/.openclaw/dingtalk-files/1773929201_client_secret_2_380293845993-4atkpamq39id7q8665m31ek9023tf4ii.apps.googleusercontent.com(1).json`
- **使用方式：**
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

with open('/root/.openclaw/workspace/google_token.json') as f:
    t = json.load(f)
creds = Credentials(token=t['token'], refresh_token=t['refresh_token'],
    token_uri=t['token_uri'], client_id=t['client_id'],
    client_secret=t['client_secret'], scopes=t['scopes'])
service = build('sheets', 'v4', credentials=creds)
# 读取：service.spreadsheets().values().get(spreadsheetId=ID, range='Sheet名').execute()
```
- **注意：** token 会自动用 refresh_token 续期，无需重新授权

---

## 自我复盘（全局）

- **2026-03-19：** SSH 连接信息未及时记录，导致哥重复提供 → 改进：重要信息当场写入 MEMORY.md
- **2026-03-19：** Property.xlsx 多次读取失败仍继续尝试，浪费时间 → 改进：连续失败2次立即换策略或告知哥
