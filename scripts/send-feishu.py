#!/usr/bin/env python3
"""
Send GitHub Trending to Feishu
通过飞书 webhook 或 API 发送消息
"""

import json
import os
import sys
import requests


def send_to_feishu_webhook(data, webhook_url):
    """通过飞书 webhook 发送消息"""
    
    # 构建消息内容
    new_repos = data.get('top_repos', [])
    continuing_repos = []
    
    # 从所有项目中找出持续飙升的
    all_repos = data.get('all_repos', [])
    previous_repos = set(data.get('previous_repos', []))
    
    for repo in all_repos:
        if repo['full_name'] in previous_repos:
            continuing_repos.append(repo)
    
    # 构建文本消息
    message = f"🐙 GitHub Trending - {datetime.now().strftime('%Y年%m月%d日')}\n\n"
    
    if new_repos:
        message += "📊 今日新上榜项目：\n\n"
        for i, repo in enumerate(new_repos[:10], 1):
            message += f"【{i}】{repo['full_name']}\n"
            message += f"⭐ {repo['total_stars']:,} | 🔀 {repo['total_forks']:,} | 🔧 {repo.get('language', 'N/A') or 'N/A'}\n"
            message += f"📝 {repo.get('summary', '')}\n"
            message += f"🔗 {repo['url']}\n\n"
    
    if continuing_repos:
        message += "---\n\n📈 持续飙升项目（昨天也在榜）：\n\n"
        for repo in continuing_repos[:5]:  # 只显示前5个
            message += f"• {repo['full_name']}\n"
            message += f"⭐ {repo['total_stars']:,} | 🔧 {repo.get('language', 'N/A') or 'N/A'}\n"
            message += f"📝 {repo.get('summary', '')}\n"
            message += f"🔗 {repo['url']}\n\n"
    
    # Webhook 请求体
    payload = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ 消息发送成功")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False


def main():
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='发送 GitHub Trending 到飞书')
    parser.add_argument('--input', '-i', required=True, help='输入 JSON 文件路径')
    parser.add_argument('--webhook', '-w', help='飞书 webhook URL（或使用环境变量 FEISHU_WEBHOOK）')
    
    args = parser.parse_args()
    
    # 获取 webhook URL
    webhook_url = args.webhook or os.environ.get('FEISHU_WEBHOOK')
    if not webhook_url:
        print("❌ 请提供飞书 webhook URL")
        sys.exit(1)
    
    # 读取数据
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 发送消息
    success = send_to_feishu_webhook(data, webhook_url)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
