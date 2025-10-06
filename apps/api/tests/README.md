# MealMind API Testing Guide

## Overview

This document outlines the testing strategy, folder structure, and conventions for the MealMind API.

---

## 📁 Folder Structure

```
tests/
├── conftest.py              # Shared fixtures (DB engine, session)
├── pytest.ini               # Pytest configuration and markers
├── README.md                # This file
│
├── unit/                    # Fast, isolated, NO external dependencies
│   ├── conftest.py          # Unit-specific fixtures
│   ├── models/              # Mirror: app/models/
│   ├── schemas/             # Mirror: app/schemas/
│   └── services/            # Mirror: app/services/
│
├── integration/             # Cross-component tests WITH external dependencies
│   ├── conftest.py          # Integration fixtures (DB, test client)
│   ├── test_migrations.py
│   ├── test_constraints.py
│   └── test_*.py            # Named by what they test, not where
│
├── e2e/                     # End-to-end user workflows
│   ├── conftest.py          # Full stack fixtures
│   └── test_*_journey.py    # Named by user journey
│
└── fixtures/                # Shared test data and factories
    └── factories.py
```

---

## 🎯 Test Types & Decision Matrix

### Unit Tests

**Location:** `unit/{component}/test_*.py`

**Characteristics:**

- 🔒 Isolated (no database, no HTTP, no file system)
- 🎯 Tests single component in isolation
- 🧪 Uses mocks/stubs for dependencies

**Examples:**

- Enum validation (`unit/models/test_enums.py`)
- Pydantic schema validation (`unit/schemas/test_recipe_schema.py`)
- Pure business logic (`unit/services/test_grocery_logic.py`)

**When to use:**

- Testing individual functions or classes
- Validating data transformations
- Testing edge cases and error handling

**Structure:** Mirrors application code structure

```
app/models/recipe.py  →  tests/unit/models/test_recipe.py
app/schemas/recipe.py →  tests/unit/schemas/test_recipe_schema.py
```

---

### Integration Tests

**Location:** `integration/test_{what_you_test}.py`

**Characteristics:**

- 🔗 Tests how components work TOGETHER
- 🗄️ Requires external dependencies (DB, APIs)
- 📦 Tests integration points, not individual modules

**Examples:**

- Database migrations (`test_migrations.py`)
- Foreign key behaviors (`test_foreign_keys.py`)
- API endpoint + database (`test_recipe_api.py`)
- Service + repository + database (`test_grocery_list_generation.py`)

**When to use:**

- Testing database schema and constraints
- Testing API endpoints with persistence
- Testing relationships between models
- Testing service layer with real database

**Structure:** Flat, named by integration being tested

```
integration/
├── test_migrations.py          # Alembic + SQLAlchemy + PostgreSQL
├── test_constraints.py         # Database constraints
├── test_relationships.py       # Model relationships
├── test_recipe_api.py          # Route + Schema + Service + DB
└── test_grocery_list_generation.py  # Multiple services + DB
```

**❌ DON'T mirror app structure in integration tests**
Integration tests are cross-cutting by nature!

---

### E2E Tests

**Location:** `e2e/test_{journey_name}.py`

**Characteristics:**

- 🎭 Tests complete user workflows
- 🌐 Simulates real user interactions
- 📊 Tests multiple features together

**Examples:**

- Complete meal planning flow (`test_meal_planning_journey.py`)
- Recipe creation to grocery list (`test_recipe_to_groceries_flow.py`)

**When to use:**

- Testing critical user journeys
- Verifying end-to-end functionality
- Testing feature combinations

**Structure:** Flat, named by user journey

```
e2e/
├── test_meal_planning_journey.py
└── test_recipe_management_flow.py
```

---

## 🏷️ Pytest Markers

Use markers to categorize and filter tests:

```python
@pytest.mark.unit
def test_enum_values():
    """Fast unit test."""
    pass

@pytest.mark.integration
def test_database_constraint(db_session):
    """Integration test with database."""
    pass

@pytest.mark.e2e
def test_user_journey(client, db_session):
    """End-to-end user workflow."""
    pass

```

**Available markers:**

- `unit` - Fast tests without external dependencies
- `integration` - Tests with database or HTTP
- `e2e` - End-to-end user workflows

---

## 🚀 Running Tests

### Run by test type

```bash
# Run only unit tests (fast, for development)
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only e2e tests
pytest -m e2e

```

### Run by folder

```bash
# Run all unit tests
pytest tests/unit

# Run all integration tests
pytest tests/integration

# Run all e2e tests
pytest tests/e2e

# Run all tests
pytest tests
```

