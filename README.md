# Reddit URL Scraper - Manual de Usuario

Sistema para extraer y organizar URLs compartidas en subreddits de Reddit.

## 🎯 ¿Qué hace?

Recopila automáticamente **todas las URLs** (enlaces web) de posts en los subreddits que configures:
- Proyectos, startups, herramientas
- Apps, sitios web, demos
- Todo se guarda en una base de datos
- Dashboard web para ver y buscar fácilmente

## ✨ Características

- 📊 **Dashboard Visual** - Interfaz web fácil de usar
- 🔍 **Búsqueda** - Encuentra URLs por palabra clave
- 📥 **Exportar a Excel** - Descarga datos en CSV
- 🔄 **Actualización Diaria** - Solo obtiene posts nuevos
- 📚 **Historial Completo** - Puede obtener posts de hasta 6 meses
- 🚫 **Sin duplicados** - No guarda la misma URL dos veces
- 🔓 **Sin cuenta Reddit** - No requiere login

## 📋 Requisitos Previos (Windows)

1. **Python 3.8 o superior**
   - Descargar de: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE:** Marcar "Add Python to PATH" durante instalación

2. **Git** (opcional, para actualizaciones)
   - Descargar de: https://git-scm.com/download/win

---

## 🚀 Instalación en Windows

### Paso 1: Descargar el Proyecto

**Opción A - Con Git:**
```powershell
git clone https://github.com/saun1790/Reddit-URL-Scraping.git
cd Reddit-URL-Scraping
```

**Opción B - Sin Git:**
1. Ve a: https://github.com/saun1790/Reddit-URL-Scraping
2. Clic en botón verde "Code" → "Download ZIP"
3. Descomprime el archivo
4. Abre PowerShell en esa carpeta (Shift + Click derecho → "Abrir PowerShell aquí")

### Paso 2: Instalar Dependencias

```powershell
# Si te da error de permisos, ejecuta esto primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Crear entorno virtual
python -m venv venv

# Instalar librerías
.\venv\Scripts\pip install -r requirements.txt
```

✅ **¡Instalación completa!**

---

## 🖥️ Usar el Dashboard

### Iniciar el Sistema

```powershell
.\venv\Scripts\python web_viewer.py
```

Verás algo como:
```
 * Running on http://127.0.0.1:3010
```

Abre tu navegador en: **http://localhost:3010**

### Configurar Subreddits

1. Clic en **⚙️ Settings** (esquina superior derecha)
2. Escribe el nombre del subreddit **sin** "r/" (ejemplo: `SideProject`)
3. Presiona Enter o clic en "+"
4. Para eliminar: clic en ❌ al lado del nombre

**Subreddits recomendados:**
- `SideProject` - Proyectos personales
- `startups` - Startups y emprendimiento  
- `entrepreneur` - Negocios
- `InternetIsBeautiful` - Sitios web interesantes

### Obtener URLs

1. Clic en **⚡ Fetch URLs**
2. Selecciona modo:
   - **Daily** (rápido, 1-2 min) - Solo posts nuevos
   - **Backfill** (lento, 5-10 min) - Posts históricos
3. Clic en **Start**
4. Espera a que termine

### Buscar y Filtrar

- **Búsqueda:** Escribe palabra clave (ej: "AI", "SaaS")
- **Filtro:** Desplegable para ver solo un subreddit
- **Exportar:** Botón "📥 Export CSV" descarga todo en Excel

---

## 💻 Uso Desde Línea de Comandos

### Actualización Diaria (Recomendado)

```powershell
.\venv\Scripts\python reddit_scraper_noauth.py --daily --subreddits SideProject startups
```

### Obtener Histórico (Primera Vez)

```powershell
# Últimos 30 días
.\venv\Scripts\python reddit_scraper_noauth.py --backfill 30 --subreddits SideProject

# Últimos 6 meses
.\venv\Scripts\python reddit_scraper_noauth.py --backfill 180 --subreddits SideProject startups
```

### Exportar a CSV

```powershell
.\venv\Scripts\python reddit_scraper_noauth.py --export urls.csv
```

### Ver Estadísticas

```powershell
.\venv\Scripts\python reddit_scraper_noauth.py --stats
```

---

## 🔄 Actualizar el Sistema

Si hay una versión nueva disponible:

```powershell
# Con Git
git pull

# Reinstalar dependencias (si hubo cambios)
.\venv\Scripts\pip install -r requirements.txt --upgrade
```

---

## 📊 Estructura de Datos

Los datos se guardan en `reddit_urls.db` (base de datos SQLite)

| Campo | Descripción |
|-------|-------------|
| `url` | Enlace web encontrado en el post |
| `post_date` | Fecha del post (UTC) |
| `subreddit` | De qué subreddit viene |
| `post_id` | ID del post en Reddit |

---

## 🆘 Solución de Problemas

### "Puerto 3010 ya está en uso"

Significa que ya tienes el dashboard abierto. Cierra la ventana anterior o:

```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :3010

# Matar el proceso (reemplaza PID con el número que aparece)
taskkill /PID <numero> /F
```

### "ModuleNotFoundError: No module named 'flask'"

Reinstala las dependencias:

```powershell
.\venv\Scripts\pip install -r requirements.txt
```

### "Error de permisos al activar venv"

Ejecuta primero:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Scraping muy lento

- Usa **Daily** en lugar de **Backfill**
- Reduce el número de días en Backfill
- Verifica tu conexión a internet

### No encuentra URLs nuevas

Posibles causas:
- No hay posts nuevos en ese subreddit
- Ya tienes todos los posts recientes
- El subreddit está inactivo

**Solución:** Prueba otro subreddit más activo

---

## 📁 Archivos del Proyecto

```
Reddit-URL-Scraping/
├── web_viewer.py             # Dashboard web
├── reddit_scraper_noauth.py  # Scraper (línea de comandos)
├── database.py               # Manejo de base de datos
├── requirements.txt          # Librerías necesarias
├── USER_GUIDE.md            # Guía completa de usuario (NO TÉCNICA)
├── templates/
│   └── index.html           # Interfaz del dashboard
└── reddit_urls.db           # Base de datos (se crea automáticamente)
```

---

## ❓ Preguntas Frecuentes

**¿Necesito una cuenta de Reddit?**  
No, el sistema funciona sin autenticación.

**¿Cuántos subreddits puedo agregar?**  
Todos los que quieras, pero recomendamos 3-5 para empezar.

**¿Los datos se guardan permanentemente?**  
Sí, todo se guarda en `reddit_urls.db`. No se pierde al cerrar.

**¿Puedo usar esto en otra computadora?**  
Sí, copia la carpeta completa (incluye el archivo `.db`).

**¿Cada cuánto debo ejecutar el scraper?**  
Depende de tus necesidades:
- Diario si quieres estar al día
- Semanal si solo revisas periódicamente
- Cuando lo necesites

---

## 📚 Documentación Adicional

- **USER_GUIDE.md** - Guía completa para usuarios (recomendado)
- **SUPER_SCRAPING_AGENT_PROMPT.md** - Documentación técnica avanzada

---

## 📞 Soporte

Si tienes problemas:
1. Revisa esta guía primero
2. Consulta **USER_GUIDE.md** para más detalles
3. Verifica que tienes la última versión (`git pull`)

---

**Última actualización:** Enero 2026  
**Versión:** 1.0  
**Licencia:** MIT
