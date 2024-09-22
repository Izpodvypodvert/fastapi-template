from loguru import logger
import sys


logger.remove()  
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO", colorize=True)
logger.add("logs/app_{time}.log", rotation="1 day", retention="7 days", level="DEBUG")
