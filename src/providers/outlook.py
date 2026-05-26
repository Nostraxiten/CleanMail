import win32com.client
import pythoncom
from datetime import datetime
from typing import List, Any
from src.providers.base import EmailProvider, EmailMessage, EmailCategory
from src.utils.logger import logger

class OutlookProvider(EmailProvider):
    """Proveedor de correo electrónico usando la API COM de Microsoft Outlook para Windows."""
    def __init__(self):
        self.outlook = None
        self.namespace = None
        self.inbox = None

    def connect(self) -> bool:
        try:
            pythoncom.CoInitialize()
            self.outlook = win32com.client.Dispatch("Outlook.Application")
            self.namespace = self.outlook.GetNamespace("MAPI")
            # 6 representa la carpeta por defecto de Bandeja de Entrada (olFolderInbox)
            self.inbox = self.namespace.GetDefaultFolder(6)
            logger.info("Conectado exitosamente a Microsoft Outlook.")
            return True
        except Exception as e:
            logger.error(f"Error al conectar con Outlook: {e}")
            return False

    def disconnect(self) -> None:
        self.outlook = None
        self.namespace = None
        self.inbox = None
        pythoncom.CoUninitialize()
        logger.info("Desconectado de Outlook.")

    def get_emails(self, folder: str = 'inbox', limit: int = 100) -> List[EmailMessage]:
        emails = []
        try:
            target_folder = self.inbox
            if folder != 'inbox':
                try:
                    target_folder = self.inbox.Folders(folder)
                except Exception:
                    logger.warning(f"Carpeta '{folder}' no encontrada en Outlook, usando Inbox por defecto.")
            
            # Obtener los elementos ordenados por fecha de recepción descendente
            items = target_folder.Items
            items.Sort("[ReceivedTime]", True)
            
            count = 0
            for i in range(1, items.Count + 1):
                if count >= limit:
                    break
                item = items[i]
                
                # Clase 43 indica un MailItem (mensaje de correo estándar)
                if getattr(item, 'Class', 0) == 43:
                    try:
                        # Extraer la fecha y hacerla naive (sin timezone) para compatibilidad
                        received_date = item.ReceivedTime
                        if hasattr(received_date, 'replace'):
                            received_date = received_date.replace(tzinfo=None)
                        else:
                            received_date = datetime.now()

                        headers = {}
                        # Intento de leer cabeceras básicas
                        try:
                            prop_accessor = item.PropertyAccessor
                            list_unsubscribe = prop_accessor.GetProperty("http://schemas.microsoft.com/mapi/string/{00020329-0000-0000-C000-000000000046}/List-Unsubscribe")
                            if list_unsubscribe:
                                headers['List-Unsubscribe'] = list_unsubscribe
                        except Exception:
                            pass

                        email_msg = EmailMessage(
                            id=item.EntryID,
                            subject=item.Subject or "",
                            sender_name=item.SenderName or "",
                            sender_email=item.SenderEmailAddress or "",
                            body=item.Body or "",
                            received_date=received_date,
                            is_read=not item.UnRead,
                            headers=headers,
                            raw_object=item
                        )
                        emails.append(email_msg)
                        count += 1
                    except Exception as e:
                        logger.error(f"Error procesando correo individual en Outlook: {e}")
            logger.info(f"Se recuperaron {len(emails)} correos desde Outlook.")
        except Exception as e:
            logger.error(f"Error al obtener correos de Outlook: {e}")
        return emails

    def move_email(self, email: EmailMessage, destination_folder: str) -> bool:
        try:
            pythoncom.CoInitialize()
            if not email.raw_object:
                logger.error("No se puede mover el correo: Objeto COM original ausente.")
                return False
            
            # Buscar o crear la carpeta destino dentro del Inbox
            parent_folder = self.inbox
            target_folder = None
            for f in parent_folder.Folders:
                if f.Name == destination_folder:
                    target_folder = f
                    break
            
            if not target_folder:
                target_folder = parent_folder.Folders.Add(destination_folder)
                logger.info(f"Creada la carpeta '{destination_folder}' en Outlook.")

            # Mover utilizando el objeto COM original
            email.raw_object.Move(target_folder)
            logger.info(f"Correo '{email.subject}' movido correctamente a '{destination_folder}'.")
            return True
        except Exception as e:
            logger.error(f"Error al mover correo en Outlook: {e}")
            return False

    def delete_email(self, email: EmailMessage) -> bool:
        try:
            pythoncom.CoInitialize()
            if not email.raw_object:
                logger.error("No se puede eliminar el correo: Objeto COM original ausente.")
                return False
            
            # Delete() mueve el correo a la carpeta de Elementos Eliminados
            email.raw_object.Delete()
            logger.info(f"Correo '{email.subject}' enviado a la papelera en Outlook.")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar correo en Outlook: {e}")
            return False

    def create_folder(self, name: str) -> bool:
        try:
            pythoncom.CoInitialize()
            for f in self.inbox.Folders:
                if f.Name == name:
                    return True
            self.inbox.Folders.Add(name)
            logger.info(f"Carpeta '{name}' creada con éxito en Outlook.")
            return True
        except Exception as e:
            logger.error(f"Error al crear carpeta '{name}' en Outlook: {e}")
            return False

    def get_folders(self) -> List[str]:
        folders = []
        try:
            pythoncom.CoInitialize()
            for f in self.inbox.Folders:
                folders.append(f.Name)
        except Exception as e:
            logger.error(f"Error al listar carpetas de Outlook: {e}")
        return folders

    def get_provider_name(self) -> str:
        return "Outlook"
