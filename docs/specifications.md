# specifications: eo_lib

## 1. Database Schema

### Table: `persons`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO` | Unique Identifier |
| `name` | `VARCHAR(100)` | `NOT NULL` | Full Name |
| `identification_id` | `VARCHAR(50)` | `UNIQUE` | Personal Identification Card |
| `birthday` | `DATE` | | Date of Birth |
| `created_at` | `TIMESTAMP` | `DEFAULT NOW()` | Record creation time |

### Table: `person_emails`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO` | Unique Identifier |
| `person_id` | `INTEGER` | `FK(persons.id)`, `NOT NULL` | Owner of the email |
| `email` | `VARCHAR(255)` | `UNIQUE`, `NOT NULL` | Email Address |

### Table: `teams`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO` | Unique Identifier |
| `name` | `VARCHAR(100)` | `UNIQUE`, `NOT NULL` | Team Name |
| `description` | `TEXT` | | Optional description |

### Table: `team_members`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO` | Unique Identifier |
| `person_id` | `INTEGER` | `FK(persons.id)` | Link to Person |
| `team_id` | `INTEGER` | `FK(teams.id)` | Link to Team |
| `role` | `VARCHAR(50)` | `NOT NULL`, `DEFAULT 'member'` | Role in team |
| `start_date` | `DATE` | `NOT NULL`, `DEFAULT NOW()` | Membership start |
| `end_date` | `DATE` | `NULLABLE` | Membership end |

### Table: `projects`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO` | Unique Identifier |
| `name` | `VARCHAR(100)` | `UNIQUE`, `NOT NULL` | Project Name |
| `description` | `TEXT` | | Optional description |
| `start_date` | `TIMESTAMP` | | Projected start date |
| `end_date` | `TIMESTAMP` | | Projected end date |
| `status` | `VARCHAR(20)` | `DEFAULT 'active'` | Status |

### Table: `organizations`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO` | Unique Identifier |
| `name` | `VARCHAR(100)` | `NOT NULL` | Organization Name |
| `description` | `TEXT` | | Optional description |
| `short_name` | `VARCHAR(50)` | `UNIQUE` | Acronym |

### Table: `organizational_units`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO` | Unique Identifier |
| `name` | `VARCHAR(100)` | `NOT NULL` | Unit Name |
| `organization_id` | `INTEGER` | `FK(organizations.id)` | Parent Org |
| `parent_id` | `INTEGER` | `FK(organizational_units.id)` | Parent Unit (Hierarchy) |
| `description` | `TEXT` | | Optional description |
| `short_name` | `VARCHAR(50)` | | Optional short name |

### Table: `project_teams`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `project_id` | `INTEGER` | `FK(projects.id)`, `PK` | Project Link |
| `team_id` | `INTEGER` | `FK(teams.id)`, `PK` | Team Link |

## 2. API Specifications (Public Interface)

### Class: `PersonController`
- `create_person(name: str, emails: list[str] = None, identification_id: str = None, birthday: date = None) -> Person`
- `get_person(id: int) -> Person`
- `update_person(id: int, name: str = None, emails: list[str] = None, identification_id: str = None, birthday: date = None) -> Person`
- `delete_person(id: int) -> None`
- `list_persons() -> list[Person]`

### Class: `TeamController`
- `create_team(name: str, description: str) -> Team`
- `get_team(id: int) -> Team`
- `update_team(id: int, name: str = None, description: str = None) -> Team`
- `delete_team(id: int) -> None`
- `list_teams() -> list[Team]`
- `add_member(team_id: int, person_id: int, role: str, start_date: date = None, end_date: date = None) -> TeamMember`
- `remove_member(member_id: int) -> None`
- `get_members(team_id: int) -> list[TeamMember]`

### Class: `ProjectController`
- `create_project(name: str, description: str = None, start_date = None, end_date = None) -> Project`
- `get_project(id: int) -> Project) -> Project`
- `update_project(id: int, name: str = None, status: str = None, description: str = None, start_date = None, end_date = None) -> Project`
- `delete_project(id: int) -> None`
- `list_projects() -> list[Project]`
- `assign_team(project_id: int, team_id: int) -> void`
- `get_teams(project_id: int) -> list[Team]`

### Class: `OrganizationController`
- `create_organization(name: str, description: str = None, short_name: str = None) -> Organization`
- `get_organization(id: int) -> Organization`
- `update_organization(id: int, name: str = None, description: str = None, short_name: str = None) -> Organization`
- `delete_organization(id: int) -> None`
- `list_organizations() -> list[Organization]`

### Class: `OrganizationalUnitController`
- `create_unit(name: str, organization_id: int, parent_id: int = None, description: str = None, short_name: str = None) -> OrganizationalUnit`
- `get_unit(id: int) -> OrganizationalUnit`
- `update_unit(id: int, name: str = None, parent_id: int = None, description: str = None, short_name: str = None) -> OrganizationalUnit`
- `delete_unit(id: int) -> None`
- `list_units(organization_id: int = None) -> list[OrganizationalUnit]`
