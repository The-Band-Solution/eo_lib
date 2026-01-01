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

### FR-03: Initiative Management
- **FR-03-A**: The system must allow creating an Initiative with `name`, `description`, `start_date`, `end_date`, and `initiative_type`.
- **FR-03-B**: A Team can be assigned to multiple Initiatives.
- **FR-03-C**: An Initiative can have multiple Teams assigned to it (Many-to-Many).
- **FR-03-E**: The system must allow listing all teams working on a specific Initiative.

### FR-04: Initiative Type Management
- **FR-04-A**: The system must allow creating a new Initiative Type (name, description).
- **FR-04-B**: The system must allow listing all Initiative Types.
- **FR-04-C**: The system must allow updating an Initiative Type.
- **FR-04-D**: The system must allow deleting an Initiative Type.

### FR-05: Role Management
- **FR-05-A**: The system must allow creating a new Role (name, description).
- **FR-05-B**: The system must allow listing all Roles.
- **FR-05-C**: The system must allow updating a Role.
- **FR-05-D**: The system must allow deleting a Role.

### FR-06: Organization Management
- **FR-06-A**: The system must allow creating an Organization with `name`, `description`, and `short_name`.
- **FR-06-B**: The system must allow listing all Organizations.
- **FR-06-C**: The system must allow updating Organization metadata.

### FR-07: Organizational Unit Management
- **FR-07-A**: The system must allow creating an Organizational Unit associated with an Organization.
- **FR-07-B**: Organizational Units must support a hierarchical structure (`parent_id`).
- **FR-07-C**: The system must allow listing all Units of an Organization.
- **FR-07-D**: The system must allow updating Unit metadata and its parent.

### FR-08: Configuration
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
- **NFR-03-B**: The system must define indexes for frequently queried columns (e.g., names, foreign keys, status) to optimize read performance.

## 3. Constraints
- Must use PostgreSQL.
- Must use SQLAlchemy.
