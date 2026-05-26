
# CleanMail

AutoCorreo (repositorio: **CleanMail**) es una aplicación de escritorio nativa para **Windows 10 y Windows 11** diseñada para automatizar la organización, clasificación y limpieza de bandejas de entrada de correo electrónico en **Microsoft Outlook** (vía COM API) y **Gmail** (vía API REST con OAuth2).

El programa clasifica de forma automática tus correos mediante expresiones regulares ponderadas y ejecuta tareas de limpieza inteligente.

---

## Características Principales

- **Clasificación Inteligente por Reglas**: Separa los correos automáticamente en categorías:
  - `IMPORTANTE`: Promociones reales y legítimas de comercios
  - `ALERTA_SEGURIDAD`: Avisos de inicios de sesión y seguridad
  - `VERIFICACION`: Códigos OTP o verificación de cuentas
  - `SPAM`: Correo no deseado y sospechoso
  - `SUSCRIPCION`: Newsletters y boletines
 
  - <img width="1490" height="710" alt="Captura de pantalla 2026-05-26 133451" src="https://github.com/user-attachments/assets/061ddd21-d0f5-48b3-a563-8c7e7f738224" />

- **Limpieza de Códigos Expirados**: Los correos detectados como códigos de verificación u OTP se eliminan automáticamente tras 15 minutos de haber sido recibidos

- **Eliminación de Spam Inmediata**: Borra directamente a la papelera los correos detectados como Spam

- **Interfaz Gráfica**: Diseñada con un tema oscuro elegante usando customtkinter

- **Ejecución Segura**: Sin necesidad de permisos de Administrador forzados para permitir la comunicación inter-procesos con Outlook

---

## Cómo Funciona

El motor del programa analiza el asunto, el remitente y el cuerpo del mensaje, asignando puntos de concordancia:

1. **Detección de Cabeceras**: Por ejemplo, `List-Unsubscribe` incrementa la puntuación de Promociones/Boletines

2. **Validación de Dominios**: Dominios conocidos (Google, Microsoft, bancos) tienen prioridad e inhiben la clasificación de Spam

3. **Filtrado RegEx**: Si las coincidencias de un grupo superan el umbral establecido, el correo se cataloga en dicho grupo y se mueve a las carpetas correspondientes

---

## Requisitos

- Python 3.10 o superior (en Windows)
- Microsoft Outlook de Escritorio (instalado para la integración con Outlook)
- Archivo de credenciales `credentials.json` en la raíz (solo si se utiliza Gmail API)

---

## Instalación

Instala las dependencias necesarias con:

```bash
pip install -r requirements.txt
```

---

## Uso

Para probarlo en modo de desarrollo:

```bash
python main.py
```

Para generar un ejecutable independiente `.exe`:

```bash
python -m PyInstaller build.spec
```

El ejecutable compilado se guardará en la carpeta `dist/AutoCorreo.exe`.

---

## Distribución

### Crear Release en GitHub

Para que otros usuarios puedan descargar el programa directamente sin instalar Python:

1. Ve a tu repositorio **CleanMail** en GitHub
2. Haz clic en **Releases** -> **Create a new release**
3. Establece una versión (ej: `v1.0.0`) y escribe una descripción
4. Arrastra y suelta el archivo **`dist/AutoCorreo.exe`** en la sección de Assets
5. Haz clic en **Publish release**

---

## Estructura del Proyecto

```
src/
├── classifier/       # Motor de clasificación de correos
├── cleaner/         # Limpieza y organización
├── gui/             # Interfaz gráfica
├── providers/       # Integraciones (Gmail, Outlook)
└── utils/           # Utilidades y configuración
```
