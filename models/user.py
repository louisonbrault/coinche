from datetime import date

from sqlalchemy import Column, Date, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    creation_date = Column(Date, nullable=False, default=date.today())
    slug_name = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=False)
    facebook_id = Column(String, unique=True)
    role = Column(String, nullable=False, default="writer")
