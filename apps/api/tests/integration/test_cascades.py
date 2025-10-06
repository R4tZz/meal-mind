"""
Integration tests for cascade behaviors.

These tests verify that database cascade behaviors (CASCADE, SET NULL)
work correctly when deleting parent records.
"""

import pytest
from datetime import date
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.recipe_ingredient import RecipeIngredient
from models.category import Category
from models.brand import Brand
from models.meal_plan import MealPlan, MealType


@pytest.mark.integration
class TestCascadeBehavior:
    """Test database cascade behaviors on delete."""

    def test_delete_recipe_cascades_to_recipe_ingredients(self, db_session):
        """Test deleting recipe also deletes its recipe_ingredients (CASCADE DELETE)."""
        recipe = Recipe(name="Pasta Carbonara")
        ingredient = Ingredient(name="Eggs")
        db_session.add_all([recipe, ingredient])
        db_session.commit()

        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=2,
        )
        db_session.add(recipe_ingredient)
        db_session.commit()

        recipe_ingredient_id = recipe_ingredient.id
        ingredient_id = ingredient.id

        # Delete recipe triggers CASCADE
        db_session.delete(recipe)
        db_session.commit()

        # RecipeIngredient should be deleted
        assert db_session.get(RecipeIngredient, recipe_ingredient_id) is None
        # Ingredient should survive
        assert db_session.get(Ingredient, ingredient_id) is not None

    def test_delete_recipe_sets_meal_plan_recipe_id_to_null(self, db_session):
        """Test deleting recipe sets meal_plan.recipe_id to NULL (SET NULL)."""
        recipe = Recipe(name="Pasta Carbonara")
        db_session.add(recipe)
        db_session.commit()

        meal_plan = MealPlan(
            recipe_id=recipe.id,
            planned_date=date.today(),
            meal_type=MealType.LUNCH,
        )
        db_session.add(meal_plan)
        db_session.commit()

        meal_plan_id = meal_plan.id

        # Delete recipe triggers SET NULL
        db_session.delete(recipe)
        db_session.commit()

        # MealPlan should survive with recipe_id set to NULL
        surviving_meal_plan = db_session.get(MealPlan, meal_plan_id)
        assert surviving_meal_plan is not None
        db_session.refresh(surviving_meal_plan)
        assert surviving_meal_plan.recipe_id is None

    def test_delete_category_sets_ingredient_category_to_null(self, db_session):
        """Test deleting category sets ingredient.category_id to NULL (SET NULL)."""
        category = Category(name="Dairy")
        ingredient = Ingredient(name="Milk", category_id=category.id)
        db_session.add_all([category, ingredient])
        db_session.commit()

        # Delete category triggers SET NULL
        db_session.delete(category)
        db_session.commit()

        # Ingredient should survive with category_id set to NULL
        db_session.refresh(ingredient)
        assert ingredient.category_id is None

    def test_delete_brand_sets_ingredient_brand_to_null(self, db_session):
        """Test deleting brand sets ingredient.brand_id to NULL (SET NULL)."""
        brand = Brand(name="Morton")
        ingredient = Ingredient(name="Sea Salt", brand_id=brand.id)
        db_session.add_all([brand, ingredient])
        db_session.commit()

        # Delete brand triggers SET NULL
        db_session.delete(brand)
        db_session.commit()

        # Ingredient should survive with brand_id set to NULL
        db_session.refresh(ingredient)
        assert ingredient.brand_id is None
