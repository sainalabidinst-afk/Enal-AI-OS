"""
DDD Order Management
=====================

Domain-Driven Design implementation for order management.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class OrderId:
    """Value Object for Order identity."""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Order ID cannot be empty")


@dataclass(frozen=True)
class Money:
    """Value Object for monetary values."""
    amount: Decimal
    currency: str
    
    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")


class OrderItem:
    """Entity representing an order line item."""
    
    def __init__(self, product_id: str, quantity: int, price: Money):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
    
    def total(self) -> Money:
        return Money(self.price.amount * self.quantity, self.price.currency)


class Order:
    """Aggregate Root for Order."""
    
    def __init__(self, order_id: OrderId, customer_id: str):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = "pending"
        self.created_at = datetime.utcnow()
        self._events = []
    
    def add_item(self, item: OrderItem) -> None:
        """Add item to order - business rule enforcement."""
        if self.status != "pending":
            raise ValueError("Cannot add items to confirmed order")
        self.items.append(item)
        self._events.append(OrderItemAdded(self.order_id, item))
    
    def remove_item(self, product_id: str) -> None:
        """Remove item from order."""
        if self.status != "pending":
            raise ValueError("Cannot remove items from confirmed order")
        self.items = [item for item in self.items if item.product_id != product_id]
    
    def confirm(self) -> None:
        """Confirm the order."""
        if not self.items:
            raise ValueError("Cannot confirm empty order")
        if self.status != "pending":
            raise ValueError("Order already confirmed")
        self.status = "confirmed"
        self._events.append(OrderConfirmed(self.order_id))
    
    def total_amount(self) -> Money:
        """Calculate total order amount."""
        if not self.items:
            return Money(Decimal("0"), "USD")
        return sum(item.total() for item in self.items)
    
    def domain_events(self) -> List["DomainEvent"]:
        """Return and clear domain events."""
        events = self._events.copy()
        self._events.clear()
        return events


class OrderItemAdded:
    """Domain Event: Item added to order."""
    
    def __init__(self, order_id: OrderId, item: OrderItem):
        self.order_id = order_id
        self.item = item
        self.occurred_at = datetime.utcnow()


class OrderConfirmed:
    """Domain Event: Order confirmed."""
    
    def __init__(self, order_id: OrderId):
        self.order_id = order_id
        self.occurred_at = datetime.utcnow()


class OrderRepository:
    """Repository interface for Order aggregate."""
    
    def save(self, order: Order) -> None:
        raise NotImplementedError()
    
    def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        raise NotImplementedError()
    
    def find_by_customer(self, customer_id: str) -> List[Order]:
        raise NotImplementedError()


class AntiCorruptionLayer:
    """Translates between external order systems and internal domain model."""
    
    def external_to_order(self, external_data: dict) -> Order:
        """Translate external system order to internal Order aggregate."""
        order_id = OrderId(external_data["order_number"])
        order = Order(order_id, external_data["customer_ref"])
        
        for item_data in external_data.get("line_items", []):
            item = OrderItem(
                product_id=item_data["sku"],
                quantity=item_data["qty"],
                price=Money(item_data["unit_price"], item_data["currency"])
            )
            order.add_item(item)
        
        return order
