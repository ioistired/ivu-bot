#!/usr/bin/env python

import discord
import bot_bin.bot
import qtoml as toml

class IvuBot(bot_bin.bot.Bot):
	startup_extensions = [
		'jishaku',
		'cogs.ivu',
	]
	def __init__(self, *args, **kwargs):
		intents = discord.Intents.default()
		intents.members = True
		super().__init__(*args, intents=intents, **kwargs)

def main():
	with open('config.toml') as f:
		config = toml.load(f)
	IvuBot(config=config).run()

if __name__ == '__main__':
	main()
