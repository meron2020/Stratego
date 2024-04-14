import asyncio
import threading

from Frontend.Game.GameHandler import GameHandler

guiHandler = GameHandler(1, 2)
threading.Thread(guiHandler.game_loop(), daemon=True).start()

