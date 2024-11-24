import json
import pytest
from sqlmodel import Session, text
from app.lib.db.database import Database
from app.lib.db.models.property import Street

@pytest.fixture
def db():
    # If test.db file exists, delete it
    if "test.db" in Database._instances:
        del Database._instances["test.db"]

    import os
    if os.path.exists("test.db"):
        os.remove("test.db")    

    return Database("test.db")

def test_create_tables(db):
    db.create_tables()
    # Check if tables are created
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))

        tables = [row[0] for row in result]
        assert "street" in tables

def test_populate_tables(db):
    db.create_tables()
    db.populate_tables()
    # Check if tables are populated
    with Session(db.engine) as session:
        short_streets = session.query(Street).filter(Street.category == "short").all()
        tall_streets = session.query(Street).filter(Street.category == "tall").all()
        assert len(short_streets) > 0
        assert len(tall_streets) > 0

def test_populate_tables_with_empty_json(db, monkeypatch):
    # Mock the json file to be empty
    def mock_load_json(file):
        return {}
    monkeypatch.setattr(json, "load", mock_load_json)
    db.create_tables()
    db.populate_tables()
    # Check if tables are not populated
    with Session(db.engine) as session:
        short_streets = session.query(Street).filter(Street.category == "short").all()
        tall_streets = session.query(Street).filter(Street.category == "tall").all()
        assert len(short_streets) == 0
        assert len(tall_streets) == 0

def test_populate_tables_with_invalid_json(db, monkeypatch):
    # Mock the json file to be invalid
    def mock_load_json(file):
        return {"invalid": "json"}
    monkeypatch.setattr(json, "load", mock_load_json)
    db.create_tables()
    with pytest.raises(KeyError):
        db.populate_tables()