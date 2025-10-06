from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from models.base import Base

if TYPE_CHECKING:
    from models.brand import Brand
    from models.category import Category
    from models.recipe_ingredient import RecipeIngredient


class Ingredient(Base):
    """Ingredient model - master catalog of reusable ingredients"""

    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(200), nullable=False, index=True, unique=True
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    brand_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("brands.id"), nullable=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), server_default=func.now(), onupdate=func.now()
    )
    category: Mapped[Optional["Category"]] = relationship(back_populates="ingredients")
    brand: Mapped[Optional["Brand"]] = relationship(back_populates="ingredients")
    recipe_ingredients: Mapped[List["RecipeIngredient"]] = relationship(
        back_populates="ingredient"
    )
