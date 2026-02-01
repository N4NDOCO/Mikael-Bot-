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
            "---🥊 Estilos de luta---\n"
            "• God Human Lv Max (2800) – R$20\n"
            "• Dragon Talor v2 (Evo) Lv Max (2800) – R$15\n"
            "• Sharkman Karatê v2 (Evo) Lv Max (2800) – R$15\n"
            "• Eletric Claw Lv Max (2800) – R$10\n\n"
            "---📦 Contas Padrão---\n"
            "• 100M Berries Lv Max (2800) – R$20\n"
            "• Level Max Lv Max (2800) – R$8\n"
            "• Fruta no Inv Lv Max (2800) – R$12\n"
            "• Tudo Random Aleatória – R$10\n\n"
            "• Conta Personalizaa -"
            "✅ Contas seguras\n"
            "📦 Entrega em até 2 dias\n"
            "❗ Chame o Entregador com /call e escolha a conta desejada\n"
            "💰 Pagamento apenas via PIX\n"
            "💸 Pix: world.blox018@gmail.com\n"
            "🚨 Não pague ainda 🚨\n"
            "⏳ Aguarda o Entregador checar conta e após escolha a sua."
        )
        await interaction.user.send(contas_msg)
        await interaction.response.send_message("As opções de contas foram enviadas no seu DM!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Contas(bot))
