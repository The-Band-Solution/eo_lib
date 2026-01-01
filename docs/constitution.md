# Constitution: eo_lib

## 1. Vision statement
To provide a robust, enterprise-grade, and strictly architectural Python library for CRUD operations that can be seamlessly imported into larger applications. It serves as a canonical example of "Correct" Software Engineering principles applied to Python.

## 2. Core Values & Principles
- **DRY (Don't Repeat Yourself)**: Domain Entities and ORM Models are ONE and the SAME. No duplicate class definitions.
- **TDD (Test Driven Development)**: All features must be defined by tests first. Code is only written to pass tests.
- **Full Documentation**: Every class and method must have a docstring explaining its purpose, arguments, and return values.
- **Layered Architecture**: MVC + Service + Repository is preserved, but Entities flow through all layers (Unified Model).
- **SOLID**: Adherence to principles where they don't conflict with Pragmatism (DRY).
- **Module-First Structure**: Every folder is a Python module and must contain an `__init__.py`. This file must expose public classes to flatten the import path (e.g., `from package import Class` instead of `from package.file import Class`).

## 3. Technology Stack
- **Language**: Python 3.10+
- **Database**: PostgreSQL (SQLAlchemy Sync)
- **Testing**: Pytest
- **Validation**: Pydantic (Optional, or handled via Type Hints/Pre-conditions)

## 4. Architecture Overview
- **Controller Layer**: Public Interface / Facade.
- **Service Layer**: Pure Business Logic.
- **Domain/Model Layer**: Unified SQLAlchemy Models (Active Record style definitions, but unrelated to persistence logic).
- **Infrastructure Layer**: Repositories handling DB sessions.

## 5. Methodology
- **Spec-Driven Development**: Requirements -> Specs -> SDD -> Code.
