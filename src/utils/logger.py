import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "AutoCorreo") -> logging.Logger:
    """Configura y retorna el registrador de eventos (logger) de la aplicación."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        app_data = os.environ.get("APPDATA", os.path.expanduser("~"))
        log_dir = os.path.join(app_data, "AutoCorreo", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "autocorreo.log")

        # Formato de logs
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        # Manejador de archivo rotativo (10 MB por archivo, máximo 5 archivos de respaldo)
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Manejador de consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Instancia global de logging
logger = setup_logger()
