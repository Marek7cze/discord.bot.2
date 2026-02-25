import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
import threading

# ==============================
# WEB SERVER FOR RAILWAY
# ==============================
app = Flask(__name__)

@app.route("/")
def home():
    return "Contact Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# ==============================
# DISCORD SETUP
# ==============================
GUILD_ID = YOUR_GUILD_ID  # Replace this

GUILD_OBJECT = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================
# CONTACT COMMAND
# ==============================
@bot.tree.command(name="contact", description="Contact a role", guild=GUILD_OBJECT)
async def contact(
    interaction: discord.Interaction,
    role: discord.Role,
    message: str
):

    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            "You do not have permission to use this.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"{role.mention}\n{message}"
    )

# ==============================
# READY EVENT
# ==============================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync(guild=GUILD_OBJECT)

# ==============================
# RUN
# ==============================
token = os.environ.get("DISCORD_TOKEN")

if token:
    bot.run(token)
else:
    print("DISCORD_TOKEN not set!")
