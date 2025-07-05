# 🌐 Backend E-Commerce API

Bienvenido a la API RESTful para la gestión de un e-commerce, desarrollada con **FastAPI** y **Python 3.13+**. Este backend está diseñado para ser simple, rápido y escalable. Utiliza **SQLite** como base de datos por defecto para facilitar el despliegue local.

---

## 🚀 Requisitos

- **Python 3.13** o superior (funciona también desde la versión 3.11)
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

---

## 🔧 Instalación paso a paso

### 1. 📂 Clona el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ecommerce-backend
```

### 2. 🌐 Crea un entorno virtual

```bash
python -m venv venv
```

### 3. 🔌 Activa el entorno virtual

- **Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **Linux/MacOS:**

  ```bash
  source venv/bin/activate
  ```

### 4. 📦 Instala las dependencias necesarias

```bash
pip install -r requirements.txt
```

---

## 🔣 Configuración del entorno

### 1. 🔹 Configura la base de datos

Copia el archivo de entorno de ejemplo:

```bash
cp .env.example .env.prod
```

Edita el archivo `.env.prod` para definir la URL de la base de datos (por defecto, SQLite):

```env
DATABASE_URL="sqlite:///nombre_de_tu_db.db"
```

Puedes cambiar `nombre_de_tu_db` por el nombre que prefieras.

---

## 🧪 Ejecución de pruebas

Para ejecutar los tests automáticos con **pytest**:

```bash
pytest
```

---

## 🛠️ Levantar el servidor de desarrollo

Inicia la aplicación con **Uvicorn**:

```bash
uvicorn main:app --reload
```

Servidor disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📄 Documentación de la API

- **Swagger UI (interactiva):**
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- **ReDoc (estática):**
  [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## ⚠️ Notas importantes

- La base de datos SQLite se genera automáticamente si no existe.
- Puedes modificar la configuración en el archivo `.env.prod`.
- Ideal para entornos de desarrollo o pruebas. Para producción, se recomienda PostgreSQL u otro motor más robusto.

---

> ✨ Este proyecto es una excelente base para comenzar a construir tu propia tienda en línea, API para móviles, o integraciones con frontend modernos como React o Angular.

---

🚀 **Desarrollado con amor y Python por <jpas.juan01@gmail.com> ♥**
