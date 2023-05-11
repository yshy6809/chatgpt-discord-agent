from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.model import Base


class Database:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)

    def _create_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def insert(self, obj):
        session = self._create_session()
        session.add(obj)
        session.commit()
        session.close()


data_base = Database('sqlite:///discord_agent.db')
