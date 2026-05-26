# AutoCorreo (CleanMail) 📧

AutoCorreo (nombre del repositorio: **CleanMail**) es una aplicación de escritorio nativa para **Windows 10 y Windows 11** diseñada para automatizar la organización, clasificación y limpieza de bandejas de entrada de correo electrónico en **Microsoft Outlook** (vía COM API) y **Gmail** (vía API REST con OAuth2).

El programa clasifica de forma automática tus correos mediante expresiones regulares ponderadas y ejecuta tareas de limpieza.

---

## ✨ Características Principales

*   **Clasificación Inteligente por Reglas**: Separa los correos automáticamente en 6 categorías:
    *   `IMPORTANTE` (⭐): Correos personales, trabajo, bancos, etc.
    *   `PROMOCION` (🏷️): Promociones reales y legítimas de comercios.
    *   `ALERTA_SEGURIDAD` (🔒): Avisos de inicios de sesión y seguridad (se mantienen en Importantes).
    *   `VERIFICACION` (🔑): Códigos OTP o verificación de cuentas.
    *   `SPAM` (🚫): Correo no deseado y sospechoso.
    *   `SUSCRIPCION` (📰): Newsletters y boletines (se mantienen en Promociones).
*   **Limpieza de Códigos Expirados (15 Minutos)**: Los correos detectados como códigos de verificación u OTP se programan en segundo plano para su eliminación automática tras **15 minutos** de haber sido recibidos/procesados.
*   **Eliminación de Spam Inmediata**: Borra directamente a la papelera los correos detectados como Spam.
*   **Interfaz Gráfica Premium**: Diseñada con un tema oscuro elegante en `customtkinter`.
*   **Ejecución Segura**: Sin necesidad de permisos de Administrador forzados para permitir la correcta comunicación inter-procesos con Outlook.

---

## 🚀 Cómo Funciona

El motor del programa analiza el asunto, el remitente y el cuerpo del mensaje, asignando puntos (scores) de concordancia:
1.  **Detección de cabeceras**: Por ejemplo, `List-Unsubscribe` incrementa la puntuación de Promociones/Boletines.
2.  **Validación de Dominios**: Dominios conocidos (Google, Microsoft, bancos) tienen prioridad e inhiben la clasificación de Spam.
3.  **Filtrado RegEx**: Si las coincidencias de un grupo superan el umbral establecido, el correo se cataloga en dicho grupo y el motor físico del limpiador procede a moverlo a las carpetas `AC_Importantes`, `AC_Promociones` o a la Papelera.

---

## 🛠️ Requisitos de Desarrollo

*   Python 3.10 o superior (en Windows)
*   Microsoft Outlook de Escritorio (instalado para la integración con Outlook)
*   Archivo de credenciales `credentials.json` en la raíz (solo si vas a utilizar la integración de Gmail API)

Instala las dependencias necesarias con:
```bash
pip install -r requirements.txt
```

Para probarlo en modo de desarrollo:
```bash
python main.py
```

Para generar un nuevo ejecutable independiente `.exe`:
```bash
python -m PyInstaller build.spec
```

El ejecutable compilado se guardará en la carpeta `dist/AutoCorreo.exe`.

---

## 📦 Cómo Publicarlo / Distribuirlo

### Paso 1: Configurar GitHub y subir el repositorio
Para inicializar este código como repositorio local y subirlo a GitHub de forma remota bajo el nombre de **CleanMail**, ejecuta los siguientes comandos desde la terminal:

```bash
# 1. Inicializar el repositorio Git local
git init

# 2. Agregar los archivos del proyecto al área de preparación
git add .

# 3. Crear el primer commit
git commit -m "Initial commit - AutoCorreo CleanMail App"

# 4. Crear el repositorio en tu cuenta de GitHub (puedes usar GitHub CLI o la web)
# Si usas GitHub CLI:
gh repo create CleanMail --public --source=. --remote=origin --push

# O manualmente si ya creaste el repo en la web de GitHub:
git branch -M main
git remote add origin https://github.com/TU_USUARIO/CleanMail.git
git push -u origin main
```

### Paso 2: Publicar una "Release" con el ejecutable
Para que otros usuarios puedan descargar el programa directamente sin tener que instalar Python:

1.  Ve a tu repositorio **CleanMail** en GitHub.
2.  En la barra lateral derecha, haz clic en **Releases** -> **Create a new release**.
3.  Establece una versión (ej: `v1.0.0`) y escribe una descripción de las notas de la versión.
4.  Arrastra y suelta el archivo ejecutable compilado **`dist/AutoCorreo.exe`** en la sección de "Binaries/Assets".
5.  Haz clic en **Publish release**. ¡Cualquier usuario de Windows podrá descargar tu herramienta directamente!
