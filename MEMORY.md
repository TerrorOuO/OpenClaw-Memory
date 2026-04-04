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
21:00 — 日报发送（替代原来的 21:15）
23:00 — 各群再次归档
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

## [jira-bug-creator 经验]

### 基础配置
- ~/.env.jira 配置：JIRA_URL=https://jira.tap4fun.com/, JIRA_PERSONAL_TOKEN（用户提供）, JIRA_PROJECT=X3NEW
- 已安装 python-dotenv、atlassian-python-api、requests

### 部门归属规则
- **海妖系统**：默认归客户端（包括界面效果类问题）
- 界面效果/显示不一致类问题：客户端（不是UI）

### 经办人映射
- 海妖系统：liuweiwei（刘为为）
- 战报系统：zhangsilin

### 版本规则
- 海妖相关 Bug：版本默认填"海妖版本"；若不存在，回退未发布最高/最低版本
- normalize_version 白名单已加"海妖版本"，避免创建时报"版本名无效"

### X3NEW 项目新建 Bug 注意事项
- X3NEW 新建界面暂不支持"归属功能"字段 customfield_12901，创建时留空，必要时事后在 Jira 内补充
- 创建完 Bug 必须附上 Jira 链接回复
- 用户会在 Jira 内自行修订字段，无需创建前确认

### 附件上传规则（2026-03-25 确认）
- `create_bug(attachment=...)` 内部会自动上传第一张附件，**不要再额外调用 upload-attachment.py 上传同一张图**，否则会重复
- 多图处理：`attachment` 传第一张，第二张起用 `upload-attachment.py` 逐个补传
- 一条消息里的所有截图全部上传到同一个 Bug 单

### 执行环境（2026-03-25 确认）
- `uv run` 默认使用系统 Python（/usr/bin/python3），不含 atlassian 包
- 正确执行路径：`/root/.cache/uv/environments-v2/run-bug-0c39fa0988fbec23/bin/python scripts/run-bug.py`
- 上传附件：`/root/.cache/uv/environments-v2/upload-attachment-2f50c7fcc10674f3/bin/python scripts/upload-attachment.py`
- run-bug.py 支持 `--dry-run` / `--confirm` 双参数防护，必须显式加 `--confirm` 才真正提单

### 兜底方案（2026-03-26 确认）
- skill 脚本路径硬编码为 Windows，Linux 环境下无法直接调用
- 兜底：直接用 python3 + requests 调 Jira REST API（读 ~/.env.jira → requests.post），不依赖 skill 脚本
- 子 agent 连续两次返回无效结果后，直接主 agent 用 REST API 创建，不再重试子 agent

---

## [代码排查]

### 环境信息
- **SSH Host:** 172.20.160.68 | User: xieyuntian | Port: 22 | OS: Windows
- **代码仓库（X3）:** E:\A2\X3_client
- **代码仓库（X3）:** E:\A2\X3_client
- **代码仓库（躺平）:** E:\A2\tangping\client（新项目，2026-04-03 起代码排查/配置编辑/UI设计切换至此）
- **项目：** X3（A2系列），Unity 客户端 + C# 服务端；躺平项目为纯 Unity 客户端，无独立 server 目录
- **仓库结构（X3）：** `client/`（Unity）、`server/`（GameServer / GameServer.Hotfix / CenterServer / MapServer）
- **仓库结构（躺平）：** 根目录 `client/`（Unity 工程）→ `Assets/Game/`（游戏逻辑脚本）、`Assets/Res/`（资源）、`Assets/Infrastructure/`、`Assets/Plugins/`；csproj 命名前缀 X6，推测内部代号 X6

### 躺平项目 Assets 结构速查
- `Assets/Game/Script/` — 游戏逻辑脚本
- `Assets/Game/MiniGames/` — 小游戏相关
- `Assets/Game/Battle/` — 战斗系统
- `Assets/Game/Config/` — 配置相关
- `Assets/Game/Common/` — 公共模块
- `Assets/Res/` — 美术资源（UI Prefab 等）
- `Assets/Editor/` — 编辑器工具脚本

### 已排查问题

