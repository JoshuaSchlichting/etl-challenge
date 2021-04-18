import os
import csv
from datetime import datetime
from typing import List


class EmptyHeaderFileError(Exception):
    pass


class FileMerger:

    def __init__(self, logger) -> None:
        """
            Args:
                logger: An object containing basic logger calls.
        """
        self._logger = logger

    def merge_files(self, *, header_file_path: str, data_file_path: str, out_file: str) -> str:
        """Creates a csv file that combines the header and data file passed.

        Args:
            header_file_path: absolute path to newline separated headers file.

            data_file_path: path to the pipe delimited data file.

            out_file: path to the file that the method will create.

        Returns:
            Name of file created as a result of the merge.
        """
        self._logger.debug(f'Merging header file "{header_file_path}" with data file "{data_file_path}"')
        if os.path.isfile(out_file):
            self._logger.warning(f'Output file already exists. Overwriting "{out_file}"!!!')
            os.remove(out_file)
        with open(out_file, 'x') as file:
            writer = csv.writer(file)
            headers = self._get_header_list(header_file_path)
            writer.writerow(headers)
            data_rows = self._get_data_rows(data_file_path)
            for row in data_rows:
                writer.writerow(row)
        self._logger.debug(f'Finished writing to file: {out_file}')
        return out_file

    def _get_header_list(self, header_file_path: str) -> list:
        """Returns header list from header file.

        This method raises an EmptyHeaderFileError if the file is empty.

        Args:
            header_file_path: Absolute filepath to the header file.
    
        Returns:
            list: each row of the header file in a list.
        """
        self._logger.debug(f'Extracting headers from {header_file_path}')
        with open(header_file_path) as file:
            payload = [x.strip() for x in file.readlines()]
        if len(payload) == 0:
            raise EmptyHeaderFileError()
        """ TODO: Ask source if there will ever be an intentional
                  blank column name (maybe for visible space in
                  the file or something to that effect?). If there
                  will never be an empty string column name, then
                  scan for that here and raise an exception if a
                  blank column name is enountered.
        """
        return payload

    def _get_data_rows(self, data_file_path: str) -> List[list]:
        """Retrieve data from data file in list of list form."""
        self._logger.debug(f'Getting data rows from {data_file_path}')
        with open(data_file_path) as file:
            file_rows = file.readlines()
        data_rows = []
        for line in file_rows:
            row = line.split('|')
            row = [x.strip() for x in row]
            data_rows.append(row)
        return data_rows
