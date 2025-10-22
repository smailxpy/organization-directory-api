# 🏢 Organization Directory API

A RESTful API built with **FastAPI**, **SQLAlchemy**, and **Alembic** — providing CRUD and advanced filtering for **Organizations**, **Buildings**, and **Activities**.

---

## 🚀 Features

- CRUD for Buildings, Activities, and Organizations  
- Filters:
  - Organizations by building  
  - Organizations by activity (recursive)  
  - Organizations by name search  
  - Organizations near coordinates (lat/lon)  
- Static API key authentication via header (`x-api-key`)  
- PostgreSQL database (Dockerized)  
- Swagger documentation at `/docs`

---

## 🛠 Tech Stack

- **FastAPI**
- **SQLAlchemy + Alembic**
- **PostgreSQL (Docker)**
- **Pydantic v2**
- **Uvicorn**

---

## ⚙️ Run locally with Docker

```bash
git clone https://github.com/smailxpy/organization-directory-api.git
cd organization-directory-api
docker compose up --build
