# ImplementationPylintBlack

## Descripción del Proyecto

Este proyecto implementa una API para la gestión de artículos y autores, utilizando Docker para la configuración de la base de datos, Adminer para la gestión visual, y un backend con CRUD completo. Se siguen las convenciones de PEP8 mediante Pylint y Black para mantener la calidad y el estilo del código. Además, las APIs están protegidas con ApiKey para seguridad adicional.

## Clonar el Repositorio

```bash
git clone https://github.com/Mariana1010P/ImplementationPylintBlack.git
cd ImplementationPylintBlack
```

## Instalación y Configuración

### 1. Variables de Entorno

El proyecto incluye un archivo `.env_example` que contiene las variables de entorno necesarias para la configuración del sistema. Debes crear un archivo `.env` en el directorio raíz del proyecto y configurar tus propias variables basadas en el ejemplo:

```bash
cp .env.example .env
```

Edita el archivo `.env` con los valores correctos para tu entorno:

```bash
# Ejemplo de variables
API_KEY = tu_api_key
MYSQL_ROOT_PASSWORD= example
MYSQL_DATABASE = db_example
MYSQL_HOST = example
MYSQL_PORT = 3306
MYSQL_USER = example
MYSQL_PASSWORD = example
```

### 2. Levantar los Contenedores con Makefile

Este proyecto incluye un archivo `Makefile` para facilitar la configuración y ejecución de los servicios. Solo necesitas ejecutar el siguiente comando para levantar los contenedores de la base de datos, Adminer y el backend:

```bash
make deploy
```

Este comando utiliza Docker y el archivo `docker-compose.yml` que tiene la siguiente configuración:

- **Base de datos MySQL**: Contenedor `database` con MySQL y volúmenes persistentes.
- **Adminer**: Disponible en `http://localhost:8080` para gestionar la base de datos visualmente.
- **FastAPI Backend**: El backend de la aplicación está configurado y se puede acceder en `http://localhost:8000`.

### 3. Acceso a Adminer

Accede a Adminer desde tu navegador en `http://localhost:8080` para gestionar la base de datos de forma visual. Los detalles de la conexión a la base de datos MySQL están definidos en el archivo `docker-compose.yml`:

- **Servidor**: `db`
- **Usuario**: `root`
- **Contraseña**: `root`
- **Base de datos**: La que definiste en tus variables de entorno.

### 4. Construcción y Ejecución de FastAPI con Docker

No necesitas instalar manualmente las dependencias de Python, ya que esto se realiza automáticamente cuando se construye el contenedor de FastAPI. El `Dockerfile` se encarga de:

- Copiar los archivos de la aplicación.
- Instalar las dependencias de Python listadas en `requirements.txt`.
- Ejecutar la aplicación utilizando `uvicorn`.

Para levantar los contenedores de la base de datos, Adminer y FastAPI, solo necesitas ejecutar:

```bash
make deploy
```

### 5. Configuración de Pylint

Pylint está configurado para analizar la calidad del código. Ejecuta el siguiente comando para verificar que el puntaje sea mayor a 7:

```bash
pylint nombre_del_paquete.py
```

Puedes personalizar las reglas de Pylint en el archivo `.pylintrc`.

### 6. Formateo del Código con Black

Para formatear el código siguiendo las convenciones de PEP8, utiliza Black:

```bash
black nombre_del_paquete.py
black . #Da formato a todo el proyecto
```

### 7. Gestión de CRUD para Artículos y Autores

El sistema permite gestionar las entidades `Artículo` y `Autor` mediante operaciones CRUD (Crear, Leer, Actualizar, Eliminar).

#### Entidades:

- **Article**:
  - `article_id`: Identificador único.
  - `title`: Título del artículo.
  - `content`: Contenido del artículo.
  - `published_date`: Fecha de publicación del artículo.
  - `autor`: Clave foránea que referencia a un Autor.

- **Author**:
  - `author_id`: Identificador único.
  - `name`: Nombre del autor.
  - `affiliation`: Afiliación del autor.

Las rutas de la API están protegidas mediante ApiKey.

### 8. Protección de Swagger con ApiKey

El acceso a la documentación interactiva de Swagger y las rutas de la API están protegidos mediante ApiKey. La clave se define en el archivo `.env` como `API_KEY`. 

