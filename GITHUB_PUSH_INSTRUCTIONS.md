# 🔐 INSTRUCCIONES PARA SUBIR A GITHUB

## ⚠️ Problema de Autenticación Detectado

Git está intentando usar las credenciales de **juliotarcaya** en lugar de **juliomapas**.

---

## ✅ SOLUCIÓN: Autenticarse con GitHub

Tienes **3 opciones** para autenticarte y subir el código:

---

### **OPCIÓN 1: GitHub CLI (Recomendado - Más Fácil)**

1. **Instalar GitHub CLI:**
   - Descarga desde: https://cli.github.com/
   - O con Winget: `winget install GitHub.cli`

2. **Autenticarse:**
   ```bash
   gh auth login
   ```
   - Selecciona: **GitHub.com**
   - Selecciona: **HTTPS**
   - Selecciona: **Login with a web browser**
   - Copia el código que aparece
   - Presiona Enter
   - Pega el código en el navegador
   - Autoriza GitHub CLI

3. **Subir el código:**
   ```bash
   git push -u origin main
   ```

---

### **OPCIÓN 2: Personal Access Token (PAT)**

1. **Crear un Token en GitHub:**
   - Ve a: https://github.com/settings/tokens
   - Clic en **Generate new token** → **Generate new token (classic)**
   - Dale un nombre: `mapacordoba-deploy`
   - Marca el checkbox: **repo** (acceso completo)
   - Clic en **Generate token**
   - **COPIA EL TOKEN** (solo se muestra una vez)

2. **Usar el token para hacer push:**
   ```bash
   git remote set-url origin https://TU_TOKEN@github.com/juliomapas/mapacordoba.git
   git push -u origin main
   ```

   Reemplaza `TU_TOKEN` con el token que copiaste.

---

### **OPCIÓN 3: GitHub Desktop (Más Visual)**

1. **Descargar GitHub Desktop:**
   - https://desktop.github.com/

2. **Abrir la aplicación:**
   - Inicia sesión con tu cuenta **juliomapas**

3. **Agregar repositorio local:**
   - **File** → **Add Local Repository**
   - Selecciona: `D:\pj\2026\resultado\proyecto\pyoclaude`

4. **Publicar:**
   - Clic en **Publish repository**
   - Repositorio ya existe en GitHub, así que:
     - Clic en **Push origin**

---

## 🚀 DESPUÉS DE SUBIR A GITHUB

Una vez que hagas `git push` exitosamente:

### **Paso 1: Verifica en GitHub**
Ve a: https://github.com/juliomapas/mapacordoba

Deberías ver todos tus archivos, incluyendo:
- ✅ `app_improved.py`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `render.yaml`
- ✅ `requirements.txt`
- ✅ `README_DEPLOYMENT.md`

---

### **Paso 2: Desplegar en Render**

#### **Opción A: Automático con render.yaml**

1. Ve a: https://dashboard.render.com/
2. Clic en **New +** → **Blueprint**
3. Conecta tu repositorio: `juliomapas/mapacordoba`
4. Render detectará `render.yaml` automáticamente
5. Clic en **Apply**
6. Espera 5-10 minutos
7. Tu app estará en: `https://dashboard-electoral-cordoba.onrender.com`

#### **Opción B: Manual**

1. Ve a: https://dashboard.render.com/
2. Clic en **New +** → **Web Service**
3. Conecta repositorio: `juliomapas/mapacordoba`
4. Configuración:
   ```
   Name: dashboard-electoral-cordoba
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app_improved:server
   Instance Type: Free
   ```
5. Clic en **Create Web Service**
6. Espera 5-10 minutos
7. Tu app estará disponible

---

## 🔧 VERIFICAR DEPLOYMENT

Abre la URL de Render y verifica:

- ✅ Mapa se carga
- ✅ Slider de año funciona
- ✅ Dropdown filtra correctamente
- ✅ KPIs se actualizan
- ✅ Gráficos funcionan
- ✅ Tabla se colapsa/expande

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Application failed to respond"

1. Ve a Render Dashboard → tu servicio → **Logs**
2. Busca errores
3. Verifica que el comando sea: `gunicorn app_improved:server`

### Error: "Failed to build"

1. Verifica que `requirements.txt` incluya `gunicorn>=21.2.0`
2. Re-deploya manualmente desde Render Dashboard

### La app está muy lenta

- Normal en plan gratuito
- Primera carga: 30-60 segundos
- Cargas subsiguientes: rápidas

---

## 📝 COMANDOS RÁPIDOS DE REFERENCIA

```bash
# Ver estado de Git
git status

# Ver remotes configurados
git remote -v

# Ver configuración de usuario
git config user.name
git config user.email

# Forzar push (solo si es necesario)
git push -u origin main --force

# Ver logs de commits
git log --oneline
```

---

## ✅ CHECKLIST FINAL

- [ ] Autenticado con GitHub (opción 1, 2 o 3)
- [ ] Push a GitHub exitoso
- [ ] Código visible en https://github.com/juliomapas/mapacordoba
- [ ] Cuenta creada en Render.com
- [ ] Repositorio conectado en Render
- [ ] Deployment completado sin errores
- [ ] URL pública funciona
- [ ] Dashboard carga correctamente

---

**¿Necesitas ayuda?**
- GitHub Docs: https://docs.github.com/
- Render Docs: https://render.com/docs

**Tu URL final será:**
`https://dashboard-electoral-cordoba.onrender.com`
(o el nombre que elijas en Render)

---

**Estado Actual:**
- ✅ Repositorio Git inicializado
- ✅ Commit creado: "Initial commit - Dashboard Electoral Cordoba Capital"
- ✅ Remote agregado: https://github.com/juliomapas/mapacordoba.git
- ⏳ Pendiente: Autenticación y push

**Próximo comando a ejecutar (después de autenticarte):**
```bash
git push -u origin main
```
