from pathlib import Path

from .constants import PEP_FIELDS_NAME, RESULTS_DIR

BOT_NAME = "pep_parse"
BASE_DIR = Path(__file__).parent.parent

SPIDER_MODULES = ["pep_parse.spiders"]
NEWSPIDER_MODULE = "pep_parse.spiders"

FEEDS = {
    f'{RESULTS_DIR}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': PEP_FIELDS_NAME,
        'overwrite': True
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

ROBOTSTXT_OBEY = True
