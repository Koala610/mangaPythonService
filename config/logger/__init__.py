import logging as logger
from datetime import datetime, timezone

cur_time = datetime.now(timezone.utc).astimezone()
cur_time = datetime.strftime(cur_time, '%z')
logger.basicConfig(
    level=logger.DEBUG,
    format='[%(asctime)s] [%(levelname)s] - %(message)s; locale: (%(pathname)s).<module>(:%(lineno)d)',
    datefmt=f'%Y-%m-%d %H:%M:%S {cur_time}')