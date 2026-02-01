# cogs/contas.py
import discord
from discord.ext import commands
from discord import app_commands

class Contas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="contas", description="Mostra as opções de contas")
    async def contas(self, interaction: discord.Interaction):
        contas_msg = (
            "✅ Contas seguras\n"
            "📦 Entrega em até 2 dias\n"
            "❗ Chame o Entregador com /call e escolha a conta desejada\n"
            "💰 Pagamento apenas via PIX\n"
            "💸 Pix: world.blox018@gmail.com\n"
            "🚨 Não pague ainda 🚨\n"
            "⏳ Aguarde o Entregador checar conta em stock e após isso escolha a sua."
        )
        await interaction.user.send(contas_msg)
        await interaction.response.send_message("As opções de contas foram enviadas no seu DM!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Contas(bot))
