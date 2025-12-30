from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here so SQLAlchemy knows about them
from app.db import models