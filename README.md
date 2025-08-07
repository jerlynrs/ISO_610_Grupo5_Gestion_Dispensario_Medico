# 💊 ISO 610 - Proyecto Final  
## 🩺 Gestión del Dispensario Médico - Grupo 5

Este es un sistema web desarrollado en Python (Flask) para la gestión de un dispensario médico universitario. Incluye módulos como: tipos de fármacos, marcas, ubicaciones, pacientes, médicos, medicamentos, visitas y reportes.

---

## ✅ Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes programas en tu computadora:

1. **[Python 3.x](https://www.python.org/downloads/)**  
2. **[PostgreSQL 17.5](https://www.postgresql.org/download/windows/)**  
   - Durante la instalación, **mantén todo por defecto**  
   - Asigna la contraseña: `123456`  
   - Anota el puerto por defecto (`5432`)

3. **Git** (opcional para clonar el repositorio):  
   [Descargar Git](https://git-scm.com/download/win)

---

## 🛠️ Configurar la Base de Datos

Debes crear una base de datos en PostgreSQL llamada:

```sql
DispensarioMedicoApec
```
Puedes hacerlo desde PgAdmin o con el siguiente comando en la terminal de PostgreSQL:

##  📥 Clonar y Ejecutar el Proyecto (Windows)
1. Abre la terminal
2. Clona el repositorio:

```
git clone https://github.com/tu-usuario/ISO_610_Grupo5_Gestion_Dispensario_Medico.git
cd ISO_610_Grupo5_Gestion_Dispensario_Medico 
```

<p>   Una vez clonado ve a la ruta del repositorio  (archivo clonado) y correr: <p> 

```python -m venv venv```

```venv\Scripts\activate```

```pip freeze > requirements.txt```

```pip install -r requirements.txt```

```pip install flask flask_sqlalchemy psycopg2-binary```

```python app.py```

## 6. Abre tu navegador y accede a:
http://127.0.0.1:5000



## 🔐 Acceso al sistema
Puedes crear un usuario administrador accediendo a la siguiente URL:

arduino
Copiar
Editar
http://127.0.0.1:5000/crear_admin
Credenciales por defecto:

Usuario: admin

Contraseña: 123456