**2026-03-19：付费玩家联盟推荐弹窗（1700服）不弹**
- 事件名：`pop_window_guild_rec_bi_pay_invite`
- 核心文件：`server/GameServer.Hotfix/PlayerMeta/Union/UnionMeta.cs` → `PayInviteAsync()`
- 根因：开服时间限制 `GuildSuggestForPurchaseDuation` 到期后永久停止触发
- 结论：设计行为，非 bug。延长需调整该配置值
- 待确认：1700服开服时间 + 配置值是否刚好卡在2月23号

**2026-03-24：世界入侵活动时间描述与实际不符**
- 核查：RuleTips.xlsx ID=1901 规则文本与实际配置时间不一致
- 实际配置：startTime+120h 起算、共6场、UTC 00/04/08/12/16/20、每场约2h
- 结论：规则文本需更新（已确认修改方案）

**2026-03-24：海妖属性界面报错（UIMechaAttributeEntry 空引用）**
- 核查：Auto_UIMechaAttributeEntry.cs 绑定路径与预制体节点命名不一致
- 结论：暂不处理

**2026-03-24：海妖 Bug 批量创建**
- X3NEW-145~148：属性界面背景遮罩缺失、技能预览背景缺失、自由属性点负数、技数值万分比未转百分比
- 等级 C，经办人 liuweiwei，修复版本"海妖版本"
- Jira 创建脚本 bug 修复：normalize_version 白名单已加"海妖版本"

**2026-03-25：海妖系统 Bug 批量创建（X3NEW-160~175，经办人 liuweiwei）**
- X3NEW-160：确认点数分配后海妖展示视频消失（B级）
- X3NEW-161：点击补充气血按钮无反馈（B级）
- X3NEW-162：分享窗口海妖头像未适配圆形框（C级）
- X3NEW-163：分享途径进入的海妖界面不应展示剩余自由点数（C级）
- X3NEW-164：分享途径进入的海妖技能界面不应展示升级预览效果（C级）
- X3NEW-165：海妖名称未使用多语言键值，直接显示中文硬编码文本（C级）
- X3NEW-166：补充气血提示文本未自适应容器宽度导致截断（C级）
- X3NEW-167：道具重置弹窗底部提示文本超框（C级）
- X3NEW-168：重置弹窗确认按钮文本不准确，应使用键值 Text_MileStone_Confim（C级）
- X3NEW-169：上阵界面添加海妖按钮缺少本地化，应使用键值 Text_Mehca_Force_Add（C级）
- X3NEW-170：选择海妖界面已解锁技能显示"未解锁"文本有误（C级）
- X3NEW-171：选择界面橙色品质卡面背景资源错误，应使用 img_mecha_force_choose_bg2（C级）
- X3NEW-172：存在海妖状态下创建部队界面顶部英雄栏缺少背景资源（C级）
- X3NEW-173：集结信息界面海妖头像未做圆形适配且尺寸过大遮挡状态文本（B级）
- X3NEW-174：部队详情界面海妖头像未做圆形适配且尺寸过大导致英雄头像超框（B级）
- X3NEW-175：治疗弹窗可治疗上限数值不准确（B级）

**2026-03-25：Unity 预制体变体制作**
- 哥询问如何制作预制体变体
- 方法：Project 窗口右键原始预制体 → Create → Prefab Variant，生成的变体继承原始预制体所有属性，可独立覆盖部分字段

**2026-03-25：战报系统 Bug 批量创建（X3NEW-176~182，经办人 zhangsilin）**
- X3NEW-176：战报界面英雄头像列表少显示一位英雄（C级）
- X3NEW-177：海妖重伤字段显示本地化键值 Text_Mehca_Mail_Severe_Injury 未转译（C级，版本：海妖版本）
- X3NEW-178：部队详情界面海妖区域缺少"海妖资讯"标题栏（C级，版本：海妖版本）
- X3NEW-179：部队详情界面海妖资讯头像未适配圆形外框（C级，版本：海妖版本）
- X3NEW-180：详细资讯界面海妖技能触发区域缺少"海妖技能触发"标题栏（C级，版本：海妖版本）
- X3NEW-181：敌方无海妖时海妖技能触发区域显示空白，应显示"该部队无海妖参战"（C级，版本：海妖版本）
- X3NEW-182：战报海妖资讯头像应使用无背景色版本头像框（C级，版本：海妖版本）

