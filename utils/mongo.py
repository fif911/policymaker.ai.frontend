import streamlit as st
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


@st.cache_resource
def get_mongo_connection() -> Collection:
    assert (MONGODB_URI := st.secrets["MONGODB_URI"]), "No MongoDB URI provided in secrets.toml."

    client: MongoClient = MongoClient(MONGODB_URI)
    db: Database = client.get_database("events")
    collection: Collection = db.get_collection("events")
    return collection
