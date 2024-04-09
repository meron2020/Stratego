import asyncio

from Frontend.Game.GameHandler import GameHandler

guiHandler = GameHandler(1, 2)
asyncio.run(guiHandler.game_loop())
