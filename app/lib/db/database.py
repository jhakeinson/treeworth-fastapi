from fastapi import Depends
from typing_extensions import Annotated
from httpx import get
from numpy import short
from sqlmodel import SQLModel, Session, create_engine, select
import pandas as pd
import json

from app.lib.utils.flatten_json import flatten_json
from app.lib.utils.get_propety_data import get_property_data

from .models.property import Property, Street


class Database:
    _instances = {}

    def __new__(cls, sqlite_file_name: str):
        if sqlite_file_name not in cls._instances:
            cls._instances[sqlite_file_name] = super().__new__(cls)
            cls._instances[sqlite_file_name].sqlite_file_name = sqlite_file_name
            cls._instances[sqlite_file_name].sqlite_url = (
                f"sqlite:///{sqlite_file_name}"
            )
            cls._instances[sqlite_file_name].engine = create_engine(
                cls._instances[sqlite_file_name].sqlite_url, echo=True
            )
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
            def get_properties_by_street_name(street_name):
                property_df = get_property_data()
                # get properties by street name
                properties = property_df[property_df["street_name"] == street_name]

                # create a list of Property objects
                return [
                    Property(
                        full_address=property["full_address"],
                        price=property["price"],
                        date_of_sale=property["date_of_sale"],
                    )
                    for _, property in properties.iterrows()
                ]

            # check if tables are already populatex.
            # if true, returm
            _props = session.exec(select(Property).limit(10)).all()
            _streets = session.exec(select(Street).limit(10)).all()

            if len(_streets) > 0 and len(_props) > 0:
                print("Tables already populated. Skippimg...")
                return

            short_json = input_json["short"]
            tall_json = input_json["tall"]

            short_streets = [
                Street(
                    name=street_name,
                    category="short",
                    tree_median_height=height,
                    properties=get_properties_by_street_name(street_name),
                )
                for street_name, height in short_json.items()
            ]
            tall_streets = [
                Street(
                    name=street_name,
                    category="tall",
                    tree_median_height=height,
                    properties=get_properties_by_street_name(street_name),
                )
                for street_name, height in tall_json.items()
            ]

            session.add_all(short_streets)
            session.add_all(tall_streets)
            session.commit()

    def get_engine(self):
        return self.engine


db = Database("dev.db")

def get_session():
    with Session(db.get_engine()) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(get_session)]