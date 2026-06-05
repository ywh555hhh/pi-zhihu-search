---
name: global-search
description: 搜索全网内容（知乎站外），返回结构化结果。支持高级 filter 语法和实时/静态索引库选择。Use when the user wants web-wide search, broader coverage than Zhihu alone, or needs to filter by host/date with `host=="x.com" AND publish_time>=...` syntax.
---

# Global Search Skill

调用知乎开放平台的 `global_search` API，检索全网公开内容，并返回结构化结果。

> 站内（知乎）请使用 `zhihu-search` skill 以获得更聚焦的结果。

## Setup

1. 前往 [知乎开放平台](https://developer.zhihu.com) 获取 `Access Secret`
2. 设置环境变量：
   ```bash
   export ZHIHU_ACCESS_SECRET="your-access-secret"
   ```

可选配置：
- `ZHIHU_OPENAPI_BASE_URL`（默认：`https://developer.zhihu.com`）
- `ZHIHU_GLOBAL_SEARCH_URL`（完整 endpoint 覆盖）

## Usage

```bash
python3 {baseDir}/scripts/global-search.py '{"query":"人工智能","count":5,"search_db":"all"}'
```

带高级筛选：
```bash
python3 {baseDir}/scripts/global-search.py '{"query":"人工智能","count":10,"filter":"host==\"example.com\" AND publish_time>=1778494631","search_db":"realtime"}'
```

## Input

```json
{
  "query": "...",
  "count": 10,
  "filter": "host==\"example.com\" AND publish_time>=1778494631",
  "search_db": "all"
}
```

| 字段       | 类型   | 必填 | 说明                                                                 |
|------------|--------|------|----------------------------------------------------------------------|
| query      | String | 是   | 搜索关键词                                                           |
| count      | Int    | 否   | 期望返回数量，脚本自动限制到 `1-20`                                |
| filter     | String | 否   | 高级语法筛选表达式，例如 `host=="x.com" AND publish_time>=1778494631` |
| search_db  | String | 否   | `all` / `realtime` / `static`，默认 `all`                            |

## Output

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

## When to Use

- 需要更广覆盖范围的内容检索
- 对某一主题进行快速信息扩展
- 用 filter 精确控制来源域名/时间范围
- 选择 realtime 索引获取最新内容
