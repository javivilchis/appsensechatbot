# bitcoin_blog_bot/generate_blog.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
# generate_blog.py
from openai import OpenAI
import os

def search_and_scrape_bitcoin_articles():
    urls = [
        "https://www.coindesk.com/markets/2025/04/15/bitcoin-price-analysis/",
        "https://bitcoinmagazine.com/markets/bitcoin-weekly-update",
    ]

    contents = []
    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all('p')
            text = "\n".join(p.get_text() for p in paragraphs)
            contents.append(text[:3000])
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return contents



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_bitcoin_blog(content_list):
    prompt = f"""
        You are a professional financial blogger. Write a new weekly blog post about Bitcoin.

        Use the following articles as source material, but write everything in your own words.
        Be engaging, clear, and insightful. The post should be 600–800 words.

        IMPORTANT: Format the output as a full HTML document, including the following structure:
        <html>
        <head>
            <title>Weekly Bitcoin Blog</title>
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

    {''.join(content_list)}
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a finance blogger that outputs HTML-formatted blog posts."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a finance blogger."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

def save_blog_to_file(blog_post):
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"_posts/{today}-bitcoin-weekly-update.md"
    os.makedirs("_posts", exist_ok=True)
    with open(filename, "w") as f:
        f.write(f"""---
title: \"Weekly Bitcoin Update - {today}\"
date: {today}
layout: post
---

{blog_post}
""")
    print(f"Saved blog as {filename}")

if __name__ == "__main__":
    articles = search_and_scrape_bitcoin_articles()
    blog = generate_bitcoin_blog(articles)
    save_blog_to_file(blog)

