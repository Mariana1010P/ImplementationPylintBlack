# ImplementationPylintBlack

## Project Description

This project implements an API for managing articles and authors, using Docker for database configuration, Adminer for visual management, and a backend with complete CRUD functionality. PEP8 conventions are followed using Pylint and Black to maintain code quality and style. Additionally, the APIs are protected with an ApiKey for added security.

## Cloning the Repository

```bash
git clone https://github.com/Mariana1010P/ImplementationPylintBlack.git
cd ImplementationPylintBlack
```

## Installation and Configuration

### 1. Environment Variables

The project includes a `.env_example` file containing the necessary environment variables for system configuration. You should create a `.env` file in the root directory of the project and configure your own variables based on the example:

```bash
cp .env.example .env
```

Edit the `.env` file with the correct values for your environment:

```bash
# Example variables
API_KEY=your_api_key
MYSQL_ROOT_PASSWORD=example
MYSQL_DATABASE=db_example
MYSQL_HOST=example
MYSQL_PORT=3306
MYSQL_USER=example
MYSQL_PASSWORD=example
```

### 2. Building and Running FastAPI with Docker

This project includes a `Makefile` to facilitate the configuration and execution of services. Just run the following command to start the containers for the database, Adminer, and the backend:

```bash
make deploy
```

**Note**: The `make deploy` command only works on Linux or Mac. On Windows, you need to use these commands:

```bash
docker compose build
docker compose up -d
```

This command uses Docker and the `docker-compose.yml` file which has the following configuration:

- **MySQL Database**: `database` container with MySQL and persistent volumes.
- **Adminer**: Available at `http://localhost:8080` for visual database management.
- **FastAPI Backend**: The backend of the application is configured and can be accessed at `http://localhost:8000`.

### 3. Accessing Adminer

Access Adminer from your browser at `http://localhost:8080` to visually manage the database. The details for connecting to the MySQL database are defined in the `docker-compose.yml` file:

- **Server**: `db`
- **User**: `root`
- **Password**: `root`
- **Database**: The one you defined in your environment variables.

### 4. Building and Running FastAPI with Docker

You do not need to manually install Python dependencies, as this is done automatically when the FastAPI container is built. The `Dockerfile` takes care of:

- Copying the application files.
- Installing the Python dependencies listed in `requirements.txt`.
- Running the application using `uvicorn`.

To start the containers for the database, Adminer, and FastAPI, simply run:

```bash
make deploy
```

### 5. Configuring Pylint

Pylint is configured to analyze code quality. Run the following command to ensure the score is above 7:

```bash
pylint name_of_package.py
```

You can customize Pylint rules in the `.pylintrc` file.

### 6. Formatting Code with Black

To format the code following PEP8 conventions, use Black:

```bash
black name_of_package.py
black . # Formats the entire project
```

### 7. CRUD Management for Articles and Authors

The system allows managing `Article` and `Author` entities through CRUD operations (Create, Read, Update, Delete).

#### Entities:

- **Article**:
  - `article_id`: Unique identifier.
  - `title`: Title of the article.
  - `content`: Content of the article.
  - `published_date`: Date the article was published.
  - `author`: Foreign key referencing an Author.

- **Author**:
  - `author_id`: Unique identifier.
  - `name`: Author's name.
  - `affiliation`: Author's affiliation.

The API routes are protected with an ApiKey.

### 8. Protecting Swagger with ApiKey

Access to the interactive Swagger documentation and the API routes is protected with an ApiKey. The key is defined in the `.env` file as `API_KEY`. 

To test the routes in Swagger, include the ApiKey in the headers of your requests:

```bash
API_KEY=your_api_key
```

### 9. Dockerfile for FastAPI

The FastAPI backend is configured in Docker using the following `Dockerfile`:

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

This Dockerfile:

- Copies the FastAPI application from the `app` directory.
- Installs the dependencies listed in `requirements.txt`.
- Configures `uvicorn` as the ASGI server to serve the FastAPI backend on port 80.

### 10. Dockerfile for MySQL

The project includes a specific `Dockerfile` for MySQL with the following configuration:

```dockerfile
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=example
ENV MYSQL_DATABASE=db_example
ENV MYSQL_USER=example
ENV MYSQL_PASSWORD=example

EXPOSE 3306
```

**Important**: The environment variables configured in the `.env` file must match those used in the MySQL `Dockerfile` to ensure consistency in database connection. Ensure that variables like `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_ROOT_PASSWORD` have the same values in both files.

---

## Project Structure

The project structure is as follows:

```
ImplementationPylintBlack/
├── FastAPI/
│   ├── app/
│   │   ├── config/                # Database configuration and environment variables
│   │   │   └── database.py
│   │   ├── routes/                # API route definitions
│   │   │   ├── article_route.py    # Routes for managing articles
│   │   │   └── author_route.py     # Routes for managing authors
│   │   ├── schemas/               # Data schemas for the API
│   │   │   ├── article.py          # Schema for the article
│   │   │   └── author.py           # Schema for the author
│   │   ├── services/              # Business logic and API services
│   │   │   ├── article_service.py   # Services related to articles
│   │   │   └── author_service.py    # Services related to authors
│   │   └── main.py                # Entry point for the FastAPI application
├── Dockerfile                      # Dockerfile for the FastAPI backend
├── requirements.txt                # Python dependencies
├── MySQL/                          # MySQL configuration and volumes
│   └── Dockerfile                  # Dockerfile for the MySQL database
├── docker-compose.yml              # Docker Compose configuration
├── Makefile                        # Script to facilitate container execution
├── .env_example                    # Example environment variable file
└── .pylintrc                       # Pylint configuration
└── README.md                       # Project documentation
```

### Description of Folders and Files

- **app/**: Contains all the FastAPI application code.
  - **config/**: Configuration files, including database connection.
  - **routes/**: Files defining API routes.
  - **schemas/**: Definitions of data schemas used in the API.
  - **services/**: Contains business logic, services, and functions related to articles and authors.
  - **main.py**: Entry point to run the application.

- **Dockerfile**: Configuration to build the Docker image for the backend.

- **requirements.txt**: List of dependencies required for the project.

- **MySQL/**: Contains the Dockerfile for configuring the MySQL container.

- **docker-compose.yml**: Configuration file for Docker Compose, orchestrating the execution of application containers.

- **Makefile**: Provides simplified commands to handle execution and deployment of containers.

- **.env_example**: Example file for necessary environment variables for configuration.

- **.pylintrc**: Configuration file for Pylint, allowing customization of code analysis rules.

- **README.md**: This file documenting the project.

## Contact

If you have any questions, feel free to reach out to us at:
- [portela.mariana.6654@eam.edu.co](mailto:portela.mariana.6654@eam.edu.co)
- [valencia.alejandro.8426@eam.edu.co](mailto:valencia.alejandro.8426@eam.edu.co)

--- 
