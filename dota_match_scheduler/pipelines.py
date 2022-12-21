# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dota_match_scheduler.models import db_connect, Match, Team, MyEnum
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from hashlib import md5


class DotaMatchSchedulerPipeline:
    def process_item(self, item, spider):
        return item


class SaveMatchesPipeline(object):
    def __init__(self):
        """
        Initialises cnnection.
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Saves matches to the database. This is called on every item.
        """
        session = self.Session()
        match = Match()

        match.team_one = item["team_left"]
        team_1_id = (
            session.query(Team.id)
            .filter(Team.team_name == item["team_left"])
            .first()
        )
        match.team_one_id = team_1_id[0]
        match.team_two = item["team_right"]
        team_2_id = (
            session.query(Team.id)
            .filter(Team.team_name == item["team_right"])
            .first()
        )
        match.team_two_id = team_2_id[0]
        match.match_time = item["start_time"]
        match.epoch_time = item["epoch_time"]
        match.match_format = item["match_format"]
        match.tournament_name = item["tournament"]
        match_id = f'{str(item["team_left"])}{str(item["team_right"])}{str(item["epoch_time"])}'.encode()
        match_id = md5(match_id)
        match_id = str(match_id.hexdigest())
        match.id = match_id

        # ! check the sqlalchemy for league and return the id

        session.add(match)
        session.commit()
        session.close()
        return item


class DuplicatesPipelines(object):
    """
    Checks to see if item is already in the database.
    """

    def __init__(self):
        """
        Initialises pipeline.
        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        match_id = f'{str(item["team_left"])}{str(item["team_right"])}{str(item["epoch_time"])}'.encode()
        match_id = md5(match_id)
        match_id = str(match_id.hexdigest())
        match_exists = (
            session.query(Match.id).filter(Match.id == match_id).one_or_none()
        )
        team_2_id = (
            session.query(Team.id)
            .filter(Team.team_name == item["team_right"])
            .first()
        )
        team_1_id = (
            session.query(Team.id)
            .filter(Team.team_name == item["team_left"])
            .first()
        )
        session.close()

        # If team name doesn't return an ID, item wil,be dropped.
        try:
            team_id = team_2_id[0]
        except TypeError:
            raise DropItem(f"Can not access id")

        try:
            team_id = team_1_id[0]
        except TypeError:
            raise DropItem(f"Can not access id")

        if match_exists is not None:
            raise DropItem(f"Duplicate match exists {match_id}")
        else:
            return item
