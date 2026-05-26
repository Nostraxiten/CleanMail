import os
import json
import threading
from typing import Any, Dict, List

DEFAULT_CONFIG = {
    "provider": "outlook",
    "scan_interval": 300,
    "verification_delete_timer": 900,  # 15 minutos en segundos
    "whitelist_domains": [
        "microsoft.com", "google.com", "apple.com", "amazon.com", "paypal.com",
        "github.com", "gitlab.com", "netflix.com", "spotify.com"
    ],
    "blacklist_domains": [
        "spam.com", "phishing.net", "lottery-win.org"
    ],
    "important_domains": [
        "bbva.com", "santander.com", "caixabank.es", "ing.es", "bankinter.com"
    ]
}

class ConfigManager:
    """Clase para gestionar la configuración de la aplicación de forma persistente y segura entre hilos."""
    def __init__(self):
        self.config_dir = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "AutoCorreo")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.lock = threading.Lock()
        self.config = DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        with self.lock:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir, exist_ok=True)
            if os.path.exists(self.config_file):
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        user_config = json.load(f)
                        self.config.update(user_config)
                except Exception:
                    pass

    def save(self) -> None:
        with self.lock:
            if not os.path.exists(self.config_dir):
                os.makedirs(self.config_dir, exist_ok=True)
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=4, ensure_ascii=False)
            except Exception:
                pass

    def get(self, key: str, default: Any = None) -> Any:
        with self.lock:
            return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self.lock:
            self.config[key] = value
        self.save()

    def reset_defaults(self) -> None:
        with self.lock:
            self.config = DEFAULT_CONFIG.copy()
        self.save()

# Instancia global de configuración
config_manager = ConfigManager()
