import ctypes
import sys
import os
import urllib.request
import winreg

def is_windows() -> bool:
    """Verifica si el sistema operativo actual es Windows."""
    return os.name == 'nt'

def get_windows_version() -> str:
    """Intenta determinar si el sistema es Windows 10, Windows 11 o desconocido."""
    if not is_windows():
        return "Not Windows"
    try:
        # Consultar la clave del Registro de Windows para obtener detalles de la compilación
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
            build = int(winreg.QueryValueEx(key, "CurrentBuild")[0])
            if build >= 22000:
                return "Windows 11"
            elif build >= 10240:
                return "Windows 10"
    except Exception:
        pass
    return "Windows (Desconocido)"

def is_admin() -> bool:
    """Determina si el programa se está ejecutando con permisos de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def request_admin() -> None:
    """Reinicia la aplicación solicitando elevación de privilegios UAC de Windows."""
    if not is_windows():
        return
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        f'"{script}" {params}',
        None,
        1
    )

def is_outlook_installed() -> bool:
    """Verifica mediante el registro de Windows si Microsoft Outlook está instalado en el equipo."""
    if not is_windows():
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Outlook.Application") as key:
            return True
    except FileNotFoundError:
        return False

def check_internet_connection() -> bool:
    """Valida si hay conexión a internet para poder conectarse a Gmail."""
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        return True
    except Exception:
        return False
