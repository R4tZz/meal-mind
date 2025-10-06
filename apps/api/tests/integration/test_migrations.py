"""
Integration tests for Alembic database migrations.

These tests verify that the database schema created by Alembic migrations
matches our expectations.
"""

import pytest
from .schema_definitions import EXPECTED_TABLES, ALL_SCHEMAS


@pytest.mark.integration
class TestDatabaseMigrations:
    """Integration tests for Alembic database migrations."""

    def _get_column_names(self, columns):
        """Extract column names from column info."""
        return {col["name"] for col in columns}

    def _get_column_dict(self, columns):
        """Convert column list to dict for easy lookup."""
        return {col["name"]: col for col in columns}

    def test_all_tables_exist(self, db_inspector):
        """Verify all expected tables were created by migrations."""
        tables = db_inspector.get_table_names()
        assert EXPECTED_TABLES.issubset(set(tables)), (
            f"Missing tables: {EXPECTED_TABLES - set(tables)}"
        )

    @pytest.mark.parametrize(
        "table_name,expected_schema",
        [
            ("recipes", ALL_SCHEMAS["recipes"]),
            ("categories", ALL_SCHEMAS["categories"]),
            ("brands", ALL_SCHEMAS["brands"]),
            ("ingredients", ALL_SCHEMAS["ingredients"]),
            ("recipe_ingredients", ALL_SCHEMAS["recipe_ingredients"]),
            ("meal_plans", ALL_SCHEMAS["meal_plans"]),
        ],
        ids=[
            "recipes",
            "categories",
            "brands",
            "ingredients",
            "recipe_ingredients",
            "meal_plans",
        ],
    )
    def test_table_schema(self, db_inspector, table_name, expected_schema):
        """Verify table has correct columns and constraints."""
        columns = db_inspector.get_columns(table_name)
        column_names = self._get_column_names(columns)
        column_dict = self._get_column_dict(columns)

        # Check all expected columns exist
        assert column_names == expected_schema["columns"], (
            f"Unexpected columns in {table_name} table: {column_names - expected_schema['columns']}"
        )

        # Check NOT NULL constraints (verify actual nullable property)
        for col_name in expected_schema["not_null"]:
            assert column_dict[col_name]["nullable"] is False, (
                f"Column '{col_name}' should be NOT NULL but allows NULL"
            )
