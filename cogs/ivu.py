import base64
import logging
import asyncio
import discord
from discord.ext import commands

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
			self.passwords = {f.read()}

	@property
	def passwords(self):
		return self._passwords

	@passwords.setter
	def passwords(self, passwords: set):
		"""
		accepts a set of length 1.
		sets internal set to also contain the base64 encoded version of the given password.
		"""
		# for CTF style fun
		passwords = passwords.copy()
		passwords.add(base64.b64encode(list(passwords)[0].encode()).decode())
		self._passwords = passwords

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

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		if message.channel.id != self.bot.config['ids']['entry_channel']:
			return

		if message.content not in self.passwords:
			return

		role = message.guild.get_role(self.bot.config['ids']['grant_role'])
		await message.author.add_roles(role)

	@commands.command(name='set-password')
	@commands.check(has_ivu_admin_role)
	async def set_password(self, ctx, password):
		with open('password.txt', 'w') as f:
			f.write(password)
		self.passwords = {password}
		await ctx.message.add_reaction(self.bot.config['success_emojis'][True])

async def setup(bot):
	await bot.add_cog(Ivu(bot))
