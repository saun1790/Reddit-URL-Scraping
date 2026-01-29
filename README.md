# 🔗 Reddit URL Scraper

Sistema profesional para extraer URLs externas de posts de Reddit. Incluye dashboard web interactivo y capacidad de backfill hasta 6 meses de datos históricos.

---

## 📋 Requisitos

- **Python 3.8+**
- **macOS / Linux / Windows**
- Conexión a Internet

---

## ⚡ Instalación Rápida

### 1. Instalar Dependencias

```bash
cd reddit_scraper
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuración Inicial (Primera vez)

El scraper NO requiere API keys de Reddit. Usa el API público sin autenticación.

---

## 🚀 Uso

### Opción 1: Dashboard Web (Recomendado)

**Iniciar el servidor:**

```bash
cd reddit_scraper
source venv/bin/activate
python web_viewer.py
```

**Abrir en navegador:**

```
http://localhost:3010
```

#### Funcionalidades del Dashboard:

- ✅ **Ver todas las URLs** con búsqueda y filtros
- ✅ **Ordenar columnas** haciendo clic en las cabeceras
- ✅ **Redimensionar columnas** arrastrando los bordes
- ✅ **Fetch URLs** con progreso en tiempo real
- ✅ **Exportar a CSV** con un clic
- ✅ **Configurar subreddits** desde el menú Settings

#### Cómo usar el Fetch:

1. Clic en **"⚡ Fetch URLs"**
2. Seleccionar modo:
   - **Daily**: Solo posts nuevos desde la última ejecución
   - **Backfill**: Histórico (hasta 180 días / ~6 meses)
3. Configurar días si es Backfill
4. Ver progreso en tiempo real
5. ¡Listo! Los datos se actualizan automáticamente

---

### Opción 2: Línea de Comandos

#### Primera vez - Obtener datos históricos (6 meses):

```bash
python reddit_scraper_noauth.py --backfill 180 --subreddits SideProject
```

#### Uso diario - Solo datos nuevos:

```bash
python reddit_scraper_noauth.py --daily --subreddits SideProject
```

#### Múltiples subreddits:

```bash
python reddit_scraper_noauth.py --backfill 90 --subreddits SideProject startups entrepreneur
```

#### Exportar a CSV:

```bash
python reddit_scraper_noauth.py --export mi_archivo.csv
```

#### Ver estadísticas:

```bash
python reddit_scraper_noauth.py --stats
```

---

## 📊 Datos Extraídos

El sistema guarda:

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **url** | URL externa encontrada | https://example.com |
| **post_date** | Fecha del post | 2026-01-29 10:30:15 |
| **subreddit** | Subreddit de origen | SideProject |
| **post_id** | ID único del post | 1qq7qfq |

**Base de datos:** `reddit_urls.db` (SQLite)

**Exportación CSV:** Formato estándar compatible con Excel/Google Sheets

---

## ⚙️ Configurar Subreddits

### Desde el Dashboard:

1. Clic en **"⚙️ Settings"**
2. Agregar o quitar subreddits
3. Se guardan automáticamente

### Desde línea de comandos:

Simplemente lista los subreddits al ejecutar:

```bash
python reddit_scraper_noauth.py --daily --subreddits SideProject startups entrepreneur
```

---

## 🔄 Automatización (Opcional)

### Ejecutar automáticamente cada día:

**macOS/Linux - Cron:**

```bash
crontab -e
```

Agregar esta línea (reemplaza la ruta):

```bash
0 9 * * * cd /ruta/a/reddit_scraper && ./venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject
```

Esto ejecutará el scraper todos los días a las 9:00 AM.

**Windows - Task Scheduler:**

1. Abrir "Programador de tareas"
2. Crear tarea básica
3. Acción: Ejecutar programa
4. Programa: `C:\ruta\a\venv\Scripts\python.exe`
5. Argumentos: `reddit_scraper_noauth.py --daily --subreddits SideProject`
6. Carpeta de inicio: `C:\ruta\a\reddit_scraper`

---

## 📈 Capacidades

| Característica | Detalle |
|----------------|---------|
| **Datos históricos** | Hasta 6 meses (~180 días) |
| **Subreddits simultáneos** | Ilimitados |
| **Sin duplicados** | Constraint único en base de datos |
| **Rate limiting** | Respeta límites de Reddit automáticamente |
| **URLs procesadas** | Filtra links internos de Reddit |
| **Actualización diaria** | Solo trae posts nuevos |

---

## 🎯 Casos de Uso

- Monitorear lanzamientos de productos en r/SideProject
- Seguir trends en r/startups, r/entrepreneur
- Análisis de contenido externo compartido
- Lead generation de nuevos proyectos
- Research de competencia

---

## 🛠️ Comandos Útiles

```bash
# Ver cuántas URLs tienes
python reddit_scraper_noauth.py --stats

# Exportar todo a CSV
python reddit_scraper_noauth.py --export reddit_urls_$(date +%Y%m%d).csv

# Backfill 3 meses de varios subreddits
python reddit_scraper_noauth.py --backfill 90 --subreddits SideProject startups entrepreneur

# Iniciar dashboard
python web_viewer.py
```

---

## 📂 Estructura de Archivos

```
reddit_scraper/
├── reddit_scraper_noauth.py  # Script principal
├── web_viewer.py              # Dashboard web
├── database.py                # Gestión de SQLite
├── reddit_urls.db            # Base de datos
├── requirements.txt           # Dependencias Python
├── templates/
│   └── index.html            # Frontend del dashboard
└── README.md                 # Este archivo
```

---

## ❓ Problemas Comunes

### El dashboard no carga:

```bash
# Verificar que el puerto 3010 esté libre
lsof -i :3010

# Reiniciar el servidor
pkill -f web_viewer.py
python web_viewer.py
```

### No encuentra posts antiguos:

Reddit API tiene límites. Con múltiples endpoints podemos obtener ~6 meses para subreddits activos.

### Error de conexión:

Verificar conexión a internet y que Reddit no esté caído.

---

## 📞 Soporte

Para dudas o problemas:

1. Verificar que el entorno virtual esté activado: `source venv/bin/activate`
2. Ver logs en la terminal donde corre el servidor
3. Revisar `reddit_urls.db` con `sqlite3 reddit_urls.db`

---

## 🎉 ¡Listo!

Ya tienes todo configurado. Abre **http://localhost:3010** y empieza a extraer URLs de Reddit.

**Recomendación:** Ejecuta un backfill de 90-180 días la primera vez, luego usa modo `--daily` para mantener actualizado.
