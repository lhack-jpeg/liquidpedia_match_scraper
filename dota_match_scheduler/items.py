# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field, Item


class MatchItem(Item):
    team_left = Field()
    team_right = Field()
    match_format = Field()
    start_time = Field()
    epoch_time = Field()
    tournament = Field()