**2026-03-26：海妖系统 Bug 批量创建**
- X3NEW-186：隐藏UI后页签选定状态丢失（C级，经办人 liuweiwei）— SetCleanMode(false) 恢复时未调用 SwitchTab，页签视觉态未同步
- X3NEW-187：治疗期间养成界面加号按钮资源应替换为 img_dtc_btn_jump（C级，经办人 liuweiwei）
- X3NEW-188：治疗弹窗海妖头像框适配不正确，建议换用排行榜常规头像框（C级，经办人 liuweiwei，含截图附件）
- X3NEW-192：视频播放时需点击一次界面才出现跳过按钮（C级，经办人 zhangli）

**2026-03-27：海妖引导重复触发 Bug 创建**
- X3NEW-232：触发海妖引导后每次重启游戏都会重复触发引导（C级，经办人 liuweiwei，版本：海妖版本）

**2026-03-30：海妖系统 Bug 批量创建（X3NEW-266/268/269/280，经办人 liuweiwei）**
- X3NEW-266：大地图集结行军中海妖与主船穿模（C级）
- X3NEW-268：主宰共鸣技能升级预览数值显示占位符未替换（"{0}""{1}"未替换为实际数值）（C级）
- X3NEW-269：海妖攻击敌方中立建筑时朝向跟随船头偏转而非朝向目标（C级）
- X3NEW-280：KVK战斗中后续回声丰碑封包攻击的海妖伤害数值未更新，始终显示首次进入战斗的轻伤重伤数据（C级）

**2026-03-30：普通海兽掉落查询（未完成）**
- 任务：查询 UnitConfigMonster.xlsx 中 MonsterType=2 普通海兽各等级奖励道具
- 状态：SSH 连接 172.20.160.68 本次无输出，任务未完成，待下次确认连接状态后继续

**2026-04-01：海妖养成界面分辨率适配 Bug 创建**
- X3NEW-301：海妖养成界面在 1:2 分辨率下布局未自适应，立绘与底部面板间存在大面积空白（C级，经办人 liuweiwei，版本：海妖版本，含截图附件）

**2026-03-26：海妖系统 Bug 批量创建（X3NEW-193~206，含重复单）**
- X3NEW-193：视频播放时需点击一次界面才出现跳过按钮（C级，经办人 zhangli）
- X3NEW-194：重复单（同X3NEW-193，待哥删除）
- X3NEW-195：橙色海妖获取界面海妖名称显示本地化键值未转译（C级，经办人 liuweiwei）
- X3NEW-196：橙色海妖获取界面未显示获取按钮（C级，经办人 liuweiwei）
- X3NEW-197：提亚马特获取界面道具内容与礼包道具不一致（C级，经办人 zhangsilin）
- X3NEW-198：购买提亚马特礼包后橙色提亚马特未正确解锁（B级，经办人 zhangsilin）
- X3NEW-201：创建部队界面海妖模型与船模型重合（B级，经办人 liuweiwei）
- X3NEW-202：选择海妖界面未解锁海妖背景资源错误且缺少整体置灰效果（C级，经办人 liuweiwei）
- X3NEW-203：行军攻击时海妖随船偏移方向（B级，经办人 liuweiwei）
- X3NEW-204：大地图攻击未播放攻击特效及目标受击特效（B级，经办人 liuweiwei）
- X3NEW-205：派遣海妖援助时援助列表未显示海妖信息（C级，经办人 liuweiwei）
- X3NEW-206：抵达援助目标后海妖模型停留在目标周围未归位（C级，经办人 liuweiwei）

**2026-03-30：海兽掉落查询链路**
- 核心表：UnitConfigMonster.xlsx，MonsterType=2 为普通海兽
- 奖励字段：Reward（个人奖励）/ TeamReward（队伍奖励）/ ExtraReward（活动期间额外奖励，按 MonsterType 挂载）
- 本次 SSH 无输出，任务未完成，待下次确认连接状态后继续

### 经办人映射补充
- 战报系统：zhangsilin
- 视频播放相关：zhangli

### 复盘
- Property.xlsx 有保护无法直接读取，遇到连续2次读取失败应立即告知哥，不要继续无效尝试
- 早间播报任务（web_fetch GitHub + write MEMORY.md）需注意 write 工具的 content 参数是必填的，不能只传 file_path
- **2026-03-30 子 agent 结果不完整：** 多个 Bug 创建子 agent 只返回中间状态（"Bug 创建成功，现在上传截图"），未给出 issue key 和链接 → 改进：子 agent 完成后主 agent 校验结果是否含 issue key，缺失时主动查 Jira 最近创建记录（jql: project=X3NEW ORDER BY created DESC）补全
- **2026-03-26 规则确认：** 哥直接描述问题现象 = 提 bug，不做代码排查和修复，直接开子 agent 提 Jira

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

