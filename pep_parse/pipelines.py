import csv
from datetime import datetime

from pytz import timezone
from scrapy.exceptions import DropItem

from .constants import RESULTS_DIR, SUMMARY_FIELDS_NAME

utc = datetime.now(timezone('UTC'))


class PepParsePipeline:
    def open_spider(self, spider):
        self.dictionary = {}
        self.timestamp = utc.strftime('%Y-%m-%dT%H-%M-%S')

    def process_item(self, item, spider):
        try:
            self.dictionary[item['Status']] = (
                self.dictionary.get(item['Status'], 0) + 1
            )
        except KeyError:
            raise DropItem("There is no status field.")
        return item

    def close_spider(self, spider):
        filepath = f'{RESULTS_DIR}/status_summary_{self.timestamp}.csv'
        self.dictionary['Total'] = sum(self.dictionary.values())
        with open(filepath, "w", encoding="utf-8") as f:
            writer = csv.writer(
                f,
                quoting=csv.QUOTE_NONE,
                dialect=csv.unix_dialect,
                escapechar="\\",
            )
            writer.writerow(SUMMARY_FIELDS_NAME)
            writer.writerows(self.dictionary.items())
