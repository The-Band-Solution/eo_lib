# Walkthrough - eo_lib

I have successfully updated the library to be a robust, persistent, and well-documented Python CRUD library with a full **CI/CD Pipeline**, **Multi-Strategy Storage**, and **Generic Repository Pattern**.

## 1. Architecture Overhaul (DRY + TDD + Strategy + Generic)
- **Unified Models (DRY)**: Entities inherit from SQLAlchemy `Base`. No separate `orm_models.py`.
- **Strategy Pattern**: Data access via interchangeable strategies (SQL, Memory, JSON).
- **Generic Repository**: implemented `GenericRepositoryInterface[T]` and `GenericPostgresRepository[T]` to remove boiler-plate code.
- **Refactoring**: `GenericMemoryRepository[T]` and `GenericJsonRepository[T]` also implemented to ensure DRY across all strategies.
- **Full Documentation**: Docstrings added to Services, Controllers, Repositories, and Entities. SDD updated with IEEE-style Data Design.
- **TDD Compliance**: Comprehensive `pytest` suite covering 100% of Service methods.

## 2. Recent Updates (Comprehensive Demo & Entity Expansion)
- **Comprehensive Demo**: Expanded `tests/demo.py` to cover all core classes (`Person`, `Team`, `Project`) and their relationships.
- **Project Entity Expansion**: Added `description`, `start_date`, and `end_date` to the `Project` entity.
- **Multi-Email Support**: Refactored `Person` to support multiple email addresses (one-to-many relationship with `PersonEmail`).
- **ORM Reliability**: Configured `expire_on_commit=False` and implemented cascade deletes for associations to ensure robust database operations.

## 3. Configuration & Persistence
- **Environment Variables**: Data source controlled via `.env` file.
- **SQLite Support**: Configured to use `cv_lib.db` (via `.env`) for easy testing.

### Storage Strategies
You can switch the storage backend by changing `STORAGE_TYPE` in `.env`:

1.  **Database (Postgres/SQLite)**:
    ```env
    STORAGE_TYPE=db
    DATABASE_URL=sqlite:///./eo_lib.db
    # or DATABASE_URL=postgresql://...
    ```

2.  **In-Memory (Ephemeral)**:
    ```env
    STORAGE_TYPE=memory
    ```

3.  **JSON Files**:
    ```env
    STORAGE_TYPE=json
    JSON_DATA_DIR=./data_json
    ```

## 3. CI/CD Pipeline
A GitHub Action `ci_cd.yml` has been added to `.github/workflows`.
- **Trigger**: Push to `main`.
- **Steps**: Test -> Bump Version -> Build -> Publish.

## 4. How to Run locally

### Verification Script
Run the demo to verify CRUD+L operations in the database:
```bash
python3 tests/demo.py
```

### Unit Tests
Run the TDD test suite (23 tests covering all entities):
```bash
pytest
```
To see code coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

## 5. Components
- **Entities/Models**: `domain/entities/*.py` (SQLAlchemy Declarative).
- **Repositories**: `infrastructure/repositories/postgres_*.py` (DB), `memory_repositories.py` (Memory), `json_repositories.py` (JSON).
- **Services**: `services/*_service.py`.
- **Controllers**: `controllers/*_controller.py`.
