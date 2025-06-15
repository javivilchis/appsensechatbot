# bitcoin_blog_bot/generate_blog.py

import os
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
from duckduckgo_search import DDGS
from openai import OpenAI
import xml.etree.ElementTree as ET

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logging.basicConfig(level=logging.INFO)

# Static category configuration
CATEGORY_CONFIG = {
    "bitcoin": {
        "prompt": "You are a professional financial blogger. Write a new weekly blog post about Bitcoin and blockchain market trends.",
        "urls": [
            "https://www.coindesk.com",
            "https://bitcoinmagazine.com/"
        ]
    },
    "ai": {
        "prompt": "You are a professional tech blogger. Write a blog post analyzing AI trends in business, research, and global impact.",
        "urls": [
            "https://www.artificialintelligence-news.com/",
            "https://news.mit.edu/topic/artificial-intelligence2",
            "https://www.wsj.com/tech/ai"
        ]
    },
    "google-ai": {
        "prompt": "You are a developer advocate. Summarize Google's latest AI announcements and innovations in a blog post.",
        "urls": [
            "https://ai.google/latest-news/",
            "https://blog.google/technology/developers/google-io-2025-collection/",
            "https://blog.google/"
        ]
    },
    "flow": {
        "prompt": "You are a professional blogger. Write a blog post about the latest updates and features in Flow using veo3.",
        "urls": [
            "https://labs.google/flow/about#overview",
            "https://labs.google/",
            "https://developers.google.com/flow",
            "https://labs.google/fx/tools/flow/faq"
        ]
    },
    "penny": {
        "prompt": "You are a professional blog post writer and SEO expert with emphasis on engaging content with web development and artificial intelligence.",
        "urls": [
            "https://www.kiplinger.com/personal-finance/farewell-to-the-penny-u-s-treasury-ends-production-of-one-cent-coin",
            "https://www.pbs.org/newshour/nation/u-s-mint-moves-ahead-with-plans-to-kill-the-penny",
            "https://www.cnn.com/2025/05/22/business/us-discontinue-penny"
        ]
    }
}

def scrape_urls(urls):
    contents = []
    for url in urls:
        try:
            logging.info(f"Scraping: {url}")
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all('p')
            text = "\n".join(p.get_text() for p in paragraphs)
            contents.append(text[:3000])
        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")
    return contents

def fetch_urls_from_duckduckgo(query, max_results=5):
    urls = []
    with DDGS() as ddgs:
        logging.info(f"Searching DuckDuckGo for: {query}")
        results = ddgs.text(query, region="wt-wt", safesearch="Moderate", max_results=max_results)
        for r in results:
            if r.get("href"):
                urls.append(r["href"])
    return urls

