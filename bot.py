import discord
from discord.ext import commands
from discord import app_commands
import os
from config import TOKEN, GUILD_ID, CARGO_ENTREGADOR

# ----- Intents -----
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # SERVER MEMBERS INTENT

bot = commands.Bot(command_prefix="/", intents=intents)

# ----- Sincronização dos comandos -----
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)  # registra comandos apenas nesse servidor
    try:
        # Garante que os comandos slash do bot sejam sincronizados
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print(f"Comandos sincronizados no servidor {GUILD_ID}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

    print("Mikael está online!")

# ----- /contas -----
@bot.tree.command(name="contas", description="Receba a lista de contas")
async def contas(interaction: discord.Interaction):
    msg = """
--🥊 Estilos de luta--
• God Human Lv Max (2800) – R$20
• Dragon Talor v2 (Evo) Lv Max (2800) – R$15
• Sharkman Karatê v2 (Evo) Lv Max (2800) – R$15
• Eletric Claw Lv Max (2800) – R$10

--📦 Contas Padrão--
• 100M Berries Lv Max (2800) – R$20
• Level Max Lv Max (2800) – R$8
• Fruta no Inv Lv Max (2800) – R$12
• Tudo Random Aleatória – R$10

✅ Contas seguras
📦 Entrega em até 2 dias
❗ Chame um Entregador no servidor com /call e escolha a conta desejada
💰 Pagamento via PIX: world.blox018@gmail.com
🚨 Não pague até o vendedor responder 🚨
"""
    # Envia DM
    await interaction.user.send(msg)
    # Resposta pública efêmera
    await interaction.response.send_message("Enviei a lista de contas em DM!", ephemeral=True)

# ----- /call -----
@bot.tree.command(name="call", description="Chame um entregador")
async def call(interaction: discord.Interaction):
    guild = bot.get_guild(GUILD_ID)
    cargo = discord.utils.get(guild.roles, name=CARGO_ENTREGADOR)
    if not cargo:
        await interaction.response.send_message("Cargo Entregador não encontrado!", ephemeral=True)
        return

    # Menciona apenas membros com o cargo
    entregadores = [m.mention for m in guild.members if cargo in m.roles]

    if entregadores:
        await interaction.response.send_message("Entregadores disponíveis: " + ", ".join(entregadores), ephemeral=True)
    else:
        await interaction.response.send_message("Nenhum entregador disponível!", ephemeral=True)

# ----- Rodar bot -----
bot.run(TOKEN)
