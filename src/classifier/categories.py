from enum import Enum
from dataclasses import dataclass
from typing import Dict

class EmailCategory(Enum):
    IMPORTANTE = 'importante'
    PROMOCION = 'promocion'
    ALERTA_SEGURIDAD = 'alerta_seguridad'
    VERIFICACION = 'verificacion'
    SPAM = 'spam'
    SUSCRIPCION = 'suscripcion'
    SIN_CLASIFICAR = 'sin_clasificar'

@dataclass
class CategoryAction:
    folder_name: str
    action: str  # 'keep', 'delete', 'delete_delayed'
    delay_seconds: int = 0
    description: str = ''
    icon: str = ''
    color: str = ''

CATEGORY_ACTIONS: Dict[EmailCategory, CategoryAction] = {
    EmailCategory.IMPORTANTE: CategoryAction('AC_Importantes', 'keep', 0, 'Correos personales e importantes', '⭐', '#4CAF50'),
    EmailCategory.PROMOCION: CategoryAction('AC_Promociones', 'keep', 0, 'Promociones reales de empresas', '🏷️', '#FF9800'),
    EmailCategory.ALERTA_SEGURIDAD: CategoryAction('AC_Importantes', 'keep', 0, 'Alertas de seguridad e inicio de sesión', '🔒', '#2196F3'),
    EmailCategory.VERIFICACION: CategoryAction('Inbox', 'delete_delayed', 900, 'Códigos de verificación (eliminar tras 15 min)', '🔑', '#9C27B0'),
    EmailCategory.SPAM: CategoryAction('', 'delete', 0, 'Correo basura y spam', '🚫', '#F44336'),
    EmailCategory.SUSCRIPCION: CategoryAction('AC_Promociones', 'keep', 0, 'Newsletters y suscripciones', '📰', '#607D8B'),
    EmailCategory.SIN_CLASIFICAR: CategoryAction('Inbox', 'keep', 0, 'Sin clasificar', '❓', '#9E9E9E'),
}
