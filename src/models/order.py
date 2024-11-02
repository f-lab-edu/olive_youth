from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlmodel import Field, Relationship, SQLModel


class OrderStatusType(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_no: str = Field(sa_column=Column(String(100), nullable=False))
    user_id: int = Field(foreign_key="users.id")

    # 배송 정보
    recipient_name: str = Field(sa_column=Column(String(50), nullable=False))
    contact_number: str = Field(sa_column=Column(String(20), nullable=False))
    delivery_address: str = Field(sa_column=Column(String(200), nullable=False))
    delivery_message: str = Field(sa_column=Column(String(100), nullable=True))

    total_price: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: OrderStatusType = Field(
        sa_column=Column(SqlEnum(OrderStatusType), nullable=False)
    )

    user: "User" = Relationship(back_populates="orders")
    order_items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int
    price: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    order: "Order" = Relationship(back_populates="order_items")
    product: "Product" = Relationship(back_populates="order_items")
