# bitcoin_blog_bot/generate_blog.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
# generate_blog.py
from openai import OpenAI
import os
# bitcoin_blog_bot/generate_blog.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mapping categories to prompts and source URLs
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
}


def scrape_urls(urls):
    contents = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all('p')
            text = "\n".join(p.get_text() for p in paragraphs)
            contents.append(text[:3000])
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return contents


def generate_blog(category: str) -> str:
    config = CATEGORY_CONFIG.get(category.lower())

    if not config:
        raise ValueError(f"Unknown category '{category}'. Available: {list(CATEGORY_CONFIG.keys())}")

    sources = scrape_urls(config["urls"])

    prompt = f"""
        {config["prompt"]}

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
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def save_blog_to_file(blog_post, category):
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"_posts/{today}-{category}-weekly-update.md"
    os.makedirs("_posts", exist_ok=True)
    with open(filename, "w") as f:
        f.write(f"""---
title: \"Weekly {category.capitalize()} Update - {today}\"
date: {today}
layout: post
---

{blog_post}
""")
    print(f"Saved blog as {filename}")


if __name__ == "__main__":
    category = "flow"  # change this to "ai" or "google-ai" as needed
    blog = generate_blog(category)
    save_blog_to_file(blog, category)