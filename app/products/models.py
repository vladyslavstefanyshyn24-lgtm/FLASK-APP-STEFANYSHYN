from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, String, Float, ForeignKey,
    Boolean, DateTime, text
)
from datetime import datetime
from typing import List


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="category", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("1")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id'), nullable=True
    )
    category: Mapped["Category"] = relationship(
        "Category", back_populates="products"
    )

    def __repr__(self) -> str:
        return f"<Product {self.name} - ${self.price}>"