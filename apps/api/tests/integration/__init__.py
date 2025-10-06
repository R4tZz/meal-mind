"""
Integration tests for MealMind API.

These tests verify that different components work together correctly:
- Database migrations and schema
- Database constraints (UNIQUE, NOT NULL, FK)
- Model relationships and cascade behaviors
- API endpoints with database persistence

Integration tests use the real database (mealmind_test) but with
transaction rollback for isolation between tests.
"""
