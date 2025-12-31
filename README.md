# Enterpprise Ontology Library

**Enterpprise Ontology Library** is a robust, strictly architectural Python library designed for managing **Persons**, **Teams**, and **Projects**. It serves as a reference implementation for **Clean Architecture**, **Spec-Driven Development**, **TDD**, and **DRY** principles in Python.

## 🌟 Features

*   **Strict Architecture**: Layered design with Controllers (Facade), Services (Logic), Repositories (Persistence), and Unified Domain Models.
*   **DRY (Don't Repeat Yourself)**: Domain Entities and ORM Models are valid as a single unified class (SQLAlchemy Declarative).
*   **CRUD+L**: Full support for Create, Read, Update, Delete, and List operations.
*   **Relational Domain**: Complex relationships (One-to-Many, Many-to-Many) between Persons, Teams, and Projects.
*   **Database Agnostic**: Built on SQLAlchemy. Supports PostgreSQL (Production) and SQLite (Testing/Dev).
*   **Fully Documented**: Comprehensive documentation and docstrings.
*   **Test Driven**: 100% Service layer coverage with `pytest`.

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (Optional, defaults to SQLite for dev)

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-org/eo_lib.git
    cd eo_lib
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install .
    # OR for development (including pytest)
    pip install .[dev]
    ```

## ⚙️ Configuration

The application uses `python-dotenv` for configuration. Create a `.env` file in the root directory:

```env
# SQLite (Recommended for trying it out)
DATABASE_URL=sqlite:///./eo_lib.db

# PostgreSQL (Production)
# DATABASE_URL=postgresql://user:password@localhost:5432/eo_lib_db
```

## 🚀 Usage

The library exposes **Controllers** as the public API.

### 1. Person Management
```python
from eo_lib import PersonController

ctrl = PersonController()

# Create
alice = ctrl.create_person("Alice", ["alice@example.com", "alice.work@example.com"])

# Update
ctrl.update_person(alice.id, name="Alice Cooper", emails=["new.email@example.com"])

# Get & List
p = ctrl.get_person(alice.id)
all_people = ctrl.list_persons()

# Delete
ctrl.delete_person(alice.id)
```

### 2. Team Management
```python
from eo_lib import TeamController
from datetime import date

ctrl = TeamController()

# Create Team
team = ctrl.create_team("Alpha Squad", "Top Priority Team")

# Add Member (with start/end dates)
member = ctrl.add_member(
    team_id=team.id, 
    person_id=1, 
    role="Lead", 
    start_date=date.today()
)

# Get Members
members = ctrl.get_members(team.id)
```

### 3. Project Management
```python
from eo_lib import ProjectController

ctrl = ProjectController()

# Create Project
proj = ctrl.create_project(
    name="Moon Mission",
    description="Exploring the lunar surface.",
    start_date=date.today()
)

# Assign Team to Project
ctrl.assign_team(proj.id, team_id=1)

# List Projects
projects = ctrl.list_projects()
```

## 🧪 Testing

### Running Unit Tests (TDD)
The project adheres to TDD. Run the full test suite with:
```bash
pytest
```

To see code coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

### Running the Verification Demo
A demonstration script is provided to verify database connectivity and basic flows:
```bash
python3 tests/demo.py
```

## 📚 Documentation
*   [Constitution](docs/constitution.md)
*   [Requirements](docs/requirements.md)
*   [Specifications](docs/specifications.md)
*   [SDD / UML](docs/sdd.md)
