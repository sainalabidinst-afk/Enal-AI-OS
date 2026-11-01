from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.core.config import settings

if settings.DATABASE_URL.startswith("sqlite"):
    sqlite_options = {"connect_args": {"check_same_thread": False}}
    if ":memory:" in settings.DATABASE_URL:
        engine = create_engine(settings.DATABASE_URL, poolclass=StaticPool, **sqlite_options)
    else:
        engine = create_engine(settings.DATABASE_URL, **sqlite_options)
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
