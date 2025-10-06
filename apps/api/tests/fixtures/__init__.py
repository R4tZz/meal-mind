"""
Shared test fixtures and factories.

This module contains reusable test data creation utilities:
- factories.py - Factory functions for creating test database records

Factory functions follow the pattern:
    def create_<model>(db_session, **kwargs):
        # Create and return model instance with sensible defaults
        # Override defaults with kwargs

Example usage:
    recipe = create_recipe(db_session, name="Custom Name")
    category = create_category(db_session)
"""
