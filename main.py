import os
import discord
from discord.ext import commands
from quiz_fetcher import fetch_quiz
from config import DISCORD_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")

@bot.command()
async def start(ctx):
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="SSC", custom_id="ssc"))
    view.add_item(discord.ui.Button(label="Bank", custom_id="bank"))
    view.add_item(discord.ui.Button(label="UPSC", custom_id="upsc"))
    view.add_item(discord.ui.Button(label="Current Affairs", custom_id="current_affairs"))
    view.add_item(discord.ui.Button(label="Utilities", custom_id="utilities"))
    await ctx.send("👋 Welcome! Choose an exam:", view=view)

@bot.event
async def on_interaction(interaction):
    cid = interaction.data['custom_id']
    if cid == "ssc":
        view = discord.ui.View()
        for sub in ["CGL", "CHSL", "MTS"]:
            view.add_item(discord.ui.Button(label=sub, custom_id=f"ssc_{sub.lower()}"))
        await interaction.response.send_message("Select SSC exam:", view=view)
    elif cid.startswith("ssc_"):
        view = discord.ui.View()
        for sec in ["English", "Current Affairs", "Aptitude", "Reasoning"]:
            view.add_item(discord.ui.Button(label=sec, custom_id=f"{cid}_{sec.replace(' ', '').lower()}"))
        await interaction.response.send_message(f"Select section for {cid.split('_')[1].upper()}:", view=view)
    elif cid.endswith(("english", "currentaffairs", "aptitude", "reasoning")):
        await interaction.response.defer()
        questions = fetch_quiz(cid)
        text = "\n".join([f"{i+1}. {q['question']}" for i, q in enumerate(questions)])
        await interaction.followup.send(f"📝 10 Questions:\n{text}\n⏱ Timer: 8 mins!")
    elif cid == "bank":
        view = discord.ui.View()
        for sub in ["PO", "Clerk"]:
            view.add_item(discord.ui.Button(label=sub, custom_id=f"bank_{sub.lower()}"))
        await interaction.response.send_message("Select Bank exam:", view=view)
    elif cid.startswith("bank_"):
        view = discord.ui.View()
        for sec in ["English", "Current Affairs", "Aptitude", "Reasoning"]:
            view.add_item(discord.ui.Button(label=sec, custom_id=f"{cid}_{sec.replace(' ', '').lower()}"))
        await interaction.response.send_message(f"Select section for {cid.split('_')[1].upper()}:", view=view)
    elif cid == "upsc":
        view = discord.ui.View()
        for sec in ["General Studies", "Current Affairs", "Essay"]:
            view.add_item(discord.ui.Button(label=sec, custom_id=f"upsc_{sec.replace(' ', '').lower()}"))
        await interaction.response.send_message("Select UPSC section:", view=view)
    elif cid.startswith("upsc_"):
        await interaction.response.defer()
        questions = fetch_quiz(cid)
        text = "\n".join([f"{i+1}. {q['question']}" for i, q in enumerate(questions)])
        await interaction.followup.send(f"📝 10 Questions:\n{text}\n⏱ Timer: 8 mins!")
    elif cid == "current_affairs":
        await interaction.response.defer()
        questions = fetch_quiz("current_affairs")
        text = "\n".join([f"{i+1}. {q['question']}" for i, q in enumerate(questions)])
        await interaction.followup.send(f"📰 Last 24h Current Affairs quiz:\n{text}")
    elif cid == "utilities":
        await interaction.response.send_message(
            "🛠 Utilities:\n- /reminder\n- /timer\n- /stopwatch (coming soon!)"
        )

bot.run(DISCORD_BOT_TOKEN)
