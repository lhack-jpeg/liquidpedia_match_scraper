# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dota_match_scheduler.models import db_connect, Match, Team, MyEnum
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem


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
        team_1_id = session.query(Team.id).filter(Team.team_name == item["team_left"]).first()
        try:
            match.team_one_id = team_1_id[0]
        except TypeError:
            DropItem(f"Can not retrive team_one_id {item}")
        match.team_two = item["team_right"]
        team_2_id = session.query(Team.id).filter(Team.team_name == item["team_right"]).first()
        try:
            match.team_two_id = team_2_id[0]
        except TypeError:
            DropItem(f"Can not retrive team_two_id {item}")
        match.match_time = item["start_time"]
        match.epoch_time = item["epoch_time"]
        match.match_format = item["match_format"]
        match_id = hash(str(item["team_left"]) + str(item["team_right"]) + str(item["epoch_time"]))
        match.id = str(match_id)

        # ! check the sqlalchemy for league and return the id

        # If doesn't exist can add to database.

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
        match_id = hash(str(item["team_left"]) + str(item["team_right"]) + str(item["epoch_time"]))
        match_id = int(match_id)
        match_exists = session.query(Match.id).filter(Match.id == match_id).one_or_none()
        team_1_id = session.query(Team.id).filter(Team.team_name == item["team_left"]).first()
        team_2_id = session.query(Team.id).filter(Team.team_name == item["team_right"]).first()
        session.close()

        if match_exists is not None:
            raise DropItem(f"Duplicate match exists {match_id}")
        else:
            return item
