# Payzee: Pay Easy, Payzee!

**Payzee** is a modern payment processor powered by **Central Bank Digital Currency (CBDC)** — also known as the **Digital Rupee** or **e-rupee (e₹)**.

## 📁 Project Structure

```
├── app.py             # Main FastAPI application entry point  
├── db/                # Redis database configuration and operations  
├── models/            # Data models for transactions, users, and payment entities  
├── routes/            # API endpoints for payments and authentication  
├── middleware/        # Request/response middleware components  
├── utils/             # Helper utilities and common functions  
├── tests/             # Unit and integration tests  
└── scripts/           # Development and setup scripts  
```

## 🚀 Setup for Development

### Prerequisites

* Python 3.11+
* Redis server
* [Poetry](https://python-poetry.org/) for dependency management

### ⚡ Quick Start

Run the setup script to prepare your development environment:

```bash
./scripts/run.sh
```

This script will:

* Install Poetry (if not already installed)
* Set up necessary `PATH` variables
* Install project dependencies
* Start the development server with hot-reload

## 🐳 Docker Setup (Recommended)

### 1. Start the full stack

Using Docker Compose:

```bash
docker-compose up -d
```

Or with Make:

```bash
make up
```

### 2. Run the app manually with Docker

```bash
# Build the API container
docker build -t payzee-api -f docker/prod.Dockerfile .

# Run the API container
docker run -p 8000:8000 --env-file .env payzee-api
```

## 🧰 Manual Setup

### 1. Install Poetry

* **Windows**:

  ```bash
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
  ```

* **Linux/macOS**:

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

### 2. Start Redis using Docker

```bash
docker run --name payzee-redis -p 6379:6379 -d redis:latest
```

### 3. Install project dependencies

```bash
poetry install
```

### 4. Start the development server

```bash
poetry run uvicorn app:app --reload
```

## 🧪 Development Tools

### ✅ Testing

Run tests with `pytest`:

```bash
# Using poetry
poetry run pytest

# Or with Make
make test
```

### 🧼 Pre-commit Hooks

We use **pre-commit** hooks with **Ruff** for linting and formatting.

Hooks handle:

* Removing trailing whitespace
* Ensuring files end with a newline
* Checking JSON/YAML syntax
* Python linting & formatting with Ruff

Pre-commit is installed with project dependencies.

To run all hooks manually:

```bash
poetry run pre-commit run --all-files
```

Or use Make:

```bash
make lint     # Run Ruff linting
make format   # Format code using Ruff
```

## 🧠 Redis Management

RedisInsight is available via Docker at:
👉 [http://localhost:5540](http://localhost:5540)

To connect:

1. Click **Add Redis database**
2. Use one of the following connection strings:

   * `redis://redis:6379`
   * `redis://host.docker.internal:6379`

This allows inspection of Redis data and keyspaces.

## 📘 API Documentation

Once the app is running, open Swagger UI at:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)
