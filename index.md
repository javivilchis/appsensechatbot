---
layout: home
title: "Bitcoin Blog Bot"
---

Welcome to the Bitcoin Weekly Blog — generated every Monday by an AI agent.

### How to run project
clone the script, once you download it make sure you have your open ai key added to your terminal and then run:
`export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx` this will add it to your env file within your system to be used within the project since we are runnning it using python.

after that, navigate to where we have the 'generate_blog.py' this is to run it manually before you deploy it to github pages.
after that, run the following script: `python generate_blog.py` 

you should see the generated blog inside the ./posts/ folder.