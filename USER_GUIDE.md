# 📘 Guía de Usuario - Reddit URL Scraper

**Para usuarios no técnicos** - Guía simple y paso a paso

---

## 🎯 ¿Qué hace este sistema?

Este sistema recopila automáticamente **todas las URLs** (enlaces) compartidas en posts de Reddit de los subreddits que tú elijas.

**Ejemplo práctico:**
- Quieres ver todos los proyectos que la gente comparte en r/SideProject
- El sistema revisa todos los posts y extrae los enlaces (sitios web, apps, demos)
- Guarda todo en una base de datos para que puedas verlos fácilmente

---

## 🚀 Inicio Rápido

### Paso 1: Abrir el Dashboard

1. **Doble clic** en el archivo `START_DASHBOARD.bat` (Windows) o ejecuta el comando en terminal
2. Espera unos segundos hasta que veas: `Running on http://127.0.0.1:3010`
3. Abre tu navegador en: **http://localhost:3010**

### Paso 2: Configurar Subreddits

1. En el dashboard, haz clic en el botón **⚙️ Settings** (arriba a la derecha)
2. Verás una lista de subreddits actuales
3. Para agregar uno nuevo:
   - Escribe el nombre SIN "r/" (ejemplo: `startups`, no `r/startups`)
   - Presiona Enter o clic en el botón "+"
4. Para eliminar uno: clic en la ❌ al lado del nombre

**Subreddits recomendados para proyectos:**
- `SideProject` - Proyectos personales y startups
- `startups` - Startups y emprendimiento
- `entrepreneur` - Negocios y emprendedores
- `AlphaAndBetaUsers` - Gente buscando beta testers
- `InternetIsBeautiful` - Sitios web interesantes
- `SomebodyMakeThis` - Ideas de proyectos

### Paso 3: Recopilar URLs

Una vez configurados los subreddits:

1. Haz clic en **⚡ Fetch URLs**
2. El sistema comenzará a buscar automáticamente
3. Verás el progreso en tiempo real
4. Cuando termine, verás: "✅ Completado"

**⏱️ Tiempo estimado:** 
- Daily (actualización diaria): 1-2 minutos
- Backfill (histórico): 5-10 minutos

---

## 📊 Cómo Usar el Dashboard

### Vista Principal

```
┌─────────────────────────────────────────────────┐
│  Reddit URL Scraper          ⚙️ Settings  ⚡ Fetch│
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 3,866 URLs collected                        │
│  📅 Last update: 2 hours ago                    │
│                                                 │
│  🔍 Search: [_______________]  🗂️ All Subreddits│
│                                                 │
│  ┌────────────────────────────────────────┐   │
│  │ Post Title                              │   │
│  │ URL: https://example.com                │   │
│  │ r/SideProject • 2026-01-30              │   │
│  │ [🔗 Visit] [🗑️ Delete]                  │   │
│  └────────────────────────────────────────┘   │
│                                                 │
│  [← Previous]  Page 1 of 78  [Next →]         │
│                                                 │
│  [📥 Export CSV]                                │
└─────────────────────────────────────────────────┘
```

### Funciones Disponibles

#### 🔍 **Buscar**
- Escribe cualquier palabra (ejemplo: "AI", "marketplace", "notion")
- Busca en títulos de posts y URLs
- Actualiza resultados en tiempo real

#### 🗂️ **Filtrar por Subreddit**
- Desplegable "All Subreddits"
- Selecciona uno específico para ver solo esos posts

#### 🔗 **Visit (Visitar)**
- Abre el enlace en una nueva pestaña
- Te lleva directo al sitio web o proyecto

#### 🗑️ **Delete (Eliminar)**
- Elimina una URL específica de tu base de datos
- Útil para limpiar enlaces rotos o irrelevantes

#### 📥 **Export CSV**
- Descarga todos los datos en formato Excel/CSV
- Incluye: título, URL, subreddit, fecha
- Perfecto para análisis o compartir con tu equipo

---

## 🔄 Modos de Recopilación

### 🟢 Daily (Recomendado para uso normal)

**¿Qué hace?**
- Busca solo posts **nuevos** desde tu última actualización
- Rápido (1-2 minutos)
- Ideal para ejecutar diariamente

**Cuándo usar:**
- Tienes el histórico completo
- Solo quieres actualizaciones diarias
- Quieres resultados rápidos

**Cómo ejecutar:**
1. Clic en ⚡ Fetch URLs
2. Selecciona "Daily (new posts only)"
3. Clic en "Start"

---

### 🔵 Backfill (Para obtener historial)

**¿Qué hace?**
- Busca posts **históricos** (hasta 180 días atrás)
- Más lento (5-10 minutos)
- Obtiene mucha más información

**Cuándo usar:**
- Primera vez que usas el sistema
- Agregaste un subreddit nuevo
- Quieres completar datos faltantes

**Cómo ejecutar:**
1. Clic en ⚡ Fetch URLs
2. Selecciona "Backfill (historical)"
3. Elige cuántos días (30, 90, 180)
4. Clic en "Start"

**⚠️ Importante:** No uses Backfill todos los días, es innecesario y lento.

---

## 💡 Casos de Uso Comunes

### Caso 1: Monitoreo Diario de Proyectos

**Objetivo:** Ver nuevos proyectos que se comparten cada día

**Pasos:**
1. Configura subreddits: `SideProject`, `startups`, `AlphaAndBetaUsers`
2. Cada mañana: abre dashboard → clic en ⚡ Fetch URLs (Daily)
3. Revisa los nuevos enlaces agregados
4. Visita los que te interesen

