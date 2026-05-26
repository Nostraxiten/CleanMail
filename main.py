import sys
from src.utils.permissions import is_windows, is_admin, request_admin, get_windows_version
from src.utils.logger import logger
from src.gui.app import AutoCorreoApp

def main():
    logger.info("Iniciando aplicación AutoCorreo...")

    # Validar que el sistema operativo sea Windows
    if not is_windows():
        logger.error("AutoCorreo solo está soportado en sistemas operativos Microsoft Windows.")
        sys.exit(1)

    logger.info(f"Sistema detectado: {get_windows_version()}")

    # Iniciar interfaz gráfica del usuario
    try:
        app = AutoCorreoApp()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Excepción crítica durante el bucle de la aplicación: {e}", exc_info=True)

if __name__ == "__main__":
    main()
