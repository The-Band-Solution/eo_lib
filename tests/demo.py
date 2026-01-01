"""
Demonstration script for the eo_lib library.

This script showcases the core functionality of the library, including
Person, Team, and Initiative operations using the Controller facades.
It initializes a clean database for each run.
"""

import sys
import os
from datetime import date, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from eo_lib import PersonController, TeamController, InitiativeController
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
    1. Person creation, listing, and updates.
    2. Team creation and member management.
    3. Initiative creation and team assignment.
    4. Cleanup and verification.
    """
    try:
        setup_database()

        person_ctrl = PersonController()
        team_ctrl = TeamController()
        initiative_ctrl = InitiativeController()

        print("\n--- 1. PERSON OPERATIONS ---")
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

        # List
        all_people = person_ctrl.get_all()
        print(f"Initial People List: {len(all_people)} people found.")

        # Update
        updated_bob = person_ctrl.update_person(
            bob.id,
            name="Bob 'The Builder' Developer",
            emails=["bob.builder@example.com", "bob@generic.com"],
        )
        print(
            f"Updated Bob: {updated_bob.name} (Emails: {[e.email for e in updated_bob.emails]})"
        )

        print("\n--- 2. TEAM OPERATIONS ---")
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

        print("\n--- 3. INITIATIVE OPERATIONS ---")
        # Create Initiative Type
        strategic_type = initiative_ctrl.create_initiative_type(
            "Strategic", "High priority long term"
        )
        print(f"Initiative Type Created: {strategic_type['name']}")

        # Create Initiative
        # Note: DTO returns dict, verify struct.
        horizon_initiative = initiative_ctrl.create_initiative(
            "Horizon Initiative",
            description="A futuristic initiative to explore the unknown.",
            start_date=date.today(),
            initiative_type_name="Strategic",
        )
        print(
            f"Initiative Created: {horizon_initiative['name']} (Status: {horizon_initiative['status']})"
        )
        print(f"Description: {horizon_initiative['description']}")
        print(f"Type: {horizon_initiative['initiative_type']}")

        # Assign Teams to Initiative
        initiative_ctrl.assign_team(horizon_initiative["id"], frontend_team.id)
        initiative_ctrl.assign_team(horizon_initiative["id"], backend_team.id)
        print(f"Teams assigned to {horizon_initiative['name']}.")

        # List Initiative Teams
        assigned_teams = initiative_ctrl.get_teams(horizon_initiative["id"])
        print(
            f"Initiative '{horizon_initiative['name']}' has {len(assigned_teams)} teams."
        )

        # Update Initiative Status
        # Update method returns DTO
        updated_initiative = initiative_ctrl.update_initiative(
            horizon_initiative["id"], status="In Progress"
        )
        print(f"Initiative Status Updated: {updated_initiative['status']}")

        print("\n--- 4. CLEANUP / DELETION ---")
        # Delete Charlie
        person_ctrl.delete(charlie.id)
        print(f"Manager (ID {charlie.id}) Deleted.")

        # Verify remaining people
        remaining_people = person_ctrl.get_all()
        print(f"Remaining People: {[p.name for p in remaining_people]}")

        # Check Backend Team after member deletion
        be_members_now = team_ctrl.get_members(backend_team.id)
        print(
            f"Backend Team now has {len(be_members_now)} members (Charlie should be gone)."
        )

        print("\n--- DEMO COMPLETED SUCCESSFULLY ---")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
