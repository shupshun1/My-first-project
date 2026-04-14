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
    total_wave = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    enemies_killed = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    bats_killed = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    swords_thrown = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    swords_missed = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    swords_hitted = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now,
                                      onupdate=datetime.datetime.now)

    def update_stats(self, kills=0, deaths=0, bosses_defeated=0, swords_thrown=0,
                     swords_missed=0, swords_hitted=0, enemies_killed=0,
                     bats_killed=0, total_wave=0):
        self.kills += kills
        self.deaths += deaths
        self.bosses_defeated += bosses_defeated
        self.swords_thrown += swords_thrown
        self.swords_missed += swords_missed
        self.swords_hitted += swords_hitted
        self.enemies_killed += enemies_killed
        self.bats_killed += bats_killed

        if total_wave > self.total_wave:
            self.total_wave = total_wave

        self.modified_date = datetime.datetime.now()