# FastAPI Template with PostgreSQL, Docker, Alembic, and FastAPI Users

This project provides a template for building a FastAPI application with PostgreSQL, Docker, Alembic migrations, and user authentication using FastAPI Users. The project also includes support for OAuth authentication (e.g., Google) using the `authlib` library, allowing easy integration with external authentication providers.

## Features

This template comes with the following features:

-   [FastAPI](https://fastapi.tiangolo.com/): A modern, fast (high-performance) web framework for building APIs with Python
-   [Docker](https://docs.docker.com/): Dockerized environment for easy setup and deployment.
-   [PostgreSQL](https://www.postgresql.org/): A powerful, open-source object-relational database.
-   [SQLAlchemy](https://docs.sqlalchemy.org/en/20/): Core database toolkit and ORM for Python, used in conjunction with PostgreSQL.
-   [Alembic](https://alembic.sqlalchemy.org/en/latest/): Database migrations for SQLAlchemy models.
-   [FastAPI Users](https://fastapi-users.github.io/fastapi-users/latest/): Ready-to-use and customizable user management, authentication, and registration with support for OAuth2, JWT, and more.
-   [loguru](https://github.com/Delgan/loguru): A simple and powerful logging library.
-   [authlib](https://docs.authlib.org/en/latest/): OAuth client and server library for handling OAuth2 authentication (used for Google, Facebook, etc.).

## Setup

## Requirements

-   Docker installed on your system.
-   Docker Compose to manage multi-container Docker applications.

## Environment Variables

Make sure to set up a .env file with the required environment variables for PostgreSQL and JWT. You can use .env.example as a reference.
Example:

```bash
# PostgreSQL configuration
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@localhost/mydatabase

# JWT Secret key for authentication
SECRET=your_jwt_secret_key
CLIENT_ID=Client ID from provider
CLIENT_SECRET=Client Secret from provider
```

## **Register your OAuth provider**:

    - Go to the Google API Console (or another provider's console).
    - Create a new project and configure OAuth credentials.
    - Set up your **Redirect URI** to point to your FastAPI callback endpoint, e.g., `http://localhost:8000/auth/google/callback`.
    - Copy your **Client ID** and **Client Secret**.

## Build and Run

-   `docker compose up --build -d` – Build and start the containers.

## API Documentation

-   [Swagger UI](http://127.0.0.1:8000/docs)
-   [Redoc](http://127.0.0.1:8000/redoc)
