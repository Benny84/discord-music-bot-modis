"""Initialises Modis."""

import logging
import sys

from modis import datatools

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

formatter = logging.Formatter(
    "{asctime} {levelname:8} {name} - {message}", style="{")
printhandler = logging.StreamHandler(sys.stdout)
printhandler.setFormatter(formatter)
filehandler = logging.FileHandler("modis.log")
filehandler.setFormatter(formatter)

logger.addHandler(printhandler)
logger.addHandler(filehandler)

logger.info("----------------NEW INSTANCE----------------")
logger.info("Loading Modis")


def console(discord_token, discord_client_id):
    """
    Start Modis in console format.

    Args:
        discord_token (str): The bot token for your Discord application
        discord_client_id: The bot's client ID
    """

    logger.info("Starting Modis in console")

    datatools.log_compare_version(logger)

    import threading
    import asyncio

    logger.debug("Loading packages")
    from modis.discord_modis import main as discord_modis_console
    from modis.reddit_modis import main as reddit_modis_console
    from modis.facebook_modis import main as facebook_modis_console

    # Create threads
    logger.debug("Initiating threads")
    loop = asyncio.get_event_loop()
    discord_thread = threading.Thread(
        target=discord_modis_console.start,
        args=[discord_token, discord_client_id, loop])
    reddit_thread = threading.Thread(
        target=reddit_modis_console.start, args=[])
    facebook_thread = threading.Thread(
        target=facebook_modis_console.start, args=[])

    # Run threads
    logger.debug("Starting threads")
    discord_thread.start()
    reddit_thread.start()
    facebook_thread.start()

    logger.debug("Root startup completed")

