import sys
import types

import pytest


def _install_fake_sqlalchemy(monkeypatch):
    fake_engine = object()
    fake_sessionmaker = object()
    fake_base = object()

    fake_sqlalchemy = types.ModuleType("sqlalchemy")
    fake_sqlalchemy.create_engine = lambda *a, **k: fake_engine
    fake_sqlalchemy.ext = types.ModuleType("sqlalchemy.ext")
    fake_sqlalchemy.ext.declarative = types.ModuleType("sqlalchemy.ext.declarative")
    fake_sqlalchemy.ext.declarative.declarative_base = lambda: fake_base
    fake_sqlalchemy.orm = types.ModuleType("sqlalchemy.orm")
    fake_sqlalchemy.orm.sessionmaker = lambda *a, **k: fake_sessionmaker

    for mod in list(sys.modules):
        if mod == "sqlalchemy" or mod.startswith("sqlalchemy."):
            monkeypatch.delitem(sys.modules, mod, raising=False)
    monkeypatch.setitem(sys.modules, "sqlalchemy", fake_sqlalchemy)
    monkeypatch.setitem(sys.modules, "sqlalchemy.ext", fake_sqlalchemy.ext)
    monkeypatch.setitem(sys.modules, "sqlalchemy.ext.declarative", fake_sqlalchemy.ext.declarative)
    monkeypatch.setitem(sys.modules, "sqlalchemy.orm", fake_sqlalchemy.orm)

    return fake_engine, fake_sessionmaker, fake_base


class TestDbSession:
    def test_engine_session_local_base_created(self, monkeypatch):
        fake_engine, fake_sessionmaker, fake_base = _install_fake_sqlalchemy(monkeypatch)
        for mod in list(sys.modules):
            if mod == "backend.app.db.session" or mod.startswith("backend.app.db."):
                monkeypatch.delitem(sys.modules, mod, raising=False)

        fake_config = type("Settings", (), {"DATABASE_URL": "sqlite:///:memory:"})()
        import backend.app.db.session as ds_module
        monkeypatch.setattr(ds_module, "settings", fake_config)

        assert ds_module.engine is fake_engine
        assert ds_module.SessionLocal is fake_sessionmaker
        assert ds_module.Base is fake_base

    def test_get_db_yields_and_closes(self, monkeypatch):
        fake_engine, fake_sessionmaker, fake_base = _install_fake_sqlalchemy(monkeypatch)
        for mod in list(sys.modules):
            if mod == "backend.app.db.session" or mod.startswith("backend.app.db."):
                monkeypatch.delitem(sys.modules, mod, raising=False)

        fake_config = type("Settings", (), {"DATABASE_URL": "sqlite:///:memory:"})()
        import backend.app.db.session as ds_module
        monkeypatch.setattr(ds_module, "settings", fake_config)

        fake_db = type("Db", (), {
            "rollback": lambda self: setattr(self, "rolled_back", True),
            "close": lambda self: setattr(self, "closed", True),
        })()
        fake_db.rolled_back = False
        fake_db.closed = False

        monkeypatch.setattr(ds_module, "SessionLocal", lambda: fake_db)

        gen = ds_module.get_db()
        db = next(gen)
        assert db is fake_db
        try:
            gen.close()
        except StopIteration:
            pass
        assert fake_db.closed is True

    def test_get_db_rolls_back_on_exception(self, monkeypatch):
        fake_engine, fake_sessionmaker, fake_base = _install_fake_sqlalchemy(monkeypatch)
        for mod in list(sys.modules):
            if mod == "backend.app.db.session" or mod.startswith("backend.app.db."):
                monkeypatch.delitem(sys.modules, mod, raising=False)

        fake_config = type("Settings", (), {"DATABASE_URL": "sqlite:///:memory:"})()
        import backend.app.db.session as ds_module
        monkeypatch.setattr(ds_module, "settings", fake_config)

        fake_db = type("Db", (), {
            "rollback": lambda self: setattr(self, "rolled_back", True),
            "close": lambda self: setattr(self, "closed", True),
        })()
        fake_db.rolled_back = False
        fake_db.closed = False

        monkeypatch.setattr(ds_module, "SessionLocal", lambda: fake_db)

        gen = ds_module.get_db()
        db = next(gen)
        assert db is fake_db
        try:
            raise ValueError("fail")
        except ValueError:
            pass
        try:
            gen.throw(ValueError("fail"))
        except ValueError:
            pass
        except StopIteration:
            pass
        assert fake_db.rolled_back is True
        assert fake_db.closed is True
