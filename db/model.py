import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CostLog(Base):
    __tablename__ = 'cost_log'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    prompt_cost = Column(Integer, nullable=False)
    complete_cost = Column(Integer, nullable=False)
    model_version = Column(String, nullable=False)
    cost_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f"<CostLog(username={self.username}, prompt_cost={self.prompt_cost}, complete_cost={self.complete_cost}, model_version={self.model_version}, cost_time={self.cost_time})>"
