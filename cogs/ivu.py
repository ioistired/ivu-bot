import base64
import logging
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger('cogs.ivu')

def has_ivu_admin_role(ctx):
	role_id = ctx.bot.config['ids']['admin_role']
	if ctx.author.get_role(role_id) is None:
		raise commands.MissingRole(role_id)
	return True

class Ivu(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# this doesn't need to be hashed or anything because it's not super sensitive
		# storing it in plain text lets admins refer to it to hand out to new attendees
		with open('password.txt') as f:
			self._set_password(f.read())

	def _set_password(self, password):
		# for CTF style fun
		self.passwords = {password, base64.b64encode(password.encode()).decode()}

	@commands.Cog.listener()
	async def on_member_join(self, member):
		entry_channel_id = self.bot.config['ids']['entry_channel']
		entry_channel = member.guild.get_channel(entry_channel_id)
		if entry_channel is None:
			logger.error('Member joined but entry channel %s not found!', entry_channel_id)
			return

		# if we send the message too quickly, the user might not see it, if
		# message history is disabled in the welcome channel
		# (as it should be)
		await asyncio.sleep(0.7)
		await entry_channel.send(self.bot.config['entry_message'])

	@app_commands.command(name='password')
	async def password_command(self, interaction, password: str):
		if password not in self.passwords:
			await interaction.response.send_message('Wrong password!', ephemeral=True)
			return

		grant_role = interaction.guild.get_role(self.bot.config['ids']['grant_role'])
		await interaction.user.add_roles(grant_role)

		if remove_role_id := self.bot.config['ids']['remove_role']:
			remove_role = interaction.guild.get_role(remove_role_id)
			await interaction.user.remove_roles(remove_role)

		await interaction.response.send_message('Thanks!', ephemeral=True)

	@commands.command(name='set-password')
	@commands.check(has_ivu_admin_role)
	async def set_password(self, ctx, password):
		with open('password.txt', 'w') as f:
			f.write(password)
		self._set_password(password)
		await ctx.message.add_reaction(self.bot.config['success_emojis'][True])

async def setup(bot):
	await bot.add_cog(Ivu(bot))
