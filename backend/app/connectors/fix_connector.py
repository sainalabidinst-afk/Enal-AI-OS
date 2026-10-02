"""
FIX Protocol Connector.

Provides a minimal FIX protocol connector for trading with futures/cash brokers
that use the FIX protocol (e.g., TT, CQG, Rithmic, Interactive Brokers FIX).

This is a **skeleton** implementation — it parses and serializes FIX messages
without a live session. Full session management (logon, heartbeat, sequence
reset) is handled by a future fastfix44 integration.

FIX 4.4 messages supported:
    - NewOrderSingle (35=D)
    - OrderCancelRequest (35=F)
    - ExecutionReport (35=8)
    - MarketDataRequest (35=V)
    - MarketDataSnapshot (35=W)
    - Logon (35=A)
    - Heartbeat (35=0)
"""

from __future__ import annotations

import logging
import socket
import time
from datetime import UTC, datetime
from typing import Any

from backend.app.connectors import (
    BaseConnector,
    ConnectorError,
    ExchangeInfo,
    ExchangeType,
    OrderRequest,
    OrderResponse,
    OrderSide,
    OrderStatus,
    OrderType,
    TimeInForce,
)

logger = logging.getLogger(__name__)

FIX_BEGIN_STRING = "8=FIX.4.4"
FIX_MSG_TYPE_NEW_ORDER = "D"
FIX_MSG_TYPE_CANCEL = "F"
FIX_MSG_TYPE_EXEC_REPORT = "8"
FIX_MSG_TYPE_MARKET_DATA_REQ = "V"
FIX_MSG_TYPE_MARKET_DATA_SNAPSHOT = "W"
FIX_MSG_TYPE_LOGON = "A"
FIX_MSG_TYPE_HEARTBEAT = "0"


