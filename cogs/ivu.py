import discord
import discord.ui
from discord import app_commands
from discord.ext import commands

def has_ivu_admin_role(ctx):
	role_id = ctx.bot.config['ids']['required_role']
	if ctx.author.get_role(role_id) is None:
		raise commands.MissingRole(role_id)
	return True

class Ivu(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='set-password')
	@commands.check(has_ivu_admin_role)
	async def set_password(self, ctx, password):
		with open('password.txt', 'w') as f:
			f.write(password)
		await ctx.message.add_reaction(self.bot.config['success_emojis'][True])

async def setup(bot):
	await bot.add_cog(Ivu(bot))
