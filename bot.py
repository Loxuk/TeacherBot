import os
import asyncio
import discord
from discord.ext import commands

# ==========================================
# SETTINGS
# ==========================================

SERVER_ID = 1515774982154879147
TEACHER_ROLE_ID = 1550582807036825771

# ==========================================
# BOT SETUP
# ==========================================

intents = discord.Intents.default()
intents.message_content = True  # Włączone, aby bot mógł prawidłowo wysyłać wiadomości na kanał

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ==========================================
# BOT STARTUP
# ==========================================

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    print("Starting slash command sync...")
    try:
        server = discord.Object(id=SERVER_ID)
        synced = await bot.tree.sync(guild=server)
        print(f"Synced {len(synced)} slash command(s) to the server!")
    except Exception as error:
        print(f"ERROR while syncing commands:")
        print(error)

# ==========================================
# CLASS SELECTION
# ==========================================

class TeacherRequestSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Class of General", description="Request a teacher for General"),
            discord.SelectOption(label="General Beginner's Guide", description="Request a teacher for the Beginner's Guide"),
            discord.SelectOption(label="Class of Jobs", description="Request a teacher for Jobs"),
            discord.SelectOption(label="Class of Health", description="Request a teacher for Health"),
            discord.SelectOption(label="Class of Plots & Regions", description="Request a teacher for Plots & Regions"),
            discord.SelectOption(label="Class of Crime", description="Request a teacher for Crime"),
            discord.SelectOption(label="Class of Government", description="Request a teacher for Government"),
            discord.SelectOption(label="Class of Money Making", description="Request a teacher for Money Making"),
            discord.SelectOption(label="Class of Internal Game Mechanics", description="Request a teacher for Internal Game Mechanics")
        ]
        super().__init__(
            placeholder="Choose the class you need help with...",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_class = self.values[0]
        teacher_role = interaction.guild.get_role(TEACHER_ROLE_ID)

        if teacher_role is None:
            await interaction.response.send_message(
                "I couldn't find the Teacher role. Please check the role ID.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Your teacher request for **{selected_class}** has been submitted!",
            ephemeral=True
        )

        await interaction.channel.send(
            f"{teacher_role.mention}\n"
            f"📚 **Teacher Request**\n"
            f"**Student:** {interaction.user.mention}\n"
            f"**Class:** {selected_class}"
        )

# ==========================================
# DROPDOWN VIEW
# ==========================================

class TeacherRequestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(TeacherRequestSelect())

# ==========================================
# SLASH COMMAND
# ==========================================

@bot.tree.command(
    name="request-a-teacher",
    description="Request a teacher for a specific class",
    guild=discord.Object(id=SERVER_ID)
)
async def request_a_teacher(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📚 **Request a Teacher**\n\nPlease choose the class you need help with:",
        view=TeacherRequestView(),
        ephemeral=True
    )

# ==========================================
# START BOT
# ==========================================

async def main():
    # Pobieranie tokenu wewnątrz funkcji uruchamiającej (naprawia błąd hostingu)
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("BŁĄD: Zmienna DISCORD_TOKEN jest pusta w panelu hostingu!")
        return
    
    # Czyszczenie i start klienta bezpośrednio w pętli asyncio
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    # Oficjalna i bezpieczna metoda dla Pythona w Dockerze
    asyncio.run(main())
