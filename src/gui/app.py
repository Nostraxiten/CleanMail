import customtkinter as ctk
import threading
import time
import os
from PIL import Image
from typing import Optional, List
from src.gui.styles import COLORS, FONTS, ICONS
from src.gui.setup_wizard import SetupWizard
from src.providers.base import EmailProvider, EmailMessage, EmailCategory
from src.providers.outlook import OutlookProvider
from src.providers.gmail import GmailProvider
from src.classifier.engine import ClassificationEngine
from src.cleaner.engine import CleanerEngine
from src.cleaner.scheduler import scheduler
from src.utils.config import config_manager
from src.utils.logger import logger

class AutoCorreoApp(ctk.CTk):
    """Aplicación principal de AutoCorreo con diseño elegante e intuitivo."""
    def __init__(self):
        super().__init__()
        
        # Configuración de Ventana
        self.title("AutoCorreo — Organización y Limpieza de Bandeja")
        self.geometry("950x650")
        self.configure(fg_color=COLORS["bg_dark"])

        self.provider: Optional[EmailProvider] = None
        self.classifier = ClassificationEngine()
        self.emails: List[EmailMessage] = []

        # Estructura del Layout
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Contenido principal
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_main_content()

        # Enlazar evento de eliminación diferida para actualizar logs en la interfaz
        scheduler.set_callback(self._on_otp_deleted)

        # Iniciar validación de configuración inicial
        self.after(500, self._check_first_run)

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, fg_color=COLORS["sidebar_bg_dark"], corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1) # Empujar elementos hacia abajo

        # Logo con Imagen Recortada
        logo_path = os.path.abspath(os.path.join("assets", "logo.png"))
        if os.path.exists(logo_path):
            try:
                logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
                logo_frame.grid(row=0, column=0, padx=10, pady=(20, 15), sticky="ew")
                logo_frame.grid_columnconfigure(1, weight=1)

                pil_img = Image.open(logo_path)
                ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(50, 50))
                logo_image_label = ctk.CTkLabel(logo_frame, image=ctk_img, text="")
                logo_image_label.grid(row=0, column=0, padx=(10, 10))
                
                logo_text_label = ctk.CTkLabel(
                    logo_frame, text="AutoCorreo", 
                    font=FONTS["heading"], text_color=COLORS["accent_primary"]
                )
                logo_text_label.grid(row=0, column=1, sticky="w")
            except Exception as e:
                logger.error(f"Error cargando logo en GUI: {e}")
                self._fallback_logo()
        else:
            self._fallback_logo()
            
    def _fallback_logo(self):
        # Logo de texto fallback
        logo_label = ctk.CTkLabel(
            self.sidebar, text=f"{ICONS['app']} AutoCorreo", 
            font=FONTS["title"], text_color=COLORS["accent_primary"]
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(25, 30))


        # Botones de Conexión
        self.btn_outlook = ctk.CTkButton(
            self.sidebar, text=f"{ICONS['outlook']} Conectar Outlook",
            font=FONTS["body_bold"], fg_color=COLORS["bg_dark_card"], text_color=COLORS["text_primary_dark"],
            hover_color=COLORS["bg_dark_hover"], height=40,
            command=self.connect_outlook
        )
        self.btn_outlook.grid(row=1, column=0, padx=20, pady=8, sticky="ew")

        self.btn_gmail = ctk.CTkButton(
            self.sidebar, text=f"{ICONS['gmail']} Conectar Gmail API",
            font=FONTS["body_bold"], fg_color=COLORS["bg_dark_card"], text_color=COLORS["text_primary_dark"],
            hover_color=COLORS["bg_dark_hover"], height=40,
            command=self.connect_gmail
        )
        self.btn_gmail.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        # Botones de Acción
        self.btn_scan = ctk.CTkButton(
            self.sidebar, text=f"{ICONS['scan']} Analizar Bandeja",
            font=FONTS["body_bold"], fg_color=COLORS["accent_secondary"], hover_color=COLORS["accent_secondary_hover"],
            height=40, state="disabled", command=self.scan_emails
        )
        self.btn_scan.grid(row=4, column=0, padx=20, pady=15, sticky="ew")

        self.btn_clean = ctk.CTkButton(
            self.sidebar, text=f"{ICONS['clean']} Ejecutar Limpieza",
            font=FONTS["body_bold"], fg_color=COLORS["success"], hover_color=COLORS["success_hover"],
            height=40, state="disabled", command=self.run_cleanup
        )
        self.btn_clean.grid(row=5, column=0, padx=20, pady=8, sticky="ew")

        # Configuración e Información Adicional
        self.theme_switch = ctk.CTkLabel(
            self.sidebar, text="AutoCorreo v1.0.0 © 2026",
            font=FONTS["small"], text_color=COLORS["text_muted_dark"]
        )
        self.theme_switch.grid(row=11, column=0, padx=20, pady=20)

    def _create_main_content(self):
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1)

        # Barra de Estado Superior
        self.status_bar = ctk.CTkFrame(self.main_content, fg_color=COLORS["bg_dark_secondary"], height=60, corner_radius=10)
        self.status_bar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.status_bar.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self.status_bar, text="Estado: No conectado a ningún buzón de correo.",
            font=FONTS["body_bold"], text_color=COLORS["text_primary_dark"]
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        # Panel de Progreso
        self.progress_bar = ctk.CTkProgressBar(self.main_content, height=8, fg_color=COLORS["bg_dark_secondary"], progress_color=COLORS["accent_primary"])
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.progress_bar.set(0)

        # Panel de Registro de Actividad y Resultados
        self.activity_frame = ctk.CTkFrame(self.main_content, fg_color=COLORS["bg_dark_secondary"], corner_radius=10)
        self.activity_frame.grid(row=2, column=0, sticky="nsew")
        self.activity_frame.grid_columnconfigure(0, weight=1)
        self.activity_frame.grid_rowconfigure(1, weight=1)

        activity_title = ctk.CTkLabel(
            self.activity_frame, text=f"{ICONS['stats']} Registro de Actividades y Resultados",
            font=FONTS["heading"], text_color=COLORS["accent_primary"]
        )
        activity_title.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.log_output = ctk.CTkTextbox(self.activity_frame, font=FONTS["mono"], fg_color=COLORS["bg_dark_card"], border_color=COLORS["border_dark"], border_width=1)
        self.log_output.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.log_output.insert("0.0", "AutoCorreo listo. Conecte un buzón para comenzar.\n")
        self.log_output.configure(state="disabled")

    def log(self, message: str):
        """Escribe mensajes en la consola visual del usuario en segundo plano de manera segura."""
        def _update():
            self.log_output.configure(state="normal")
            self.log_output.insert("end", f"{message}\n")
            self.log_output.see("end")
            self.log_output.configure(state="disabled")
        self.after(0, _update)

    def _check_first_run(self):
        # Desencadenar el asistente de configuración al arrancar
        SetupWizard(self, self._on_wizard_complete)

    def _on_wizard_complete(self, selected_provider: str):
        self.log(f"Configuración guardada: Proveedor preferido -> {selected_provider.upper()}")
        if selected_provider == "outlook":
            self.connect_outlook()
        else:
            self.connect_gmail()

    def connect_outlook(self):
        self.status_label.configure(text="Intentando conectar a Microsoft Outlook...", text_color=COLORS["warning"])
        def _connect():
            self.provider = OutlookProvider()
            if self.provider.connect():
                self.status_label.configure(text=f"Buzón: Microsoft Outlook {ICONS['success']}", text_color=COLORS["success"])
                self.btn_scan.configure(state="normal")
                self.log("Conectado exitosamente a la cuenta activa de Microsoft Outlook.")
            else:
                self.status_label.configure(text="Conexión a Outlook fallida.", text_color=COLORS["error"])
                self.log("Error al inicializar la conexión con Microsoft Outlook.")
        threading.Thread(target=_connect, daemon=True).start()

    def connect_gmail(self):
        self.status_label.configure(text="Iniciando autorización de Gmail...", text_color=COLORS["warning"])
        def _connect():
            self.provider = GmailProvider()
            if self.provider.connect():
                self.status_label.configure(text=f"Buzón: Gmail API {ICONS['success']}", text_color=COLORS["success"])
                self.btn_scan.configure(state="normal")
                self.log("Conectado exitosamente a Gmail mediante OAuth2.")
            else:
                self.status_label.configure(text="Conexión a Gmail fallida.", text_color=COLORS["error"])
                self.log("Error al inicializar la conexión con Gmail. Verifique credentials.json.")
        threading.Thread(target=_connect, daemon=True).start()

    def scan_emails(self):
        if not self.provider:
            return
        self.btn_scan.configure(state="disabled")
        self.progress_bar.set(0.1)
        self.log("\nIniciando escaneo de correos en la Bandeja de Entrada...")
        
        def _scan():
            try:
                self.emails = self.provider.get_emails(limit=50)
                self.progress_bar.set(0.5)
                self.log(f"Se descargaron {len(self.emails)} correos de la bandeja.")
                
                # Clasificación paso a paso
                classified_count = 0
                for email in self.emails:
                    self.classifier.classify(email)
                    classified_count += 1
                
                self.progress_bar.set(0.8)
                self.log(f"Clasificación terminada. Total correos analizados: {classified_count}")
                
                # Desglose de resultados para el usuario
                categories_summary = {}
                for email in self.emails:
                    categories_summary[email.category.value] = categories_summary.get(email.category.value, 0) + 1
                
                self.log("Resumen del análisis:")
                for cat_name, count in categories_summary.items():
                    self.log(f"  • {cat_name.upper()}: {count} correos")
                
                self.btn_clean.configure(state="normal")
                self.progress_bar.set(1.0)
            except Exception as e:
                self.log(f"Error en el análisis: {e}")
                logger.error(f"Error en escaneo de bandeja: {e}")
            finally:
                self.btn_scan.configure(state="normal")
                
        threading.Thread(target=_scan, daemon=True).start()

    def run_cleanup(self):
        if not self.provider or not self.emails:
            return
        self.btn_clean.configure(state="disabled")
        self.log("\nEjecutando limpieza y ordenamiento...")
        self.progress_bar.set(0.2)
        
        def _clean():
            try:
                cleaner = CleanerEngine(self.provider)
                stats = cleaner.clean(self.emails)
                self.progress_bar.set(0.8)
                
                self.log("\nResultados de la Limpieza:")
                self.log(f"  ✓ Spam eliminado permanentemente: {stats['deleted_spam']}")
                self.log(f"  ✓ Códigos OTP/Verificación programados para borrar en 15m: {stats['scheduled_otp']}")
                self.log(f"  ✓ Correos importantes clasificados: {stats['moved_important']}")
                self.log(f"  ✓ Promociones legítimas organizadas: {stats['moved_promo']}")
                
                self.progress_bar.set(1.0)
                self.emails = [] # Limpiar caché local de correos analizados
            except Exception as e:
                self.log(f"Error al limpiar: {e}")
            finally:
                self.btn_clean.configure(state="disabled")
                self.btn_scan.configure(state="normal")
                
        threading.Thread(target=_clean, daemon=True).start()

    def _on_otp_deleted(self, email: EmailMessage):
        self.log(f"⏱️ [Programador] Eliminado código de verificación expirado (15m): '{email.subject}' de {email.sender_email}")

if __name__ == "__main__":
    app = AutoCorreoApp()
    app.mainloop()
