#!/usr/bin/env python

import bot_bin.bot
import qtoml as toml

class IvuBot(bot_bin.bot.Bot):
	startup_extensions = [
		'jishaku',
		'cogs.ivu',
	]

def main():
	with open('config.toml') as f:
		config = toml.load(f)
	IvuBot(config=config).run()

if __name__ == '__main__':
	main()
