import threading
import time
from datetime import datetime, timedelta
from typing import List, Tuple, Callable, Optional
from src.providers.base import EmailMessage, EmailProvider
from src.utils.logger import logger

class DeletionScheduler:
    """Planificador encargado de posponer y ejecutar la eliminación de correos tras un intervalo de tiempo (ej: 15 min)."""
    def __init__(self):
        self.queue: List[Tuple[EmailMessage, EmailProvider, datetime]] = []
        self.lock = threading.Lock()
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.on_deleted_callback: Optional[Callable[[EmailMessage], None]] = None

    def set_callback(self, callback: Callable[[EmailMessage], None]) -> None:
        self.on_deleted_callback = callback

    def add_to_queue(self, email: EmailMessage, provider: EmailProvider, delay_seconds: int) -> None:
        target_time = datetime.now() + timedelta(seconds=delay_seconds)
        with self.lock:
            # Evitar duplicados
            if not any(item[0].id == email.id for item in self.queue):
                self.queue.append((email, provider, target_time))
                logger.info(f"Correo '{email.subject}' programado para eliminación en {delay_seconds}s (a las {target_time.strftime('%H:%M:%S')}).")
        
        self.start()

    def start(self) -> None:
        with self.lock:
            if self.is_running:
                return
            self.is_running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        self.is_running = False

    def _run_loop(self) -> None:
        while self.is_running:
            now = datetime.now()
            to_delete = []
            
            with self.lock:
                # Filtrar los correos que ya superaron su tiempo de vida
                remaining_queue = []
                for item in self.queue:
                    email, provider, delete_time = item
                    if now >= delete_time:
                        to_delete.append((email, provider))
                    else:
                        remaining_queue.append(item)
                self.queue = remaining_queue

            # Ejecutar eliminaciones fuera del bloqueo para no congelar la cola
            for email, provider in to_delete:
                try:
                    logger.info(f"Eliminando diferido: Correo '{email.subject}' (OTP/Verificación).")
                    provider.delete_email(email)
                    if self.on_deleted_callback:
                        self.on_deleted_callback(email)
                except Exception as e:
                    logger.error(f"Error al eliminar correo diferido '{email.subject}': {e}")

            time.sleep(5)

    def get_pending_count(self) -> int:
        with self.lock:
            return len(self.queue)

    def get_pending_list(self) -> List[Tuple[str, str, int]]:
        """Retorna una lista simplificada para la interfaz: (Asunto, Remitente, Segundos restantes)."""
        now = datetime.now()
        result = []
        with self.lock:
            for email, _, delete_time in self.queue:
                remaining = int((delete_time - now).total_seconds())
                result.append((email.subject, email.sender_email, max(0, remaining)))
        return result

# Instancia global del planificador
scheduler = DeletionScheduler()
