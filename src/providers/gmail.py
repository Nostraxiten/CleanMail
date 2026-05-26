import os
import base64
from datetime import datetime
from typing import List, Optional
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from src.providers.base import EmailProvider, EmailMessage, EmailCategory
from src.utils.logger import logger

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailProvider(EmailProvider):
    """Proveedor de correo electrónico usando la API REST oficial de Gmail."""
    def __init__(self):
        self.service = None
        self.creds = None
        app_data = os.environ.get("APPDATA", os.path.expanduser("~"))
        self.token_path = os.path.join(app_data, "AutoCorreo", "gmail_token.json")
        self.credentials_path = os.path.abspath("credentials.json")

    def connect(self) -> bool:
        try:
            if os.path.exists(self.token_path):
                self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_path):
                        logger.error(f"Falta el archivo 'credentials.json' para configurar Gmail API en: {self.credentials_path}")
                        return False
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Guardar el token para la próxima ejecución
                with open(self.token_path, 'w', encoding='utf-8') as token_file:
                    token_file.write(self.creds.to_json())

            self.service = build('gmail', 'v1', credentials=self.creds)
            logger.info("Conectado exitosamente a Gmail API.")
            return True
        except Exception as e:
            logger.error(f"Error al conectar con Gmail API: {e}")
            return False

    def disconnect(self) -> None:
        self.service = None
        logger.info("Desconectado de Gmail API.")

    def get_emails(self, folder: str = 'inbox', limit: int = 100) -> List[EmailMessage]:
        emails = []
        if not self.service:
            logger.error("Gmail no está conectado.")
            return emails
        try:
            # Si folder es 'inbox', filtramos por la bandeja de entrada
            query = 'label:INBOX'
            if folder != 'inbox':
                query = f'label:{folder}'
            
            results = self.service.users().messages().list(userId='me', q=query, maxResults=limit).execute()
            messages = results.get('messages', [])
            
            for msg_summary in messages:
                msg_id = msg_summary['id']
                try:
                    msg = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
                    payload = msg.get('payload', {})
                    headers_list = payload.get('headers', [])
                    
                    subject = next((h['value'] for h in headers_list if h['name'].lower() == 'subject'), 'Sin asunto')
                    sender = next((h['value'] for h in headers_list if h['name'].lower() == 'from'), 'Desconocido')
                    date_str = next((h['value'] for h in headers_list if h['name'].lower() == 'date'), '')
                    list_unsubscribe = next((h['value'] for h in headers_list if h['name'].lower() == 'list-unsubscribe'), None)
                    
                    # Intentar parsear fecha
                    try:
                        received_date = datetime.strptime(date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
                    except Exception:
                        received_date = datetime.now()

                    # Decodificar el cuerpo del correo
                    body = self._parse_body(payload)
                    is_read = 'UNREAD' not in msg.get('labelIds', [])
                    
                    headers_dict = {}
                    if list_unsubscribe:
                        headers_dict['List-Unsubscribe'] = list_unsubscribe

                    email_msg = EmailMessage(
                        id=msg_id,
                        subject=subject,
                        sender_name=sender.split('<')[0].strip(),
                        sender_email=sender,
                        body=body,
                        received_date=received_date,
                        is_read=is_read,
                        headers=headers_dict,
                        raw_object=msg
                    )
                    emails.append(email_msg)
                except Exception as e:
                    logger.error(f"Error procesando correo {msg_id} en Gmail: {e}")
            logger.info(f"Se recuperaron {len(emails)} correos desde Gmail.")
        except Exception as e:
            logger.error(f"Error al obtener correos de Gmail: {e}")
        return emails

    def _parse_body(self, payload: dict) -> str:
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif 'parts' in part:
                    body += self._parse_body(part)
        else:
            data = payload.get('body', {}).get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        return body

    def move_email(self, email: EmailMessage, destination_folder: str) -> bool:
        if not self.service:
            return False
        try:
            # En Gmail las carpetas son Etiquetas (Labels). Primero validamos/creamos la etiqueta.
            label_id = self._get_or_create_label_id(destination_folder)
            if not label_id:
                return False

            self.service.users().messages().modify(
                userId='me',
                id=email.id,
                body={
                    'addLabelIds': [label_id],
                    'removeLabelIds': ['INBOX']
                }
            ).execute()
            logger.info(f"Correo '{email.subject}' movido/etiquetado en Gmail como '{destination_folder}'.")
            return True
        except Exception as e:
            logger.error(f"Error al mover correo en Gmail: {e}")
            return False

    def delete_email(self, email: EmailMessage) -> bool:
        if not self.service:
            return False
        try:
            # Enviar a la papelera (Trash)
            self.service.users().messages().trash(userId='me', id=email.id).execute()
            logger.info(f"Correo '{email.subject}' enviado a la papelera de Gmail.")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar correo en Gmail: {e}")
            return False

    def create_folder(self, name: str) -> bool:
        return self._get_or_create_label_id(name) is not None

    def get_folders(self) -> List[str]:
        folders = []
        if not self.service:
            return folders
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            folders = [l['name'] for l in labels if l.get('type') == 'user']
        except Exception as e:
            logger.error(f"Error al listar etiquetas de Gmail: {e}")
        return folders

    def get_provider_name(self) -> str:
        return "Gmail"

    def _get_or_create_label_id(self, label_name: str) -> Optional[str]:
        if not self.service:
            return None
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            for label in labels:
                if label['name'].lower() == label_name.lower():
                    return label['id']
            
            # Crear etiqueta nueva si no existe
            new_label = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            created = self.service.users().labels().create(userId='me', body=new_label).execute()
            return created['id']
        except Exception as e:
            logger.error(f"Error al buscar/crear la etiqueta '{label_name}' en Gmail: {e}")
            return None
