import datetime
import sqlalchemy
from sqlalchemy.orm import declarative_base

SqlAlchemyBase = declarative_base()


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=False, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    gender = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    kills = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    deaths = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    bosses_defeated = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    total_score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    level = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now,
                                      onupdate=datetime.datetime.now)


    def update_stats(self, kills=0, deaths=0, bosses=0, score=0):
        self.kills += kills
        self.deaths += deaths
        self.bosses_defeated += bosses
        self.total_score += score
        self.level = 1 + (self.total_score // 1000)
        self.modified_date = datetime.datetime.now()