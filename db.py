from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime, Float
import databases as databases

from sets import settings
from datetime import datetime

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = MetaData()
database.connect()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(80)),
    Column("surname", String(120)),
    Column("email", String(80)),
    Column("password", String(120)),
)
excursions = Table(
    "excursions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(120)),
    Column("description", String(400)),
    Column("price", DECIMAL),
)
orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("excursion_id", Integer, ForeignKey("excursions.id")),
    Column("order_date", DateTime, default=datetime.now()),
    Column("status", String(50), default="Booking"),
)


engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata.create_all(engine)
