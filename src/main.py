import logging

from database import Database

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)


class EtlScript:
    def __init__(self):
        self.database_conn = Database("acme")
        self.header_file = "../headers.txt"
        self.data_file = "../data.csv"
        self.out_file = "../output.csv"

    def load_file_to_database(self, file_path: str):
        self.database_conn.load_file(file_path)

    def run(self):
        # Your code starts here.

        # If this looks messy, just know I only have these imports placed here 
        # because I want to be compliant with the "# Your code starts here." above
        from file_merger import FileMerger
        merger = FileMerger(logger=logging.getLogger('FileMerger'))
        merged_file_path = merger.merge_files(
            header_file_path=self.header_file,
            data_file_path=self.data_file,
            out_file=self.out_file
        )
        logger.info(f'Merged file created: {merged_file_path}')
        self.load_file_to_database(file_path=merged_file_path)


if __name__ == "__main__":
    EtlScript().run()
