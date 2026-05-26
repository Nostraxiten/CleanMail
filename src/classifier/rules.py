import re
from typing import List, Tuple

# Patrones para SPAM
SPAM_SUBJECT_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(winner|won|lottery|congratulations|claim\s+your\s+prize)\b', re.I), 5),
    (re.compile(r'\b(act\s+now|urgent|click\s+immediately|limited\s+spots)\b', re.I), 4),
    (re.compile(r'\b(make\s+money|earn\s+\$|work\s+from\s+home|bitcoin\s+profit)\b', re.I), 5),
    (re.compile(r'\b(viagra|cialis|pharmacy|weight\s*loss\s*pill)\b', re.I), 5),
    (re.compile(r'\b(nigerian|inheritance|beneficiary|wire\s+transfer)\b', re.I), 5),
    (re.compile(r'\b(has ganado|felicidades|premio|reclama)\b', re.I), 4),
    (re.compile(r'\b(dinero\s+fácil|trabaja\s+desde\s+casa|gana\s+dinero)\b', re.I), 4),
]

SPAM_BODY_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(click\s+here\s+to\s+claim|send\s+money|bank\s+account\s+details)\b', re.I), 4),
]

# Patrones para VERIFICACIÓN
VERIFICATION_SUBJECT_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(verification|verificación)\s*(code|código)\b', re.I), 5),
    (re.compile(r'\b(one[\s-]?time\s*password|OTP|código\s+de\s+acceso)\b', re.I), 5),
    (re.compile(r'\bverif(y|ica)\s+(your|tu)\s+(email|correo|account|cuenta)\b', re.I), 4),
    (re.compile(r'\b(security|seguridad)\s*(code|código)\b', re.I), 4),
    (re.compile(r'\b(confirm|confirma)\s+(your|tu)\s+(email|correo|identity|identidad)\b', re.I), 3),
    (re.compile(r'\b(two[\s-]?factor|2FA|autenticación)\b', re.I), 4),
]

VERIFICATION_BODY_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(your|tu)\s+(verification|verificación)\s+(code|código)\s*(is|es|:)\s*\d{4,8}\b', re.I), 5),
    (re.compile(r'\b(enter|ingresa|introduce)\s+(this|este|the|el)\s+(code|código)\b', re.I), 4),
    (re.compile(r'\bcode\s*:\s*\d{4,8}\b', re.I), 5),
    (re.compile(r'\bcódigo\s*:\s*\d{4,8}\b', re.I), 5),
    (re.compile(r'\b(expires?|expira|válido)\s+(in|en|por|durante)\s+\d+\s+(minutes?|minutos?)\b', re.I), 3),
]

# Patrones para ALERTA DE SEGURIDAD
SECURITY_SUBJECT_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(security\s+alert|alerta\s+de\s+seguridad)\b', re.I), 5),
    (re.compile(r'\b(new|nuevo)\s+(sign[\s-]?in|inicio\s+de\s+sesión)\b', re.I), 5),
    (re.compile(r'\b(login|inicio)\s+(attempt|intento)\b', re.I), 4),
    (re.compile(r'\b(unrecognized|no\s+reconocido)\s+(device|dispositivo)\b', re.I), 5),
    (re.compile(r'\b(suspicious|sospechosa)\s+(activity|actividad)\b', re.I), 5),
    (re.compile(r'\b(password|contraseña)\s+(reset|changed|cambiada|restablecida)\b', re.I), 4),
]

SECURITY_BODY_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(new|nuevo)\s+(sign[\s-]?in|inicio)\s+(from|on|desde|en|detected|detectado)\b', re.I), 4),
    (re.compile(r'\b(was\s+this\s+you|fuiste\s+tú|reconoces\s+esta\s+actividad)\b', re.I), 4),
]

# Patrones para PROMOCIONES
PROMOTION_SUBJECT_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(special\s+offer|oferta\s+especial)\b', re.I), 3),
    (re.compile(r'\b(limited\s+time|tiempo\s+limitado|exclusive|exclusiv[oa])\b', re.I), 3),
    (re.compile(r'\b(discount|descuento|%\s*off|rebaja)\b', re.I), 3),
    (re.compile(r'\b(sale|rebajas|ofertas?)\b', re.I), 2),
    (re.compile(r'\b(free\s+shipping|envío\s+gratis|envío\s+gratuito)\b', re.I), 3),
    (re.compile(r'\b(buy\s+one|compra\s+uno|coupon|cupón|promo\s+code|código\s+promo)\b', re.I), 3),
]

PROMOTION_BODY_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\bunsubscribe\b|\bdarse\s+de\s+baja\b', re.I), 2),
    (re.compile(r'\b(view\s+in\s+browser|ver\s+en\s+el\s+navegador)\b', re.I), 2),
]

# Patrones para CORREOS IMPORTANTES
IMPORTANT_SUBJECT_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(invoice|factura|receipt|recibo)\b', re.I), 3),
    (re.compile(r'\b(order|pedido)\s+(confirm|shipping|envío|tracking|seguimiento)\b', re.I), 3),
    (re.compile(r'\b(payment|pago)\s+(confirm|received|recibido)\b', re.I), 3),
    (re.compile(r'\b(appointment|cita|meeting|reunión)\b', re.I), 2),
]

# Patrones para SUSCRIPCIONES
SUBSCRIPTION_SUBJECT_PATTERNS: List[Tuple[re.Pattern, int]] = [
    (re.compile(r'\b(newsletter|boletín|weekly\s+digest|resumen\s+semanal)\b', re.I), 4),
]
