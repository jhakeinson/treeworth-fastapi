import json
import pytest
from sqlmodel import Session, select, text
from app.lib.db.database import Database
from app.lib.db.models.property import Property, Street

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
        assert "property" in tables

def test_populate_tables(db):
    db.create_tables()
    db.populate_tables()
    # Check if tables are populated
    with Session(db.engine) as session:
        properties = session.exec(select(Property).limit(10))
        short_streets = session.exec(select(Street).filter(Street.category == "short").limit(10))
        tall_streets = session.exec(select(Street).filter(Street.category == "tall").limit(10))
        assert len(short_streets.all()) > 0
        assert len(tall_streets.all()) > 0
        assert len(properties.all()) > 0

def test_populate_tables_with_empty_json(db, monkeypatch):
    # Mock the json file to be empty
    def mock_load_json(file):
        return {}
    monkeypatch.setattr(json, "load", mock_load_json)
    db.create_tables()
    db.populate_tables()
    # Check if tables are not populated
    with Session(db.engine) as session:
        properties = session.exec(select(Property).limit(10))
        short_streets = session.exec(select(Street).filter(Street.category == "short").limit(10))
        tall_streets = session.exec(select(Street).filter(Street.category == "tall").limit(10))
        assert len(properties.all()) == 0
        assert len(short_streets.all()) == 0
        assert len(tall_streets.all()) == 0

def test_populate_tables_with_invalid_json(db, monkeypatch):
    # Mock the json file to be invalid
    def mock_load_json(file):
        return {"invalid": "json"}
    monkeypatch.setattr(json, "load", mock_load_json)
    db.create_tables()
    with pytest.raises(KeyError):
        db.populate_tables()