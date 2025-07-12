# create_tables.py
from db.session import engine, Base
from models.models import CachedQuestion

# Create all tables
Base.metadata.create_all(bind=engine)
