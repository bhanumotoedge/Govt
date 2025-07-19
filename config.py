import os

# AI API Keys

AI_KEYS = {
“gemini1”: os.environ.get(“GEMINI1_KEY”),
“gemini2”: os.environ.get(“GEMINI2_KEY”),
“gemini3”: os.environ.get(“GEMINI3_KEY”),
“together”: os.environ.get(“TOGETHER_KEY”),
“openrouter”: os.environ.get(“OPENROUTER_KEY”),
“deepinfra”: os.environ.get(“DEEPINFRA_KEY”),
“deepseek”: os.environ.get(“DEEPSEEK_KEY”)
}

# News API Keys

NEWS_KEYS = {
“gnews”: os.environ.get(“GNEWS_KEY”),
“newsapi”: os.environ.get(“NEWSAPI_KEY”)
}

# Discord Bot Token

DISCORD_TOKEN = os.environ.get(“DISCORD_TOKEN”)

# Validate critical environment variables

if not DISCORD_TOKEN:
raise ValueError(“DISCORD_TOKEN environment variable is required”)

print(“✅ Config loaded successfully”)
