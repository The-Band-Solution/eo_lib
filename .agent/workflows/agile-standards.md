---
description: Enforce Agile & Project Management Standards for tasks
---

Follow this workflow ensuring all work adheres to "The Band Project" standards.

## 1. Branching Strategy (GitFlow)
- **main**: Stable production branch. Restricted.
- **developing**: Integration branch for new work. Branched from `main`.
- **features**: Feature/Bugfix branches. Fork/Branch from `developing`.
    - Format: `feat/<name>`, `bugfix/issue-<id>`, `fix/<name>`.

## 2. Definition of Ready (DoR) Check
Before moving a task to "In Progress":
- [ ] **Documentation First**:
    - [ ] Update `docs/*.md` (e.g., `requirements.md`, `sdd.md`) before creating the issue.
    - [ ] **Reference**: Description MUST link to docs (e.g., "Implement Req 1.1 as detailed in `docs/requirements.md`").
- [ ] **Hierarchy Check**: Confirm strict hierarchy: `Epic -> User Story -> Task`.
- [ ] **Governance**: Ensure work is associated with "The Band Project" ecosystem.
- [ ] **readiness**:
    - [ ] Clear Objective defined?
    - [ ] Acceptance Criteria defined?
    - [ ] Technical Plan ready?
- [ ] **GitHub Issue**:
    - [ ] **Draft**: Provide technical proposal/text to the user.
    - [ ] **Approval**: Mandatory user approval before proceeding.
    - [ ] **Create**: Create the issue on GitHub ONLY after approval.
    - [ ] **Fields Requirement**:
        - [ ] **Label**: Must be set.
        - [ ] **Type**: Must be set.
        - [ ] **Milestone**: Must be set.
        - [ ] **Project**: Must be set to "The Band Project".
    - [ ] **Start**: Begin programming only after issue creation.

## 3. Artifact Maintenance
Maintain the following artifacts throughout the lifecycle:
- [ ] `task.md`: For detailed task tracking.
- [ ] `implementation_plan.md`: For technical planning and review.
- [ ] `docs/backlog.md`: Must include **Releases** section with:
    - PR Number & Link
    - Description
    - Commit SHA & Link

## 4. Implementation Standards
- [ ] **TDD**: Code must pass all tests.
- [ ] **Style**: Code must pass `black`, `flake8`, `isort`.
- [ ] **Business Logic**: All business rules requirements must be satisfied and verified.

## 5. Pull Request Standards
- [ ] **Process**:
    - [ ] Create PR from feature branch targeting `developing`.
    - [ ] **Template**: Use `.github/pull_request_template.md`.
- [ ] **Content Requirements**:
    - [ ] **Related Issues**: List linked issues (e.g., `Closes #1`).
    - [ ] **Modifications**: Detailed list of technical changes.
    - [ ] **How to Test**: Clear steps for verification.


## 6. Release Strategy (CD)
- [ ] **Promotion**: `developing` -> `main`.
- [ ] **Trigger**: All tests passed on `developing`.
- [ ] **Process**:
    - [ ] Open Pull Request from `developing` to `main`.
    - [ ] Title Format: `release: <description>`.
    - [ ] No direct commits to `main` allowed.

## 7. Merge Standards
- [ ] **Conflict Free**: PR can be merged if there are no conflicts.
- [ ] **Cleanup**: Delete the feature branch (locally and remotely) after successful merge.

## 8. Definition of Done (DoD)
- [ ] **Verification**:
    - [ ] Test suite passing.
    - [ ] Linting checks passing.
- [ ] **Documentation**:
    - [ ] Update Google-style docstrings.
    - [ ] Update relevant `docs/*.md` files.
    - [ ] Update/Create `walkthrough.md`.
- [ ] **Closure**:
    - [ ] Close related GitHub Issues.
    - [ ] Update hierarchical status in `docs/backlog.md`.
