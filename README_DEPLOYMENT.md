# 🚀 GUÍA DE DEPLOYMENT - DASHBOARD ELECTORAL CÓRDOBA

Esta guía te mostrará cómo subir tu dashboard a GitHub y desplegarlo en línea **GRATIS** usando Render.

---

## 📋 REQUISITOS PREVIOS

1. **Cuenta de GitHub** - [Crear cuenta](https://github.com/signup) (gratis)
2. **Cuenta de Render** - [Crear cuenta](https://render.com/signup) (gratis)
3. **Git instalado** - Verificar con `git --version` en terminal

---

## 🗂️ PASO 1: PREPARAR ARCHIVOS (YA ESTÁ LISTO)

Los siguientes archivos ya están creados y listos:

- ✅ `Procfile` - Indica cómo ejecutar la app
- ✅ `runtime.txt` - Especifica Python 3.13.7
- ✅ `render.yaml` - Configuración de Render
- ✅ `requirements.txt` - Dependencias de Python (con gunicorn)
- ✅ `.gitignore` - Archivos que NO se subirán a GitHub
- ✅ `app_improved.py` - Dashboard con `server` expuesto

---

## 📤 PASO 2: SUBIR A GITHUB

### Opción A: Desde la Terminal (Recomendado)

```bash
# 1. Inicializar repositorio Git (si no está inicializado)
git init

# 2. Configurar tu identidad (reemplaza con tus datos)
git config user.name "Tu Nombre"
git config user.email "tu_email@ejemplo.com"

# 3. Agregar todos los archivos
git add .

# 4. Crear primer commit
git commit -m "Initial commit - Dashboard Electoral Córdoba Capital"

# 5. Crear repositorio en GitHub
# Ve a https://github.com/new
# Nombre: dashboard-electoral-cordoba
# Descripción: Dashboard interactivo de resultados electorales - Córdoba Capital
# Público o Privado (tu elección)
# NO marques "Initialize with README" (ya tienes archivos)

# 6. Conectar con tu repositorio de GitHub
# Reemplaza 'TU_USUARIO' con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/dashboard-electoral-cordoba.git

# 7. Subir a GitHub
git branch -M main
git push -u origin main
```

### Opción B: Usando GitHub Desktop

1. Descarga [GitHub Desktop](https://desktop.github.com/)
2. Abre la app y ve a **File > Add Local Repository**
3. Selecciona la carpeta `D:\pj\2026\resultado\proyecto\pyoclaude`
4. Clic en **Publish repository**
5. Dale un nombre: `dashboard-electoral-cordoba`
6. Elige Público/Privado y clic **Publish**

---

## 🌐 PASO 3: DESPLEGAR EN RENDER

### Opción A: Usando render.yaml (Automático)

1. **Ve a [Render Dashboard](https://dashboard.render.com/)**

2. **Clic en "New +" → "Blueprint"**

3. **Conecta tu repositorio de GitHub:**
   - Autoriza Render para acceder a GitHub
   - Selecciona `dashboard-electoral-cordoba`

4. **Render detectará automáticamente el `render.yaml`**
   - Nombre del servicio: `dashboard-electoral-cordoba`
   - Plan: **Free**

5. **Clic en "Apply"**

6. **Espera 5-10 minutos mientras Render despliega**

7. **Tu app estará en:** `https://dashboard-electoral-cordoba.onrender.com`

### Opción B: Manual (sin render.yaml)

1. **Ve a [Render Dashboard](https://dashboard.render.com/)**

2. **Clic en "New +" → "Web Service"**

3. **Conecta tu repositorio:**
   - Clic en **Connect a repository**
   - Selecciona `dashboard-electoral-cordoba`

4. **Configura el servicio:**
   ```
   Name: dashboard-electoral-cordoba
   Region: Oregon (más cercano a Argentina: Frankfurt si está disponible)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app_improved:server
   Instance Type: Free
   ```

5. **Clic en "Create Web Service"**

6. **Espera a que termine el deploy** (5-10 minutos)

7. **Tu app estará disponible en:** `https://dashboard-electoral-cordoba.onrender.com`

---

## ⚠️ IMPORTANTE: LIMITACIONES DEL PLAN GRATUITO

### Render Free Tier:
- ✅ **Gratis para siempre**
- ⚠️ **La app se "duerme" después de 15 minutos de inactividad**
  - Primera carga después de "despertar" tarda ~30-60 segundos
  - Usuarios subsiguientes cargan normal
- ⚠️ **750 horas de runtime al mes** (suficiente para uso moderado)
- ⚠️ **Se reinicia automáticamente cada 24 horas**

### Alternativas Gratuitas:
- **Railway** - 500 horas gratis/mes, mismo proceso
- **Fly.io** - 3 apps gratis, más rápido
- **PythonAnywhere** - Siempre activo pero más lento

---

## 🔧 PASO 4: VERIFICAR DEPLOYMENT

1. **Abre la URL de Render:** `https://tu-app.onrender.com`

2. **Primera carga tomará ~30-60 segundos** (plan gratuito)

3. **Verifica que funcione:**
   - ✅ Mapa se carga correctamente
   - ✅ Slider de año funciona
   - ✅ Dropdown de seccional filtra
   - ✅ KPIs se actualizan
   - ✅ Tabla colapsable funciona

4. **Revisa logs en Render Dashboard:**
   - Ve a tu servicio
   - Clic en **Logs**
   - Verifica que no haya errores

---

## 🔄 PASO 5: ACTUALIZAR EL DASHBOARD (EN EL FUTURO)

Cuando hagas cambios al código:

```bash
# 1. Guarda tus cambios
git add .

# 2. Crea un commit descriptivo
git commit -m "Descripción de los cambios"

# 3. Sube a GitHub
git push origin main

# 4. Render detectará el cambio y re-desplegará automáticamente
# (toma 5-10 minutos)
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Application failed to start"

**Causa:** Falta `gunicorn` o error en `Procfile`

**Solución:**
1. Verifica que `requirements.txt` incluya `gunicorn>=21.2.0`
2. Verifica que `Procfile` contenga: `web: gunicorn app_improved:server`
3. Re-deploya manualmente desde Render Dashboard

### Error: "Module not found"

**Causa:** Falta una dependencia en `requirements.txt`

**Solución:**
1. Agrega la dependencia faltante a `requirements.txt`
2. Commit y push:
   ```bash
   git add requirements.txt
   git commit -m "Add missing dependency"
   git push origin main
   ```

### Error: "Cannot find data files"

**Causa:** Los archivos de datos están en `.gitignore`

**Solución:**
1. Si necesitas los archivos procesados en producción, edita `.gitignore`:
   ```
   # Comenta estas líneas:
   # data/processed/*.csv
   # data/processed/*.db
   # data/processed/*.geojson
   ```
2. Commit y push:
   ```bash
   git add .gitignore data/processed/
   git commit -m "Include processed data files"
   git push origin main
   ```

### La app carga muy lento

**Causa:** Plan gratuito de Render "duerme" la app después de inactividad

**Soluciones:**
- **Opción 1:** Usa [UptimeRobot](https://uptimerobot.com/) para hacer ping cada 5 minutos (gratis)
- **Opción 2:** Upgrade a plan pagado de Render ($7/mes para app siempre activa)
- **Opción 3:** Acepta los 30-60 segundos de carga inicial

---

## 🎨 PERSONALIZAR LA URL

### En Render:
La URL gratuita es: `https://dashboard-electoral-cordoba.onrender.com`

Si quieres un dominio personalizado (ej: `www.tudominio.com`):
1. Compra un dominio en Namecheap, GoDaddy, etc. ($10-15/año)
2. En Render Dashboard → Settings → Custom Domain
3. Agrega tu dominio y configura DNS según instrucciones

---

## 📊 MONITOREO

### Ver estadísticas en Render:
1. Ve a tu servicio en Render Dashboard
2. Pestaña **Metrics:**
   - CPU usage
   - Memory usage
   - Request count

### Ver logs en tiempo real:
1. Pestaña **Logs**
2. Filtra por errores: `level:error`

---

## ✅ CHECKLIST FINAL

Antes de compartir tu dashboard:

- [ ] Dashboard funciona localmente: `python app_improved.py`
- [ ] Código subido a GitHub exitosamente
- [ ] Deployment en Render completado sin errores
- [ ] URL pública funciona correctamente
- [ ] Todos los años (2021, 2023, 2025) muestran datos
- [ ] Mapa se visualiza correctamente
- [ ] Dropdown filtra correctamente
- [ ] Tabla colapsable funciona
- [ ] Responsive (probado en móvil)

---

## 🔗 RECURSOS ÚTILES

- **Documentación de Render:** https://render.com/docs
- **Dash Deployment:** https://dash.plotly.com/deployment
- **GitHub Guides:** https://guides.github.com/

---

## 🎉 ¡LISTO!

Tu dashboard electoral ahora está:
- ✅ Versionado en GitHub
- ✅ Desplegado en la nube
- ✅ Accesible desde cualquier dispositivo
- ✅ Actualizable con un simple `git push`

**URL de tu dashboard:** `https://dashboard-electoral-cordoba.onrender.com`

---

**Versión:** 1.0
**Fecha:** 2025-12-26
**Autor:** Dashboard Electoral Córdoba Capital
