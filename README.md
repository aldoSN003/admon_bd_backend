
# 🚀 FastAPI Project Setup

Este es el repositorio base para nuestra REST API modular construida con **FastAPI** y **Python**. Sigue los pasos a continuación para configurar tu entorno de desarrollo.

-----

## 📋 Requisitos Previos

Asegúrate de tener instalado lo siguiente:

  * **Python 3.9+**
  * **Git**

-----

## 💻 1. Clonar el Repositorio

Abre tu terminal y ejecuta el siguiente comando para descargar el código fuente.

```bash
git clone https://github.com/aldoSN003/admon_bd_backend.git

```

-----

## 🛠️ 2. Configuración del Entorno Virtual

Es fundamental trabajar dentro de un **entorno virtual** (`venv`) para aislar las dependencias del proyecto de tu instalación global de Python.

### A. Crear y Activar el Entorno

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno (Linux/macOS)
source venv/bin/activate

# Activar el entorno (Windows - PowerShell)
# .\venv\Scripts\Activate.ps1
```

### B. Instalar Dependencias

Una vez activado el entorno, utiliza el archivo `requirements.txt` para instalar todas las librerías necesarias (FastAPI, Uvicorn, etc.).

```bash
pip install -r requirements.txt
```

-----

## ▶️ 3. Ejecutar la Aplicación

Una vez que todas las dependencias estén instaladas, puedes iniciar el servidor de desarrollo de FastAPI con **Uvicorn**.

```bash
uvicorn app.main:app --reload
```

  * El servidor estará disponible en: **`http://127.0.0.1:8000`**
  * La documentación interactiva de la API (Swagger UI) estará en: **`http://127.0.0.1:8000/docs`**

-----

## 🛑 4. Detener el Entorno

Cuando termines de trabajar, puedes desactivar el entorno virtual para volver a tu entorno de sistema normal.

```bash
deactivate
```
