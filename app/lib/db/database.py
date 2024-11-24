from numpy import short
from sqlmodel import SQLModel, Session, create_engine
import pandas as pd
import json

from app.lib.utils.flatten_json import flatten_json

from .models.property import Street

class Database:
    _instances = {}

    def __new__(cls, sqlite_file_name: str):
        if sqlite_file_name not in cls._instances:
            cls._instances[sqlite_file_name] = super().__new__(cls)
            cls._instances[sqlite_file_name].sqlite_file_name = sqlite_file_name
            cls._instances[sqlite_file_name].sqlite_url = f"sqlite:///{sqlite_file_name}"
            cls._instances[sqlite_file_name].engine = create_engine(cls._instances[sqlite_file_name].sqlite_url, echo=True)
        return cls._instances[sqlite_file_name]

    def __init__(self, sqlite_file_name: str):
        # No need to initialize anything here since it's done in __new__
        pass

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)
        print("Tables created")

    def populate_tables(self):
        with open("data/city-trees.json", "r") as file:
            input_json = json.load(file)
            
            # check if input_json is empty dict, if empty return
            if not input_json:
                return

            input_json = flatten_json(input_json)

        with Session(self.engine) as session:
            short_json = input_json["short"]
            tall_json = input_json["tall"]

            short_streets = [Street(name=street_name, category="short", tree_median_height=height) for street_name, height in short_json.items()]
            tall_streets = [Street(name=street_name, category="tall", tree_median_height=height) for street_name, height in tall_json.items()]

            session.add_all(short_streets)
            session.add_all(tall_streets)
            session.commit()

db = Database("dev.db")