Para probar las rutas en Swagger, incluye la ApiKey en los encabezados de las solicitudes:

```bash
API_KEY=tu_api_key
```


### 9. Dockerfile para FastAPI

El backend de FastAPI está configurado en Docker usando el siguiente `Dockerfile`:

```dockerfile
FROM python:3.12

COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y mariadb-client && pip install mysqlclient

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

Este Dockerfile:

- Copia la aplicación FastAPI desde el directorio `app`.
- Instala las dependencias de la aplicación listadas en `requirements.txt`.
- Configura `uvicorn` como el servidor ASGI para servir el backend de FastAPI en el puerto 80.

### 10. Dockerfile para MySQL

El proyecto incluye un `Dockerfile` específico para MySQL con la configuración:

```dockerfile
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD example
ENV MYSQL_DATABASE db_example
ENV MYSQL_USER example
ENV MYSQL_PASSWORD example

EXPOSE 3306
```

**Importante**: Las variables de entorno configuradas en el archivo `.env` deben coincidir con las que se utilizan en el `Dockerfile` de MySQL para garantizar la consistencia en la conexión a la base de datos. Asegúrate de que las variables como `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_ROOT_PASSWORD` tengan los mismos valores en ambos archivos.

---
## Estructura del Proyecto

La estructura del proyecto es la siguiente:

```
ImplementationPylintBlack/
├── FastAPI/
│   ├── app/
│   │   ├── config/                # Configuración de la base de datos y variables de entorno
│   │   │   └── database.py
│   │   ├── routes/                # Definición de rutas de la API
│   │   │   ├── article_route.py    # Rutas para gestionar artículos
│   │   │   └── author_route.py     # Rutas para gestionar autores
│   │   ├── schemas/               # Esquemas de datos para la API
│   │   │   ├── article.py          # Esquema para el artículo
│   │   │   └── author.py           # Esquema para el autor
│   │   ├── services/              # Lógica de negocio y servicios de la API
│   │   │   ├── article_service.py   # Servicios relacionados con artículos
│   │   │   └── author_service.py    # Servicios relacionados con autores
│   │   └── main.py                # Punto de entrada de la aplicación FastAPI
├── Dockerfile                      # Dockerfile para el backend de FastAPI
├── requirements.txt                # Dependencias de Python
├── MySQL/                          # Configuración y volúmenes para MySQL
│   └── Dockerfile                  # Dockerfile para la base de datos MySQL
├── docker-compose.yml              # Configuración de Docker Compose
├── Makefile                        # Script para facilitar la ejecución de contenedores
├── .env_example                    # Ejemplo de archivo de variables de entorno
└── .pylintrc                       # Configuración de Pylint
└── README.md                       # Documentación del proyecto
```

### Descripción de las Carpetas y Archivos

- **app/**: Contiene todo el código de la aplicación FastAPI.
  - **config/**: Archivos de configuración, incluyendo la conexión a la base de datos.
  - **routes/**: Archivos que definen las rutas de la API.
  - **schemas/**: Definiciones de los esquemas de datos utilizados en la API.
  - **services/**: Contiene la lógica de negocio, servicios y funciones relacionadas con los artículos y autores.
  - **main.py**: Punto de entrada para ejecutar la aplicación.

- **Dockerfile**: Configuración para construir la imagen Docker del backend.

- **requirements.txt**: Lista de dependencias necesarias para el proyecto.

- **MySQL/**: Contiene el Dockerfile específico para configurar el contenedor de MySQL.

- **docker-compose.yml**: Archivo de configuración para Docker Compose, que orquesta la ejecución de los contenedores de la aplicación.

- **Makefile**: Proporciona comandos simplificados para manejar la ejecución y el despliegue de los contenedores.

- **.env_example**: Archivo de ejemplo para las variables de entorno necesarias para la configuración.

- **.pylintrc**: Archivo de configuración para Pylint, que permite personalizar las reglas de análisis de código.

- **README.md**: Este archivo que documenta el proyecto.


## Contacto

Si tienes alguna duda, no dudes en contactarnos en:
- [portela.mariana.6654@eam.edu.co](mailto:portela.mariana.6654@eam.edu.co)
- [valencia.alejandro.8426@eam.edu.co](mailto:valencia.alejandro.8426@eam.edu.co)
---
