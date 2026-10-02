"""
Broker/Exchange Connector Framework.

Provides a unified interface for connecting to trading brokers and exchanges,
supporting both REST API connectors (Binance, Bybit, OKX, Alpaca) and
FIX protocol connectors.

ADR-003: Each connector is a thin adapter over the exchange/broker SDK.
ADR-004: Business logic (position sizing, risk checks) resides in domain services.

Usage::

    manager = ConnectorManager()
    binance = manager.get_connector("binance")
    account = await binance.fetch_account()
    order = await binance.place_order(symbol="BTCUSDT", side="BUY", amount=0.001)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

logger = logging.getLogger(__name__)


class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"


class OrderStatus(StrEnum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class TimeInForce(StrEnum):
    GDC = "GDC"
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


class ExchangeType(StrEnum):
    BINANCE = "binance"
    BYBIT = "bybit"
    OKX = "okx"
    ALPACA = "alpaca"
    FIX = "fix"
    PAPER = "paper"


@dataclass
class Instrument:
    symbol: str
    exchange: str
    asset: str
    quote_currency: str
    min_qty: float = 0.0
    max_qty: float | None = None
    step_size: float = 0.0000001
    tick_size: float = 0.01
    status: str = "TRADING"


@dataclass
class OrderRequest:
    symbol: str
    side: OrderSide
    order_type: OrderType
    amount: float
    price: float | None = None
    time_in_force: TimeInForce = TimeInForce.GTC
    client_order_id: str | None = None
    reduce_only: bool = False
    trailing_offset: float | None = None


@dataclass
class OrderResponse:
    order_id: str
    client_order_id: str | None
    symbol: str
    side: OrderSide
    order_type: OrderType
    amount: float
    filled: float
    remaining: float
    price: float | None
    average_fill_price: float | None
    status: OrderStatus
    timestamp: datetime
    fee: float = 0.0
    fee_currency: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "client_order_id": self.client_order_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "type": self.order_type.value,
            "amount": self.amount,
            "filled": self.filled,
            "remaining": self.remaining,
            "price": self.price,
            "average_fill_price": self.average_fill_price,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "fee": self.fee,
            "fee_currency": self.fee_currency,
        }


@dataclass
class Position:
    symbol: str
    exchange: str
    quantity: float
    entry_price: float
    mark_price: float
    unrealized_pnl: float
    realized_pnl: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Balance:
    asset: str
    free: float
    locked: float
    usd_value: float = 0.0


@dataclass
class ExchangeInfo:
    exchange: str
    type: ExchangeType
    connected: bool
    authenticated: bool
    server_time: datetime | None = None
    rate_limit: dict[str, Any] = field(default_factory=dict)


class ConnectorError(Exception):
    """Base exception for connector operations."""


class ConnectorNotConfiguredError(ConnectorError):
    """Raised when connector credentials are not configured."""


class BaseConnector:
    """
    Abstract base class for broker/exchange connectors.

    All connectors must implement:
        - connect() / disconnect()
        - fetch_account() -> dict[str, Any]
        - place_order(OrderRequest) -> OrderResponse
        - cancel_order(order_id) -> bool
        - fetch_orders(symbol) -> list[OrderResponse]
        - fetch_positions() -> list[Position]
        - fetch_balances() -> list[Balance]
        - fetch_instruments() -> list[Instrument]
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        api_passphrase: str | None = None,
        testnet: bool = True,
        exchange_type: ExchangeType = ExchangeType.PAPER,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.testnet = testnet
        self.exchange_type = exchange_type
        self._connected = False
        self._authenticated = False

    async def connect(self) -> None:
        """Initialize the connector. Must be called before use."""
        raise NotImplementedError

    async def disconnect(self) -> None:
        """Clean up resources."""
        self._connected = False
        self._authenticated = False

    async def fetch_account(self) -> dict[str, Any]:
        """Fetch account information."""
        raise NotImplementedError

    async def place_order(self, request: OrderRequest) -> OrderResponse:
        """Place an order on the exchange."""
        raise NotImplementedError

    async def cancel_order(self, order_id: str, symbol: str | None = None) -> bool:
        """Cancel an existing order."""
        raise NotImplementedError

    async def fetch_orders(
        self,
        symbol: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[OrderResponse]:
        """Fetch order history."""
        raise NotImplementedError

    async def fetch_positions(self, symbols: list[str] | None = None) -> list[Position]:
        """Fetch open positions."""
        raise NotImplementedError

    async def fetch_balances(self) -> list[Balance]:
        """Fetch account balances."""
        raise NotImplementedError

    async def fetch_instruments(self) -> list[Instrument]:
        """Fetch available trading instruments."""
        raise NotImplementedError

    async def get_info(self) -> ExchangeInfo:
        """Get exchange connection information."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _validate_order(self, request: OrderRequest) -> None:
        """Validate order request fields."""
        if request.amount <= 0:
            raise ConnectorError(f"Amount must be positive, got {request.amount}")
        if request.order_type == OrderType.LIMIT and request.price is None:
            raise ConnectorError("LIMIT order requires a price")
        if request.order_type == OrderType.MARKET and request.price is not None:
            logger.debug("Market order price will be ignored")

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def authenticated(self) -> bool:
        return self._authenticated


class PaperTradingConnector(BaseConnector):
    """
    Paper-trading connector for simulation and testing.

    Maintains an in-memory order book and position tracker.
    No real money or external API calls are made.
    """

    def __init__(self) -> None:
        super().__init__(exchange_type=ExchangeType.PAPER)
        self._orders: dict[str, OrderResponse] = {}
        self._positions: dict[str, Position] = {}
        self._balances: dict[str, Balance] = {}
        self._instruments: list[Instrument] = []
        self._order_counter: int = 0
        self._server_time: datetime | None = None

    async def connect(self) -> None:
        self._connected = True
        self._authenticated = True
        self._server_time = datetime.now(UTC)
        self._instrument_cache = [
            Instrument(symbol="BTCUSDT", exchange="paper", asset="BTC", quote_currency="USDT"),
            Instrument(symbol="ETHUSDT", exchange="paper", asset="ETH", quote_currency="USDT"),
            Instrument(symbol="SOLUSDT", exchange="paper", asset="SOL", quote_currency="USDT"),
        ]
        logger.info("Paper trading connector connected")

    async def fetch_account(self) -> dict[str, Any]:
        return {
            "exchange": "paper",
            "account_id": "paper-001",
            "status": "active",
            "can_trade": True,
            "can_withdraw": True,
            "permissions": ["trade", "withdraw", "read"],
        }

    async def place_order(self, request: OrderRequest) -> OrderResponse:
        self._validate_order(request)
        self._order_counter += 1
        order_id = f"paper-{self._order_counter:08d}"
        ts = datetime.now(UTC)

        if request.order_type == OrderType.MARKET:
            filled = request.amount
            avg_price = request.price or 100.0
        else:
            filled = request.amount
            avg_price = request.price or 100.0

        order = OrderResponse(
            order_id=order_id,
            client_order_id=request.client_order_id,
            symbol=request.symbol,
            side=request.side,
            order_type=request.order_type,
            amount=request.amount,
            filled=filled,
            remaining=request.amount - filled,
            price=request.price,
            average_fill_price=avg_price,
            status=OrderStatus.FILLED if filled == request.amount else OrderStatus.PARTIALLY_FILLED,
            timestamp=ts,
            fee=filled * 0.001,
            fee_currency=request.symbol[:3],
            raw={},
        )
        self._orders[order_id] = order

        # Update position
        pos = self._positions.get(request.symbol)
        if pos:
            if request.side == OrderSide.BUY:
                pos.quantity += filled
                pos.entry_price = (pos.entry_price * (pos.quantity - filled) + avg_price * filled) / pos.quantity  # noqa: E501
                pos.unrealized_pnl = 0.0
            else:
                pos.quantity -= filled
                pos.unrealized_pnl = 0.0
        else:
            qty = filled if request.side == OrderSide.BUY else -filled
            self._positions[request.symbol] = Position(
                symbol=request.symbol,
                exchange="paper",
                quantity=qty,
                entry_price=avg_price,
                mark_price=avg_price,
                unrealized_pnl=0.0,
                realized_pnl=0.0,
            )

        return order

    async def cancel_order(self, order_id: str, symbol: str | None = None) -> bool:
        order = self._orders.get(order_id)
        if order and order.status in (OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED):
            order.status = OrderStatus.CANCELED
            return True
        return False

    async def fetch_orders(
        self,
        symbol: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[OrderResponse]:
        orders = list(self._orders.values())
        if symbol:
            orders = [o for o in orders if o.symbol == symbol]
        if status:
            orders = [o for o in orders if o.status.value == status]
        return sorted(orders, key=lambda o: o.timestamp, reverse=True)[:limit]

    async def fetch_positions(self, symbols: list[str] | None = None) -> list[Position]:
        positions = list(self._positions.values())
        if symbols:
            positions = [p for p in positions if p.symbol in symbols]
        return positions

    async def fetch_balances(self) -> list[Balance]:
        return list(self._balances.values())

    async def fetch_instruments(self) -> list[Instrument]:
        return self._instrument_cache

    async def get_info(self) -> ExchangeInfo:
        return ExchangeInfo(
            exchange="paper",
            type=self.exchange_type,
            connected=self._connected,
            authenticated=self._authenticated,
            server_time=self._server_time,
            rate_limit={"requests_per_minute": 0},
        )


class ConnectorManager:
    """
    Manages broker/exchange connectors.

    Usage::

        manager = ConnectorManager()
        connector = await manager.get_connector("binance")
    """

    _connectors: dict[str, BaseConnector] = {}

    def __init__(self) -> None:
        self._connectors: dict[str, BaseConnector] = {}

    def register(self, exchange: str, connector: BaseConnector) -> None:
        self._connectors[exchange.lower()] = connector

    async def get_connector(self, exchange: str) -> BaseConnector:
        key = exchange.lower()
        if key in self._connectors:
            return self._connectors[key]
        return await self._create_connector(exchange)

    async def _create_connector(self, exchange: str) -> BaseConnector:
        key = exchange.lower()
        if key in ("paper", "simulation", "mock"):
            connector: BaseConnector = PaperTradingConnector()
            self._connectors[key] = connector
            return connector

        if key in ("binance", "bybit", "okx", "alpaca"):
            return await self._load_exchange_connector(key)

        if key in ("fix", "fixtrading"):
            from backend.app.connectors.fix_connector import FIXConnector

            connector = FIXConnector()
            self._connectors[key] = connector
            return connector

        raise ConnectorError(f"Unknown exchange type: {exchange}")

    async def _load_exchange_connector(self, exchange: str) -> BaseConnector:
        """
        Dynamically load a REST API exchange connector.

        These connectors require API credentials and use ccxt or similar
        libraries. They are loaded lazily to avoid hard dependencies.
        """
        try:
            mod = __import__(f"backend.app.connectors.{exchange}_connector", fromlist=[""])
            connector_cls = getattr(mod, f"{exchange.capitalize()}Connector")
            connector = connector_cls(exchange_type=ExchangeType(exchange))
            self._connectors[exchange] = connector
            return connector
        except ImportError as e:
            raise ConnectorError(
                f"Exchange connector '{exchange}' not installed. "
                f"Install the required SDK or use 'paper' for simulation."
            ) from e

    async def list_connectors(self) -> list[dict[str, Any]]:
        results = []
        for name, connector in self._connectors.items():
            info = await connector.get_info()
            results.append({
                "exchange": name,
                "type": info.type.value,
                "connected": info.connected,
                "authenticated": info.authenticated,
            })
        return results

    async def close_all(self) -> None:
        for connector in self._connectors.values():
            try:
                await connector.disconnect()
            except Exception as e:
                logger.warning(f"Error disconnecting {connector}: {e}")
        self._connectors.clear()


from backend.app.connectors.base_action import (  # noqa: E402
    ActionConnectorError,
    ActionConnectorManager,
    ActionRequest,
    ActionResult,
    ActionType,
    BaseActionConnector,
    action_connector_manager,
    safe_path,
)

__all__ = [
    "connector_manager",
    "ConnectorManager",
    "BaseConnector",
    "PaperTradingConnector",
    "FIXConnector",
    "Instrument",
    "OrderRequest",
    "OrderResponse",
    "Position",
    "Balance",
    "ExchangeInfo",
    "OrderSide",
    "OrderType",
    "OrderStatus",
    "TimeInForce",
    "ExchangeType",
    "ConnectorError",
    "ConnectorNotConfiguredError",
    "action_connector_manager",
    "ActionConnectorManager",
    "BaseActionConnector",
    "ActionResult",
    "ActionRequest",
    "ActionType",
    "ActionConnectorError",
    "safe_path",
]
