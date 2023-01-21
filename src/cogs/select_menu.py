import discord

class SelectMenu(discord.ui.Select):
    def __init__(self,command_name:str,args:list,placeholder:str=""):
        options=[]
        for item in args:
            options.append(discord.SelectOption(label=item, value=f"{command_name}:{item}", description=""))
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        command_name, command_option = self.values[0].split(":")[:2]
        command = interaction._client.tree.get_command(command_name)
        cogs = interaction._client._BotBase__cogs.get(command_name.capitalize())
        await interaction.response.defer(thinking=True)
        await command.callback(cogs, interaction, command_option)