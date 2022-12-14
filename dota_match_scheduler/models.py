import enum
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from variables import DB


Base = declarative_base()


class MyEnum(enum.Enum):
    one = 'Bo1'
    two = 'Bo2'
    three = 'Bo3'
    four = 'Bo5'

    def return_enum(self, value):
        '''
        Checks the value passed through matches 
        '''
        for k, v in vars(self):
            if v == value:
                return self[k]


def db_connect():
    """
    Returns a connection instance.
    """
    return create_engine(f'mysql+mysqldb://{DB["USER"]}:{DB["PWORD"]}@localhost/{DB["DB"]}', pool_pre_ping=True)


class Match(Base):
    __tablename__ = "matches"

    id = Column(String(256), primary_key=True)
    team_one = Column("team_one", String(128), nullable=False)
    team_two = Column("team_two", String(128), nullable=False)
    match_format = Column('match_format', Enum(MyEnum))
    match_time = Column("match_time", DateTime, nullable=False)
    epoch_time = Column("epoch", BigInteger, nullable=False)
    team_one_id = relationship("Teams", backref="team_one_id")
    team_two_id = relationship("Teams", backref="team_two_id")
    # ! Need to add league_id to link back leagues table


class Team(Base):
    """This constructor is for the team/organisation data."""

    __tablename__ = "teams"

    # id (BigInt): team id
    # team_name(Var Char): Organisation/team name

    id = Column(BigInteger, primary_key=True)
    team_name = Column(String(255))
