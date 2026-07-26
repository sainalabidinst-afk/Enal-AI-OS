"""
Tests for Multi-Agent Coordination
=================================
Tests for agent-to-agent protocol and shared memory.
"""

import pytest


class TestBlackboard:
    """Tests for shared blackboard system."""

    @pytest.mark.asyncio
    async def test_blackboard_write_and_read(self):
        from apps.organization.communication import Blackboard
        bb = Blackboard()
        await bb.write("shared_key", {"data": "value"}, agent_id="agent-1")
        result = await bb.read("shared_key")
        assert result == {"data": "value"}

    @pytest.mark.asyncio
    async def test_blackboard_read_all(self):
        from apps.organization.communication import Blackboard
        bb = Blackboard()
        await bb.write("key1", "value1")
        await bb.write("key2", "value2")
        all_entries = await bb.read_all()
        assert "key1" in all_entries
        assert "key2" in all_entries

    @pytest.mark.asyncio
    async def test_blackboard_shared_memory(self):
        from apps.organization.communication import Blackboard
        bb = Blackboard()
        await bb.write("task_result", {"status": "done"}, agent_id="worker-1")
        history = bb.get_history()
        assert len(history) > 0


class TestMailbox:
    """Tests for agent mailbox system."""

    def test_send_and_receive(self):
        from apps.organization.communication import Mailbox, Message, MessageType
        mb = Mailbox()
        msg = Message(
            id="msg-1",
            sender_id="agent-a",
            recipient_id="agent-b",
            type=MessageType.TASK,
            subject="Do work",
            body={"task": "test"},
        )
        mb.send(msg)
        received = mb.receive("agent-b")
        assert len(received) == 1
        assert received[0].sender_id == "agent-a"

    def test_peek(self):
        from apps.organization.communication import Mailbox, Message, MessageType
        mb = Mailbox()
        msg = Message(
            id="msg-2",
            sender_id="agent-a",
            recipient_id="agent-b",
            type=MessageType.TASK,
            subject="Peek test",
            body={},
        )
        mb.send(msg)
        peeked = mb.peek("agent-b")
        received = mb.receive("agent-b")
        assert len(peeked) == 1
        assert len(received) == 1  # Peek doesn't remove


class TestMessageTypes:
    """Tests for message types."""

    def test_message_types_exist(self):
        from apps.organization.communication import MessageType, Priority
        assert MessageType.TASK.value == "task"
        assert MessageType.REPLY.value == "reply"
        assert MessageType.QUERY.value == "query"
        assert Priority.NORMAL.value == 2


class TestSemanticGraphEvidence:
    """Tests for semantic graph evidence scoring."""

    def test_evidence_score_calculation(self):
        from backend.app.core.semantic_graph import SemanticProjectGraph
        graph = SemanticProjectGraph()
        data = {
            "sources": [
                {"url": "https://example.com", "confidence": 0.9},
                {"url": "https://test.com", "confidence": 0.8},
            ]
        }
        class MockNode:
            def __init__(self):
                self.id = "test-node"
                self.node_type = "component"
                self.name = "Test Component"
                self.description = "Test"
                self.properties = data
                self.project_id = "proj-1"
        score = graph._calculate_evidence_score(MockNode())
        assert score == 0.85

    def test_citation_formatting(self):
        from backend.app.core.semantic_graph import SemanticProjectGraph
        graph = SemanticProjectGraph()
        data = {"sources": [{"url": "https://example.com", "confidence": 0.9}]}
        class MockNode:
            def __init__(self):
                self.id = "test-node"
                self.node_type = "component"
                self.name = "Test"
                self.description = "Test"
                self.properties = data
        citation = graph._format_citation(MockNode())
        assert "https://example.com" in citation