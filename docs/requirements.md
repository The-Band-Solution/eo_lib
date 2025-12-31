# Requirements: eo_lib

## 1. Functional Requirements (FR)

### FR-01: Person Management
- **FR-01-A**: The system must allow creating a new Person with `name` and zero or more `emails`.
- **FR-01-B**: The system must allow retrieving a Person by ID.
- **FR-01-C**: The system must allow updating Person details.
- **FR-01-D**: The system must allow deleting a Person.

### FR-02: Team Management
- **FR-02-A**: The system must allow creating a Team with a `name` and `description`.
- **FR-02-B**: The system must allow adding a Person to a Team as a Team Member with a specific `role`.
- **FR-02-C**: A Person can belong to multiple Teams.
- **FR-02-D**: The system must allow listing all members of a specific Team.

### FR-03: Project Management
- **FR-03-A**: The system must allow creating a Project with `name`, `description`, `start_date`, and `end_date`.
- **FR-03-B**: A Team can be assigned to multiple Projects.
- **FR-03-C**: A Project can have multiple Teams assigned to it (Many-to-Many).
- **FR-03-D**: The system must allow listing all teams working on a specific Project.

### FR-02: Configuration
- **FR-02-A**: The database connection string must be configurable via Environment Variables or a Config object passed at initialization.

## 2. Non-Functional Requirements (NFR)

### NFR-01: Architecture
- **NFR-01-A**: The system must strictly follow MVC + Service + Repository layers.
- **NFR-01-B**: The Domain layer must have no dependencies on the Infrastructure layer (DIP).

### NFR-02: Quality
- **NFR-02-A**: All public methods must be type-hinted.
- **NFR-02-B**: Custom exceptions must be raised for business errors (e.g., `UserNotFoundException`, `UserAlreadyExistsException`), rather than leaking SQL errors.

### NFR-03: Performance
- **NFR-03-A**: Database connections must be pooled and managed efficiently (Singleton/Pool).

## 3. Constraints
- Must use PostgreSQL.
- Must use SQLAlchemy.
