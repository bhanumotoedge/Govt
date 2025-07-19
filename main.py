import os
import discord
from discord.ext import commands
import asyncio
import traceback
from quiz_fetcher import fetch_quiz
from config import DISCORD_TOKEN

# Set up intents

intents = discord.Intents.default()
intents.message_content = True

# Create bot instance

bot = commands.Bot(command_prefix=”/”, intents=intents)

@bot.event
async def on_ready():
“”“Event triggered when bot is ready”””
print(f”✅ Bot is ready as {bot.user}”)
print(f”📊 Bot is in {len(bot.guilds)} guilds”)

```
# Sync slash commands
try:
    synced = await bot.tree.sync()
    print(f"✅ Synced {len(synced)} command(s)")
except Exception as e:
    print(f"❌ Failed to sync commands: {e}")
```

@bot.event
async def on_error(event, *args, **kwargs):
“”“Handle bot errors”””
print(f”❌ Bot error in {event}: {traceback.format_exc()}”)

@bot.command(name=“start”)
async def start_command(ctx):
“”“Start command to show main menu”””
try:
embed = discord.Embed(
title=“🎯 Government Exam Prep Bot”,
description=“Choose your exam category:”,
color=0x00ff00
)

```
    view = MainMenuView()
    await ctx.send(embed=embed, view=view)
    
except Exception as e:
    print(f"❌ Error in start command: {e}")
    await ctx.send("❌ An error occurred. Please try again.")
```

@bot.tree.command(name=“quiz”, description=“Start a quiz”)
async def quiz_slash(interaction: discord.Interaction):
“”“Slash command for starting quiz”””
try:
embed = discord.Embed(
title=“🎯 Government Exam Prep Bot”,
description=“Choose your exam category:”,
color=0x00ff00
)

```
    view = MainMenuView()
    await interaction.response.send_message(embed=embed, view=view)
    
except Exception as e:
    print(f"❌ Error in quiz slash command: {e}")
    await interaction.response.send_message("❌ An error occurred. Please try again.", ephemeral=True)
```

class MainMenuView(discord.ui.View):
def **init**(self):
super().**init**(timeout=300)  # 5 minute timeout

