"""
Integration tests for database constraints.

These tests verify that database constraints (UNIQUE, foreign keys, etc.)
are properly enforced by the database.
"""

import pytest
from sqlalchemy.exc import IntegrityError
from datetime import date
from models.meal_plan import MealType
from models.category import Category
from models.brand import Brand
from models.ingredient import Ingredient
from models.recipe_ingredient import RecipeIngredient
from models.recipe import Recipe
from models.meal_plan import MealPlan


# Test constants
INVALID_FK_ID = 99999  # Intentionally invalid ID for FK constraint tests


@pytest.mark.integration
class TestUniqueConstraints:
    """Test UNIQUE constraints are enforced."""

    @pytest.mark.parametrize(
        "model_class, test_name",
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


@pytest.mark.integration
class TestForeignKeyConstraints:
    """Test foreign key constraints are enforced."""

    def test_recipe_ingredient_foreign_keys(self, db_session):
        """Test recipe_id and ingredient_id FKs are enforced."""

        # Test 1: Invalid recipe_id
        ingredient = Ingredient(name="Sugar")
        db_session.add(ingredient)
        db_session.commit()

        with pytest.raises(IntegrityError, match="violates foreign key constraint"):
            recipe_ingredient = RecipeIngredient(
                recipe_id=INVALID_FK_ID,
                ingredient_id=ingredient.id,
                quantity=1,
            )
            db_session.add(recipe_ingredient)
            db_session.commit()

        db_session.rollback()

        # Test 2: Invalid ingredient_id
        recipe = Recipe(name="Pasta")
        db_session.add(recipe)
        db_session.commit()

        with pytest.raises(IntegrityError, match="violates foreign key constraint"):
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=INVALID_FK_ID,
                quantity=1,
            )
            db_session.add(recipe_ingredient)
            db_session.commit()

    def test_ingredient_foreign_keys(self, db_session):
        """Test brand_id and category_id FKs are enforced."""
        # Test invalid category_id
        with pytest.raises(IntegrityError, match="violates foreign key constraint"):
            ingredient = Ingredient(name="Test", category_id=INVALID_FK_ID)
            db_session.add(ingredient)
            db_session.commit()

        db_session.rollback()

        # Test invalid brand_id
        with pytest.raises(IntegrityError, match="violates foreign key constraint"):
            ingredient = Ingredient(name="Test", brand_id=INVALID_FK_ID)
            db_session.add(ingredient)
            db_session.commit()

    def test_meal_plan_foreign_keys(self, db_session):
        """Test recipe_id FK is enforced."""
        # Test invalid recipe_id
        with pytest.raises(IntegrityError, match="violates foreign key constraint"):
            meal_plan = MealPlan(
                planned_date=date.today(),
                meal_type=MealType.LUNCH,
                recipe_id=INVALID_FK_ID,
            )
            db_session.add(meal_plan)
            db_session.commit()
