---
name: github-trending-daily
description: |
  每日自动获取 GitHub Trending 热门项目，筛选新项目并检测持续飙升项目。
  
  使用场景：
  1. 追踪 GitHub 每日热门开源项目
  2. 发现新上榜的有趣项目
  3. 监控持续受欢迎的项目趋势
  
  功能特点：
  - 并发请求加速（2秒内完成）
  - 智能中文标签生成（AI、智能体、代码等）
  - 跨天对比检测新上榜 vs 持续飙升项目
  - 本地缓存机制避免重复展示
  
  输出格式：
  - 新项目：完整信息（⭐、🔧语言、📝简介、🔗链接）
  - 持续飙升：单独列出，含完整信息
---

# GitHub Trending Daily

每日自动获取 GitHub Trending 热门项目，智能筛选并生成中文简介。

## 使用方法

### 基本用法

```bash
python3 scripts/github-trending-daily.py --top 10 --days 14
```

### 参数说明

- `--top N`：返回前 N 个项目（默认 10）
- `--days N`：筛选近 N 天创建的项目（默认 14）
- `--language LANG`：按编程语言过滤（如 python, typescript）
- `--output FILE`：输出 JSON 文件

### 环境变量

```bash
export GITHUB_TOKEN=your_token  # 提高 API 限流
```

## 输出示例

```
📊 今日新上榜项目：

【1】CodebuffAI/codebuff
⭐ 4,101 | 🔀 471 | 🔧 TypeScript
📝 【代码】终端代码生成工具
🔗 https://github.com/CodebuffAI/codebuff

📈 持续飙升项目（昨天也在榜）：
• anthropics/prompt-eng-interactive-tutorial
⭐ 32,976 | 🔧 Jupyter Notebook
📝 【教程、提示词】Anthropic 交互式提示词工程教程
```

## 缓存机制

- **缓存位置**：`~/.cache/github-trending/previous_top10.json`
- **作用**：存储前一天榜单，用于对比检测新项目
- **清理**：建议设置定时任务每周清理一次

## 实现原理

1. **抓取**：请求 GitHub Trending 页面获取热门项目
2. **并发**：使用 ThreadPoolExecutor 并发获取项目详情
3. **摘要**：关键词匹配生成中文标签和简介
4. **对比**：加载本地缓存，检测新项目 vs 持续飙升
5. **输出**：格式化输出，更新缓存供下次使用

## 性能

- 总耗时：约 2 秒（并发优化后）
- 并发数：10 线程
- API 超时：5 秒

## 依赖

- Python 3.8+
- requests
- beautifulsoup4
