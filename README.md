## Library Management Backend

Simple backend for a **library system** built with **FastAPI** and **PostgreSQL**.  
You can **register/login users**, **manage books**, and **issue/return books**.

---

## 1. Quick Setup

- Python 3.10+
- PostgreSQL running locally

```bash
git clone <your-repo-url>
cd library_backend

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt  # or install FastAPI, Uvicorn, psycopg2, python-jose
```

Make sure PostgreSQL matches `Connection_db/Connect_db.py`:

- host: `localhost`
- database: `library_db`
- user: `library_user`
- password: `library@123`

Start the API:

```bash
uvicorn main:app --reload
```

Open docs in browser: `http://localhost:8000/docs`

---

## 2. Basic Actions (with commands)

Assume API is running at `http://localhost:8000`.

### 2.1 Register a User

`POST /User/register`

```bash
curl -X POST http://localhost:8000/User/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### 2.2 Login and Get Token

`POST /auth/login`

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

Response:

```json
{
  "access_token": "YOUR_JWT_TOKEN",
  "token_type": "bearer"
}
```

Save token:

```bash
TOKEN=YOUR_JWT_TOKEN
```

---

## 3. Admin Actions (require token)

Send header: `Authorization: Bearer <TOKEN>`

### 3.1 List All Users

`GET /User/`

```bash
curl http://localhost:8000/User/ \
  -H "Authorization: Bearer $TOKEN"
```

### 3.2 Add a Book

`POST /Books/`

```bash
curl -X POST http://localhost:8000/Books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "The Hobbit",
    "genre": "Fantasy",
    "copies_available": 5
  }'
```

---

## 4. Books & Issued Books

### 4.1 See All Books

`GET /Books/`

```bash
curl http://localhost:8000/Books/
```

### 4.2 Search Books by Genre

`GET /Books/search?genre=<genre>`

```bash
curl "http://localhost:8000/Books/search?genre=Fantasy"
```

### 4.3 Issue a Book

`POST /issued-books/`

```bash
curl -X POST http://localhost:8000/issued-books/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_name": "Admin User",
    "book_title": "The Hobbit"
  }'
```

### 4.4 See Books Issued to a User

`GET /issued-books/see-books-issued-on-you?user_id=<id>`

```bash
curl "http://localhost:8000/issued-books/see-books-issued-on-you?user_id=1"
```

### 4.5 Return a Book

`DELETE /issued-books/?issued_id=<id>&book_title=<title>`

```bash
curl -X DELETE "http://localhost:8000/issued-books/?issued_id=1&book_title=The%20Hobbit"
```

---

## 5. Notes

- Passwords are stored as plain text (demo only).
- JWT `SECRET_KEY` and DB credentials are hardcoded; use environment variables in real deployments.

## Library Management Backend (FastAPI + PostgreSQL)

This project is a **Library Management System backend** built with **FastAPI** and **PostgreSQL**. It provides REST APIs for:

- **User management** (registration, list, delete)
- **Authentication** with JWT tokens
- **Book catalogue** (list, add, search by genre)
- **Issuing and returning books** and tracking issued records

---

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM/DB access**: `psycopg2`
- **Auth**: JWT (via `python-jose` / `jose`)

---

## Project Structure

- `main.py` – FastAPI app entrypoint, includes all routers
- `routes/users.py` – User registration and admin user operations
- `routes/books.py` – Book listing, insertion (admin), and search
- `routes/issued_books.py` – Issue/return books and issued-book queries
- `auth/authentication.py` – Login and JWT token creation
- `auth/jwt_auth.py` – Helpers for creating and validating JWT tokens
- `Connection_db/Connect_db.py` – PostgreSQL connection helper
- `Models/Table_schema.py` – Database table creation helpers

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd library_backend
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

Make sure you have `psycopg2`, `fastapi`, `uvicorn`, `python-jose` (or `jose`), and any other required packages installed:

```bash
pip install fastapi uvicorn psycopg2-binary python-jose[cryptography] python-multipart
```

4. **Configure PostgreSQL**

Create a PostgreSQL database and user that match the settings in `Connection_db/Connect_db.py`:

- **host**: `localhost`
- **database**: `library_db`
- **user**: `library_user`
- **password**: `library@123`

Adjust these values in `Connect_db.py` if your local setup is different.

5. **Create database tables**

`Models/Table_schema.py` contains helper functions for creating tables (`users`, `books`, `issued_books`). Run that script once (or use your own migrations) to create the tables before starting the API.

---

## Running the Application

From the project root:

```bash
uvicorn main:app --reload
```

The API will be available at:

- **Base URL**: `http://127.0.0.1:8000`
- **Interactive docs**: `http://127.0.0.1:8000/docs`

---

## Authentication Flow