**Resultado:** Siempre al día con nuevos proyectos y startups

---

### Caso 2: Investigación de Mercado

**Objetivo:** Analizar qué tipo de productos se están lanzando

**Pasos:**
1. Backfill de 90 días en `SideProject`
2. Export CSV para análisis
3. Busca palabras clave específicas (ej: "AI", "productivity", "B2B")
4. Analiza tendencias

**Resultado:** Reporte completo de lanzamientos recientes

---

### Caso 3: Encontrar Competencia

**Objetivo:** Ver qué proyectos similares al tuyo existen

**Pasos:**
1. Configura subreddits relevantes a tu nicho
2. Usa la búsqueda con keywords de tu producto
3. Visita los enlaces similares
4. Analiza sus enfoques

**Resultado:** Lista de competidores y alternativas

---

## 📝 Preguntas Frecuentes (FAQ)

### ❓ ¿Cada cuánto debo ejecutar el scraper?

**Respuesta:** Depende de tus necesidades:
- **Diario:** Si quieres estar al día con nuevos proyectos
- **Semanal:** Si solo revisas periódicamente
- **Cuando necesites:** El sistema guarda todo, puedes ejecutarlo cuando quieras

### ❓ ¿Cuántos subreddits puedo agregar?

**Respuesta:** Todos los que quieras, pero considera:
- Más subreddits = más tiempo de scraping
- Recomendamos 3-5 para empezar
- Puedes agregar/quitar cuando quieras

### ❓ ¿Los datos se guardan permanentemente?

**Respuesta:** Sí, todo se guarda en una base de datos local:
- No se pierde al cerrar el navegador
- Puedes acumular datos por meses
- Solo se pierde si borras el archivo `reddit_urls.db`

### ❓ ¿Qué pasa si veo URLs duplicadas?

**Respuesta:** El sistema automáticamente:
- Detecta URLs duplicadas
- Solo guarda una versión
- Si aparecen duplicados, son posts diferentes con el mismo enlace

### ❓ ¿Puedo usar esto en diferentes computadoras?

**Respuesta:** Sí, pero cada computadora tiene su propia base de datos:
- **Opción 1:** Usa Export CSV para transferir datos
- **Opción 2:** Copia el archivo `reddit_urls.db` entre computadoras
- **Opción 3:** Instala en un servidor para acceso remoto

### ❓ ¿Es legal scrapear Reddit?

**Respuesta:** Sí, este sistema:
- Usa datos públicos de Reddit
- Respeta las reglas de rate limiting
- No requiere login ni acceso privado
- Es similar a usar Reddit normalmente

### ❓ ¿Necesito una cuenta de Reddit?

**Respuesta:** No, el sistema funciona sin autenticación.

### ❓ ¿Qué hago si el scraping falla?

**Respuesta:** Revisa:
1. ¿Tienes internet?
2. ¿Reddit está funcionando? (visita reddit.com)
3. Intenta de nuevo en 5 minutos (puede ser rate limiting temporal)
4. Si persiste, contacta soporte

---

## 🎓 Tips y Mejores Prácticas

### ✅ Hazlo

- **Ejecuta Daily regularmente** - Mantén tu base de datos actualizada
- **Usa la búsqueda** - Filtra por keywords relevantes
- **Exporta regularmente** - Haz backups de tus datos
- **Limpia URLs irrelevantes** - Mantén tu base de datos limpia
- **Prueba diferentes subreddits** - Encuentra comunidades activas

### ❌ Evita

- **No ejecutes Backfill diario** - Es innecesario y lento
- **No agregues demasiados subreddits** - Empieza con 3-5
- **No cierres durante scraping** - Espera a que termine
- **No borres reddit_urls.db** - Es tu base de datos principal

---

## 🆘 Solución de Problemas

### Problema: "No se abre el dashboard"

**Solución:**
1. Verifica que el puerto 3010 no esté en uso
2. Cierra otras instancias del programa
3. Reinicia el sistema

### Problema: "No encuentra nuevas URLs"

**Posibles causas:**
- No hay posts nuevos en ese subreddit
- Ya tienes todos los posts recientes
- El subreddit está poco activo

**Solución:** Prueba con un subreddit más activo o usa Backfill

### Problema: "Scraping muy lento"

**Causas comunes:**
- Estás usando Backfill con muchos días
- Internet lento
- Rate limiting de Reddit

**Solución:** 
- Usa Daily en lugar de Backfill
- Reduce el número de días en Backfill
- Espera unos minutos e intenta de nuevo

### Problema: "Error al exportar CSV"

**Solución:**
1. Cierra el archivo CSV si está abierto en Excel
2. Intenta exportar con otro nombre
3. Verifica permisos de escritura en la carpeta

---

## 📞 Soporte

Si tienes problemas no listados aquí:

1. **Revisa los logs** - El dashboard muestra mensajes de error
2. **Intenta reiniciar** - Cierra y vuelve a abrir el sistema
3. **Documenta el error** - Toma captura de pantalla
4. **Contacta soporte** - Incluye detalles del error

---

## 🎉 ¡Listo para Empezar!

Ya tienes todo lo necesario para:
- ✅ Configurar el sistema
- ✅ Recopilar URLs de Reddit
- ✅ Buscar y filtrar proyectos
- ✅ Exportar datos para análisis

**Siguiente paso:** Abre el dashboard y comienza a explorar proyectos interesantes!

---

**Última actualización:** Enero 2026  
**Versión:** 1.0  
**Soporte:** Consulta el archivo README.md para detalles técnicos