### Run by module

```bash
# Run unit tests for models only
pytest tests/unit/models

# Run specific integration test
pytest tests/integration/test_migrations.py

# Run specific test function
pytest tests/integration/test_migrations.py::test_all_tables_exist
```

### Combine filters

```bash
# Run unit tests matching pattern
pytest tests/unit -k "recipe"

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html
```

---

## 📝 Naming Conventions

### Test Files

- **Unit:** `test_{module_name}.py` (mirrors source file)
  - `test_recipe.py`, `test_ingredient.py`
- **Integration:** `test_{what_being_tested}.py` (describes integration)
  - `test_migrations.py`, `test_recipe_api.py`, `test_foreign_keys.py`
- **E2E:** `test_{journey_name}.py` (describes user flow)
  - `test_meal_planning_journey.py`, `test_recipe_flow.py`

### Test Functions

Use descriptive names that explain what is being tested:

```python
# Good ✅
def test_recipe_cascade_delete_removes_ingredients(db_session):
    """Deleting recipe should cascade delete recipe_ingredients."""

def test_ingredient_name_must_be_unique(db_session):
    """Database should enforce unique constraint on ingredient name."""

# Bad ❌
def test_recipe():
    """Too vague."""

def test_1():
    """Meaningless."""
```

### Test Classes

Optional, use to group related tests:

```python
class TestRecipeMigration:
    """Tests for recipe table schema."""

    def test_table_exists(self):
        pass

    def test_columns_correct(self):
        pass

class TestRecipeCascade:
    """Tests for recipe deletion cascade behavior."""

    def test_cascade_to_ingredients(self):
        pass

    def test_cascade_to_meal_plans(self):
        pass
```

---

## 🔧 Fixtures

### Fixture Scope

Fixtures are organized by scope and location:

#### Root Level (`tests/conftest.py`)

**Session-scoped:** Database engine, test database setup

```python
@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine once per test session."""
```

**Function-scoped:** Database session with transaction rollback

```python
@pytest.fixture(scope="function")
def db_session(test_engine):
    """Fresh database session for each test with rollback."""
```

#### Unit Level (`tests/unit/conftest.py`)

**Unit-specific fixtures:** Mocks, stubs, sample data (no DB)

```python
@pytest.fixture
def sample_recipe_data():
    """Sample recipe data dictionary."""
    return {"name": "Pasta", "servings": 4}
```

#### Integration Level (`tests/integration/conftest.py`)

**Integration fixtures:** Sample database records, test client

```python
@pytest.fixture
def sample_category(db_session):
    """Create sample category in database."""
    category = Category(name="Dairy")
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def test_client():
    """FastAPI test client."""
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)
```

#### Shared Fixtures (`tests/fixtures/factories.py`)

**Factory functions:** Reusable data creators

```python
def create_recipe(db_session, **kwargs):
    """Factory to create recipe with custom attributes."""
    defaults = {"name": "Test Recipe", "servings": 4}
    defaults.update(kwargs)
    recipe = Recipe(**defaults)
    db_session.add(recipe)
    db_session.commit()
    return recipe
```

---

## 📊 Coverage Goals

### Target Coverage

- **Overall:** 90-95%
- **Critical paths:** 100% (FK behaviors, constraints, relationships)
- **Unit tests:** High coverage (>95%)
- **Integration tests:** Focus on integration points
- **E2E tests:** Critical user journeys

### What to test at 100%

- ✅ All foreign key behaviors (CASCADE, RESTRICT, SET NULL)
- ✅ All unique constraints
- ✅ All relationship navigations
- ✅ Enum validation
- ✅ Critical business logic

### What NOT to prioritize

- ❌ Simple getters/setters
- ❌ `__repr__` methods
- ❌ Framework code (SQLAlchemy ORM internals)
- ❌ Auto-generated code

---

## ✅ Best Practices

### DO:

- ✅ Write tests that are **independent** (no shared state)
- ✅ Use **descriptive test names** that explain intent
- ✅ Keep tests **focused** (one assertion per concept)
- ✅ Use **fixtures** for reusable setup
- ✅ Use **markers** to categorize tests
- ✅ Test **edge cases** and **error conditions**
- ✅ Write tests **before** or **alongside** code (TDD)

### DON'T:

- ❌ Create test dependencies (test2 depends on test1)
- ❌ Use shared mutable state across tests
- ❌ Write tests without assertions
- ❌ Test implementation details (test behavior, not internals)
- ❌ Copy-paste test code (use fixtures/factories)
- ❌ Skip cleanup (use transaction rollback)
- ❌ Commit failing tests

