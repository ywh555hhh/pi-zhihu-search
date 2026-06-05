# pi-zhihu-search

> 知乎开放平台搜索能力 **pi skill 四合一**：知乎站内搜索 + 知乎直答 + 全网搜索 + 知乎热榜

一个 npm 包，把知乎开放平台的四个搜索/问答 API 封装成 [pi coding agent](https://github.com/earendil-works/pi) 可直接加载的 skill。**零第三方依赖**（只用 Python 标准库），**一条命令安装**。

[![npm version](https://img.shields.io/npm/v/pi-zhihu-search.svg)](https://www.npmjs.com/package/pi-zhihu-search)
[![npm downloads](https://img.shields.io/npm/dm/pi-zhihu-search.svg)](https://www.npmjs.com/package/pi-zhihu-search)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pi-package](https://img.shields.io/badge/pi--package-%E2%9C%93-blue)](https://pi.dev/packages)

## ✨ 功能

| Skill | 说明 |
|------|------|
| 🔍 `zhihu-search` | 知乎站内搜索（问题/回答/文章），返回结构化结果 |
| 💬 `zhida` | 知乎直答（zhida-fast-1p5 / zhida-thinking-1p5 / zhida-agent） |
| 🌐 `global-search` | 全网搜索，支持 `filter` 高级语法 + realtime/static 索引 |
| 🔥 `hot-list` | 知乎热榜（最多 30 条），含缩略图与摘要 |

## 📦 安装

```bash
# 一键安装到 pi（用户级别，所有项目可用）
pi install npm:pi-zhihu-search

# 或者项目级别
pi install -l npm:pi-zhihu-search

# 也可以直接从 GitHub 装最新开发版
pi install git:github.com/ywh555hhh/pi-zhihu-search
```

安装完成后重启 pi，四个 skill 会被自动加载，输入 `/skill:zhihu-search` 即可调用。

## 🔑 配置

> ⚠️ **安全提醒**：永远不要把 Access Secret 写进代码、`.env` 文件或提交到 Git。本项目只通过**环境变量**读取。

### 1. 获取 Access Secret

前往 [知乎开放平台](https://developer.zhihu.com) 申请一个 Access Secret。

### 2. 设置环境变量

**macOS / Linux**：加入 `~/.zshrc` 或 `~/.bashrc`：
```bash
export ZHIHU_ACCESS_SECRET="your-access-secret-here"
```

**Windows PowerShell**：
```powershell
[System.Environment]::SetEnvironmentVariable("ZHIHU_ACCESS_SECRET", "your-access-secret-here", "User")
```

### 3. 可选配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `ZHIHU_OPENAPI_BASE_URL` | `https://developer.zhihu.com` | 自定义网关/代理时改这个 |
| `ZHIHU_ZHIHU_SEARCH_URL` | `${BASE}/api/v1/content/zhihu_search` | 单独覆盖知乎搜索 endpoint |
| `ZHIHU_ZHIDA_URL` | `${BASE}/v1/chat/completions` | 单独覆盖直答 endpoint |
| `ZHIHU_GLOBAL_SEARCH_URL` | `${BASE}/api/v1/content/global_search` | 单独覆盖全网搜索 endpoint |
| `ZHIHU_HOT_LIST_URL` | `${BASE}/api/v1/content/hot_list` | 单独覆盖热榜 endpoint |

## 🚀 使用

### 在 pi 中调用

启动 pi 后，agent 会自动看到这些 skill 并在合适的时机调用它们。你也可以直接用命令：

```
/skill:zhihu-search
```

agent 会询问你要搜索什么，然后把结果整理给你。

### 命令行直接调用

每个 skill 的脚本都是独立可执行的，方便测试和集成：

```bash
# 知乎站内搜索
python3 skills/zhihu-search/scripts/zhihu-search.py \
  '{"query":"RAG 评测方法","count":5}'

# 知乎直答（带思考链）
python3 skills/zhida/scripts/zhida.py \
  '{"model":"zhida-thinking-1p5","messages":[{"role":"user","content":"什么是 RAG？"}]}'

# 全网搜索（带 filter 限定域名）
python3 skills/global-search/scripts/global-search.py \
  '{"query":"人工智能","count":5,"filter":"host==\"36kr.com\""}'

# 知乎热榜
python3 skills/hot-list/scripts/hot-list.py '{"limit":10}'
```

## 📊 输出示例

### zhihu-search
```json
{
  "code": 0,
  "message": "success",
  "item_count": 2,
  "items": [
    {
      "title": "RAG 评测方法综述",
      "summary": "本文介绍了主流 RAG 评测框架，包括 RAGAS、TruLens ...",
      "url": "https://zhuanlan.zhihu.com/p/123456789",
      "author_name": "张三",
      "vote_up_count": 128,
      "comment_count": 15,
      "edit_time": 1710000000
    }
  ]
}
```

### zhida
```json
{
  "code": 0,
  "id": "chatcmpl-xxxx",
  "model": "zhida-thinking-1p5",
  "content": "RAG 是 Retrieval-Augmented Generation 的缩写...",
  "reasoning_content": "先解释缩写，再说明工作流程与价值。",
  "finish_reason": "stop"
}
```

### global-search
```json
{
  "code": 0,
  "message": "success",
  "item_count": 2,
  "items": [
    {
      "title": "人工智能发展趋势与展望",
      "summary": "近年来，人工智能（AI）的发展速度令人瞩目 ...",
      "url": "https://example.com/article",
      "author_name": "张三",
      "edit_time": 1710000000
    }
  ]
}
```

### hot-list
```json
{
  "code": 0,
  "message": "success",
  "total": 10,
  "item_count": 10,
  "items": [
    {
      "title": "如何评价某个热点问题？",
      "url": "https://www.zhihu.com/question/123456789",
      "thumbnail_url": "https://pic1.zhimg.com/v2-d4b0f8...jpg",
      "summary": "这是该问题的内容摘要"
    }
  ]
}
```

## 🛠️ 系统要求

- **Python 3.7+**（脚本只用标准库，零第三方依赖）
- **网络**访问 `developer.zhihu.com`
- **pi coding agent**（也兼容 Claude Code、Codex CLI、Amp、Droid 等支持 Agent Skills 标准的工具）

## ❓ 常见问题

<details>
<summary>报错 <code>Set ZHIHU_ACCESS_SECRET first (Bearer auth only)</code></summary>

环境变量没设好。重新执行 `export` 后**新开一个终端**，或者用 `echo $ZHIHU_ACCESS_SECRET` 确认能打印出来。
</details>

<details>
<summary>报错 <code>HTTP 403</code> 或 <code>HTTP 401</code></summary>

Access Secret 无效或过期。回 [知乎开放平台](https://developer.zhihu.com) 重新生成。
</details>

<details>
<summary>想换 API 网关（公司内网代理、预发环境）</summary>

设置对应的 `_URL` 环境变量即可，例如 `export ZHIHU_OPENAPI_BASE_URL="https://internal-proxy.example.com"`。
</details>

<details>
<summary>想用流式输出 zhida？</summary>

当前版本只支持非流式。流式支持会随官方 API 一起来，下个版本会加。
</details>

## 🗂️ 项目结构

```
pi-zhihu-search/
├── package.json                  # pi package manifest
├── README.md                     # 本文件
├── LICENSE                       # MIT
├── .gitignore
└── skills/
    ├── zhihu-search/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── zhihu-search.py
    ├── zhida/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── zhida.py
    ├── global-search/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── global-search.py
    └── hot-list/
        ├── SKILL.md
        └── scripts/
            └── hot-list.py
```

## 🤝 贡献

欢迎 PR 和 issue！如果知乎开放平台加了新 API 或者改了协议，提个 issue 一起完善。

## 📄 License

MIT © 2025 [ywh555hhh](https://github.com/ywh555hhh)

## 🙏 致谢

- [知乎开放平台](https://developer.zhihu.com) — 提供底层 API
- [pi coding agent](https://github.com/earendil-works/pi) — 极简的 terminal coding agent
- [Agent Skills 标准](https://agentskills.io/specification) — skill 格式规范
