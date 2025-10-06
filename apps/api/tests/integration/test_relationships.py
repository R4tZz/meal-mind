"""
Integration tests for SQLAlchemy relationships.

These tests verify that model relationships are properly configured
and work bidirectionally.
"""

import pytest
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.recipe_ingredient import RecipeIngredient
from models.category import Category
from models.brand import Brand
from models.meal_plan import MealPlan
from models.meal_plan import MealType
from datetime import date


@pytest.mark.integration
class TestRelationships:
    """Test SQLAlchemy model relationships."""

    def test_recipe_ingredients_relationship(self, db_session):
        """Test recipe can access its ingredients through relationship."""
        # Create a recipe
        recipe = Recipe(name="Pasta Carbonara")
        db_session.add(recipe)
        db_session.commit()

        # Create an ingredient
        ingredient = Ingredient(name="Eggs")
        db_session.add(ingredient)
        db_session.commit()

        # Link them through recipe_ingredient
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=2,
        )
        db_session.add(recipe_ingredient)
        db_session.commit()

        # Test the relationship works
        assert len(recipe.recipe_ingredients) == 1
        assert recipe.recipe_ingredients[0].ingredient.name == "Eggs"
        assert recipe.recipe_ingredients[0].quantity == 2

    def test_ingredient_recipes_relationship(self, db_session):
        """Test ingredient can access recipes that use it."""

        # Create an ingredient
        ingredient = Ingredient(name="Eggs")
        db_session.add(ingredient)
        db_session.commit()

        # Create a recipe
        recipe = Recipe(name="Pasta Carbonara")
        db_session.add(recipe)
        db_session.commit()

        # Link them
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=2,
        )
        db_session.add(recipe_ingredient)
        db_session.commit()

        # Test the reverse relationship
        assert len(ingredient.recipe_ingredients) == 1
        assert ingredient.recipe_ingredients[0].recipe.name == "Pasta Carbonara"
        assert ingredient.recipe_ingredients[0].quantity == 2

    def test_category_ingredients_relationship(self, db_session):
        """Test category can access its ingredients."""
        # Create a category
        category = Category(name="Dairy")
        db_session.add(category)
        db_session.commit()

        # Create multiple ingredients with that category_id
        milk = Ingredient(name="Milk", category_id=category.id)
        cheese = Ingredient(name="Cheese", category_id=category.id)
        db_session.add_all([milk, cheese])
        db_session.commit()

        # Verify: category.ingredients returns all of them
        assert len(category.ingredients) == 2
        ingredient_names = {ing.name for ing in category.ingredients}
        assert ingredient_names == {"Milk", "Cheese"}

    def test_optional_brand_relationship(self, db_session):
        """Test ingredient can exist without a brand."""
        # Test 1: Ingredient without brand
        ingredient_no_brand = Ingredient(name="Salt")
        db_session.add(ingredient_no_brand)
        db_session.commit()

        # Verify it works and ingredient.brand is None
        assert ingredient_no_brand.brand is None

        # Test 2: Ingredient with brand
        brand = Brand(name="Morton")
        db_session.add(brand)
        db_session.commit()

        ingredient_with_brand = Ingredient(name="Sea Salt", brand_id=brand.id)
        db_session.add(ingredient_with_brand)
        db_session.commit()

        # Verify the relationship works when brand is present
        assert ingredient_with_brand.brand is not None
        assert ingredient_with_brand.brand.name == "Morton"

    def test_recipe_meal_plans_relationship(self, db_session):
        """Test recipe can access meal plans that use it."""

        # Create a recipe
        recipe = Recipe(name="Pasta")
        db_session.add(recipe)
        db_session.commit()

        # Create a meal plan using this recipe
        meal_plan = MealPlan(
            recipe_id=recipe.id,
            planned_date=date.today(),
            meal_type=MealType.LUNCH,
        )
        db_session.add(meal_plan)
        db_session.commit()

        # Test relationship
        assert len(recipe.meal_plans) == 1
        assert recipe.meal_plans[0].meal_type == MealType.LUNCH

    def test_ingredient_used_in_multiple_recipes(self, db_session):
        """Test an ingredient can be used in multiple recipes."""
        # Create an ingredient
        ingredient = Ingredient(name="Tomato")
        db_session.add(ingredient)
        db_session.commit()

        # Create multiple recipes
        recipe1 = Recipe(name="Tomato Soup")
        recipe2 = Recipe(name="Pasta with Tomato Sauce")
        db_session.add_all([recipe1, recipe2])
        db_session.commit()

        # Link the ingredient to both recipes
        soup_link = RecipeIngredient(
            recipe_id=recipe1.id, ingredient_id=ingredient.id, quantity=3
        )
        pasta_link = RecipeIngredient(
            recipe_id=recipe2.id, ingredient_id=ingredient.id, quantity=5
        )
        db_session.add_all([soup_link, pasta_link])
        db_session.commit()

        # Verify the ingredient is linked to both recipes
        assert len(ingredient.recipe_ingredients) == 2
        linked_recipe_names = {ri.recipe.name for ri in ingredient.recipe_ingredients}
        assert linked_recipe_names == {"Tomato Soup", "Pasta with Tomato Sauce"}
