import customtkinter as ctk
from src.gui.styles import COLORS, FONTS, ICONS
from src.utils.config import config_manager
from src.utils.permissions import is_outlook_installed
from src.utils.logger import logger

class SetupWizard(ctk.CTkToplevel):
    """Ventana emergente de primer inicio y asistente de configuración rápida."""
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_save_callback = on_save_callback
        
        self.title("Configuración Inicial - AutoCorreo")
        self.geometry("500x450")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg_dark"])
        
        # Mantener foco y comportamiento modal
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        # Título
        title_label = ctk.CTkLabel(
            self, text="¡Bienvenido a AutoCorreo!", 
            font=FONTS["title"], text_color=COLORS["accent_primary"]
        )
        title_label.pack(pady=(30, 10))

        desc_label = ctk.CTkLabel(
            self, text="Configura tu proveedor de correo electrónico por defecto.",
            font=FONTS["body"], text_color=COLORS["text_secondary_dark"]
        )
        desc_label.pack(pady=(0, 25))

        # Marco de Selección de Proveedor
        self.provider_frame = ctk.CTkFrame(self, fg_color=COLORS["bg_dark_secondary"], corner_radius=12)
        self.provider_frame.pack(fill="x", padx=40, pady=10)

        self.provider_var = ctk.StringVar(value=config_manager.get("provider", "outlook"))

        # Radio Buttons
        self.outlook_radio = ctk.CTkRadioButton(
            self.provider_frame, text=f"{ICONS['outlook']} Microsoft Outlook (Escritorio)",
            variable=self.provider_var, value="outlook",
            font=FONTS["body_bold"], text_color=COLORS["text_primary_dark"],
            fg_color=COLORS["accent_primary"], hover_color=COLORS["accent_primary_hover"]
        )
        self.outlook_radio.pack(anchor="w", padx=30, pady=15)

        self.gmail_radio = ctk.CTkRadioButton(
            self.provider_frame, text=f"{ICONS['gmail']} Gmail (API REST)",
            variable=self.provider_var, value="gmail",
            font=FONTS["body_bold"], text_color=COLORS["text_primary_dark"],
            fg_color=COLORS["accent_primary"], hover_color=COLORS["accent_primary_hover"]
        )
        self.gmail_radio.pack(anchor="w", padx=30, pady=15)

        # Estado de compatibilidad
        self.status_info = ctk.CTkLabel(
            self, text="", font=FONTS["small"], text_color=COLORS["warning"]
        )
        self.status_info.pack(pady=10)
        self._check_outlook_status()

        # Botón Guardar
        save_btn = ctk.CTkButton(
            self, text="Comenzar Limpieza", font=FONTS["body_bold"],
            fg_color=COLORS["accent_primary"], hover_color=COLORS["accent_primary_hover"],
            text_color=COLORS["bg_dark"], height=40, corner_radius=8,
            command=self._save_and_close
        )
        save_btn.pack(pady=(30, 20))

    def _check_outlook_status(self):
        if not is_outlook_installed():
            self.status_info.configure(
                text="⚠️ Microsoft Outlook no está instalado en este equipo.\nSi seleccionas Gmail, necesitarás un archivo credentials.json."
            )
        else:
            self.status_info.configure(
                text="✨ Se ha detectado Outlook instalado correctamente en el sistema.",
                text_color=COLORS["success"]
            )

    def _save_and_close(self):
        selected_provider = self.provider_var.get()
        config_manager.set("provider", selected_provider)
        logger.info(f"Proveedor configurado en el asistente inicial: {selected_provider}")
        self.on_save_callback(selected_provider)
        self.destroy()
