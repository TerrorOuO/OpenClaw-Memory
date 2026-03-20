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
| 代码排查 | 代码排查群 | 21:00 / 00:00 归档 | [代码排查] |
| 配表编辑 | 配置编辑群 | 21:00 / 00:00 归档 | [配置编辑群] |
| 数值讨论 | 数值讨论群 | 21:00 / 00:00 归档 | [数值讨论] |
| 系统设计 | 系统设计群 | 21:00 / 00:00 归档 | [系统设计] |
| UI设计 | UI设计群 | 21:00 / 00:00 归档 | [UI设计] |
| 主 session | 主群 | 21:15 发日报 / 00:30 统一整理 / 09:30 播报 | 全局管理 |

**完整时序：**
```
21:00 — 各群归档任务触发（同一 session，按分区整理各群内容）
21:15 — 发日报给哥
00:00 — 各群再次归档
00:30 — 统一整理所有分区并 push GitHub
09:30 — 早间播报（以 00:00 归档为准）
```

**重要说明：**
- 所有群共用同一个 session，分区群只是哥方便联系上下文的组织方式
- cron 任务统一在这个 session 里管理，不会在每个群里重复触发
- 09:30 播报只会触发一次，回复到 cron 配置时指定的 channel（当前为 hub-channel 主群）
- 实际归档质量依赖 00:30 的统一整理，各群 21:00/00:00 的任务是分区整理的辅助

**主 session 职责：**
- 统筹规划，未明确分区的内容先在主群讨论
- ⚠️ 固定五个分区：代码排查、配置编辑、数值讨论、系统设计、UI设计。不得自行新增分区
- 新分区只在哥明确说"拉群了"之后，才在后续归档时建立对应分区
- ⚠️ 所有群共用同一个 session，哥的消息可能来自不同群、针对不同任务。每次回复前先根据消息内容自行判断所属分区，确认上下文后再作答，避免串台
- ⚠️ 哥不会带前缀说明当前在哪个群，也不会主动优化上下文，完全交给我自行判断。不要要求哥说明分区
- ⚠️ 各群对话上下文无法真正隔离，需多 bot 实例才能实现

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

**2026-03-20：融合玩法 SLG 新项目立项讨论**
- 方向：小游戏买量 → 有机过渡至 SLG，核心要求有明显爆点
- 哥的参考方向：物理导流+模拟经营、竖切面城建+塔防、天空汽艇+索降钓鱼、卡牌城建塔防等14个方向
- 我补充的方向（按机会排序）：
  1. 地下钻探+资源争夺+塔防（买量素材好做，挖宝即时反馈，与SLG资源争夺天然契合）
  2. 寄生/感染城建+肉鸽（题材新颖，Plague Inc验证过传播性，SLG阶段感染其他玩家有强社交属性）
  3. 建筑拆解重组+物理+塔防（物理引擎买量天然病毒传播，Besiege已验证受众）
  4. 重力翻转城建+塔防、时间回溯+城建+塔防、食物链城建+生态模拟、梦境入侵+城建、绳索物理+城建+割草
- 待续：哥尚未确认感兴趣方向，后续展开小游戏玩法设计和SLG衔接机制

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

### 关键内容记录

**2026-03-20：ItemObtain 获取途径配置**
- 需求：为 1142（经验）、220001（紫色碎片）、220002（橙色碎片）新增获取途径
- 关联表：Item.ObtainID → ItemObtain.ID → ShopItemCfg（钻石商店商品）
- 现状：
  - 1142 ObtainID 为空，需新增途径：情报(503)、每日心动(597)、海兽(504)、钻石商店(405)
  - 220001/220002 ObtainID 原填 19|651（占位，不对），需替换
  - 钻石商店途径需先在 ShopItemCfg 新增商品行（1000046/47/48），Sort 和 Price 待策划定
  - 礼包途径需在 ItemObtain 新增两行（100351/100352），Value（礼包ID）待确认
- 读表方法：scp 直接传输 xlsx 会截断（200KB vs 442KB），需用 `ssh python3 -c "sys.stdout.buffer.write(open(...,'rb').read())"` 方式传输二进制文件

**表结构速查**
- Item 表：ObtainID 列填 ItemObtain.ID，多个用 `|` 分隔
- ItemObtain 表：ObtainType(3=礼包/4=商店/5=界面/6=兑换)，Value 对应各类型参数
- ShopGroupCfg ID=101：钻石商店，Content=1011
- ShopItemCfg：ShopType=1011 为钻石商店商品，ConsumeItem=1002（钻石）

### 复盘
- 暂无

---

## [UI设计]