**2026-03-23：融合玩法 SLG 立项方向（第二轮，排除已提方向后新增8个）**
- 背景：在排除第一轮所有方向后，继续产出新方向
- 新增8个方向（均附原型参考游戏、买量第一帧、SLG衔接逻辑）：
  1. 冰面滑行领地（原型：Penguins Arena）— 滑行撞击 → 冰原领地争夺
  2. 管道拼接城建（原型：Where's My Water）— 管道引流 → 城市供给网络/运输线攻防
  3. 弹珠弹射攻城（原型：Peggle）— 弹珠弹跳 → 攻城器械操作，攻防双方都有操作深度
  4. 磁力吸附合兵（原型：Mob Control）— 磁力吸兵 → 征兵/集结可视化，英雄对撞决胜
  5. 光线折射破阵（原型：Lazors）— 镜面折射 → 信号塔/瞭望网络，视野即情报优势
  6. 沙盘堆叠地形（原型：Sand Balls）— 堆沙挖沙 → 战场地形工程，攻城前双方改造地形
  7. 颜色覆盖圈地（原型：Paper.io 2）— 画线圈地 → 领土扩张，圈地路线暴露可被截击
  8. 炼金合成经营（原型：Little Alchemy 2）— 元素合成 → 科技树/军备系统，稀有元素逼迫扩张或贸易
- 待续：哥尚未确认感兴趣方向

**2026-03-31：Quarantine Zone: The Last Check 游戏系统分析**
- 开发：Brigada Games | 发行：Devolver Digital | 引擎：UE5 | 发售：2026-01-12
- 类型：模拟经营，单人，买断制；首周销量 50 万份，Steam 畅销榜第三
- 核心玩法：第一人称检查幸存者（类 Papers, Please）+ 等距视角基地管理 + 夜间无人机塔防
- 检查系统：使用反射锤/扫描仪/手电筒等工具逐项核查症状，判决放行/隔离/消灭，误判有双向惩罚
- 经济循环：白天检查赚钱 → 升级设施（宿舍/防御/发电机）→ 维护成本持续消耗，形成压力
- 口碑：褒贬不一，核心检查玩法受认可，基地管理深度不足、发售 bug 较多被批评
- 对 SLG 立项的启示：双视角切换可映射"小游戏钩子+大地图策略"；道德压力是天然买量素材；昼夜节奏对比避免疲劳；需注意双系统联动深度
- 分析文档已生成 .docx 并传至 Windows 桌面：quarantine_zone_analysis.docx

**2026-03-25：怪谈题材融合 SLG 立项讨论**
- 买量钩子：家人敲门 / 判断门外是人还是怪物，私密室内场景
- 开场玩法对标 Last Asylum：俯视角房间为主视角，点击大门进入独立第一人称小游戏判断真假，判断完退回俯视角
- 收留对象从"家人"扩展为"幸存者"解决数量上限问题，买量素材保持"家人敲门"不变
- 房间体系 = SLG 城建等比缩放：客厅（主堡）→ 卧室（民居）→ 厨房（农场）→ 武器间（兵营）→ 瞭望台（侦察塔）
- 过渡叙事：怪物成群结队来了，单靠一家守不住 → 联合幸存者据点 → SLG 大地图
- 后续可扩展小游戏类型：夜间巡逻手电筒扫描、声音方向判断、物资检查验证身份等
- 待续：哥尚未确认是否继续推进该方向

### 复盘
- 跨 session 通信：sessions_list 查不到其他 session，label="main" 路由待验证
- 两个 session 都显示 key 为 main，真实唯一 key 暂未确认，后续需要测试
- **2026-03-25 归档漏项**：00:30 统一整理未将怪谈立项讨论同步至系统设计分区，已手动补录

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

