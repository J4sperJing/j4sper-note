---
title: 0-入门概念
description: agent的入门概念
date: 2026-09-15
tags:
  - books
  - ai-agent-book
---
# Agent组成

一个最小极简的agent，需要：
**Agent = LLM + 上下文 + 工具**

对于生产可用的，harness工程所做的：
**Agent = Model + Harness**
**Harness = 上下文管理 + 工具接口 + 约束 + 验证 + 纠正**

加入了 约束、验证、纠正，来约束agent 能做的范围、 结果是否正确、错误时如何补救

