from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Pipelines
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
RESULTS_DIR_NAME = 'results'

# Scrapy
BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    RESULTS_DIR_NAME + '/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
}
