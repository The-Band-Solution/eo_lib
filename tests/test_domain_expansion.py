import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from eo_lib.domain.base import Base
from eo_lib.domain.entities import (
    Organization,
    OrganizationalUnit,
    Initiative,
    Team,
    TeamMember,
    Person,
    Role,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_organization_creation(session):
    org = Organization(
        name="Horizon Corp", short_name="HC", description="Main organization"
    )
    session.add(org)
    session.commit()

    saved_org = session.query(Organization).filter_by(name="Horizon Corp").first()
    assert saved_org is not None
    assert saved_org.short_name == "HC"


def test_organization_person_m2m(session):
    org = Organization(name="Horizon Corp")
    p1 = Person(name="John Doe", emails=["john@example.com"])
    p2 = Person(name="Jane Doe", emails=["jane@example.com"])

    org.persons.append(p1)
    org.persons.append(p2)

    session.add(org)
    session.commit()

    saved_org = session.query(Organization).first()
    assert len(saved_org.persons) == 2
    assert p1.organizations[0].name == "Horizon Corp"


def test_organizational_unit_recursion(session):
    org = Organization(name="Horizon Corp")
    session.add(org)
    session.commit()

    parent_ou = OrganizationalUnit(name="Engineering", organization_id=org.id)
    session.add(parent_ou)
    session.commit()

    child_ou = OrganizationalUnit(
        name="Mobile Team", organization_id=org.id, parent_id=parent_ou.id
    )
    session.add(child_ou)
    session.commit()

    saved_parent = (
        session.query(OrganizationalUnit).filter_by(name="Engineering").first()
    )
    assert len(saved_parent.children) == 1
    assert saved_parent.children[0].name == "Mobile Team"
    assert saved_parent.children[0].parent.name == "Engineering"


def test_initiative_recursion(session):
    p_parent = Initiative(name="Moonshot")
    session.add(p_parent)
    session.commit()

    p_child = Initiative(name="Apollo 11", parent_id=p_parent.id)
    session.add(p_child)
    session.commit()

    saved_parent = session.query(Initiative).filter_by(name="Moonshot").first()
    assert len(saved_parent.sub_initiatives) == 1
    assert saved_parent.sub_initiatives[0].name == "Apollo 11"
    assert saved_parent.sub_initiatives[0].parent.name == "Moonshot"


def test_organization_links(session):
    org = Organization(name="Horizon Corp")
    session.add(org)
    session.commit()

    team = Team(name="A-Team", short_name="AT", organization_id=org.id)
    initiative = Initiative(name="Project X", organization_id=org.id)

    session.add_all([team, initiative])
    session.commit()

    saved_org = session.query(Organization).first()
    assert len(saved_org.teams) == 1
    assert len(saved_org.initiatives) == 1
    assert team.organization.name == "Horizon Corp"
    assert team.short_name == "AT"
    assert initiative.organization.name == "Horizon Corp"


def test_initiative_person_m2m(session):
    initiative = Initiative(name="Project Omega")
    p1 = Person(name="Alice", emails=["alice@example.com"])
    p2 = Person(name="Bob", emails=["bob@example.com"])

    initiative.persons.append(p1)
    initiative.persons.append(p2)

    session.add(initiative)
    session.commit()

    saved_initiative = session.query(Initiative).filter_by(name="Project Omega").first()
    assert len(saved_initiative.persons) == 2
    assert p1.initiatives[0].name == "Project Omega"
    assert p2.initiatives[0].name == "Project Omega"


def test_team_member_role(session):
    org = Organization(name="Horizon Corp")
    team = Team(name="A-Team", organization_id=org.id)
    person = Person(name="John Doe", emails=["john@example.com"])
    role = Role(name="Lead", description="Team Lead")

    session.add_all([org, team, person, role])
    session.commit()

    membership = TeamMember(person_id=person.id, team_id=team.id, role=role)
    session.add(membership)
    session.commit()

    saved_membership = session.query(TeamMember).first()
    assert saved_membership.role.name == "Lead"
    assert saved_membership.person.name == "John Doe"
    assert saved_membership.team.name == "A-Team"