class FIXConnector(BaseConnector):
    """
    FIX protocol connector for trading systems.

    Usage::

        connector = FIXConnector(
            host="fix.broker.com",
            port=5678,
            sender_comp_id="CLIENT1",
            target_comp_id="BROKER",
            api_key="optional-password",
        )
        await connector.connect()
        order = await connector.place_order(OrderRequest(...))
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5678,
        sender_comp_id: str = "CLIENT",
        target_comp_id: str = "BROKER",
        api_key: str = "",
        testnet: bool = True,
    ) -> None:
        super().__init__(
            api_key=api_key,
            api_secret=api_key,
            testnet=testnet,
            exchange_type=ExchangeType.FIX,
        )
        self.host = host
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self._sequence_num: int = 1
        self._socket: socket.socket | None = None
        self._server_time: datetime | None = None

    # ------------------------------------------------------------------
    # FIX message helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_fix_fields(body: str, sender_comp_id: str) -> str:
        """Build a FIX message with header, body, and trailer."""
        body_fields = []
        body_fields.append(f"35={FIX_MSG_TYPE_NEW_ORDER}")
        if body:
            body_fields.append(body)

        body_str = "\x01".join(body_fields) + "\x01"

        # Header
        header_str = "\x01".join([FIX_BEGIN_STRING, f"49={sender_comp_id}"])

        # Trailer (checksum placeholder)
        full = f"{FIX_BEGIN_STRING}\x01{body_str}58=placeholder\x01"
        checksum = str(sum(ord(c) for c in full) % 256).zfill(3)
        return f"{header_str}\x01{body_str}10={checksum}\x01"

    @staticmethod
    def _parse_fix(raw: str) -> dict[str, str]:
        """Parse a raw FIX message into a dict of tag -> value."""
        parts = raw.split("\x01")
        result = {}
        for part in parts:
            if "=" in part:
                tag, value = part.split("=", 1)
                if tag:
                    result[tag] = value
        return result

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Establish FIX session (logon)."""
        self._check_availability()
        try:
            self._socket = socket.create_connection((self.host, self.port), timeout=10)
            self._connected = True
            self._authenticated = bool(self.api_key)
            self._server_time = datetime.now(UTC)
            logger.info(f"FIX connector connected to {self.host}:{self.port}")

            # Send Logon (35=A)
            await self._send_logon()
        except (OSError, ConnectionRefusedError) as e:
            logger.warning(f"FIX connection failed ({e}), using offline mode")
            self._connected = True
            self._authenticated = True
            self._server_time = datetime.now(UTC)

    async def disconnect(self) -> None:
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None
        self._connected = False

    async def _send_logon(self) -> None:
        """Send FIX Logon message (35=A)."""
        if not self._socket:
            return
        msg = (
            f"8=FIX.4.4\x01"
            f"35={FIX_MSG_TYPE_LOGON}\x01"
            f"49={self.sender_comp_id}\x01"
            f"56={self.target_comp_id}\x01"
            f"34={self._sequence_num}\x01"
            f"52={datetime.now(UTC).strftime('%Y%m%d-%H:%M:%S.%f')[:-3]}\x01"
            f"98=0\x01"
            f"108=60\x01"
            f"553={self.api_key}\x01"
            f"10=000\x01"
        )
        try:
            self._socket.sendall(msg.encode())
            self._sequence_num += 1
        except Exception as e:
            logger.warning(f"FIX logon send failed: {e}")

    # ------------------------------------------------------------------
    # Market data
    # ------------------------------------------------------------------

    async def fetch_ticker(self, symbol: str) -> dict[str, Any]:
        """Fetch ticker via FIX MarketDataRequest (35=V)."""
        if self._socket:
            req_id = str(int(time.time()))
            msg = (
                f"8=FIX.4.4\x01"
                f"35={FIX_MSG_TYPE_MARKET_DATA_REQ}\x01"
                f"49={self.sender_comp_id}\x01"
                f"56={self.target_comp_id}\x01"
                f"34={self._sequence_num}\x01"
                f"52={datetime.now(UTC).strftime('%Y%m%d-%H:%M:%S.%f')[:-3]}\x01"
                f"262={req_id}\x01"
                f"146={symbol}\x01"
                f"263=1\x01"
                f"10=000\x01"
            )
            try:
                self._socket.sendall(msg.encode())
                self._sequence_num += 1
            except Exception as e:
                logger.warning(f"FIX market data request failed: {e}")

        return {
            "symbol": symbol,
            "bid": 0.0,
            "ask": 0.0,
            "last": 0.0,
            "volume": 0.0,
            "timestamp": datetime.now(UTC).isoformat(),
            "source": "fix",
        }

    # ------------------------------------------------------------------
    # Order management
    # ------------------------------------------------------------------

    async def _create_order_fix(self, request: OrderRequest) -> str:
        """Convert OrderRequest to a FIX NewOrderSingle (35=D) message string."""
        side_fix = "1" if request.side == OrderSide.BUY else "2"
        ord_type_fix = "1" if request.order_type == OrderType.MARKET else "2"
        tif_fix = "0" if request.time_in_force == TimeInForce.GTC else "1"

        ts = datetime.now(UTC).strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        order_id = request.client_order_id or f"fix-{int(time.time())}"

        msg = (
            f"8=FIX.4.4\x01"
            f"35={FIX_MSG_TYPE_NEW_ORDER}\x01"
            f"49={self.sender_comp_id}\x01"
            f"56={self.target_comp_id}\x01"
            f"34={self._sequence_num}\x01"
            f"52={ts}\x01"
            f"11={order_id}\x01"
            f"38={request.amount}\x01"
            f"40={ord_type_fix}\x01"
            f"44={request.price or 0}\x01"
            f"54={side_fix}\x01"
            f"55={request.symbol}\x01"
            f"59={tif_fix}\x01"
            f"10=000\x01"
        )
        return msg

    async def place_order(self, request: OrderRequest) -> OrderResponse:
        """Place a new order via FIX NewOrderSingle (35=D)."""
        self._check_availability()
        self._validate_order(request)
        self._sequence_num += 1

        order_id = request.client_order_id or f"fix-{int(time.time())}-{self._sequence_num}"
        ts = datetime.now(UTC)

        # Send FIX message (best-effort)
        if self._socket:
            fix_msg = await self._create_order_fix(request)
            try:
                self._socket.sendall(fix_msg.encode())
            except Exception as e:
                logger.warning(f"FIX order send failed: {e}")

        return OrderResponse(
            order_id=order_id,
            client_order_id=request.client_order_id,
            symbol=request.symbol,
            side=request.side,
            order_type=request.order_type,
            amount=request.amount,
            filled=0.0,
            remaining=request.amount,
            price=request.price,
            average_fill_price=None,
            status=OrderStatus.NEW,
            timestamp=ts,
            fee=0.0,
            fee_currency=request.symbol[:3] if len(request.symbol) >= 3 else "USD",
            raw={"protocol": "FIX.4.4", "msg_type": "D"},
        )

    async def cancel_order(self, order_id: str, symbol: str | None = None) -> bool:
        """Send FIX OrderCancelRequest (35=F)."""
        self._sequence_num += 1
        if self._socket:
            ts = datetime.now(UTC).strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
            msg = (
                f"8=FIX.4.4\x01"
                f"35=F\x01"
                f"49={self.sender_comp_id}\x01"
                f"56={self.target_comp_id}\x01"
                f"34={self._sequence_num}\x01"
                f"52={ts}\x01"
                f"342={order_id}\x01"
                f"10=000\x01"
            )
            try:
                self._socket.sendall(msg.encode())
            except Exception as e:
                logger.warning(f"FIX cancel failed: {e}")
        return True

    # ------------------------------------------------------------------
    # Account methods (FIX does not standardize these)
    # ------------------------------------------------------------------

    async def fetch_account(self) -> dict[str, Any]:
        return {
            "exchange": "fix",
            "account_id": self.sender_comp_id,
            "type": ExchangeType.FIX.value,
            "connected": self._connected,
            "authenticated": self._authenticated,
        }

    async def fetch_orders(
        self,
        symbol: str | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[OrderResponse]:
        return []

    async def fetch_positions(self, symbols: list[str] | None = None) -> list[Any]:
        return []

    async def fetch_balances(self) -> list[Any]:
        return []

    async def fetch_instruments(self) -> list[Any]:
        return []

    async def get_info(self) -> ExchangeInfo:
        return ExchangeInfo(
            exchange=f"{self.host}:{self.port}",
            type=self.exchange_type,
            connected=self._connected,
            authenticated=self._authenticated,
            server_time=self._server_time,
            rate_limit={"heartbeat_interval_sec": 60},
        )

    def _check_availability(self) -> None:
        if not self.api_key and not self.testnet:
            raise ConnectorError("FIX API key required for authenticated mode")
