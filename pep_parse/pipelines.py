import csv
from datetime import datetime

from pytz import timezone
from scrapy.exceptions import DropItem

from pep_parse.settings import BASE_DIR

from .constants import RESULTS_DIR, SUMMARY_FIELDS_NAME

utc = datetime.now(timezone('UTC'))


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = {}
        self.timestamp = utc.strftime('%Y-%m-%dT%H-%M-%S')

    def process_item(self, item, spider):
        try:
            self.statuses[item['status']] = (
                self.statuses.setdefault(item['status'], 0) + 1
            )
        except KeyError:
            raise DropItem("There is no status field.")
        return item

    def close_spider(self, spider):
        dirpath = BASE_DIR / RESULTS_DIR
        filename = f'{dirpath}/status_summary_{self.timestamp}.csv'
        self.statuses['Total'] = sum(self.statuses.values())
        with open(filename, "w", encoding="utf-8") as f:
            writer = csv.writer(
                f,
                quoting=csv.QUOTE_NONE,
                dialect=csv.unix_dialect,
                escapechar="\\",
            )
            writer.writerow(SUMMARY_FIELDS_NAME)
            writer.writerows(self.statuses.items())
