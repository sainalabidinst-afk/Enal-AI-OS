"""
Smart Home / IoT Action Connector
=================================

Provides smart home operations for Jenny: turn_on, turn_off, set_brightness, set_temperature.
Supports MQTT (local) and Home Assistant API (both local and cloud).
"""

from __future__ import annotations

import json
import logging
from typing import Any

from backend.app.connectors.base_action import (
    ActionConnectorError,
    ActionResult,
    ActionType,
    BaseActionConnector,
)

logger = logging.getLogger(__name__)


class SmartHomeConnector(BaseActionConnector):
    """Smart home connector supporting MQTT and Home Assistant API."""

    def __init__(
        self,
        mqtt_broker: str = "",
        mqtt_port: int = 1883,
        mqtt_user: str = "",
        mqtt_password: str = "",
        ha_url: str = "",
        ha_token: str = "",
        connector_type: ActionType = ActionType.SMART_HOME,
    ) -> None:
        super().__init__(connector_type=connector_type)
        self._mqtt_broker = mqtt_broker
        self._mqtt_port = mqtt_port
        self._mqtt_user = mqtt_user
        self._mqtt_password = mqtt_password
        self._ha_url = ha_url.rstrip("/") if ha_url else ""
        self._ha_token = ha_token
        self._mqtt_client: Any | None = None
        self._connected = bool(mqtt_broker) or bool(ha_url)

    async def connect(self) -> None:
        if not self._mqtt_broker and not self._ha_url:
            raise ActionConnectorError("No smart home backend configured (mqtt_broker or ha_url)")
        self._connected = True
        logger.info("SmartHomeConnector ready (ha_url=%s)", self._ha_url or "MQTT only")

    async def disconnect(self) -> None:
        self._connected = False
        if self._mqtt_client:
            try:
                self._mqtt_client.disconnect()
            except Exception:
                pass
            self._mqtt_client = None

    async def list_actions(self) -> list[str]:
        return ["turn_on", "turn_off", "set_brightness", "set_temperature", "get_state"]

    async def execute(self, action: str, params: dict[str, Any]) -> ActionResult:
        action_map = {
            "turn_on": self._turn_on,
            "turn_off": self._turn_off,
            "set_brightness": self._set_brightness,
            "set_temperature": self._set_temperature,
            "get_state": self._get_state,
        }

        handler = action_map.get(action)
        if not handler:
            raise ActionConnectorError(f"Unknown action: {action}")

        try:
            data = await handler(params)
            return ActionResult(
                success=True,
                data=data,
                action=action,
                connector=self.connector_type.value,
            )
        except Exception as e:
            logger.error("SmartHome action '%s' failed: %s", action, e)
            return ActionResult(
                success=False,
                error=str(e),
                action=action,
                connector=self.connector_type.value,
            )

    async def _send_ha_service(
        self, service: str, entity_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Send a Home Assistant service call."""
        import aiohttp

        if not self._ha_url or not self._ha_token:
            raise ActionConnectorError("Home Assistant URL and token not configured")

        headers = {
            "Authorization": f"Bearer {self._ha_token}",
            "Content-Type": "application/json",
        }
        payload = {"entity_id": entity_id}
        if data:
            payload.update(data)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._ha_url}/api/services/{service}",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status != 200:
                    raise ActionConnectorError(f"Home Assistant API error: HTTP {resp.status}")
                result = await resp.json()

        return {"service": service, "entity_id": entity_id, "result": result, "success": True}

    async def _send_mqtt(self, topic: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Publish to MQTT broker."""
        if not self._mqtt_broker:
            raise ActionConnectorError("MQTT broker not configured")

        try:
            import paho.mqtt.publish as mqtt_publish

            auth = None
            if self._mqtt_user and self._mqtt_password:
                auth = {"username": self._mqtt_user, "password": self._mqtt_password}

            mqtt_publish.single(
                topic=topic,
                payload=json.dumps(payload),
                hostname=self._mqtt_broker,
                port=self._mqtt_port,
                auth=auth,
            )
            return {"topic": topic, "payload": payload, "published": True}
        except ImportError as e:
            raise ActionConnectorError(
                "MQTT requires 'paho-mqtt'. Install with: pip install paho-mqtt"
            ) from e

    async def _turn_on(self, params: dict[str, Any]) -> dict[str, Any]:
        entity_id = params.get("entity_id", "")
        topic = params.get("topic", "")
        payload = params.get("payload", {"state": "on"})
        if not entity_id and not topic:
            raise ActionConnectorError("Either 'entity_id' or 'topic' is required for turn_on")
        if entity_id and self._ha_url:
            return await self._send_ha_service("homeassistant/turn_on", entity_id, {})
        if topic:
            return await self._send_mqtt(topic, payload)
        return {"entity_id": entity_id, "state": "on", "note": "Local stub"}

    async def _turn_off(self, params: dict[str, Any]) -> dict[str, Any]:
        entity_id = params.get("entity_id", "")
        topic = params.get("topic", "")
        payload = params.get("payload", {"state": "off"})
        if not entity_id and not topic:
            raise ActionConnectorError("Either 'entity_id' or 'topic' is required for turn_off")
        if entity_id and self._ha_url:
            return await self._send_ha_service("homeassistant/turn_off", entity_id, {})
        if topic:
            return await self._send_mqtt(topic, payload)
        return {"entity_id": entity_id, "state": "off", "note": "Local stub"}

    async def _set_brightness(self, params: dict[str, Any]) -> dict[str, Any]:
        entity_id = params.get("entity_id", "")
        brightness = int(params.get("brightness", 100))
        if brightness < 0 or brightness > 100:
            raise ActionConnectorError("brightness must be between 0 and 100")
        if not entity_id:
            raise ActionConnectorError("'entity_id' is required for set_brightness")
        if self._ha_url:
            return await self._send_ha_service(
                "light/turn_on", entity_id, {"brightness": int(brightness * 2.55)}
            )
        return {"entity_id": entity_id, "brightness": brightness, "note": "Local stub"}

    async def _set_temperature(self, params: dict[str, Any]) -> dict[str, Any]:
        entity_id = params.get("entity_id", "")
        temperature = float(params.get("temperature", 22.0))
        if temperature < 10 or temperature > 40:
            raise ActionConnectorError("temperature must be between 10 and 40")
        if not entity_id:
            raise ActionConnectorError("'entity_id' is required for set_temperature")
        if self._ha_url:
            return await self._send_ha_service(
                "climate/set_temperature", entity_id, {"temperature": temperature}
            )
        return {"entity_id": entity_id, "temperature": temperature, "note": "Local stub"}

    async def _get_state(self, params: dict[str, Any]) -> dict[str, Any]:
        entity_id = params.get("entity_id", "")
        if not entity_id:
            raise ActionConnectorError("'entity_id' is required for get_state")
        if not self._ha_url:
            return {"entity_id": entity_id, "state": "unknown", "note": "HA not configured"}

        import aiohttp

        headers = {"Authorization": f"Bearer {self._ha_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self._ha_url}/api/states/{entity_id}",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status != 200:
                    raise ActionConnectorError(f"Home Assistant API error: HTTP {resp.status}")
                result = await resp.json()

        return {"entity_id": entity_id, "state": result}
