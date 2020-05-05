from sqlalchemy import Column, Integer, String

from peachy.db.base import Base, engine


class User(Base):
    __tablename__ = "peachy_users"

    pk = Column(Integer, primary_key=True)

    first_name = Column(String)
    last_name = Column(String)

    discord_id = Column(Integer, unique=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


Base.metadata.create_all(bind=engine)
