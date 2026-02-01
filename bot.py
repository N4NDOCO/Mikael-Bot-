import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN, GUILD_ID, CARGO_ENTREGADOR

# IMPORTA DESCONTO DO BOT AFK
from afk_bot import user_discount   # <-- ajuste o nome se for diferente

# ----- Intents -----
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

MAX_DISCOUNT = 20

# ================= CONTAS =================
ACCOUNTS = {
    "God Human Lv Max (2800)": 20,
    "Dragon Talor v2 (Evo) Lv Max (2800)": 15,
    "Sharkman Karatê v2 (Evo) Lv Max (2800)": 15,
    "Eletric Claw Lv Max (2800)": 10,
    "100M Berries Lv Max (2800)": 20,
    "Level Max Lv Max (2800)": 8,
    "Fruta no Inv Lv Max (2800)": 12,
    "Tudo Random Aleatória": 10
}

CUSTOM_ACCOUNT_PRICE = 25

# ================= FUNÇÕES =================
def apply_discount(price, percent):
    return round(price * (1 - percent / 100))

def format_price(original, discounted=None):
    if discounted is None:
        return f"R${original}"
    return f"~~R${original}~~ ➜ **R${discounted}**"

# ----- READY -----
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print("Mikael está online!")

# ----- /contas -----
@bot.tree.command(name="contas", description="Receba a lista de contas")
async def contas(interaction: discord.Interaction):
    user = interaction.user
    desconto = min(user_discount.get(user.id, 0), MAX_DISCOUNT)

    msg = f"💸 **Seu desconto atual:** {desconto}%\n"
    msg += "⚠️ Conta personalizada possui **desconto 5x reduzido**\n\n"

    msg += "**--🥊 Estilos de luta--**\n"
    for nome, preco in ACCOUNTS.items():
        if desconto > 0:
            novo = apply_discount(preco, desconto)
            msg += f"• {nome} – {format_price(preco, novo)}\n"
        else:
            msg += f"• {nome} – R${preco}\n"

    msg += "\n**--🗒️ Conta Personalizada--**\n"
    if desconto > 0:
        d_personal = desconto // 5
        novo = apply_discount(CUSTOM_ACCOUNT_PRICE, d_personal)
        msg += f"• Personalizada – {format_price(CUSTOM_ACCOUNT_PRICE, novo)}\n"
    else:
        msg += f"• Personalizada – R${CUSTOM_ACCOUNT_PRICE}\n"

    msg += (
        "\n✅ Contas seguras\n"
        "📦 Entrega em até 2 dias\n"
        "❗ Chame o Entregador com **/call**\n"
        "💰 Pagamento apenas via PIX\n"
        "💸 Pix: world.blox018@gmail.com\n"
        "🚨 **Não pague ainda** 🚨\n"
        "⏳ Aguarde o entregador checar o stock\n"
    )

    await interaction.user.send(msg)
    await interaction.response.send_message(
        "📩 Enviei a lista completa de contas em DM!",
        ephemeral=True
    )

# ----- /call -----
@bot.tree.command(name="call", description="Chame um entregador")
async def call(interaction: discord.Interaction):
    guild = bot.get_guild(GUILD_ID)
    cargo = discord.utils.get(guild.roles, name=CARGO_ENTREGADOR)

    if not cargo:
        await interaction.response.send_message(
            "Cargo Entregador não encontrado!",
            ephemeral=True
        )
        return

    entregadores = [m.mention for m in guild.members if cargo in m.roles]

    if entregadores:
        await interaction.response.send_message(
            "📞 **Entregadores disponíveis:**\n" + ", ".join(entregadores),
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "⚠️ Nenhum entregador disponível!",
            ephemeral=True
        )

# ----- RUN -----
bot.run(TOKEN)
