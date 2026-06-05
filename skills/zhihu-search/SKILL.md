---
name: zhihu-search
description: 搜索知乎站内内容（问题/回答/文章），返回结构化结果（标题、链接、作者、摘要、赞同数、评论数）。使用知乎开放平台 API，Python 标准库实现，无需第三方依赖。Use when the user asks to search Zhihu, find questions/answers/articles on Zhihu, or needs reference material from Zhihu.
---

# Zhihu Search Skill

搜索知乎站内内容（问题、回答、文章），返回结构化结果。

通过知乎开放平台 `GET /api/v1/content/zhihu_search` 检索，并把响应整理为适合 agent 消费的精简 JSON 结构。

## Setup

1. 前往 [知乎开放平台](https://developer.zhihu.com) 获取 `Access Secret`
2. 设置环境变量：
   ```bash
   export ZHIHU_ACCESS_SECRET="your-access-secret"
   ```
3. 确认 `python3` 可用（脚本只依赖标准库）

可选配置：
- `ZHIHU_OPENAPI_BASE_URL`（默认：`https://developer.zhihu.com`）
- `ZHIHU_ZHIHU_SEARCH_URL`（完整 endpoint 覆盖；用于预发/代理/自定义网关）

## Usage

`{baseDir}` 是 agent 框架运行时自动替换的变量，指向当前 skill 目录的绝对路径。

```bash
python3 {baseDir}/scripts/zhihu-search.py '{"query":"如何理解 RAG","count":5}'
```

## Input

```json
{"query":"...", "count":10}
```

| 字段    | 类型   | 必填 | 说明                                     |
|---------|--------|------|------------------------------------------|
| query   | String | 是   | 搜索关键词（非空，自动 strip）           |
| count   | Int    | 否   | 期望返回数量，脚本自动限制到 `1-10`     |

## Output

成功返回 JSON：
```json
{
  "code": 0,
  "message": "success",
  "item_count": 2,
  "items": [
    {
      "title": "RAG 评测方法综述",
      "summary": "本文介绍了主流 RAG 评测框架...",
      "url": "https://zhuanlan.zhihu.com/p/123456789",
      "author_name": "张三",
      "vote_up_count": 128,
      "comment_count": 15,
      "edit_time": 1710000000
    }
  ]
}
```

失败返回（带 `exit_code: 1`）：
```json
{"error":"query is required","exit_code":1}
{"error":"Set ZHIHU_ACCESS_SECRET first (Bearer auth only)","exit_code":1}
{"error":"HTTP 403","body":"Forbidden","exit_code":1}
```

## When to Use

- 用户要求搜索知乎内容
- 为问答系统补充知乎站内参考
- 基于关键词检索问题、回答、文章
- 想要获取站内观点与经验