```
async def on_timeout(self):
    """Disable view when timeout occurs"""
    for item in self.children:
        item.disabled = True

@discord.ui.button(label="SSC", style=discord.ButtonStyle.primary, emoji="📚")
async def ssc_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await self.handle_exam_selection(interaction, "ssc")

@discord.ui.button(label="Bank", style=discord.ButtonStyle.primary, emoji="🏦")
async def bank_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await self.handle_exam_selection(interaction, "bank")

@discord.ui.button(label="UPSC", style=discord.ButtonStyle.primary, emoji="🏛️")
async def upsc_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await self.handle_exam_selection(interaction, "upsc")

@discord.ui.button(label="Current Affairs", style=discord.ButtonStyle.success, emoji="📰")
async def current_affairs_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await self.handle_quiz_request(interaction, "current_affairs")

@discord.ui.button(label="Utilities", style=discord.ButtonStyle.secondary, emoji="🛠️")
async def utilities_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    embed = discord.Embed(
        title="🛠️ Utilities",
        description="Available utilities:\n• `/timer` - Set a timer\n• `/reminder` - Set a reminder\n• `/help` - Show help",
        color=0x808080
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

async def handle_exam_selection(self, interaction: discord.Interaction, exam_type: str):
    """Handle exam type selection"""
    try:
        if exam_type == "ssc":
            view = SSCExamView()
            embed = discord.Embed(title="📚 SSC Exams", description="Select your SSC exam:", color=0x3498db)
        elif exam_type == "bank":
            view = BankExamView()
            embed = discord.Embed(title="🏦 Bank Exams", description="Select your Bank exam:", color=0xe74c3c)
        elif exam_type == "upsc":
            view = UPSCExamView()
            embed = discord.Embed(title="🏛️ UPSC", description="Select your UPSC section:", color=0xf39c12)
        
        await interaction.response.send_message(embed=embed, view=view)
        
    except Exception as e:
        print(f"❌ Error handling exam selection: {e}")
        await interaction.response.send_message("❌ An error occurred. Please try again.", ephemeral=True)

async def handle_quiz_request(self, interaction: discord.Interaction, category_id: str):
    """Handle quiz request and fetch questions"""
    try:
        await interaction.response.defer(thinking=True)
        
        # Fetch questions
        questions = fetch_quiz(category_id)
        
        if not questions:
            await interaction.followup.send("❌ Unable to fetch questions. Please try again later.")
            return
        
        # Create quiz embed
        embed = discord.Embed(
            title=f"📝 Quiz: {category_id.replace('_', ' ').title()}",
            description=f"**{len(questions)} Questions | ⏱️ 8 minutes**",
            color=0x2ecc71
        )
        
        # Add questions to embed
        quiz_text = ""
        for i, q in enumerate(questions, 1):
            quiz_text += f"\n**{i}.** {q['question']}\n"
            for option in q['options']:
                quiz_text += f"   {option}\n"
            quiz_text += "\n"
        
        # Split into multiple embeds if too long
        if len(quiz_text) > 4000:
            # Send first part
            embed.description += f"\n\n{quiz_text[:3500]}"
            await interaction.followup.send(embed=embed)
            
            # Send remaining questions
            remaining_text = quiz_text[3500:]
            embed2 = discord.Embed(
                title="📝 Quiz (Continued)",
                description=remaining_text,
                color=0x2ecc71
            )
            await interaction.followup.send(embed=embed2)
        else:
            embed.description += f"\n\n{quiz_text}"
            await interaction.followup.send(embed=embed)
        
        # Send timer message
        timer_embed = discord.Embed(
            title="⏱️ Timer Started!",
            description="You have 8 minutes to complete this quiz.\nGood luck! 🍀",
            color=0xff9f43
        )
        await interaction.followup.send(embed=timer_embed)
        
    except Exception as e:
        print(f"❌ Error handling quiz request: {e}")
        await interaction.followup.send("❌ An error occurred while fetching the quiz. Please try again.")
```

class SSCExamView(discord.ui.View):
def **init**(self):
super().**init**(timeout=300)

```
@discord.ui.button(label="CGL", style=discord.ButtonStyle.primary)
async def cgl_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = SectionView("ssc_cgl")
    embed = discord.Embed(title="📚 SSC CGL", description="Select section:", color=0x3498db)
    await interaction.response.send_message(embed=embed, view=view)

@discord.ui.button(label="CHSL", style=discord.ButtonStyle.primary)
async def chsl_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = SectionView("ssc_chsl")
    embed = discord.Embed(title="📚 SSC CHSL", description="Select section:", color=0x3498db)
    await interaction.response.send_message(embed=embed, view=view)

@discord.ui.button(label="MTS", style=discord.ButtonStyle.primary)
async def mts_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = SectionView("ssc_mts")
    embed = discord.Embed(title="📚 SSC MTS", description="Select section:", color=0x3498db)
    await interaction.response.send_message(embed=embed, view=view)
```

class BankExamView(discord.ui.View):
def **init**(self):
super().**init**(timeout=300)

```
@discord.ui.button(label="PO", style=discord.ButtonStyle.primary)
async def po_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = SectionView("bank_po")
    embed = discord.Embed(title="🏦 Bank PO", description="Select section:", color=0xe74c3c)
    await interaction.response.send_message(embed=embed, view=view)

@discord.ui.button(label="Clerk", style=discord.ButtonStyle.primary)
async def clerk_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    view = SectionView("bank_clerk")
    embed = discord.Embed(title="🏦 Bank Clerk", description="Select section:", color=0xe74c3c)
    await interaction.response.send_message(embed=embed, view=view)
```

class UPSCExamView(discord.ui.View):
def **init**(self):
super().**init**(timeout=300)

```
@discord.ui.button(label="General Studies", style=discord.ButtonStyle.primary)
async def gs_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await MainMenuView().handle_quiz_request(interaction, "upsc_generalstudies")

@discord.ui.button(label="Current Affairs", style=discord.ButtonStyle.primary)
async def ca_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await MainMenuView().handle_quiz_request(interaction, "upsc_currentaffairs")

@discord.ui.button(label="Essay", style=discord.ButtonStyle.primary)
async def essay_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await MainMenuView().handle_quiz_request(interaction, "upsc_essay")
```

