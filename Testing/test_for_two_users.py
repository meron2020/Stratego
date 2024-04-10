import asyncio
import threading

from Frontend.Game.GameHandler import GameHandler

guiHandler = GameHandler(1, 1)
threading.Thread(asyncio.run(guiHandler.game_loop()), daemon=True).start()