- **日报格式**：每条 bullet point 用自然语言概述工作梗概，不写具体文件名/函数名/表名等细节。例如：「核查了某问题，确认是规则文本与配置不一致」而非「核查了 ActvInvasion.xlsx + RuleTips.xlsx ID=1901」。
- **cron 时间**：首次归档 21:00（原来 21:15），日报发送 21:00，23:00/00:30 归档及 GitHub push 维持不变。
- **归档原则**：主 session 工作内容不依赖分区 cron，直接进入主 session 归档；主 session 本身也是归档入口。
- **归档三步强制流程（违反即为失职）：**
  1. **归档前必须先读当天日记** `memory/YYYY-MM-DD.md`，以日记为 source of truth，逐条对照写入 MEMORY.md，不凭印象回顾
  2. **日记随手记，不攒**：每完成一个话题（bug提交/立项讨论/技术问答）立即追加到当天日记，不等 cron 触发
  3. **归档后做条目校验**：对比日记条目数与 MEMORY.md 新增条目数，不一致时不 push，先补全再 push
- **规则确认即同步**：任何规则、规范、约定一旦确认，立刻写入 MEMORY.md 对应区块，不等下一次 session。

## 全局工作规范

- **Bug 创建流程：** 收到 bug 描述后，直接 spawn 子 agent 执行（runtime="subagent"），子 agent 内使用 `--confirm` 正式创建；主 agent 不等待，立即响应用户，可继续接收新的 bug
- **长任务处理：** 执行前先发一条消息告知"开始了，预计 XX 秒"；真正需要中间播报的任务用子 agent 执行，子 agent 通过 message 工具直接把进度和结果发到 hub-channel；主 agent 保持响应，随时可以打断
- **子 agent 播报规范：** 子 agent 每完成一个关键步骤，立即 message(action=send, channel=hub-channel, target=hub-user) 发送进度；最终结果也由子 agent 直接发给用户，不经过主 agent 中转
- **任务判断标准：** 需要多步工具调用、网络请求、SSH 操作、预计超过 10s 的任务 → 用子 agent + 实时播报；简单读文件、本地计算、快速查询 → 主 agent 直接做
- ⚠️ 不能因为"熟悉这类操作"就跳过判断，每次收到任务都要先评估时长再决定是否用子 agent
- ⚠️ 每次实际执行超过 10s 但没有用子 agent 的任务，事后必须在自我复盘里记录：任务类型、实际耗时、为什么判断失误，方便后续积累判断经验
- **子 agent 模型选择：** 轻量任务（搜索/归档/SSH读文件/播报）用轻量模型；深度推理任务（数值设计/系统设计/立项讨论）用强力模型；具体模型名见 TOOLS.md
- **手动切换：** 深度讨论时哥可发 `/model` 切换，或告知我"用强力模型"，我在子 agent 里指定
- **状态汇报：** 工具调用超时或无输出时立即说明并切换方案，不沉默等催
- **分区判断：** 哥不带前缀说明当前在哪个群，由我根据消息内容自行判断所属分区

## 全局工具权限

### Google Sheets 访问
- **token 路径：** `/root/.openclaw/workspace/google_token.json`
- **账号：** xieyuntian@nibirutech.com
- **权限范围：** spreadsheets（读写）、drive、documents（2026-04-02 扩权，已更新 token）
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

### Datain API 配置（2026-04-02 首次配置）
- **API Key：** 43ac2313-714c-4756-b6fa-ca4763ca9059
- **已写入：** ~/.bashrc 持久化
- **X3 游戏编码：** 1090，环境：TRINO_HF

---

## [数据查询记录]

**2026-04-02：海妖拥有量统计（截止4月2日）**
- 定义：`ods_user_hero` 表中 `change_type='11', attribute3='1'` 为获得海妖（等级1）；`hero_id` 以 `4001` 开头为海妖类型
- 两日去重 DAU：13,135人
- 持有情况：仅拥有 40011001（174人，1.32%）、仅拥有 40011002（292人，2.22%）、两只都有（69人，0.53%）、合计持有（535人，4.07%）
- R级规律：R级越高渗透率越高；40011002 在中R以上明显更受欢迎

**2026-04-02：4.1日收入数据**
- 4.1日总收入：$17,361；环比前一日 +59.96%；环比上周同日 +66.96%；同比去年 +409.5%
- 海妖收入占比：4.1日 $8,608（49.58%，221人付费）；4.2日截至上午 $6,716（60.20%，195人付费）
- 月收入预估（中性）：海妖带来月增量约 $90,000~$180,000，对应月收入提升 +43%~+57%

