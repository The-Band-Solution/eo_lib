---
description: Enforce Agile & Project Management Standards for tasks
---

Follow this workflow ensuring all work adheres to "The Band Project" standards.

## 1. Definition of Ready (DoR) Check
Before moving a task to "In Progress":
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
    - [ ] **Start**: Begin programming only after issue creation.

## 2. Artifact Maintenance
Maintain the following artifacts throughout the lifecycle:
- [ ] `task.md`: For detailed task tracking.
- [ ] `implementation_plan.md`: For technical planning and review.

## 3. Implementation Standards
- [ ] **TDD**: Code must pass all tests.
- [ ] **Style**: Code must pass `black`, `flake8`, `isort`.
- [ ] **Business Logic**: All business rules requirements must be satisfied and verified.

## 4. Pull Request Standards
- [ ] **Process**:
    - [ ] Create PR from feature branch targeting `main`.
    - [ ] **Template**: Use `.github/pull_request_template.md`.
- [ ] **Content Requirements**:
    - [ ] **Related Issues**: List linked issues (e.g., `Closes #1`).
    - [ ] **Modifications**: Detailed list of technical changes.
    - [ ] **How to Test**: Clear steps for verification.

    - [ ] **How to Test**: Clear steps for verification.

## 5. Merge Standards
- [ ] **Conflict Free**: PR can be merged if there are no conflicts.
- [ ] **Cleanup**: Delete the feature branch (locally and remotely) after successful merge.

## 6. Definition of Done (DoD)
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
