# Liquidpedia Match scraper

## By Luke Hackett

---

This scrapy spyder crawls [Liquidpedia upcoming matches](https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches)

It is used to extract the following items:

- Match format
- Team one
- Team two
- Start time / Epoch time
- Tournament name.

### The pipelines:

#### Check for duplicate items/bad items

The pipeline first checks to ensure that both teams have a current team id.
It also ensure that each match is unique by checking the md5 hash value of the
`md5(f'{team_left}{team_right}{epoch_time}')`
If the either of the above conditions are met they are ignore from the next pipelines.

#### Create match instances and send to Database.

The pipeline runs after the first one to save the remaining items to the matches database.
The teams model instance is created and save for each item in the database and commited and save in the database.

### To run the spider:

1. Navigate to the root of the project in the terminal
2. Run `scrapy crawl match_scheduler`
