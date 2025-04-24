# AppSense ChatBot 🤖

AppSenseChatBot is a smart, Python-powered chatbot that leverages the OpenAI API for intelligent responses, along with BeautifulSoup and Requests for web scraping and dynamic data fetching.

## 📦 Features

- 🧠 OpenAI-powered natural language understanding
- 🌐 Web scraping with BeautifulSoup
- 🔗 Fetch and process live data using Requests
- 🧩 Modular, extensible Python architecture
- 📝 Ideal for chat, content summarization, or info extraction tasks

## 🛠️ Requirements

- Python 3.8+
- `openai`
- `beautifulsoup4`
- `requests`

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/javivilchis/appsensechatbot.git
cd appsensechatbot
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

or manually
```bash
pip install openai beautifulsoup4 requests
```
### 4. Set up your environment variables
Create a .env file in the root directory with your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key
```

You can also directly export it in your shell:
```bash
export OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the chatbot
```bash
python main.py
```
Or modify main.py as needed to suit your interaction style.

### 📁 Project Structure

```
appsensechatbot/
├── main.py
├── chatbot.py
├── utils/
│   └── scraper.py
├── .env
├── requirements.txt
└── README.md
```

### 🔍 Example Use Cases
	•	Chat-style Q&A powered by OpenAI
	•	Summarizing web articles
	•	Auto-fetching and parsing live content
	•	Intelligent responses based on external data

### 🧪 Testing

Basic testing can be done by running main.py. Unit tests can be added under a tests/ folder using unittest or pytest.

### 📄 License

### MIT © Javi Vilchis
