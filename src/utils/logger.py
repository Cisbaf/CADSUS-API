import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

# Força timezone local do processo
os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

os.makedirs("logs", exist_ok=True)

class LocalTimeFormatter(logging.Formatter):
    def converter(self, timestamp):
        return time.localtime(timestamp)

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(
    filename="logs/requests.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)

formatter = LocalTimeFormatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# ERROR também no stderr, para aparecer em `docker compose logs`.
# INFO (que carrega o corpo da requisição, com CPF/CNS) fica só no arquivo.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
