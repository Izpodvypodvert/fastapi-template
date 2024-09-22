# FastAPI Template with PostgreSQL, Docker, Alembic, and FastAPI Users

This project provides a template for building a FastAPI application with PostgreSQL, Docker, Alembic migrations, and user authentication using FastAPI Users.

## Features

This template comes with the following features:

-   [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python
-   [Docker](https://docs.docker.com/): Dockerized environment for easy setup and deployment.
-   [PostgreSQL](https://www.postgresql.org/): A powerful, open-source object-relational database.
-   [SQLAlchemy](https://docs.sqlalchemy.org/en/20/): Core database toolkit and ORM for Python, used in conjunction with PostgreSQL.
-   [Alembic](https://alembic.sqlalchemy.org/en/latest/): Database migrations for SQLAlchemy models.
-   [FastAPI Users](https://fastapi-users.github.io/fastapi-users/latest/): Ready-to-use and customizable user management, authentication, and registration with support for OAuth2, JWT, and more.
-   [loguru](https://github.com/Delgan/loguru): A simple and powerful logging library.

## Setup

## Requirements

-   Docker installed on your system.
-   Docker Compose to manage multi-container Docker applications.

## Environment Variables

Make sure to set up a .env file with the required environment variables for PostgreSQL and JWT. You can use .env.example as a reference.
Example:

```bash
# PostgreSQL configuration
POSTGRES_USER=myuser              # Имя пользователя базы данных
POSTGRES_PASSWORD=mypassword      # Пароль для пользователя
POSTGRES_DB=mydatabase            # Название базы данных
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost/mydatabase  # URL для подключения к базе данных

# JWT Secret key for authentication
SECRET_KEY=your_jwt_secret_key    # Секретный ключ для подписи JWT токенов
```

## Build and Run

-   `docker compose up --build -d` – Build and start the containers.

## API Documentation

-   [Swagger UI](http://127.0.0.1:8000/docs)
-   [Redoc](http://127.0.0.1:8000/redoc)
