from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Any

class EmailCategory(Enum):
    IMPORTANTE = 'importante'
    PROMOCION = 'promocion'
    ALERTA_SEGURIDAD = 'alerta_seguridad'
    VERIFICACION = 'verificacion'
    SPAM = 'spam'
    SUSCRIPCION = 'suscripcion'
    SIN_CLASIFICAR = 'sin_clasificar'

@dataclass
class EmailMessage:
    id: str
    subject: str
    sender_name: str
    sender_email: str
    body: str
    received_date: datetime
    is_read: bool
    category: EmailCategory = EmailCategory.SIN_CLASIFICAR
    headers: Optional[dict] = None
    raw_object: Any = None

class EmailProvider(ABC):
    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión con el proveedor de correo electrónico."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Cierra de forma segura la sesión y recursos con el proveedor."""
        pass

    @abstractmethod
    def get_emails(self, folder: str = 'inbox', limit: int = 100) -> List[EmailMessage]:
        """Obtiene la lista de correos electrónicos de la carpeta especificada."""
        pass

    @abstractmethod
    def move_email(self, email: EmailMessage, destination_folder: str) -> bool:
        """Mueve un mensaje de correo electrónico a la carpeta/etiqueta de destino."""
        pass

    @abstractmethod  
    def delete_email(self, email: EmailMessage) -> bool:
        """Elimina (o envía a la papelera) un mensaje de correo electrónico."""
        pass

    @abstractmethod
    def create_folder(self, name: str) -> bool:
        """Crea una nueva carpeta o etiqueta para la organización de correos."""
        pass

    @abstractmethod
    def get_folders(self) -> List[str]:
        """Retorna los nombres de las carpetas o etiquetas disponibles."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Retorna el nombre comercial del proveedor de correo (ej: 'Outlook', 'Gmail')."""
        pass
