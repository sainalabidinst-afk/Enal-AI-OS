from backend.app.core.telemetry.aggregator import Aggregator


def test_chat_kpis_count_requests_separately_from_message_characters() -> None:
    aggregator = Aggregator()
    aggregator.record_chat(
        chat_id="chat-1",
        conversation_id="conversation-1",
        workspace_id="workspace-1",
        status="success",
        error=None,
        message_length=12,
        total_time_ms=40,
    )
    aggregator.record_chat(
        chat_id="chat-2",
        conversation_id="conversation-1",
        workspace_id="workspace-1",
        status="success",
        error=None,
        message_length=28,
        total_time_ms=60,
    )

    assert aggregator.chat_kpis() == {
        "total_messages": 2,
        "total_characters": 40,
        "avg_latency_ms": 50.0,
    }


def test_empty_chat_kpis_have_zero_values() -> None:
    assert Aggregator().chat_kpis() == {
        "total_messages": 0,
        "total_characters": 0,
        "avg_latency_ms": 0.0,
    }