### 群说明
- 专职处理 UI 设计、UX 交互逻辑输出，以及结合二者生产供客户端使用的 prefab
- 每晚 21:00 / 00:00 自动归档到此分区并 push GitHub
- prefab 生成规则：参考分辨率 1080×1920，CanvasScaler ScaleWithScreenSize，Image 组件 guid: c81b19283ff80804a88d4f1bed8bd2ef

### 工作记录

**2026-03-20：UIMechaRepair 修理机甲弹窗**
- 任务：根据设计图拼接预制体，使用 UILogin 目录下 img_mecha_window_* 资源
- 产出：Assets/Editor/CreateUIMechaRepair.cs（已推送到 E:\A2\X3_client\client\Assets\Editor\）
- 执行方式：Unity 编译后 Tools → UI → Create Mecha Repair Prefab
- 输出路径：Assets/Res/UI/Prefab/UILogin/UIMechaRepair.prefab
- 布局基准：Root 900×650，居中，各元素 anchoredPosition 已按目标图像素测量换算
- 待验收：Unity 启动后执行脚本，截图对比目标图做微调

### 项目 UI 预制体通用规则（来自 UITest.prefab）

**脚本 GUID 速查**
- Image 组件：c81b19283ff80804a88d4f1bed8bd2ef
- 自定义 Button：5e2aea1dd1bda784e98010997c09baef（含缩放反馈 pressed scale 0.95）
- 自定义 Button（另一种）：1da2a900e79078449848779d2f553a64（LongPress 支持）
- Text 组件（项目自定义）：3501d990b4af08747a2fa646f81c04dd
- Text 组件（另一种）：abe1a3836752dc54794a1bd01f8e3e9c
- 文字阴影/描边：325c83ddc30c0544a91a2f6ecbc561a1
- UIBase（弹窗根节点）：e8f4194e9ed83794da496c6236ff0d7f（含 clickMaskClose / DoTween 动画）
- CanvasScaler：0cd44c1031e13a943bb63640046fad76
- HorizontalLayoutGroup：30649d3a9faa99c48a7b1166b86bf2a0
- DOTween 动画组件：4d0390bd8b8ffd640b34fe25065ff1df

**层级结构规范**
- Root 尺寸：1000×730，anchor/pivot 居中 (0.5, 0.5)
- 背景层：BG 节点（stretch 铺满 Root）→ 子节点放 bg 图和装饰横条
- 顶部栏：TOP 节点（anchor top 全宽，高 110）→ 子节点放标题图和关闭按钮
  - 关闭按钮：anchor 右上 (1,1)，pos(-64,-58)，size 104×104
  - 标题图：anchor 顶中，pos(0,-55)，size 600×100
- 内容区：Content 节点（居中，1000×400，pos 0,15）
- 按钮行：Button 节点（anchor 底中，pos 0,118，800×150）+ HorizontalLayoutGroup
- 材料/道具行：item 节点（居中，1000×100）+ HorizontalLayoutGroup

**HP 血条规范**
- hp 容器节点（anchor 顶中，500×70）
- bg 子节点：stretch 铺满，挂 hp_bg 图
- hp 子节点：anchorMin(0,0) anchorMax(1,1)，sizeDelta(-260,-10)，pos(-120,0)，挂 hp 前景图（不用 Filled，用偏移裁切）
- 右侧数值框：anchor 右(1,0.5)，pos(93,0)，140×80

**装饰横条（bg_mask）规范**
- 属于背景层，放在 BG 节点下，不要放在功能节点（如 hp）里
- 作为标题下方或内容区分隔的横向装饰条使用
- 水平方向拉伸（anchorMin.x=0, anchorMax.x=1），垂直方向固定高度

**按钮规范**
- 用 HorizontalLayoutGroup 自动排列，不手动摆坐标
- 每个按钮子节点：bg（stretch 铺满按钮图）+ TEXT（文字，stretch 留边距）
- 文字颜色：金色 (0.97, 0.90, 0.59)，带描边组件

**文字规范**
- BestFit: 1，MinSize: 3，MaxSize 按需设置
- 标题文字：FontSize 46，金色 (0.97, 0.90, 0.59)，带描边
- 按钮文字：FontSize 50，金色，Bold
- 数值文字（HP等）：FontSize 40，黄色 (0.73, 0.68, 0.16)
- 材料数量：FontSize 30，红色 (0.67, 0.06, 0.06)，Bold

**Sprite 引用格式**
- m_Sprite: {fileID: 21300000, guid: <meta中的guid>, type: 3}

### 复盘（2026-03-20 UIMechaRepair 任务）

