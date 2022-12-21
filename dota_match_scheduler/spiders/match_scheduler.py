import scrapy
import datetime
import pytz
from dota_match_scheduler.items import MatchItem

from scrapy.utils.response import open_in_browser


class MatchSchedulerSpider(scrapy.Spider):
    name = "match_scheduler"
    allowed_domains = ["liquipedia.net"]
    start_urls = [
        "https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches"
    ]

    def parse(self, response):
        aus_tz = pytz.timezone("Australia/Sydney")
        time_format = "%Y-%m-%d %H:%M:%S"
        match_item = MatchItem()

        match_table = response.xpath(
            '//*[contains(@class, "panel-box wiki-bordercolor-light toggle-area toggle-area-1 matches-list")]'
        )

        match_info = match_table.xpath(".//table")
        for match in match_info:
            # * The structure of the html has the teams in one row, the match info the second
            # * in the second row.
            team_info = match.xpath(".//tr[1]")
            game_time = match.xpath(".//tr[2]")

            match_item["match_format"] = team_info.xpath(
                ".//td[@class='versus']/div/abbr/text()"
            ).get()
            match_item["team_right"] = team_info.xpath(
                './/td[@class="team-right"]/span/span/a/@title'
            ).get()
            match_item["team_left"] = team_info.xpath(
                './/td[@class="team-left"]/span/span/a/@title'
            ).get()

            match_item["start_time"] = int(
                game_time.xpath(".//td/span/span/@data-timestamp").get()
            )
            match_item["epoch_time"] = match_item["start_time"]
            match_item["tournament"] = game_time.xpath(
                ".//td/div/div/a/@title"
            ).get()
            match_item["tournament"] = match_item["tournament"][:-2]

            if match_item["match_format"] is None:
                pass
            elif match_item["team_left"] is None:
                pass
            elif match_item["team_right"] is None:
                pass
            else:
                match_item["team_left"] = match_item["team_left"].split("(")
                match_item["team_left"] = match_item["team_left"][0].strip()
                match_item["start_time"] = aus_tz.localize(
                    datetime.datetime.fromtimestamp(match_item["start_time"])
                )
                match_item["start_time"] = match_item["start_time"].strftime(
                    time_format
                )

                yield match_item
