# Enterprise Ontology Library

**Enterprise Ontology Library** is a robust, strictly architectural Python library designed for managing **Persons**, **Teams**, and **Initiatives**. It serves as a reference implementation for **Clean Architecture**, **Spec-Driven Development**, **TDD**, and **DRY** principles in Python, leveraging a generic core implementation (`libbase`).

## 🌟 Features

*   **Strict Architecture**: Layered design with Controllers (Facade), Services (Logic), Repositories (Persistence), and Unified Domain Models.
*   **Generic Patterns**: Built on top of `libbase` for reusable generic Service, Controller, and Repository patterns.
*   **DRY (Don't Repeat Yourself)**: Domain Entities and ORM Models are valid as a single unified class (SQLAlchemy Declarative).
*   **CRUD+L**: Full support for Create, Read, Update, Delete, and List operations.
*   **Relational Domain**: Complex relationships (One-to-Many, Many-to-Many) between Persons, Teams, and Initiatives.
*   **Database Agnostic**: Built on SQLAlchemy. Supports PostgreSQL (Production) and SQLite (Testing/Dev).
*   **Fully Documented**: Comprehensive documentation and docstrings.
*   **Test Driven**: 100% Service layer coverage with `pytest`.

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (Optional, defaults to SQLite for dev)

### Direct Installation (Recommended)

You can install `eo_lib` directly from our official releases without cloning the repository. This is the fastest way to start using the library in your projects.

1.  **Install via pip**:
    Download and install the latest wheel (`.whl`) from our [GitHub Releases](https://github.com/The-Band-Solution/eo_lib/releases):

    ```bash
    # Install version v0.2.0
    pip install https://github.com/The-Band-Solution/eo_lib/releases/download/v0.2.0/eo_lib-0.2.0-py3-none-any.whl
    ```

### Development Setup (Clone)

If you wish to contribute or run the internal demos, clone the repository:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/The-Band-Solution/eo_lib.git
    cd eo_lib
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install for development**:
    ```bash
    pip install -e .[dev]
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

The library exposes **Generic Controllers** as the public API.

### 1. Person Management
```python
from eo_lib import PersonController

ctrl = PersonController()

# Create
alice = ctrl.create_person("Alice", ["alice@example.com", "alice.work@example.com"])

# Update (Generic API)
# Uses update_details wrapper internally or generic update
ctrl.update_person(alice.id, name="Alice Cooper", emails=["new.email@example.com"])

# Get & List (Generic API)
p = ctrl.get_by_id(alice.id)
all_people = ctrl.get_all()

# Delete (Generic API)
ctrl.delete(alice.id)
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

# Generic List
all_teams = ctrl.get_all()
```

### 3. Initiative Management
```python
from eo_lib import InitiativeController

ctrl = InitiativeController()

# Create Initiative
init = ctrl.create_initiative(
    name="Moon Mission",
    description="Exploring the lunar surface.",
    start_date=date.today(),
    initiative_type_name="Strategic"
)

# Assign Team to Initiative
ctrl.assign_team(init.id, team_id=1)

# List Initiatives (Generic API)
initiatives = ctrl.get_all()
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
