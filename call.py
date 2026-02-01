import discord
from discord.ext import commands
from discord import app_commands
import random
import config

class Call(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="call", description="Chamar um entregador")
    async def call(self, interaction: discord.Interaction):

        guild = interaction.guild

        # 🔒 Só funciona no canal correto
        if interaction.channel.id != config.CALL_CHANNEL_ID:
            await interaction.response.send_message(
                "❌ Use este comando no canal correto.",
                ephemeral=True
            )
            return

        cargo = discord.utils.get(guild.roles, name=config.CARGO_ENTREGADOR)
        if not cargo:
            await interaction.response.send_message(
                "❌ Cargo Entregador não encontrado.",
                ephemeral=True
            )
            return

        entregadores = [
            m for m in guild.members
            if cargo in m.roles and not m.bot
        ]

        if not entregadores:
            await interaction.response.send_message(
                "❌ Nenhum entregador disponível.",
                ephemeral=True
            )
            return

        entregador = random.choice(entregadores)

        # ✅ responde rápido (evita erro “aplicativo não respondeu”)
        await interaction.response.send_message(
            "✅ Veja a DM",
            ephemeral=True
        )

        # 🔐 PERMISSÕES DO CANAL
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            entregador: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )
        }

        channel_name = f"ticket-{interaction.user.name}".lower()

        canal = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            reason="Ticket criado via /call"
        )

        await canal.send(
            f"📦 **Atendimento iniciado**\n\n"
            f"👤 Cliente: {interaction.user.mention}\n"
            f"🚚 Entregador: {entregador.mention}\n\n"
            f"Use este chat para combinar a entrega."
        )

async def setup(bot):
    await bot.add_cog(Call(bot))
