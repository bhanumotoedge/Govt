# Government Exam Prep Bot

A Discord bot for Indian government exam preparation with AI-generated quizzes for SSC, Bank, UPSC, and Current Affairs.

## Features

- 📚 **Multiple Exam Support**: SSC (CGL, CHSL, MTS), Bank (PO, Clerk), UPSC
- 🤖 **AI-Generated Quizzes**: Uses multiple AI APIs for question generation
- 📰 **Current Affairs**: Real-time news-based questions
- ⏱️ **Timer & Utilities**: Built-in timer and reminder features
- 🎯 **Interactive Interface**: Discord buttons and slash commands

## Setup Instructions

### 1. Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd govt-exam-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DISCORD_TOKEN="your_discord_bot_token"
export GEMINI1_KEY="your_gemini_api_key"
export OPENROUTER_KEY="your_openrouter_api_key"
# ... other API keys

# Run the bot
python main.py
```

### 2. Railway.app Deployment

#### Environment Variables to Set in Railway:

**Required:**

- `DISCORD_TOKEN` - Your Discord bot token

**AI APIs (at least one required):**

- `GEMINI1_KEY` - Google Gemini API key
- `GEMINI2_KEY` - Second Gemini key (optional)
- `GEMINI3_KEY` - Third Gemini key (optional)
- `OPENROUTER_KEY` - OpenRouter API key
- `TOGETHER_KEY` - Together AI API key
- `DEEPINFRA_KEY` - DeepInfra API key
- `DEEPSEEK_KEY` - DeepSeek API key

**News APIs (optional):**

- `GNEWS_KEY` - GNews API key
- `NEWSAPI_KEY` - NewsAPI key

#### Railway Deployment Steps:

1. **Connect to Railway:**
- Go to [railway.app](https://railway.app)
- Sign up/login with GitHub
- Click “New Project” → “Deploy from GitHub repo”
- Select your repository
1. **Configure Environment Variables:**
- In Railway dashboard, go to your project
- Click “Variables” tab
- Add all the environment variables listed above
1. **Deploy:**
- Railway will automatically deploy when you push to main branch
- Check logs in Railway dashboard for any errors

#### File Structure for Railway:

```
your-project/
├── main.py              # Main bot file
├── config.py            # Configuration and API keys
├── quiz_fetcher.py      # Quiz generation logic
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file (optional)
```

### 3. Getting API Keys

#### Discord Bot Token:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
1. Create new application → Bot → Copy token
1. Enable “Message Content Intent” in Bot settings

#### AI API Keys:

- **Google Gemini**: [Google AI Studio](https://makersuite.google.com/)
- **OpenRouter**: [openrouter.ai](https://openrouter.ai/)
- **Together AI**: [together.ai](https://www.together.ai/)
- **DeepInfra**: [deepinfra.com](https://deepinfra.com/)
- **DeepSeek**: [deepseek.com](https://www.deepseek.com/)

#### News API Keys:

- **GNews**: [gnews.io](https://gnews.io/)
- **NewsAPI**: [newsapi.org](https://newsapi.org/)

## Usage

### Commands:

- `/quiz` - Start a quiz (slash command)
- `/start` - Show main menu (prefix command)
- `/timer <minutes>` - Set a timer
- `/help` - Show help information

### Quiz Categories:

- **SSC**: CGL, CHSL, MTS (English, Current Affairs, Aptitude, Reasoning)
- **Bank**: PO, Clerk (English, Current Affairs, Aptitude, Reasoning)
- **UPSC**: General Studies, Current Affairs, Essay
- **Current Affairs**: Latest news-based questions

## Troubleshooting

### Common Issues:

1. **Bot not responding:**
- Check DISCORD_TOKEN is correct
- Verify bot has necessary permissions in server
- Check Railway logs for errors
1. **No questions generated:**
- Ensure at least one AI API key is valid
- Check API key quotas/limits
- Verify internet connectivity
1. **Import errors:**
- Check all files are uploaded to Railway
- Verify requirements.txt includes all dependencies
1. **Permission errors:**
- Bot needs “Send Messages”, “Use Slash Commands”, “Embed Links” permissions
- Make sure bot is added to server with correct permissions

### Railway-Specific Tips:

- **Logs**: Check Railway dashboard → Your project → “Deployments” → Click on deployment → View logs
- **Environment Variables**: Use Railway dashboard, don’t put secrets in code
- **Automatic Deploys**: Push to main branch to trigger redeploy
- **Custom Start Command**: Railway auto-detects Python apps, but you can specify in `Procfile`:
  
  ```
  web: python main.py
  ```

### Log Messages to Watch:

- ✅ `Config loaded successfully` - Configuration working
- ✅ `Bot is ready as <BotName>` - Bot connected to Discord
- ✅ `Synced X command(s)` - Slash commands registered
- ❌ `DISCORD_TOKEN environment variable is required` - Missing bot token
- ❌ `No AI API key available` - All AI APIs are unavailable

## Support

If you encounter issues:

1. Check Railway logs for error messages
1. Verify all environment variables are set correctly
1. Test API keys independently
1. Ensure Discord bot has proper permissions

## License

This project is open source. Feel free to modify and use as needed.
