import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """Создаёт и настраивает логер."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(logs_dir / "log.log", maxBytes=2000000, backupCount=5)
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-3d] %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
