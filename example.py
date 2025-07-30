import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio

# Token bot
DISCORD_TOKEN = "BOT_TOKEN"

# Inisialisasi bot dengan prefix
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Bot aktif sebagai {bot.user}")
    
@bot.event
async def on_ready():
    print(f'Bot login sebagai {bot.user}')
    
    # Activity:
    activity = discord.Activity(type=discord.ActivityType.watching, name="Beri nama activity") # Ganti nama activity sesuai keinginan
    await bot.change_presence(activity=activity)


@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, pesan):
    await ctx.send(pesan)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, user: discord.User, *, pesan: str):
    try:
        await user.send(pesan)
        await ctx.message.delete()
    except Exception as e:
            await ctx.send(f"❌ Gagal mengirim DM: {e}")

@bot.command()
async def ava(ctx, user: discord.User = None):
    user = user or ctx.author
    embed = discord.Embed(
        title=f"Avatar {user.display_name}",
        color=discord.Color.green()
    )
    embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def annc(ctx, *, pesan: str):
    embed = discord.Embed(
        title="📢 Pengumuman",
        description=pesan,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def help(ctx):
    embed = discord.Embed(
    title="🔖 **Daftar Perintah**",
    description="Berikut adalah daftar perintah yang tersedia\n"
                "👤 **Umum** :\n"
                "!ava = Menampilkan avatar pengguna\n\n"

                "👑 **Admin Only**\n"
                "!say = Mengirim pesan sebagai bot\n"
                "!dm = Mengirim pesan langsung ke pengguna\n"
                "!annc = Membuat pengumuman\n"
                "!setticket = Setup ticket\n",
    color=discord.Color.from_rgb(100, 150, 255)
    )
    await ctx.send(embed=embed) # Ganti description sesuai kebutuhan 

@bot.command()
@commands.has_permissions(administrator=True)
async def setticket(ctx):
    embed = discord.Embed(
        title="🎫 Ticket Support",
        description="Klik tombol **Open Ticket** untuk open ticket.",
        color=discord.Color.blue()
    )
    view = TicketView()
    await ctx.send(embed=embed, view=view)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(OpenTicketButton())

class OpenTicketButton(Button):
    def __init__(self):
        super().__init__(label="Open Ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = discord.utils.get(guild.categories, name="TICKETS")
        if not category:
            category = await guild.create_category("TICKETS")
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}".replace(" ", "-"),
            overwrites=overwrites,
            category=category,
            reason="Ticket created"
        )
        await channel.send(
            f"{interaction.user.mention} Ticket berhasil dibuat.\n"
            "Tag : <@1392777231478030434>",
            view=CloseTicketView()
        )
        await interaction.response.send_message(f"Ticket telah dibuat: {channel.mention}", ephemeral=True)

class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseTicketButton())

class CloseTicketButton(Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")

    async def callback(self, interaction: discord.Interaction):
        await interaction.channel.delete(reason="Ticket closed")

bot.run("TOKEN_BOT") # Ganti dengan token bot discordmu