def generate_blog(category: str) -> str:
    config = CATEGORY_CONFIG.get(category.lower())

    if not config:
        logging.warning(f"Unknown category '{category}', using DuckDuckGo fallback.")
        fallback_urls = fetch_urls_from_duckduckgo(category, max_results=5)
        if not fallback_urls:
            raise ValueError(f"No results found for category '{category}' via DuckDuckGo.")
        prompt = f"You are a professional content writer. Write a blog post based on recent updates and insights related to '{category}'."
        sources = scrape_urls(fallback_urls)
    else:
        prompt = config["prompt"]
        sources = scrape_urls(config["urls"])

    full_prompt = f"""
{prompt}
Make the blog post sound as human and as engaging as possible, add real world examples and make it as informative as possible.

Use the following articles as source material, but write everything in your own words.
Be engaging, clear, and insightful. The post should be 600–800 words.

IMPORTANT: Format the output as a full HTML document, including the following structure:
<html>
<head>
    <title>Weekly Blog Update</title>
</head>
<body>
    <h1>Title of the Blog</h1>
    <h2>Subtitle with date and author</h2>
    <p>Intro paragraph with strong opinion or overview.</p>
    <p>Use <strong>bold</strong> text for key points and <a href="https://example.com" title="Example Link" target="_blank">links</a> where helpful.</p>
    ...
</body>
</html>

Do NOT escape the HTML (no backslashes before tags). Just return the clean HTML content.

Here are the sources to draw insights from:

{"".join(sources)}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior blogger that outputs HTML-formatted articles."},
            {"role": "user", "content": full_prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def update_index_html():
    posts_dir = "_posts"
    post_files = sorted(
        [f for f in os.listdir(posts_dir) if f.endswith(".md")],
        reverse=True
    )

    list_items = "\n".join(
        [f'<li><a href="{fname}">{fname.replace("-", " ").replace(".md", "").title()}</a></li>'
         for fname in post_files]
    )

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Weekly Blog Posts</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f9f9f9;
            color: #222;
            padding: 2rem;
            margin: 0;
            animation: fadeIn 1s ease-in-out;
        }}
        h1 {{
            font-size: 2.5rem;
            color: #1a1a1a;
            margin-bottom: 1rem;
        }}
        ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        li {{
            margin-bottom: 1rem;
            padding: 1rem;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }}
        li:hover {{
            transform: translateY(-3px);
        }}
        a {{
            text-decoration: none;
            color: #007acc;
            font-weight: 600;
            font-size: 1.1rem;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: translateY(20px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <h1>Weekly Blog Posts</h1>
    <ul>
        {list_items}
    </ul>
</body>
</html>
"""

    with open(os.path.join(posts_dir, "index.html"), "w") as f:
        f.write(index_html)
    print("Updated _posts/index.html")

def update_rss_feed():
    posts_dir = "_posts"
    rss_file = os.path.join(posts_dir, "rss.xml")

    items = []
    post_files = sorted(
        [f for f in os.listdir(posts_dir) if f.endswith(".md")],
        reverse=True
    )

    for post in post_files:
        date_part = post.split("-")[:3]
        date = "-".join(date_part)
        title = post.replace(".md", "").replace("-", " ").title()
        link = f"https://<YOUR_DOMAIN>/{post}"

        item = f"""
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <pubDate>{date}</pubDate>
            <guid>{link}</guid>
        </item>
        """
        items.append(item)

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Bitcoin Blog Bot RSS Feed</title>
    <link>https://<YOUR_DOMAIN>/</link>
    <description>Daily tech & crypto blog</description>
    {''.join(items)}
</channel>
</rss>"""

    with open(rss_file, "w") as f:
        f.write(rss_content)
    logging.info("RSS feed updated.")

def save_blog_to_file(blog_post, category):
    # Use America/Chicago timezone (Central Time)
    today = datetime.now(ZoneInfo("America/Chicago")).strftime('%Y-%m-%d')
    filename = f"_posts/{today}-{category}-weekly-update.md"
    os.makedirs("_posts", exist_ok=True)

    # SEO metadata block
    seo_meta = f"""
<!-- SEO Meta Tags -->
<meta name="description" content="Explore the latest updates and expert insights on {category}. Stay ahead with our weekly {category} trends and analysis.">
<meta name="keywords" content="{category}, artificial intelligence, machine learning, bitcoin, ai trends, technology blog, updates, weekly blog">
<meta name="author" content="Bitcoin Blog Bot">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""---
title: "Weekly {category.capitalize()} Update - {today}"
date: {today}
layout: post
---

{seo_meta}

{blog_post}
""")
    logging.info(f"Saved blog as {filename}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate blog posts by category.")
    parser.add_argument("--categories", required=True, help="Comma-separated blog categories")
    args = parser.parse_args()

    for category in args.categories.split(","):
        category = category.strip()
        blog = generate_blog(category)
        save_blog_to_file(blog, category)

    update_index_html()
    update_rss_feed()
    import argparse

    parser = argparse.ArgumentParser(description="Generate blog posts by category.")
    parser.add_argument("--categories", required=True, help="Comma-separated blog categories")
    args = parser.parse_args()

    for category in args.categories.split(","):
        category = category.strip()
        blog = generate_blog(category)
        save_blog_to_file(blog, category)

    update_index_html()
    update_rss_feed()