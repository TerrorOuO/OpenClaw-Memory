#!/usr/bin/env python3
"""
每日 AI 新闻摘要脚本
信源：
  1. Hacker News Algolia API（稳定，支持按热度排序）
  2. The Rundown AI 首页文章列表
过滤：排除纯研究/论文类，保留应用/产品/工具/商业类
"""

import urllib.request
import urllib.parse
import json
import re
from datetime import datetime, timezone, timedelta

EXCLUDE_KEYWORDS = ['arxiv', 'paper', 'benchmark', 'dataset', 'preprint', 'survey', 'theorem', 'proof']

def fetch_hn_ai_news():
    """用 HN Algolia API 抓昨天的 AI 相关热门帖子"""
    tz8 = timezone(timedelta(hours=8))
    yesterday = datetime.now(tz8) - timedelta(days=1)
    ts_start = int(yesterday.replace(hour=0, minute=0, second=0).timestamp())
    ts_end   = int(yesterday.replace(hour=23, minute=59, second=59).timestamp())

    queries = ['AI', 'LLM', 'OpenAI', 'Claude', 'Gemini', 'ChatGPT', 'agent']
    seen, items = set(), []

    for q in queries:
        params = urllib.parse.urlencode({
            'query': q,
            'tags': 'story',
            'numericFilters': f'created_at_i>{ts_start},created_at_i<{ts_end},points>10',
            'hitsPerPage': 20
        })
        url = f'https://hn.algolia.com/api/v1/search?{params}'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            r = urllib.request.urlopen(req, timeout=15)
            data = json.loads(r.read())
        except Exception as e:
            print(f'HN fetch error ({q}):', e)
            continue

        for hit in data.get('hits', []):
            title = (hit.get('title') or '').strip()
            link  = hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            points   = hit.get('points') or 0
            comments = hit.get('num_comments') or 0
            oid = hit.get('objectID')

            if not title or oid in seen:
                continue
            seen.add(oid)

            title_lower = title.lower()
            if any(kw in title_lower for kw in EXCLUDE_KEYWORDS):
                continue
            if 'arxiv.org' in link:
                continue

            score = points + comments * 0.5
            items.append({
                'title': title,
                'link': link,
                'points': points,
                'comments': comments,
                'score': score,
                'hn_link': f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            })

    return sorted(items, key=lambda x: x['score'], reverse=True)


def fetch_rundown_latest():
    """抓取 The Rundown AI 最新文章"""
    url = 'https://www.therundown.ai'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=15)
        html = r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print('Rundown fetch error:', e)
        return []

    pattern = r'href="(/p/[a-z0-9\-]+)"'
    paths = list(dict.fromkeys(re.findall(pattern, html)))  # 去重保序

    # 提取标题：找 <a href="/p/xxx">标题</a>
    title_pattern = r'href="(/p/[a-z0-9\-]+)"[^>]*>\s*([^<]{15,}?)\s*(?:PLUS:|<)'
    title_map = {}
    for path, title in re.findall(title_pattern, html):
        if path not in title_map:
            title_map[path] = title.strip()

    items = []
    for path in paths[:6]:
        title = title_map.get(path)
        if not title:
            # 从 path 生成可读标题
            title = path.replace('/p/', '').replace('-', ' ').title()
        items.append({
            'title': title,
            'link': f'https://www.therundown.ai{path}',
            'source': 'The Rundown AI'
        })
    return items


def build_digest():
    tz8 = timezone(timedelta(hours=8))
    yesterday = (datetime.now(tz8) - timedelta(days=1)).strftime('%Y-%m-%d')

    hn_items     = fetch_hn_ai_news()
    rundown_items = fetch_rundown_latest()

    combined = []
    hn_titles = {i['title'].lower() for i in hn_items}

    for item in hn_items:
        combined.append({
            'title': item['title'],
            'link':  item['link'],
            'meta':  f"🔥 {item['points']}分 · {item['comments']}评论 · Hacker News"
        })

    for item in rundown_items:
        if item['title'].lower() not in hn_titles:
            combined.append({
                'title': item['title'],
                'link':  item['link'],
                'meta':  '📰 The Rundown AI'
            })

    top10 = combined[:10]
    if not top10:
        return f'🤖 AI 日报 {yesterday}\n\n暂无数据，可能是节假日或信源无更新。'

    lines = [f'🤖 AI 日报 {yesterday}（热度 Top {len(top10)}）\n']
    for i, item in enumerate(top10, 1):
        lines.append(f"{i}. {item['title']}")
        lines.append(f"   {item['meta']}")
        lines.append(f"   {item['link']}\n")

    return '\n'.join(lines)


if __name__ == '__main__':
    print(build_digest())