class SectionView(discord.ui.View):
def **init**(self, exam_prefix: str):
super().**init**(timeout=300)
self.exam_prefix = exam_prefix

```
@discord.ui.button(label="English", style=discord.ButtonStyle.secondary)
async def english_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await MainMenuView().handle_quiz_request(interaction, f"{self.exam_prefix}_english")

@discord.ui.button(label="Current Affairs", style=discord.ButtonStyle.secondary)
async def current_affairs_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await MainMenuView().handle_quiz_request(interaction, f"{self.exam_prefix}_currentaffairs")

@discord.ui.button(label="Aptitude", style=discord.ButtonStyle.secondary)
async def aptitude_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await MainMenuView().handle_quiz_request(interaction, f"{self.exam_prefix}_aptitude")

@discord.ui.button(label="Reasoning", style=discord.ButtonStyle.secondary)
async def reasoning_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await MainMenuView().handle_quiz_request(interaction, f"{self.exam_prefix}_reasoning")
```

# Additional utility commands

@bot.tree.command(name=“timer”, description=“Set a timer”)
async def timer_command(interaction: discord.Interaction, minutes: int):
“”“Set a timer for specified minutes”””
if minutes <= 0 or minutes > 60:
await interaction.response.send_message(“❌ Timer must be between 1-60 minutes.”, ephemeral=True)
return

```
await interaction.response.send_message(f"⏱️ Timer set for {minutes} minute(s)!")

await asyncio.sleep(minutes * 60)

try:
    await interaction.followup.send(f"⏰ {interaction.user.mention} Your {minutes} minute timer is up!")
except:
    # If followup fails, try to send a new message
    channel = interaction.channel
    if channel:
        await channel.send(f"⏰ {interaction.user.mention} Your {minutes} minute timer is up!")
```

@bot.tree.command(name=“help”, description=“Show help information”)
async def help_command(interaction: discord.Interaction):
“”“Show help information”””
embed = discord.Embed(
title=“🤖 Bot Help”,
description=“Available commands and features:”,
color=0x3498db
)

```
embed.add_field(
    name="📝 Quiz Commands",
    value="`/quiz` - Start a quiz\n`/start` - Show main menu",
    inline=False
)

embed.add_field(
    name="🛠️ Utility Commands",
    value="`/timer [minutes]` - Set a timer\n`/help` - Show this help",
    inline=False
)

embed.add_field(
    name="📚 Exam Categories",
    value="• SSC (CGL, CHSL, MTS)\n• Bank (PO, Clerk)\n• UPSC\n• Current Affairs",
    inline=False
)

await interaction.response.send_message(embed=embed, ephemeral=True)
```

# Error handling for commands

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
“”“Handle application command errors”””
print(f”❌ Command error: {error}”)

```
if interaction.response.is_done():
    try:
        await interaction.followup.send("❌ An error occurred while processing your command.", ephemeral=True)
    except:
        pass
else:
    try:
        await interaction.response.send_message("❌ An error occurred while processing your command.", ephemeral=True)
    except:
        pass
```

# Handle general bot errors

@bot.event
async def on_command_error(ctx, error):
“”“Handle command errors”””
print(f”❌ Command error: {error}”)
await ctx.send(“❌ An error occurred while processing your command.”)

# Graceful shutdown

async def shutdown():
“”“Graceful shutdown function”””
print(“🔄 Shutting down bot…”)
await bot.close()

def main():
“”“Main function to run the bot”””
try:
if not DISCORD_TOKEN:
raise ValueError(“DISCORD_TOKEN environment variable is required”)

```
    print("🚀 Starting Government Exam Prep Bot...")
    bot.run(DISCORD_TOKEN)
    
except KeyboardInterrupt:
    print("\n⏹️ Bot stopped by user")
except Exception as e:
    print(f"❌ Critical error: {e}")
    traceback.print_exc()
finally:
    print("👋 Bot shutdown complete")
```

if **name** == “**main**”:
main()
