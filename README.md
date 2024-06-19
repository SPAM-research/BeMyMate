# ChatAgents

LLM agents for collaborative tutorchat sessions.

## Installation

```
git clone https://gitlab.com/h2282/chatagents
cd chatagents
chmod u+x install.sh
./install.sh
```

## Usage

- Run the ollama server
- Get a model from the [library](https://ollama.ai/library): `ollama pull llama3:latest`
- Run the app: `python3 main.py` and enjoy the agents.

## Style Guide

The Style Guide is based on the opinionated FastAPI Best Practices repository:
[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#project-structure)

### Project Structure

Organize the project in a way that is consistent, straightforward, and free of surprises.

#### Example Structure

```
chatagents/
├── alembic/
├── src/
│   ├── auth/
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── aws/
│   │   ├── client.py
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   └── posts/
│       ├── router.py
│       ├── schemas.py
│       ├── models.py
│       ├── dependencies.py
│       ├── constants.py
│       ├── exceptions.py
│       ├── service.py
│       └── utils.py
│   ├── config.py
│   ├── models.py
│   ├── exceptions.py
│   ├── pagination.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── auth/
│   ├── aws/
│   └── posts/
├── templates/
│   └── index.html
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── .gitignore
├── logging.ini
└── alembic.ini
```

### Code Practices

#### Async Routes

FastAPI supports both async and sync routes. Prefer async routes for I/O intensive tasks.

#### CPU Intensive Tasks

For CPU-intensive tasks, use background workers or separate processes to avoid blocking the main event loop.

#### Pydantic Models

Use Pydantic models for data validation and serialization. Customize models using a global base model for consistency.

#### Dependencies

Use FastAPI's dependency injection system to validate and manage dependencies. Chain dependencies to reduce code duplication and improve reusability.

#### Response Serialization

Always use `response_model` to validate and serialize responses. Avoid returning raw Pydantic models directly.

### Documentation

#### Hiding Docs in Production

Hide API documentation by default in production environments. Show it only in selected environments like local and staging.

#### Detailed Route Documentation

Provide detailed documentation for each route, including `response_model`, `status_code`, `description`, and `tags`.

#### Database Naming Conventions

Use consistent naming conventions for database entities:

- Lowercase snake_case for table names.
- Singular form (e.g., `user`, `post`).
- Prefix related tables (e.g., `payment_account`, `payment_bill`).
- Use `_id` suffix for foreign keys and `_at` suffix for timestamps.

### Testing

#### Async Test Client

Use an async test client from the start to avoid issues with event loops during integration tests.

#### Linters

Use `ruff` for linting and formatting to maintain code quality and consistency.

### Bonus Section

Read and share best practices and experiences in the project's issues section. Contributions are welcome.

## About

FastAPI Best Practices and Conventions used in startups.

For more details and best practices, refer to the issues section of the project.

---

This style guide aims to maintain consistency, improve code quality, and ensure a smooth development experience. Follow these guidelines to contribute effectively to the ChatAgents project.
