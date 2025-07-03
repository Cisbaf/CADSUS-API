# src/utils/logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Cria a pasta de logs se necessário
os.makedirs("logs", exist_ok=True)

# Configura o logger
logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

# Rotaciona o log diariamente
handler = TimedRotatingFileHandler(
    filename="logs/requests.log",
    when="midnight",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
