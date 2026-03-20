# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## 模型分级（按成本/能力）

| 角色 | 当前模型 | 用途 |
|---|---|---|
| 轻量 | claude-haiku-4-5 | 子 agent 搜索/归档/SSH读文件/播报 |
| 默认 | claude-sonnet-4-6 | 主对话、代码排查、配表分析 |
| 强力 | claude-opus-4-6 | 数值设计、系统设计、立项讨论 |

> 模型换了只改这里，规则不用动。



Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