---

## 自我复盘（全局）

- **2026-03-19：** SSH 连接信息未及时记录，导致哥重复提供 → 改进：重要信息当场写入 MEMORY.md
- **2026-03-19：** Property.xlsx 多次读取失败仍继续尝试，浪费时间 → 改进：连续失败2次立即换策略或告知哥
- **2026-03-19：** Mecha 数值对比时误读列顺序，把橙色/紫色声望列搞反，误报大量差异 → 改进：读设计文档前必须先打印表头确认列结构，不能假设列顺序
- **2026-03-19：** MechaSkill 配置规律检查——40000801 PropNum Lv1 填了 1400 应为 -1400，漏了负号。同类减伤技能 PropNum 全级应为负数，配置时要检查同组数值符号一致性
- **2026-03-20：** 工具调用超时或无输出时没有主动告知，沉默等哥来催 → 改进：每次工具调用结束必须主动汇报状态；超时或无输出立即说明并切换方案，不等催；长任务中间加进度播报
- **2026-03-20 gen_i18n 脚本分析任务：** SSH 读文件 + 多次 scp + grep 分析，实际耗时约 40s，应用子 agent 但直接自己跑了 → 判断失误原因：看到 SSH 操作就习惯性直接做，没有先估时长
- **2026-03-24 早间播报任务：** write 工具的 content 参数是必填的，不能只传 file_path，否则会报 validation failed
- **2026-03-26 Jira 子 agent 多次失败：** spawn 子 agent 创建 Bug 时，子 agent 反复卡在"找 env 文件"阶段无法完成 → 改进：子 agent 连续两次返回无效结果后，直接主 agent 用 python3 调 Jira REST API 创建，不再重试子 agent；同时记录直接调 API 的方式（读 ~/.env.jira → requests.post）作为兜底方案
- **2026-03-26 jira-bug-creator skill 路径问题：** skill 脚本路径硬编码为 Windows（c:\Users\caoxinying\...），在 Linux 环境下无法直接调用 → 兜底方案：直接用 python3 + requests 调 Jira REST API，不依赖 skill 脚本
- **2026-03-31 早间同步失败：** 09:30 cron 触发早间同步，web_fetch 成功拉取 GitHub MEMORY.md，但 write 工具调用时漏传 content 参数，导致写入失败（同 03-24 的老问题）→ 强化记忆：write 工具必须同时传 file_path + content，缺一不可，调用前心理默念一遍
- **2026-03-31 子 agent 反复返回意图而非结果：** 两个子 agent（游戏分析任务）运行超过 8-13 分钟，最终只返回"现在我来生成..."的意图描述，没有实际执行 → 根因推测：子 agent token 消耗过大导致上下文截断，或任务拆解过细导致 agent 陷入规划循环 → 改进：子 agent 任务描述要聚焦单一目标，避免在一个 task 里塞入"收集+分析+生成+传输"四步；超过 10 分钟无实质结果时主 agent 直接接管执行
- **2026-03-31 Google token 权限不足：** token scopes 仅 spreadsheets.readonly，无法创建 Docs/Sheets → 需要重新走 OAuth 授权扩展 scope（drive 或 docs 写权限）才能输出到 Google 文档；当前兜底方案：生成 .docx 通过 SCP 传到 Windows
- **2026-04-02 Google token 已扩权：** 重新走 OAuth 授权，新增 spreadsheets（读写）、drive、documents scope，token 已更新，后续可直接输出到 Google Docs/Sheets
- **2026-03-26 规则确认：** 哥直接描述问题现象 = 提 bug，不做代码排查，直接提单。收到问题描述时先判断意图（有"帮我查/为什么"→排查；直接描述现象→提单）

## 数据检查经验积累

- **减伤/负向属性**：PropNum 应为负数，若某级出现正数需立即核查
- **跨品质对比**：紫色/橙色同字段列顺序不一定相同，读表前先确认表头
- **规律性检查**：同一技能组各级数值应呈线性增长，出现断层或符号异常即为错误
- **设计文档对比**：先打印表头行确认列映射，再做数值比对

[[END_MARKER_SANITIZED]]
<<<END_EXTERNAL_UNTRUSTED_CONTENT id="ff5c70e9f1c10f1c">>>