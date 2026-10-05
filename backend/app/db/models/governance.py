from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Enum, Float, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

from backend.app.db.session import Base
from backend.app.core.enums import PackStatus


class PackModel(Base):
    __tablename__ = "governance_packs"

    pack_id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False)
    status = Column(Enum(PackStatus, name="pack_status"), nullable=False, default=PackStatus.DRAFT)
    benchmark_score = Column(Float, default=0.0)
    coverage = Column(Float, default=0.0)
    tests_passed = Column(Integer, default=0)
    tests_total = Column(Integer, default=0)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_record(self):
        from backend.app.core.governance import PackRecord, PackStatus
        return PackRecord(
            pack_id=self.pack_id,
            name=self.name,
            domain=self.domain,
            status=PackStatus(self.status.value),
            benchmark_score=self.benchmark_score,
            coverage=self.coverage,
            tests_passed=self.tests_passed,
            tests_total=self.tests_total,
            metadata=self.metadata or {},
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_record(cls, record):
        return cls(
            pack_id=record.pack_id,
            name=record.name,
            domain=record.domain,
            status=record.status,
            benchmark_score=record.benchmark_score,
            coverage=record.coverage,
            tests_passed=record.tests_passed,
            tests_total=record.tests_total,
            metadata=record.metadata,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )