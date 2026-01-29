# FastAPI AI Platform

A modern backend platform built with **FastAPI**, focused on **clean architecture, security, coding standards**, and **AI-ready features** such as RAG and Agents.  
The project uses **uv** for fast, deterministic dependency management and **GitHub Actions CI** for quality checks.

---

## Features

### Core Backend
-  FastAPI (async, high-performance)
-  Authentication & user management
-  Blog / content APIs
-  Modular and scalable structure

### AI Capabilities
-  RAG (Retrieval-Augmented Generation)
  - PDF ingestion
  - Vector search
  - LLM-based answers
-  AI Agents (planned)
  - Tool usage
  - Multi-step reasoning
  - Task orchestration

### Infrastructure & Quality
-  **uv** for dependency & lock management
-  Celery + Redis (background jobs)
-  PostgreSQL & MongoDB support
-  CI for **security & coding standards**
-  Linting, formatting, and type checking

---

##  Tech Stack

| Category | Tools |
|-------|------|
| API | FastAPI, Starlette |
| Auth | python-jose, passlib |
| ORM | SQLAlchemy, Alembic |
| Databases | PostgreSQL, MongoDB |
| Async | asyncpg, uvloop |
| AI / ML | transformers, sentence-transformers, OpenAI |
| Queue | Celery, Redis |
| Dependency Mgmt | **uv** |
| Linting | Ruff, Black |
| Typing | MyPy |
| CI | GitHub Actions |

---

##  Project Structure (Simplified)