---

## 🗄️ Database Testing

### Test Database Setup

1. **Create test database:**

   ```bash
   docker exec meal-mind-db-1 psql -U postgres -c "CREATE DATABASE mealmind_test;"
   ```

2. **Run migrations on test DB:**

   ```bash
   DATABASE_URL=postgresql://postgres:postgres@localhost:54322/mealmind_test uv run alembic upgrade head
   ```

3. **Tests use transaction rollback:**
   Each test runs in a transaction that rolls back, keeping the database clean.

### Transaction Rollback Pattern

```python
@pytest.fixture(scope="function")
def db_session(test_engine):
    """Provide a database session with automatic rollback."""
    connection = test_engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

---

## 🎓 Examples

### Unit Test Example

```python
# tests/unit/models/test_enums.py

import pytest
from models.enums import MealType

@pytest.mark.unit
class TestMealTypeEnum:
    """Unit tests for MealType enum."""

    def test_lunch_value(self):
        """MealType.LUNCH has correct string value."""
        assert MealType.LUNCH.value == "lunch"

    def test_dinner_value(self):
        """MealType.DINNER has correct string value."""
        assert MealType.DINNER.value == "dinner"

    def test_invalid_value_raises_error(self):
        """Creating MealType with invalid value raises ValueError."""
        with pytest.raises(ValueError):
            MealType("breakfast")
```

### Integration Test Example

```python
# tests/integration/test_constraints.py

import pytest
from sqlalchemy.exc import IntegrityError
from models.category import Category
from models.brand import Brand
from models.ingredient import Ingredient

@pytest.mark.integration
class TestUniqueConstraints:
    """Integration tests for database unique constraints."""

    @pytest.mark.parametrize(
        "model_class,test_name",
        [
            (Category, "Beverages"),
            (Brand, "Coca-Cola"),
            (Ingredient, "Sugar"),
        ],
        ids=["category", "brand", "ingredient"],
    )
    def test_unique_name_constraint(self, db_session, model_class, test_name):
        """Test that duplicate names are rejected."""
        # Create first instance successfully
        first = model_class(name=test_name)
        db_session.add(first)
        db_session.commit()

        # Try to create duplicate - should fail
        duplicate = model_class(name=test_name)
        db_session.add(duplicate)

        with pytest.raises(IntegrityError):
            db_session.commit()
```

### E2E Test Example

```python
# tests/e2e/test_meal_planning_journey.py

import pytest
from datetime import date, timedelta

@pytest.mark.e2e
def test_complete_meal_planning_flow(client, db_session):
    """User can create recipe, plan meal, and view grocery list."""

    # Step 1: Create recipe
    response = client.post("/api/recipes", json={
        "name": "Pasta Carbonara",
        "servings": 4,
        "ingredients": [
            {"name": "Pasta", "quantity": 400, "unit": "g"},
            {"name": "Eggs", "quantity": 4, "unit": "whole"}
        ]
    })
    assert response.status_code == 201
    recipe_id = response.json()["id"]

    # Step 2: Plan the recipe
    response = client.post("/api/meal-plans", json={
        "recipe_id": recipe_id,
        "planned_date": str(date.today() + timedelta(days=1)),
        "meal_type": "DINNER"
    })
    assert response.status_code == 201

    # Step 3: Generate grocery list
    response = client.get("/api/grocery-list")
    assert response.status_code == 200

    grocery_list = response.json()
    assert len(grocery_list["items"]) == 2
    assert any(item["name"] == "Pasta" for item in grocery_list["items"])
```

---

## 🔄 Continuous Integration

Tests are automatically run in CI/CD pipeline:

```yaml
# .github/workflows/test.yml
- name: Run unit tests
  run: pytest -m unit --cov

- name: Run integration tests
  run: pytest -m integration

- name: Run e2e tests
  run: pytest -m e2e
```

---

## 📚 Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Markers](https://docs.pytest.org/en/stable/how-to/mark.html)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

---

## 🆘 Troubleshooting

### Database state issues

- Ensure transaction rollback is working in fixtures
- Check that tests are independent (no shared state)
- Verify test database is clean: recreate if needed

### Import errors

- Ensure PYTHONPATH includes project root
- Check that `__init__.py` files exist in test folders
- Verify virtual environment is activated

### Fixture not found

- Check fixture scope (session vs function)
- Ensure `conftest.py` is in correct location
- Verify fixture name matches usage

---

**Last Updated:** October 7, 2025  
**Maintained by:** MealMind Development Team
