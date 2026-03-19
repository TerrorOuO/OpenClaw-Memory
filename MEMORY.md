# MEMORY.md - Long-Term Memory

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

## [代码排查]

### 环境信息
- **SSH Host:** 172.20.160.68 | User: xieyuntian | Port: 22 | OS: Windows
- **代码仓库:** E:\A2\X3_client
- **配置表路径:** E:\x3\design\data_dev_siren（当前版本 data_dev_siren）
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

## [配表]

### 表结构速查
- **FunctionUnlock：** ID / EnumName / IsOn / SeverLimit / TimeLimit(→TimeCycle.ID) / PlayerLvLimit / ChapterTaskLimit / TaskLimit
- **TimeCycle：** ID / IsOn / Attribution / TriggerType / StartTime / DurationType / Duration / CycleType / ReOpenTime
  - TriggerType=2（开服时间）+ Attribution=4（服务器）是最常用的开服天数配置
  - StartTime 格式：`Nd 00:00:00`，N = 目标天数 - 1（开服第1天=`00:00:00`，第14天=`13d 00:00:00`）
- **SoldierEquipLevel：** ID / EquipType / SoldierType / EquipLevel / PropType(→BuffID,数值) / UpdateCondition / CostMaterial
  - SoldierType: 1=猎人 2=射手 3=斗士
  - PropType 格式：`属性ID,数值|属性ID,数值`

### 已处理配表需求

**2026-03-19：FunctionUnlock 1096 海妖开服第14天解锁**
- TimeCycle 新增一行：TriggerType=2, Attribution=4, StartTime=`13d 00:00:00`
- FunctionUnlock 1096 行 TimeLimit 填新 TimeCycle ID

### 复盘
- 暂无

---

## [数值]

### 学习进度
- 暂无

### 已分析问题

**2026-03-19：射手武器属性 120022（single archer soldiers attack）**
- 蓝隼火铳 Lv.1 PropType = `120022,1 | 11007,36800`
- 120022 = 射手单体攻击，数值单位待确认（Property.xlsx 读取失败）
- 推测为万分比（+1 = +0.01%），待验证

### 复盘
- 暂无

---

## [系统设计]

### 立项 / 设计决策记录
- 暂无

### 复盘
- 暂无

---

## [配置编辑群]

### 群说明
- 专职处理配表编辑需求，每晚 21:30 自动归档到此分区并 push GitHub

### 关键内容记录
- 暂无

### 复盘
- 暂无

---

## [数值讨论]

### 群说明
- 专职讨论数值问题，每晚 21:30 自动归档讨论结果到此分区并 push GitHub

### 讨论记录
- 暂无

### 复盘
- 暂无

---

## 自我复盘（全局）

- **2026-03-19：** SSH 连接信息未及时记录，导致哥重复提供 → 改进：重要信息当场写入 MEMORY.md
- **2026-03-19：** Property.xlsx 多次读取失败仍继续尝试，浪费时间 → 改进：连续失败2次立即换策略或告知哥
