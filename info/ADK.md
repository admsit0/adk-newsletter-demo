# 📘 ADK Standards & Deployment Engineering

Este documento detalla la especificación estricta requerida para desplegar agentes de Google ADK en producción (Cloud Run), basada en la arquitectura "Workspace".

---

## 1. 🏗️ Estructura de Directorios (The "Workspace" Standard)

ADK no está diseñado para correr scripts sueltos en producción. Funciona escaneando **paquetes Python**. Para que tu agente aparezca en el menú y se ejecute correctamente, debes seguir esta jerarquía:

### ❌ Estructura Incorrecta (Script suelto)

_Esto provoca que ADK no detecte el agente o falle al intentar escanear `.`_

```text
/ (root)
├── main.py   <-- MAL: ADK espera un paquete, no un archivo en root.
├── Dockerfile
```

### ✅ Estructura Correcta (Paquete Agente)

_Esto habilita el modo "Workspace" y el menú de selección._

```text
/ (root)
├── Dockerfile
├── requirements.txt
└── gdg_agent/          <-- 1. CARPETA DEL PAQUETE (Nombre de tu agente)
    ├── __init__.py     <-- 2. ARCHIVO VACÍO (Obligatorio para ser paquete)
    └── agent.py        <-- 3. ENTRY POINT (Debe llamarse 'agent.py')
```

---

## 2. 🐍 Código: Convenciones de Nombrado

Dentro de `gdg_agent/agent.py`, ADK busca "ganchos" específicos. Si no los encuentra, lanzará errores como `No root_agent found`.

### Regla 1: El nombre del archivo

Debe ser **`agent.py`**. No `main.py`, ni `bot.py`. ADK busca explícitamente este nombre dentro de los paquetes.

### Regla 2: La variable expuesta

Debes asignar tu agente principal a una variable llamada **`root_agent`** al final del archivo.

```python
# gdg_agent/agent.py

# ... tu código ...
editor_boss = LlmAgent(...)

# --- ADK ENTRY POINT ---
root_agent = editor_boss  # <--- OBLIGATORIO
```

### Regla 3: Agentes como Herramientas (El error "Callable")

ADK exige que las `tools` sean funciones (`callable`), no objetos. No puedes meter un agente dentro de otro directamente.

**Patrón Wrapper:**

```python
# MAL ❌
tools = [research_agent]

# BIEN ✅
def ask_researcher(query: str):
    return research_agent.route(query)

tools = [ask_researcher]
```

---

## 3. 🐳 Dockerfile: Ingeniería de Despliegue

El contenedor de ADK es delicado con los permisos y la red. Copia este Dockerfile estándar para evitar problemas.

### Puntos Críticos

1. **Permisos de Escritura (`chown`):** ADK necesita escribir archivos temporales (`.adk/`, logs) en tiempo de ejecución. Si copias los archivos como `root` y ejecutas como `appuser`, la aplicación crasheará al arrancar (`Container failed to start`).
2. **Binding de Red (`0.0.0.0`):** Cloud Run requiere que escuches en todas las interfaces. ADK por defecto escucha en `localhost`.
3. **Comando de Arranque (`adk web .`):** Debes usar el punto (`.`) para indicarle que escanee el directorio actual buscando los paquetes (estructura del punto 1).

### Dockerfile "Golden Master"

```dockerfile
FROM python:3.11-slim

# Optimización Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema y Python
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# --- SEGURIDAD Y PERMISOS (CRÍTICO) ---
# 1. Crear usuario no-root
RUN adduser --disabled-password --gecos '' appuser
# 2. Darle propiedad de la carpeta /app (Soluciona el crash de arranque)
RUN chown -R appuser:appuser /app

# Cambiar al usuario
USER appuser

# --- CONFIGURACIÓN DE EJECUCIÓN ---
ENV PORT=8080
# Forzar host 0.0.0.0 para que Cloud Run vea el servicio
ENV HOST=0.0.0.0

# --- COMANDO DE ARRANQUE ---
# "adk web ." -> Escanea la carpeta buscando paquetes (gdg_agent/agent.py)
# "sh -c" -> Asegura la expansión correcta de variables
CMD ["sh", "-c", "adk web . --host 0.0.0.0 --port ${PORT}"]
```

---

## 4. 🌍 Configuración de Entorno (Cloud Run)

Incluso con el código perfecto, el despliegue fallará si el entorno no es correcto.

### Variables de Entorno Obligatorias

- `GOOGLE_GENAI_USE_VERTEXAI=true`: Activa el backend de Google Cloud.
- `GOOGLE_CLOUD_PROJECT=tu-id`: Identifica quién paga.
- `GOOGLE_CLOUD_LOCATION=us-central1`: **VITAL.** Si tu Cloud Run está en Europa pero el modelo (ej. Gemini 2.0) solo está en EE.UU., necesitas esto para redirigir las peticiones de inferencia.

### Permisos IAM (Identity Access Management)

La cuenta de servicio del contenedor necesita:

1. **Vertex AI User:** Para invocar modelos.
2. **Storage Object Admin:** Para operaciones de build y logs.

---

## 5. 🚦 Resumen de Errores Típicos (ADK)

| Error en Logs                           | Significado "Real"                            | Solución                                        |
| --------------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| `Container failed to start`             | Crash por permisos o `main.py` no encontrado. | Usar `chown` en Dockerfile y `adk web .`.       |
| `Directory 'main:agent' does not exist` | Sintaxis antigua en estructura nueva.         | Cambiar CMD a `adk web .`.                      |
| `No root_agent found`                   | Falta la variable mágica.                     | Añadir `root_agent = mi_agente` en `agent.py`.  |
| `Input should be callable`              | Pasaste un `LlmAgent` a `tools`.              | Envuélvelo en una función `def`.                |
| `404 Model not found`                   | El modelo no está en tu región de Cloud Run.  | Añadir ENV `GOOGLE_CLOUD_LOCATION=us-central1`. |

```

```
