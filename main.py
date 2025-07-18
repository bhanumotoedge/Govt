import os
import discord
from discord.ext import commands
import requests

TOKEN = os.environ.get('BOT_TOKEN')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Fetch recent news
async def get_latest_news():
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "lang": "en",
        "country": "in",
        "max": 5,
        "apikey": os.environ.get('NEWS_API_KEY')
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        headlines = [f"- {article['title']}" for article in articles]
        return "\n".join(headlines)
    else:
        return "❌ Could not fetch news right now."

# /start command
@bot.tree.command(name="start", description="Start the bot")
async def start(interaction: discord.Interaction):
    view = MainMenu()
    await interaction.response.send_message("📚 *Select exam type or tool:*", view=view, ephemeral=True)

# Main Menu
class MainMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🏛 SSC", style=discord.ButtonStyle.primary)
    async def ssc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔹 Select SSC exam:", view=SSCMenu(), ephemeral=True)

    @discord.ui.button(label="🏦 Bank", style=discord.ButtonStyle.primary)
    async def bank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔹 Select Bank exam:", view=BankMenu(), ephemeral=True)

    @discord.ui.button(label="🇮🇳 UPSC", style=discord.ButtonStyle.primary)
    async def upsc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔹 Select UPSC section:", view=UPSCMenu(), ephemeral=True)

    @discord.ui.button(label="🛠 Utilities", style=discord.ButtonStyle.secondary)
    async def utilities(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🛠 Utilities:", view=UtilitiesMenu(), ephemeral=True)

    @discord.ui.button(label="📰 Current Affairs", style=discord.ButtonStyle.success)
    async def current_affairs(self, interaction: discord.Interaction, button: discord.ui.Button):
        headlines = await get_latest_news()
        await interaction.response.send_message(f"📰 Latest news (last 24h):\n{headlines}", ephemeral=True)

# SSC Menu
class SSCMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="CGL", style=discord.ButtonStyle.success)
    async def cgl(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 Select section:", view=SSCSectionsMenu(), ephemeral=True)

    @discord.ui.button(label="CHSL", style=discord.ButtonStyle.success)
    async def chsl(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 Select section:", view=SSCSectionsMenu(), ephemeral=True)

    @discord.ui.button(label="MTS", style=discord.ButtonStyle.success)
    async def mts(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 Select section:", view=SSCSectionsMenu(), ephemeral=True)

# SSC Sections Menu (quizzes)
class SSCSectionsMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="English", style=discord.ButtonStyle.secondary)
    async def english(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 English quiz coming soon!", ephemeral=True)

    @discord.ui.button(label="Quant", style=discord.ButtonStyle.secondary)
    async def quant(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 Quant quiz coming soon!", ephemeral=True)

    @discord.ui.button(label="Reasoning", style=discord.ButtonStyle.secondary)
    async def reasoning(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 Reasoning quiz coming soon!", ephemeral=True)

    @discord.ui.button(label="Current Affairs", style=discord.ButtonStyle.secondary)
    async def current_affairs_quiz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 Current Affairs quiz coming soon!", ephemeral=True)

# Bank Menu
class BankMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="PO", style=discord.ButtonStyle.success)
    async def po(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 Select section:", view=SSCSectionsMenu(), ephemeral=True)

    @discord.ui.button(label="Clerk", style=discord.ButtonStyle.success)
    async def clerk(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 Select section:", view=SSCSectionsMenu(), ephemeral=True)

# UPSC Menu
class UPSCMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="GS", style=discord.ButtonStyle.success)
    async def gs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 GS quiz coming soon!", ephemeral=True)

    @discord.ui.button(label="Current Affairs", style=discord.ButtonStyle.success)
    async def ca_quiz(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 Current Affairs quiz coming soon!", ephemeral=True)

# Utilities Menu
class UtilitiesMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⏱ Stopwatch", style=discord.ButtonStyle.secondary)
    async def stopwatch(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏱ Stopwatch started! (manual now)", ephemeral=True)

    @discord.ui.button(label="⏳ Timer", style=discord.ButtonStyle.secondary)
    async def timer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏳ Timer feature coming soon!", ephemeral=True)

    @discord.ui.button(label="⏰ Reminder", style=discord.ButtonStyle.secondary)
    async def reminder(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⏰ Reminder feature coming soon!", ephemeral=True)

bot.run(TOKEN)
