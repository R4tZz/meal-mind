from enum import Enum


class MealType(str, Enum):
    """Meal type enumeration."""

    LUNCH = "lunch"
    DINNER = "dinner"
