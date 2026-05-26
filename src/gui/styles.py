"""
AutoCorreo — Estilos y temas para la interfaz gráfica.
Define la paleta de colores, fuentes y estilos del tema oscuro/claro.
"""

# ═══════════════════════════════════════════════════════════════
# Paleta de colores principal
# ═══════════════════════════════════════════════════════════════

COLORS = {
    # Fondo principal
    "bg_dark": "#1a1a2e",
    "bg_dark_secondary": "#16213e",
    "bg_dark_card": "#1f2940",
    "bg_dark_hover": "#253350",
    "bg_light": "#f0f2f5",
    "bg_light_secondary": "#ffffff",
    "bg_light_card": "#ffffff",

    # Acentos
    "accent_primary": "#e2b714",       # Dorado/amarillo (del logo)
    "accent_primary_hover": "#c9a012",
    "accent_secondary": "#3a86ff",     # Azul brillante
    "accent_secondary_hover": "#2d6fcc",

    # Estados
    "success": "#4CAF50",
    "success_hover": "#388E3C",
    "warning": "#FF9800",
    "warning_hover": "#F57C00",
    "error": "#F44336",
    "error_hover": "#D32F2F",
    "info": "#2196F3",
    "info_hover": "#1976D2",

    # Texto
    "text_primary_dark": "#e8e8e8",
    "text_secondary_dark": "#a0a0b0",
    "text_muted_dark": "#6b6b80",
    "text_primary_light": "#1a1a2e",
    "text_secondary_light": "#555570",
    "text_muted_light": "#8888a0",

    # Bordes
    "border_dark": "#2a3a5c",
    "border_light": "#d0d5dd",

    # Categorías de correo
    "cat_importante": "#4CAF50",
    "cat_promocion": "#FF9800",
    "cat_seguridad": "#2196F3",
    "cat_verificacion": "#9C27B0",
    "cat_spam": "#F44336",
    "cat_suscripcion": "#607D8B",
    "cat_sin_clasificar": "#9E9E9E",

    # Sidebar
    "sidebar_bg_dark": "#0f1529",
    "sidebar_bg_light": "#1a1a2e",
    "sidebar_hover_dark": "#1a2340",

    # Scrollbar
    "scrollbar_dark": "#2a3a5c",
    "scrollbar_light": "#c0c5cd",
}

# ═══════════════════════════════════════════════════════════════
# Fuentes
# ═══════════════════════════════════════════════════════════════

FONTS = {
    "title": ("Segoe UI", 22, "bold"),
    "heading": ("Segoe UI", 16, "bold"),
    "subheading": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 12),
    "body_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 10),
    "small_bold": ("Segoe UI", 10, "bold"),
    "mono": ("Consolas", 11),
    "mono_small": ("Consolas", 9),
    "icon_large": ("Segoe UI Emoji", 28),
    "icon_medium": ("Segoe UI Emoji", 18),
    "icon_small": ("Segoe UI Emoji", 14),
    "counter": ("Segoe UI", 36, "bold"),
}

# ═══════════════════════════════════════════════════════════════
# Dimensiones
# ═══════════════════════════════════════════════════════════════

DIMENSIONS = {
    "window_width": 1100,
    "window_height": 700,
    "window_min_width": 850,
    "window_min_height": 550,
    "sidebar_width": 240,
    "card_corner_radius": 12,
    "button_corner_radius": 8,
    "button_height": 38,
    "padding_large": 20,
    "padding_medium": 12,
    "padding_small": 6,
    "progress_height": 8,
    "border_width": 1,
}

# ═══════════════════════════════════════════════════════════════
# Iconos (emojis para la GUI)
# ═══════════════════════════════════════════════════════════════

ICONS = {
    "app": "📧",
    "outlook": "📨",
    "gmail": "✉️",
    "scan": "🔍",
    "clean": "🧹",
    "settings": "⚙️",
    "connect": "🔗",
    "disconnect": "🔌",
    "importante": "⭐",
    "promocion": "🏷️",
    "seguridad": "🔒",
    "verificacion": "🔑",
    "spam": "🚫",
    "suscripcion": "📰",
    "sin_clasificar": "❓",
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "clock": "⏰",
    "trash": "🗑️",
    "folder": "📁",
    "stats": "📊",
    "shield": "🛡️",
    "rocket": "🚀",
    "loading": "⏳",
    "check": "✓",
    "cross": "✗",
    "arrow_right": "→",
    "arrow_left": "←",
    "refresh": "🔄",
    "moon": "🌙",
    "sun": "☀️",
}

# ═══════════════════════════════════════════════════════════════
# Animación / Transiciones
# ═══════════════════════════════════════════════════════════════

ANIMATION = {
    "progress_speed": 20,       # ms entre actualizaciones de progreso
    "fade_duration": 300,       # ms para transiciones fade
    "pulse_interval": 1000,     # ms para efecto pulso
    "status_display_time": 5000,  # ms que se muestra un mensaje de estado
}
