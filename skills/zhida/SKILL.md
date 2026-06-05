---
name: zhida
description: 调用知乎直答 API（zhida-fast-1p5 / zhida-thinking-1p5 / zhida-agent），返回结构化回答（content + reasoning_content）。OpenAI Chat Completions 风格输入，Python 标准库实现。Use when the user wants a Zhihu-native answer, deep reasoning via zhihu zhihu-direct-answer, or needs zhida-fast / zhida-thinking / zhida-agent responses.
---

# Zhida Skill

调用知乎开放平台的 `zhida` 直答 API，使用 Chat Completions 风格输入。

## Setup

1. 前往 [知乎开放平台](https://developer.zhihu.com) 获取 `Access Secret`
2. 设置环境变量：
   ```bash
   export ZHIHU_ACCESS_SECRET="your-access-secret"
   ```
3. 确认 `python3` 可用

可选配置：
- `ZHIHU_OPENAPI_BASE_URL`（默认：`https://developer.zhihu.com`）
- `ZHIHU_ZHIDA_URL`（完整 endpoint 覆盖；设置后优先）

## Usage

```bash
python3 {baseDir}/scripts/zhida.py '{"model":"zhida-thinking-1p5","messages":[{"role":"user","content":"什么是 RAG？"}]}'
```

## Input

OpenAI 风格 body：
```json
{
  "model": "zhida-agent",
  "messages": [{"role":"user","content":"..."}]
}
```

| 字段     | 类型            | 必填 | 说明                                             |
|----------|-----------------|------|--------------------------------------------------|
| model    | String          | 是   | 模型档位，不能为空                               |
| messages | Array[Message]  | 是   | 对话消息列表，非空                               |
| stream   | Bool            | 否   | 当前脚本仅支持非流式                             |

### 可选模型

- `zhida-fast-1p5` — 通用问答
- `zhida-thinking-1p5` — 强调推理质量
- `zhida-agent` — 复杂任务、需要更强规划能力

## Output

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

失败（带 `exit_code: 1`）：
```json
{"error":"messages is required","exit_code":1}
{"error":"model is required","exit_code":1}
{"error":"HTTP 400","body":{"error":{"message":"invalid model","type":"invalid_request_error","param":"model","code":"model_not_found"}},"exit_code":1}
```

## When to Use

- 用户想要知乎直答的回答（带站内知识增强）
- 需要 zhida-thinking 的推理过程
- 在多轮对话中调用单轮回答生成
- 内容总结与归纳、概念解释
