import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('BOT_TOKEN')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")
    try:
        synced = await bot.tree.sync()  # Sync slash commands globally
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="start", description="Start the bot")
async def start(interaction: discord.Interaction):
    view = MainMenu()
    await interaction.response.send_message("📚 *Select exam type:*", view=view, ephemeral=True)

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
        await interaction.response.send_message("⏰ Utilities coming soon!", ephemeral=True)

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
    async def current_affairs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📰 Current affairs quiz coming soon!", ephemeral=True)

class BankMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="PO", style=discord.ButtonStyle.success)
    async def po(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 Select section:", view=SSCSectionsMenu(), ephemeral=True)

    @discord.ui.button(label="Clerk", style=discord.ButtonStyle.success)
    async def clerk(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 Select section:", view=SSCSectionsMenu(), ephemeral=True)

class UPSCMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="GS", style=discord.ButtonStyle.success)
    async def gs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📚 GS quiz coming soon!", ephemeral=True)

    @discord.ui.button(label="Current Affairs", style=discord.ButtonStyle.success)
    async def ca(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📰 Current affairs quiz coming soon!", ephemeral=True)

bot.run(TOKEN)
