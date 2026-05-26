from typing import List, Dict, Any
from src.providers.base import EmailProvider, EmailMessage, EmailCategory
from src.classifier.categories import CATEGORY_ACTIONS
from src.cleaner.scheduler import scheduler
from src.utils.logger import logger
from src.utils.config import config_manager

class CleanerEngine:
    """Motor que ejecuta las acciones físicas sobre los correos según su categoría y configuración."""
    
    def __init__(self, provider: EmailProvider):
        self.provider = provider

    def clean(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        stats = {
            "processed": len(emails),
            "moved_important": 0,
            "moved_promo": 0,
            "deleted_spam": 0,
            "scheduled_otp": 0,
            "ignored": 0
        }

        # Asegurar que las carpetas destino existen antes de realizar los movimientos
        folders_to_create = set()
        for action in CATEGORY_ACTIONS.values():
            if action.action == 'keep' and action.folder_name != 'Inbox':
                folders_to_create.add(action.folder_name)

        for folder in folders_to_create:
            self.provider.create_folder(folder)

        # Invertir iteración de correos para evitar problemas al eliminar/mover en cascada si aplica
        for email in emails:
            action_cfg = CATEGORY_ACTIONS.get(email.category)
            if not action_cfg:
                stats["ignored"] += 1
                continue

            if action_cfg.action == 'delete':
                # Eliminar SPAM de forma inmediata
                success = self.provider.delete_email(email)
                if success:
                    stats["deleted_spam"] += 1
                    logger.info(f"Eliminado inmediato (Spam): '{email.subject}'")
                else:
                    stats["ignored"] += 1

            elif action_cfg.action == 'delete_delayed':
                # Agregar al planificador de eliminación de códigos de verificación
                delay = config_manager.get("verification_delete_timer", 900)
                scheduler.add_to_queue(email, self.provider, delay)
                stats["scheduled_otp"] += 1
                logger.info(f"Programado para eliminar: '{email.subject}' en {delay}s.")

            elif action_cfg.action == 'keep' and action_cfg.folder_name != 'Inbox':
                # Mover correos importantes, promociones y alertas a sus carpetas correspondientes
                success = self.provider.move_email(email, action_cfg.folder_name)
                if success:
                    if action_cfg.folder_name == 'AC_Importantes':
                        stats["moved_important"] += 1
                    elif action_cfg.folder_name == 'AC_Promociones':
                        stats["moved_promo"] += 1
                else:
                    stats["ignored"] += 1
            else:
                stats["ignored"] += 1

        logger.info(f"Limpieza finalizada. Estadísticas: {stats}")
        return stats