1. **Register user** (public)
   - `POST /User/register`
   - Body: `name`, `email`, `password`

2. **Login** (public)
   - `POST /auth/login`
   - Body: `email`, `password`
   - Returns: `access_token` (JWT) and `token_type`

3. **Use token for protected routes**
   - Add header: `Authorization: Bearer <access_token>`
   - Admin-only routes check `role == "ADMIN"` in the JWT payload.

---

## Main Endpoints (Overview)

### Users (`/User`)

- `POST /User/register` – Register a new user.
- `GET /User/` – **Admin only**: list all users.
- `DELETE /User/?email=<email>` – **Admin only**: delete a user by email.

### Auth (`/auth`)

- `POST /auth/login` – Login with email and password, returns JWT token.

### Books (`/Books`)

- `GET /Books/` – List all books.
- `POST /Books/` – **Admin only**: insert a new book.
- `GET /Books/search?genre=<genre>` – Search books by genre.

### Issued Books (`/issued-books`)

- `GET /issued-books/gener?genre=<genre>` – List books by genre (from issued-books router).
- `POST /issued-books/` – Issue a book to a user (reduces `copies_available`).
- `GET /issued-books/see_table` – **Admin only**: see all issued records.
- `GET /issued-books/?email=<email>` – See a user’s credentials (id, name, email).
- `GET /issued-books/see-books-issued-on-you?user_id=<id>` – See all books issued to a user.
- `DELETE /issued-books/?issued_id=<id>&book_title=<title>` – Return a book (increments `copies_available`).

---

## Notes & Improvements

- Passwords are currently stored in plain text; in a real system, use hashing (e.g. `passlib`) before saving to the database.
- The DB connection is created at module import time; consider using connection pooling or FastAPI dependencies for better resource management.
- `SECRET_KEY` in `auth/jwt_auth.py` should be stored in environment variables in production.

# Library Management Backend (FastAPI)

This project is a **FastAPI-based backend** for a simple library management system.  
It manages **users, books, and issued books**, and includes **JWT-based authentication** and **role-based access control (ADMIN / USER)**.

## Features

- **User management**
  - Create and store users with roles (`ADMIN`, `USER`)
  - Validate and fetch user credentials
- **Books management**
  - View all books
  - Add books (ADMIN only)
  - Search books by genre
- **Issued books**
  - Issue a book to a user (decrease available copies)
  - View all issued books (ADMIN only)
  - View books issued to a specific user
  - Return a book (increase available copies)
- **Authentication**
  - Login with email and password
  - JWT token generation and validation
  - Protect endpoints using user roles

## Project Structure

- `main.py` – FastAPI app entrypoint; includes all routers.
- `routes/`
  - `users.py` – User-related routes.
  - `books.py` – Book listing, creation, and search routes.
  - `issued_books.py` – Book issuing, returning, and related queries.
- `auth/`
  - `authentication.py` – Login endpoint that issues JWTs.
  - `jwt_auth.py` – Helpers for creating and validating JWT tokens.
- `Connection_db/`
  - `Connect_db.py` – PostgreSQL connection helper (`connect_library_db`).
- `Models/`
  - `Table_schema.py` – Functions to create the `users`, `books`, and `issued_books` tables.
- `requirements.txt` – Python dependencies for this project.

## Requirements

- Python 3.10+
- PostgreSQL running with a database and user matching the settings in `Connection_db/Connect_db.py`:
  - `host="localhost"`
  - `database="library_db"`
  - `user="library_user"`
  - `password="library@123"`

You can change these values in `Connect_db.py` to match your local/PostgreSQL configuration.

## Installation

1. **Clone the repository** (or copy the project folder).
2. (Recommended) **Create and activate a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Linux/macOS
   # .venv\Scripts\activate   # on Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure PostgreSQL is running** and that the `library_db` database and `library_user` user exist with the correct password.

## Running the Application

1. Make sure the database is accessible.
2. Start the FastAPI app with Uvicorn from the project root:

   ```bash
   uvicorn main:app --reload
   ```

3. Open the interactive API docs in your browser:

   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Authentication & Roles

- Use the `/auth/login` endpoint with a valid email/password from the `users` table to obtain a **JWT access token**.
- Send the token as a **Bearer token** in the `Authorization` header to access protected endpoints (e.g., admin-only operations).
- The JWT payload includes the user's `email` and `role`; admin-only endpoints check that `role == "ADMIN"`.

## Notes

- Initial table creation is handled in `Models/Table_schema.py` (the functions are called at the bottom of that file).
- You may want to:
  - Secure the `SECRET_KEY` in `auth/jwt_auth.py`.
  - Move DB credentials to environment variables.
  - Add proper migrations (e.g., with Alembic) for production use.

# library_app
