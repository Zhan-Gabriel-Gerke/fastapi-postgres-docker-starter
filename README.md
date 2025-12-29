# FastAPI Todo API with PostgreSQL & Docker

A robust, production-ready REST API for managing Todos, built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. The project supports containerization via **Docker** and includes a comprehensive test suite using **Pytest**.

## 🚀 Features

- **Authentication & Authorization**:
  - JWT (JSON Web Token) based authentication.
  - Password hashing with Bcrypt.
  - Role-based access control (Admin vs. User).
- **Todo Management**:
  - CRUD operations (Create, Read, Update, Delete).
  - Filtering and validation.
- **User Management**:
  - Profile updates (Password, Phone number).
- **Admin Dashboard**:
  - View all todos across users.
  - Administrative deletion capabilities.
- **Infrastructure**:
  - Docker & Docker Compose support.
  - PostgreSQL database integration.
  - Pydantic for data validation and settings management.
- **Testing**:
  - Integration tests with Pytest.
  - Isolated test database environment.

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Containerization**: Docker, Docker Compose
- **Testing**: Pytest, TestClient
- **Security**: OAuth2, Passlib (Bcrypt), Python-Jose

## ⚙️ Configuration

Create a `.env` file in the root directory. You can use the example below:

```ini
# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=postgres

# Security
SECRET_KEY=your_super_secret_key_change_this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Note**: If running locally (without Docker), change `DB_HOST` to `localhost`.

For testing, create a `.env.test` file:

```ini
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db_test
DB_PORT=5432
DB_NAME=postgres_test
SECRET_KEY=test_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🐳 Running with Docker (Recommended)

Ensure you have Docker and Docker Compose installed.

1. **Build and start the containers:**
   ```bash
   docker-compose up -d --build
   ```

2. **Access the API:**
   The application will be available at `http://localhost:8000`.

3. **API Documentation:**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 🏃 Running Locally

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi-postgres-docker-starter
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start a local PostgreSQL database** and update your `.env` file accordingly.

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Running Tests

Tests run in an isolated Docker container to ensure environment consistency.

Run the provided script:
```bash
./run_tests.sh
```

Or run manually via Docker Compose:
```bash
docker-compose --profile test --env-file .env.test run --rm web pytest
```