**错误记录**
1. Root 尺寸用了 900×650，实际项目标准是 1000×730，导致整体比例偏小
2. 按钮用手动 anchoredPosition 摆坐标，实际项目用 HorizontalLayoutGroup 自动排列
3. bg_mask 放进了 hp 节点里，实际应放在 BG 节点下作为背景装饰层
4. HP 前景条用了 Image.Type=Filled，实际项目用 sizeDelta 偏移裁切（anchorMin/Max 拉伸 + sizeDelta 负值）
5. Text 组件用了 `Resources.GetBuiltinResource<Font>("Arial.ttf")`，新版 Unity 不支持，导致编译报错
6. 没有先读参考预制体就开始写脚本，导致层级结构和规范偏差大

**经验总结**
- 拿到新 UI 任务，第一步必须先读同目录下已有的参考预制体，提取层级结构和组件规范，再动手
- 装饰性资源（横条、背景纹理）归属背景层，功能性资源（血条、图标）归属内容层，不要混放
- 项目有自己的 Button/Text 组件，不要用 Unity 原生组件替代
- Editor 脚本生成预制体效率高，但坐标精度依赖对设计图的像素测量，误差会累积，后续考虑直接生成 YAML 预制体文件精度更高

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

**2026-03-20：SLG 主堡升级数值设计复盘（我的设计 vs Sonnet）**
- 我的设计表：https://docs.google.com/spreadsheets/d/141Wf9ZE4CfkmHvmBk5L52CQjCh_wlLUWyWs58vN12NM
- Sonnet 设计表：https://docs.google.com/spreadsheets/d/1gMYB_gwOioH0oGxQpmS4Di9bIr7zyFvgZcZD7WYCtjs（tab: 主堡升级数值（公式））
- 核心差距：
  1. 时间精度：我的设计 69 天偏松，Sonnet 精确卡 91 天，且把加速机制显式建模
  2. 资源比例：我的四种资源各自独立指数，后期铁矿严重失衡；Sonnet 以粮食为基准用比例系数统一换算
  3. 战力曲线：我用幂函数后期增量递减；Sonnet 用倍率增长保证高级玩家碾压感，且明确主堡战力占全账号 15-20%
  4. 付费设计：我只有模糊的"加速道具"；Sonnet 明确四个卡点（Lv10/16/21/26）与 T3/T4/T5 兵解锁强绑定
  5. 玩家分层：我没有分层；Sonnet 明确免费（Lv21/60天）、中度（Lv26/64天）、重度（Lv30/91天）三层
  6. 文档质量：我停留在"数值能跑通"；Sonnet 有完整的设计逻辑推导，适合评审对齐
- 学习要点：数值设计不只是公式，要有商业化逻辑推导和玩家分层视角

### 复盘
- 暂无

---

## 全局工作规范

- **长任务处理：** 执行前先发一条消息告知"开始了，预计 XX 秒"；真正需要中间播报的任务用子 agent 执行，主 agent 保持响应接收进度推送；平台限制导致同一条消息内的过程描述对哥不可见
- **进度播报格式：** 任务开始前："好，开始做 XXX，预计 XX 秒。" → 执行完："完成，结果是 ZZZ"
- **工具调用规范：** 先执行完所有工具调用，再一次性输出完整结论；不在回复中间插过程性描述
- **状态汇报：** 工具调用超时或无输出时立即说明并切换方案，不沉默等催
- **分区判断：** 哥不带前缀说明当前在哪个群，由我根据消息内容自行判断所属分区

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
- **2026-03-19：** Mecha 数值对比时误读列顺序，把橙色/紫色声望列搞反，误报大量差异 → 改进：读设计文档前必须先打印表头确认列结构，不能假设列顺序
- **2026-03-19：** MechaSkill 配置规律检查——40000801 PropNum Lv1 填了 1400 应为 -1400，漏了负号。同类减伤技能 PropNum 全级应为负数，配置时要检查同组数值符号一致性
- **2026-03-20：** 工具调用超时或无输出时没有主动告知，沉默等哥来催 → 改进：每次工具调用结束必须主动汇报状态；超时或无输出立即说明并切换方案，不等催；长任务中间加进度播报
- **2026-03-20：** 回复中间夹杂工具调用导致消息被拆成两段，看起来像输出中断 → 改进：先执行完所有工具调用，再一次性输出完整结论；不在回复中间插过程性描述

## 数据检查经验积累

- **减伤/负向属性**：PropNum 应为负数，若某级出现正数需立即核查
- **跨品质对比**：紫色/橙色同字段列顺序不一定相同，读表前先确认表头
- **规律性检查**：同一技能组各级数值应呈线性增长，出现断层或符号异常即为错误
- **设计文档对比**：先打印表头行确认列映射，再做数值比对
