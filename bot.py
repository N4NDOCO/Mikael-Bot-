# bot.py - Mikael (Bot)
import discord
from discord.ext import commands
from discord import app_commands
import config

# Intents necessários para slash commands e identificar membros online
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Criar bot
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Carregar cogs
initial_extensions = ["cogs.contas", "cogs.call"]
for extension in initial_extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f"Mikael está online!")
    try:
        # Sincroniza os comandos com o servidor específico
        synced = await bot.tree.sync(guild=discord.Object(id=config.GUILD_ID))
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

# Rodar o bot
bot.run(config.TOKEN)