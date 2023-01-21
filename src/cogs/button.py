import discord
from discord import Interaction, ButtonStyle

class Button(discord.ui.Button):
    def __init__(self, *, style: ButtonStyle=ButtonStyle.link, label: str="label", emoji: str=None):
        super().__init__(style=style, label=label, emoji=emoji)

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message("clicked")
        pass

class DeleteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.grey, label="Delete", emoji="❌")

    async def callback(self, interaction: Interaction):
        await interaction.message.delete()