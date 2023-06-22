from datetime import date

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, relationship

from database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, default=date.today())
    creator = Column(Integer, ForeignKey("users.id"), nullable=False, default=0)
    player_a1_id = mapped_column(ForeignKey("users.id"), nullable=False)
    player_a1 = relationship("User", foreign_keys=[player_a1_id])
    player_a2_id = mapped_column(ForeignKey("users.id"), nullable=False)
    player_a2 = relationship("User", foreign_keys=[player_a2_id])
    player_b1_id = mapped_column(ForeignKey("users.id"), nullable=False)
    player_b1 = relationship("User", foreign_keys=[player_b1_id])
    player_b2_id = mapped_column(ForeignKey("users.id"), nullable=False)
    player_b2 = relationship("User", foreign_keys=[player_b2_id])
    score_a = Column(Integer, nullable=False)
    score_b = Column(Integer, nullable=False)
    stars_a = Column(Integer, nullable=False, default=0)
    stars_b = Column(Integer, nullable=False, default=0)
    a_won = Column(Boolean, nullable=False)
    b_won = Column(Boolean, nullable=False)
