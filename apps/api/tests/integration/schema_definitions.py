"""
Database schema definitions for migration tests.

This file contains the expected schema for all database tables.
Update these when you add/modify migrations.

Organization:
    CORE_TABLES: Main entity tables (recipes, categories, brands, ingredients)
    JUNCTION_TABLES: Many-to-many relationship tables (recipe_ingredients)
    FEATURE_TABLES: Feature-specific tables (meal_plans)
    SYSTEM_TABLES: Framework/system tables (alembic_version)
    
    ALL_SCHEMAS: Dictionary mapping table names to their schemas
"""

# ============================================================================
# TABLE GROUPS
# ============================================================================

CORE_TABLES = {
    "recipes",
    "categories",
    "brands",
    "ingredients",
}

JUNCTION_TABLES = {
    "recipe_ingredients",
}

FEATURE_TABLES = {
    "meal_plans",
}

SYSTEM_TABLES = {
    "alembic_version",
}

# All expected tables (combination of all groups)
EXPECTED_TABLES = CORE_TABLES | JUNCTION_TABLES | FEATURE_TABLES | SYSTEM_TABLES


# ============================================================================
# CORE TABLE SCHEMAS
# ============================================================================

RECIPE_SCHEMA = {
    "columns": {
        "id",
        "name",
        "description",
        "prep_time_minutes",
        "cook_time_minutes",
        "servings",
        "instructions",
        "created_at",
        "updated_at",
    },
    "not_null": {
        "id",
        "name",
    },
}

CATEGORY_SCHEMA = {
    "columns": {"id", "name", "description", "created_at", "updated_at"},
    "not_null": {"id", "name"},
}

BRAND_SCHEMA = {
    "columns": {"id", "name", "description", "created_at", "updated_at"},
    "not_null": {"id", "name"},
}

INGREDIENT_SCHEMA = {
    "columns": {
        "id",
        "name",
        "category_id",
        "brand_id",
        "notes",
        "created_at",
        "updated_at",
    },
    "not_null": {
        "id",
        "name",
    },
}


# ============================================================================
# JUNCTION TABLE SCHEMAS
# ============================================================================

RECIPE_INGREDIENT_SCHEMA = {
    "columns": {
        "id",
        "recipe_id",
        "ingredient_id",
        "quantity",
        "unit",
        "preparation",
        "display_order",
        "is_optional",
        "created_at",
        "updated_at",
    },
    "not_null": {
        "id",
        "recipe_id",
        "ingredient_id",
    },
}


# ============================================================================
# FEATURE TABLE SCHEMAS
# ============================================================================

MEAL_PLAN_SCHEMA = {
    "columns": {
        "id",
        "recipe_id",
        "planned_date",
        "meal_type",
        "notes",
        "created_at",
        "updated_at",
    },
    "not_null": {
        "id",
        "planned_date",
        "meal_type",
    },
}


# ============================================================================
# ALL SCHEMAS DICTIONARY
# ============================================================================
# Maps table names to their schema definitions for easy iteration.
# Useful for parametrized tests and bulk operations.

ALL_SCHEMAS = {
    # Core tables
    "recipes": RECIPE_SCHEMA,
    "categories": CATEGORY_SCHEMA,
    "brands": BRAND_SCHEMA,
    "ingredients": INGREDIENT_SCHEMA,
    # Junction tables
    "recipe_ingredients": RECIPE_INGREDIENT_SCHEMA,
    # Feature tables
    "meal_plans": MEAL_PLAN_SCHEMA,
}
