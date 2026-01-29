# cogs/call.py
import discord
from discord.ext import commands
from discord import app_commands
import config

class Call(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="call", description="Chama um Entregador")
    async def call(self, interaction: discord.Interaction):
        guild = interaction.guild
        cargo = discord.utils.get(guild.roles, name=config.CARGO_ENTREGADOR)
        if not cargo:
            await interaction.response.send_message("Cargo Entregador não encontrado!", ephemeral=True)
            return

        # Encontrar todos os membros com o cargo Entregador online
        entregadores = [m.mention for m in guild.members if cargo in m.roles and m.status != discord.Status.offline]
        if not entregadores:
            await interaction.response.send_message("Nenhum Entregador disponível no momento.", ephemeral=True)
            return

        mentions = ', '.join(entregadores)
        await interaction.response.send_message(f"{interaction.user.mention} chamou um Entregador! Disponíveis: {mentions}")

async def setup(bot):
    await bot.add_cog(Call(bot))