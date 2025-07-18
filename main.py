import os
import discord
from discord.ext import commands

TOKEN = os.environ.get('BOT_TOKEN')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")

@bot.tree.command(name="start", description="Start the bot")
async def start(interaction: discord.Interaction):
    await interaction.response.send_message("✅ Bot is alive! Menu coming soon.")

bot.run(TOKEN)
