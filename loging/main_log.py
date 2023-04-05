from loguru import logger
from datetime import date


today = date.today().strftime('%d.%m.%Y')
logger.add(f"log_files//{today}.txt", format="{time} {level} {message}", level="DEBUG", rotation="1 day", compression="zip")


async def entry_log(name, info):

    logger.info(f"Пользователь {name}: {info}")