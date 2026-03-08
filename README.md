# GitHub Trending Daily Skill

每日自动获取 GitHub Trending 热门项目，智能筛选新项目并检测持续飙升项目。

## 📦 文件结构

```
github-trending-daily/
├── SKILL.md                           # 技能说明文档
├── scripts/
│   └── github-trending-daily.py       # 主脚本
└── README.md                          # 本文件
```

## 🚀 快速开始

### 安装依赖

```bash
pip3 install requests beautifulsoup4 --break-system-packages
```

### 配置 GitHub Token（可选，提高 API 限流）

```bash
export GITHUB_TOKEN=your_github_token
```

### 运行

```bash
python3 scripts/github-trending-daily.py --top 10 --days 14
```

## 📋 功能特点

1. **并发加速**：使用 ThreadPoolExecutor，2 秒内完成抓取
2. **智能摘要**：关键词匹配生成中文标签（AI、智能体、代码等）
3. **跨天对比**：本地缓存检测新项目 vs 持续飙升项目
4. **格式化输出**：清晰的 ⭐、🔧、📝、🔗 信息展示

## 💡 实现原理

```
┌─────────────────┐
│ 1. 抓取 Trending │ → 请求 GitHub Trending 页面
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. 并发获取详情  │ → ThreadPoolExecutor 10线程并发
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. 生成中文摘要  │ → 关键词匹配自动生成标签
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. 加载昨日缓存  │ → ~/.cache/github-trending/previous_top10.json
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. 对比检测      │ → 新项目加入榜单，重复项目仅提示
└────────┬────────┘
         ▼
┌─────────────────┐
│ 6. 更新缓存      │ → 保存今日榜单供明天对比
└─────────────────┘
```

## 🔧 缓存机制

- **位置**：`~/.cache/github-trending/previous_top10.json`
- **作用**：存储前一天 Top 10 项目列表
- **清理**：建议每周清理一次过期缓存

## 📊 输出示例

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
🔗 https://github.com/anthropics/prompt-eng-interactive-tutorial
```

## ⚡ 性能

- 总耗时：约 2 秒
- 并发数：10 线程
- API 超时：5 秒

## 📄 License

MIT
