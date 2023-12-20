from collections import defaultdict
import datetime as dt
import csv

from pep_parse.settings import DATETIME_FORMAT, RESULTS_DIR_NAME, BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_count = defaultdict(int)

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        total_count = sum(self.status_count.values())
        self.status_count['Total'] = total_count

        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)

        results_dir = BASE_DIR / RESULTS_DIR_NAME
        results_dir.mkdir(exist_ok=True)

        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(
                f, dialect='unix',
                fieldnames=['Status', 'Count'],
                quoting=csv.QUOTE_NONE
            )
            writer.writeheader()

            rows_to_write = [{'Status': status, 'Count': count}
                             for status, count in self.status_count.items()]
            writer.writerows(rows_to_write)
