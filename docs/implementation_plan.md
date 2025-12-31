# Implementation Plan - Python CRUD Library (MVC+Repo+Service)

This plan outlines the creation of a Python library `eo_lib_antigravity` designed for CRUD operations, following an MVC + Repository + Service architecture, complete with SDD (Software Design Description) and UML documentation.

## User Review Required

> [!IMPORTANT]
> **Architecture Update**: Standard Strict Clean Architecture (Separated Entity/ORM) is being replaced by a **DRY / Pragmatic Architecture**:
> - **DRY (Don't Repeat Yourself)**: Domain Entities and ORM Models are ONE and the SAME.
> - **Strategy Pattern (Storage)**: Data access is abstracted behind Repository Interfaces. Concrete strategies include:
>     - **SQL**: Database (Postgres/SQLite).
>     - **Memory**: Ephemeral in-memory dictionary.
>     - **JSON**: File-based persistence.
> - **Generic Repository Pattern**: Use Python `TypeVar` and `Generic[T]` with Abstract Base Classes (ABC) to implement common CRUD operations once, reducing duplication across Person/Team/Project repositories.
> - **TDD (Test Driven Development)**: All features must be defined by tests first. be fully documented (Docstrings).
>
> **Design Patterns & OO Principles:**
> - **Repository Pattern**: Persists the Unified Models.
> - **Dependency Injection**: Service receives Repository via constructor.
> - **Singleton Pattern**: For Database Connection.
> - **Factory Pattern**: Wiring.




## Proposed Changes

### Project Structure (Root)

#### [NEW] [pyproject.toml](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/pyproject.toml)
- Configuration for build system and dependencies.

#### [NEW] [README.md](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/README.md)
- General documentation and usage examples.

#### [NEW] [docs/constitution.md](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/docs/constitution.md)
- Project Charter: Vision, Goals, Scope, and Stakeholders.

#### [NEW] [docs/requirements.md](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/docs/requirements.md)
- Functional Requirements: Manage Person, Team, TeamMember, Project.

#### [UPDATE] [docs/specifications.md](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/docs/specifications.md)
- Update API Signatures to include full CRUD+L: `create`, `get`, `update`, `delete`, `list_all`.

#### [UPDATE] [docs/sdd.md](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/docs/sdd.md)
- Update Class Diagrams to show full CRUD+L methods.

### Source Code (`src/eo_lib_antigravity`)

#### [REFACTOR] Separate Files by Entity

**Domain Repositories (Interfaces)**
- `domain/repositories/person_repository.py`
- `domain/repositories/team_repository.py`
- `domain/repositories/project_repository.py`
- *Delete* `domain/repositories/interfaces.py`

**Infrastructure Repositories**
- `infrastructure/repositories/postgres_person_repository.py`
- `infrastructure/repositories/postgres_team_repository.py`
- `infrastructure/repositories/postgres_project_repository.py`
- *Delete* `infrastructure/repositories/postgres_repositories.py`

**Services**
- `services/person_service.py`
- `services/team_service.py`
- `services/project_service.py`
- *Delete* `services/domain_services.py`

**Controllers**
- `controllers/person_controller.py`
- `controllers/team_controller.py`
- `controllers/project_controller.py`
- *Delete* `controllers/facade.py`

**Factories & Init**
- Update `factories.py` and `__init__.py` to reflect new paths.

#### [NEW] [__init__.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/__init__.py)
- Exposes Controllers for Person, Team, Project.

#### [NEW] [config.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/config.py)
- Configuration management.

### Source Code (`src/eo_lib_antigravity`)

#### [REFACTOR] Merge ORM into Domain (DRY)
- **Rules**: Entities will inherit from SQLAlchemy `Base`. No separate `orm_models.py`.
- **Files to Update**:
    - `domain/entities/person.py` (Becomes SQLAlchemy Model)
    - `domain/entities/team.py` (Becomes SQLAlchemy Model)
    - `domain/entities/project.py` (Becomes SQLAlchemy Model)
    - **DELETE** `infrastructure/database/orm_models.py`

#### [REFACTOR] Update Repositories
- Remove `_to_domain` and `_to_model` methods.
- Repositories now interact directly with the Unified Models.

#### [NEW] [src/eo_lib_antigravity/infrastructure/repositories/memory_repositories.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/infrastructure/repositories/memory_repositories.py)
- `InMemoryPersonRepository`, `InMemoryTeamRepository`, `InMemoryProjectRepository`.

#### [NEW] [src/eo_lib_antigravity/infrastructure/repositories/json_repositories.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/infrastructure/repositories/json_repositories.py)
- `JsonPersonRepository`, `JsonTeamRepository`, `JsonProjectRepository`.
- Logic to read/write JSON files.

#### [UPDATE] [src/eo_lib_antigravity/factories.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/factories.py)
- Update `ServiceFactory` to read `STORAGE_TYPE` from Config and instantiate the correct Repository Strategy.

#### [UPDATE] [src/eo_lib_antigravity/config.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/config.py)
- Add `STORAGE_TYPE` (db, memory, json) and `JSON_DATA_DIR`.

#### [NEW] [src/eo_lib_antigravity/domain/repositories/generic_repository.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/domain/repositories/generic_repository.py)
- Define `T = TypeVar('T')`.
- `class GenericRepositoryInterface(ABC, Generic[T])`: Defines `add`, `get`, `update`, `delete`, `list`.

#### [REFCTOR] [src/eo_lib_antigravity/domain/repositories/*.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/domain/repositories/)
- Update specific interfaces (Person, Team, Project) to inherit from `GenericRepositoryInterface`.

#### [NEW] [src/eo_lib_antigravity/infrastructure/repositories/generic_postgres_repository.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/infrastructure/repositories/generic_postgres_repository.py)
- Implement `GenericPostgresRepository(GenericRepositoryInterface)` with shared SQLAlchemy logic.
- Shortcuts the need for repetitive CRUD code in concrete Postgres repositories.

#### [REFCTOR] [src/eo_lib_antigravity/infrastructure/repositories/postgres_*.py](file:///home/paulossjunior/projects/horizon_project/eo_lib_antigravity/src/eo_lib_antigravity/infrastructure/repositories/postgres_*.py)
- Inherit from `GenericPostgresRepository`. Only implement entity-specific methods (e.g., `add_member`, `assign_team`).


## Verification Plan

### Automated Tests
- Run simple python scripts to import the library and perform CRUD operations.
- `python3 tests/demo_usage.py`

### Manual Verification
- Review `docs/sdd.md` for UML correctness.
