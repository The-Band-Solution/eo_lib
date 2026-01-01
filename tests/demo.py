"""
Demonstration script for the eo_lib library.

This script showcases the core functionality of the library, including
Organization, Unit, Person, Team, and Initiative operations using the Controller facades.
It initializes a clean database for each run.
"""

import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from eo_lib import (
    PersonController,
    TeamController,
    InitiativeController,
    OrganizationController,
    OrganizationalUnitController,
)
from eo_lib.infrastructure.database.postgres_client import PostgresClient
from eo_lib.domain.base import Base  # Unified Model Base


def setup_database():
    """
    Initializes the database by dropping and recreating all tables.

    This ensures a clean state for the demonstration.
    """
    print("Initializing Database Tables...")
    client = PostgresClient()
    # Import all models from the centralized package
    from eo_lib.domain.entities import (
        Person,
        PersonEmail,
        Team,
        TeamMember,
        Initiative,
        InitiativeType,
        Organization,
        OrganizationalUnit,
    )

    from sqlalchemy import text
    
    # Drop legacy tables to clean old schema
    with client._engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS project_teams CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS project_persons CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS projects CASCADE"))
        conn.commit()

    Base.metadata.drop_all(client._engine)
    Base.metadata.create_all(client._engine)


def main():
    """
    Executes the demonstration workflow.

    Covers:
    1. Organization and Organizational Unit operations.
    2. Person creation, listing, and updates.
    3. Team creation and member management.
    4. Initiative creation and team assignment.
    5. Cleanup and verification.
    """
    try:
        setup_database()

        org_ctrl = OrganizationController()
        unit_ctrl = OrganizationalUnitController()
        person_ctrl = PersonController()
        team_ctrl = TeamController()
        initiative_ctrl = InitiativeController()

        print("\n--- 1. ORGANIZATION OPERATIONS ---")
        # Create Organization
        acme = org_ctrl.create_organization(
            "Acme Corp", description="A global conglomerate", short_name="ACME"
        )
        print(f"Organization Created: {acme.name} ({acme.short_name})")

        # Create Organizational Units (Hierarchy)
        engineering = unit_ctrl.create_unit(
            "Engineering", organization_id=acme.id, description="R&D and Product"
        )
        software_dev = unit_ctrl.create_unit(
            "Software Development",
            organization_id=acme.id,
            parent_id=engineering.id,
            short_name="SOFT-DEV",
        )
        hr = unit_ctrl.create_unit("Human Resources", organization_id=acme.id)
        
        print(f"Units Created: {engineering.name}, {software_dev.name} (Parent: {engineering.name}), {hr.name}")

        # List Units
        all_units = unit_ctrl.get_all()
        print(f"Total Units in ACME: {len(all_units)}")

        print("\n--- 2. PERSON OPERATIONS ---")
        # Create
        alice = person_ctrl.create_person(
            "Alice Programmer",
            ["alice@example.com", "alice.work@example.com"],
            identification_id="ID-001",
            birthday=date(1990, 5, 15),
        )
        bob = person_ctrl.create_person(
            "Bob Developer",
            ["bob@example.com"],
            identification_id="ID-002",
            birthday=date(1985, 10, 20),
        )
        charlie = person_ctrl.create_person("Charlie Manager", [])  # No emails

        print(
            f"Created Persons: ID {alice.id} ({alice.name}) - ID Card: {alice.identification_id}, Bday: {alice.birthday}"
        )
        print(
            f"Created Persons: ID {bob.id} ({bob.name}) - ID Card: {bob.identification_id}, Bday: {bob.birthday}"
        )
        print(f"Created Persons: ID {charlie.id} ({charlie.name})")

        # Update
        updated_bob = person_ctrl.update_person(
            bob.id,
            name="Bob 'The Builder' Developer",
            emails=["bob.builder@example.com", "bob@generic.com"],
        )
        print(
            f"Updated Bob: {updated_bob.name} (Emails: {[e.email for e in updated_bob.emails]})"
        )

        print("\n--- 3. TEAM OPERATIONS ---")
        # Create Teams
        frontend_team = team_ctrl.create_team("Frontend Team", "Specialized in UI/UX")
        backend_team = team_ctrl.create_team(
            "Backend Team", "Specialized in APIs and DBs"
        )
        print(f"Teams Created: {frontend_team.name}, {backend_team.name}")

        # Add Members
        team_ctrl.add_member(
            frontend_team.id, alice.id, "Lead Developer", start_date=date.today()
        )
        team_ctrl.add_member(
            backend_team.id, updated_bob.id, "Senior Engineer", start_date=date.today()
        )
        team_ctrl.add_member(
            backend_team.id, charlie.id, "Product Owner", start_date=date.today()
        )

        print(f"Members added to teams.")

        # List Members
        fe_members = team_ctrl.get_members(frontend_team.id)
        be_members = team_ctrl.get_members(backend_team.id)
        print(
            f"Frontend Team ({len(fe_members)} members): {[m.role.name for m in fe_members]}"
        )
        print(
            f"Backend Team ({len(be_members)} members): {[m.role.name for m in be_members]}"
        )

        print("\n--- 4. INITIATIVE OPERATIONS ---")
        # Create Initiative Type
        strategic_type = initiative_ctrl.create_initiative_type(
            "Strategic", "High priority long term"
        )
        print(f"Initiative Type Created: {strategic_type['name']}")

        # Create Initiative
        horizon_initiative = initiative_ctrl.create_initiative(
            "Horizon Initiative",
            description="A futuristic initiative to explore the unknown.",
            start_date=date.today(),
            initiative_type_name="Strategic",
        )
        print(
            f"Initiative Created: {horizon_initiative['name']} (Status: {horizon_initiative['status']})"
        )

        # Assign Teams to Initiative
        initiative_ctrl.assign_team(horizon_initiative["id"], frontend_team.id)
        initiative_ctrl.assign_team(horizon_initiative["id"], backend_team.id)
        print(f"Teams assigned to {horizon_initiative['name']}.")

        print("\n--- 5. CLEANUP / DELETION ---")
        # Delete Charlie
        person_ctrl.delete(charlie.id)
        print(f"Manager (ID {charlie.id}) Deleted.")

        # Verify remaining people
        remaining_people = person_ctrl.get_all()
        print(f"Remaining People: {[p.name for p in remaining_people]}")

        print("\n--- DEMO COMPLETED SUCCESSFULLY ---")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
