import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('BOT_TOKEN')

# Enable message content intent if needed later (not needed for now)
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
    await interaction.response.send_message("✅ Bot is alive! Menu coming soon.")

bot.run(TOKEN)
