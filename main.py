import discord
from discord.ext import commands
from quiz_fetcher import fetch_quiz
import os
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Type /start"))

@bot.command()
async def start(ctx):
    view = discord.ui.View()
    exams = [
        ("SSC", "ssc"),
        ("Bank", "bank"),
        ("UPSC", "upsc"),
        ("Current Affairs", "current_affairs"),
        ("Utilities", "utilities")
    ]
    
    for label, custom_id in exams:
        button = discord.ui.Button(
            label=label, 
            custom_id=custom_id,
            style=discord.ButtonStyle.primary
        )
        view.add_item(button)
    
    await ctx.send("👋 Welcome to Exam Prep Bot! Choose an exam:", view=view)

@bot.event
async def on_interaction(interaction):
    try:
        cid = interaction.data['custom_id']
        
        # SSC Exam Flow
        if cid == "ssc":
            view = discord.ui.View()
            for sub in config.EXAM_OPTIONS["ssc"]:
                button = discord.ui.Button(
                    label=sub, 
                    custom_id=f"ssc_{sub.lower()}",
                    style=discord.ButtonStyle.secondary
                )
                view.add_item(button)
            await interaction.response.send_message("Select SSC exam:", view=view)
        
        elif cid.startswith("ssc_"):
            view = discord.ui.View()
            for sec in config.EXAM_OPTIONS["sections"]["ssc"]:
                sec_id = sec.replace(' ', '').lower()
                button = discord.ui.Button(
                    label=sec, 
                    custom_id=f"{cid}_{sec_id}",
                    style=discord.ButtonStyle.success
                )
                view.add_item(button)
            await interaction.response.send_message(f"Select section for {cid.split('_')[1].upper()}:", view=view)
        
        # Bank Exam Flow
        elif cid == "bank":
            view = discord.ui.View()
            for sub in config.EXAM_OPTIONS["bank"]:
                button = discord.ui.Button(
                    label=sub, 
                    custom_id=f"bank_{sub.lower()}",
                    style=discord.ButtonStyle.secondary
                )
                view.add_item(button)
            await interaction.response.send_message("Select Bank exam:", view=view)
        
        elif cid.startswith("bank_"):
            view = discord.ui.View()
            for sec in config.EXAM_OPTIONS["sections"]["bank"]:
                sec_id = sec.replace(' ', '').lower()
                button = discord.ui.Button(
                    label=sec, 
                    custom_id=f"{cid}_{sec_id}",
                    style=discord.ButtonStyle.success
                )
                view.add_item(button)
            await interaction.response.send_message(f"Select section for {cid.split('_')[1].upper()}:", view=view)
        
        # UPSC Exam Flow
        elif cid == "upsc":
            view = discord.ui.View()
            for sec in config.EXAM_OPTIONS["sections"]["upsc"]:
                sec_id = sec.replace(' ', '').lower()
                button = discord.ui.Button(
                    label=sec, 
                    custom_id=f"upsc_{sec_id}",
                    style=discord.ButtonStyle.success
                )
                view.add_item(button)
            await interaction.response.send_message("Select UPSC section:", view=view)
        
        # Quiz Display
        elif any(key in cid for key in ["english", "currentaffairs", "aptitude", "reasoning", "generalstudies", "essay"]):
            await interaction.response.defer()
            questions = fetch_quiz(cid)
            
            formatted = []
            for i, q in enumerate(questions):
                options = "\n".join([f"{chr(65+j)}. {opt}" for j, opt in enumerate(q['options'])])
                formatted.append(f"**{i+1}. {q['question']}**\n{options}\n✅ Answer: {q['answer']}")
            
            await interaction.followup.send(f"📝 **Quiz Started!**\n\n" + "\n\n".join(formatted) + "\n\n⏱ **Timer: 8 minutes!**")
        
        # Current Affairs
        elif cid == "current_affairs":
            await interaction.response.defer()
            questions = fetch_quiz(cid)
            
            formatted = []
            for i, q in enumerate(questions):
                options = "\n".join([f"{chr(65+j)}. {opt}" for j, opt in enumerate(q['options'])])
                formatted.append(f"**{i+1}. {q['question']}**\n{options}\n✅ Answer: {q['answer']}")
            
            await interaction.followup.send("📰 **Latest Current Affairs:**\n\n" + "\n\n".join(formatted))
        
        # Utilities
        elif cid == "utilities":
            embed = discord.Embed(
                title="🛠 Utilities Menu",
                description="Available utility commands:",
                color=0x3498db
            )
            embed.add_field(name="/reminder", value="Set study reminders", inline=False)
            embed.add_field(name="/timer", value="Set a study timer", inline=False)
            embed.add_field(name="/stopwatch", value="Track your study time (coming soon)", inline=False)
            await interaction.response.send_message(embed=embed)
    
    except Exception as e:
        print(f"Error: {e}")
        await interaction.response.send_message("❌ Something went wrong. Please try again later.", ephemeral=True)

# Get token from environment
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")

bot.run(BOT_TOKEN)
