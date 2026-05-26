from src.providers.base import EmailMessage, EmailCategory
from src.classifier.rules import (
    SPAM_SUBJECT_PATTERNS, SPAM_BODY_PATTERNS,
    VERIFICATION_SUBJECT_PATTERNS, VERIFICATION_BODY_PATTERNS,
    SECURITY_SUBJECT_PATTERNS, SECURITY_BODY_PATTERNS,
    PROMOTION_SUBJECT_PATTERNS, PROMOTION_BODY_PATTERNS,
    IMPORTANT_SUBJECT_PATTERNS, SUBSCRIPTION_SUBJECT_PATTERNS
)
from src.utils.logger import logger
from src.utils.config import config_manager

class ClassificationEngine:
    """Motor encargado de analizar y etiquetar un correo electrónico en base a reglas y puntuaciones."""
    
    def classify(self, email: EmailMessage) -> EmailCategory:
        # 1. Comprobar si pertenece a dominios importantes configurados o de confianza
        important_domains = config_manager.get("important_domains", [])
        whitelist_domains = config_manager.get("whitelist_domains", [])
        
        sender_lower = email.sender_email.lower()
        if any(domain in sender_lower for domain in important_domains):
            return EmailCategory.IMPORTANTE
            
        if any(domain in sender_lower for domain in whitelist_domains):
            # Whitelist por defecto se mantiene en la bandeja habitual o importante
            return EmailCategory.IMPORTANTE

        # 2. Comprobar si el dominio del remitente está en la lista negra (SPAM automático)
        blacklist_domains = config_manager.get("blacklist_domains", [])
        if any(domain in sender_lower for domain in blacklist_domains):
            return EmailCategory.SPAM

        scores = {
            EmailCategory.SPAM: 0,
            EmailCategory.VERIFICACION: 0,
            EmailCategory.ALERTA_SEGURIDAD: 0,
            EmailCategory.PROMOCION: 0,
            EmailCategory.IMPORTANTE: 0,
            EmailCategory.SUSCRIPCION: 0
        }

        # Puntuación de SPAM
        scores[EmailCategory.SPAM] += self._evaluate_patterns(email.subject, SPAM_SUBJECT_PATTERNS)
        scores[EmailCategory.SPAM] += self._evaluate_patterns(email.body, SPAM_BODY_PATTERNS)

        # Puntuación de Verificación / OTP
        scores[EmailCategory.VERIFICACION] += self._evaluate_patterns(email.subject, VERIFICATION_SUBJECT_PATTERNS)
        scores[EmailCategory.VERIFICACION] += self._evaluate_patterns(email.body, VERIFICATION_BODY_PATTERNS)

        # Puntuación de Alertas de Seguridad
        scores[EmailCategory.ALERTA_SEGURIDAD] += self._evaluate_patterns(email.subject, SECURITY_SUBJECT_PATTERNS)
        scores[EmailCategory.ALERTA_SEGURIDAD] += self._evaluate_patterns(email.body, SECURITY_BODY_PATTERNS)

        # Puntuación de Promociones
        scores[EmailCategory.PROMOCION] += self._evaluate_patterns(email.subject, PROMOTION_SUBJECT_PATTERNS)
        scores[EmailCategory.PROMOCION] += self._evaluate_patterns(email.body, PROMOTION_BODY_PATTERNS)
        # Si tiene cabecera List-Unsubscribe, es un claro indicador de newsletter/promoción
        if email.headers and 'List-Unsubscribe' in email.headers:
            scores[EmailCategory.PROMOCION] += 3

        # Puntuación de Transacciones/Importantes
        scores[EmailCategory.IMPORTANTE] += self._evaluate_patterns(email.subject, IMPORTANT_SUBJECT_PATTERNS)

        # Puntuación de Suscripciones/Boletines
        scores[EmailCategory.SUSCRIPCION] += self._evaluate_patterns(email.subject, SUBSCRIPTION_SUBJECT_PATTERNS)

        # Encontrar la categoría con la puntuación máxima
        best_cat = EmailCategory.SIN_CLASIFICAR
        max_score = 0
        for cat, score in scores.items():
            if score > max_score:
                max_score = score
                best_cat = cat

        # Umbral mínimo de confianza
        if max_score >= 3:
            email.category = best_cat
        else:
            email.category = EmailCategory.SIN_CLASIFICAR

        logger.debug(f"Correo clasificado: '{email.subject}' -> {email.category.value} (Puntaje: {max_score})")
        return email.category

    def _evaluate_patterns(self, text: str, patterns: list) -> int:
        if not text:
            return 0
        score = 0
        for pattern, weight in patterns:
            if pattern.search(text):
                score += weight
        return score
