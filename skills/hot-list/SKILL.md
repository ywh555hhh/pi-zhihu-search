---
name: hot-list
description: 获取知乎热榜列表（标题、链接、缩略图、摘要），适合热点追踪、内容推荐、趋势发现。Use when the user wants Zhihu trending topics, hot questions, or current popular content on Zhihu.
---

# Hot List Skill

获取知乎当前热榜（最多 30 条），返回标题、链接、缩略图、摘要。

## Setup

1. 前往 [知乎开放平台](https://developer.zhihu.com) 获取 `Access Secret`
2. 设置环境变量：
   ```bash
   export ZHIHU_ACCESS_SECRET="your-access-secret"
   ```

可选配置：
- `ZHIHU_OPENAPI_BASE_URL`（默认：`https://developer.zhihu.com`）
- `ZHIHU_HOT_LIST_URL`（完整 endpoint 覆盖）

## Usage

```bash
python3 {baseDir}/scripts/hot-list.py '{"limit":10}'
```

## Input

```json
{"limit":10}
```

| 字段  | 类型 | 必填 | 说明                          |
|-------|------|------|-------------------------------|
| limit | Int  | 否   | 期望返回数量，默认 `30`，最大 `30` |

## Output

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

`thumbnail_url` 和 `summary` 始终返回字符串，无数据时为空字符串。

## When to Use

- 获取当前知乎热点内容
- 为助手提供热点推荐素材
- 趋势观察与热点发现
- 内容创作的选题参考
