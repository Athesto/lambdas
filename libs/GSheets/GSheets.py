#!/usr/bin/env python3
# Builtin imports
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from hashlib import md5
import base64

# 3rd party import
import pygsheets

class GSheetsModel(ABC):
    @abstractmethod
    def to_gsheet(self, data):
        pass

class GSheets:
    def __init__(self, secret_key_base64, spreadsheet_name, **kwargs):
        service_account_json = base64.b64decode(secret_key_base64).decode('utf-8')
        self.__pygsheets_client = pygsheets.authorize(service_account_json=service_account_json)
        self.__spreadsheet = self.__pygsheets_client.open(spreadsheet_name)

    def create(self, instance:GSheetsModel):
        try:
            self.__worksheet = self.__spreadsheet.worksheet_by_title(instance.__class__.__name__)
        except pygsheets.exceptions.WorksheetNotFound:
            self.__worksheet = self.__spreadsheet.add_worksheet(instance.__class__.__name__)

        titles, values, indexes = self.__get_title_values_index(instance)

        if self.__worksheet.cell('A1').value == '':
            self.__worksheet.insert_rows(0, values=["index", *titles])

        index = self.__generate_id(indexes)

        if index in set(self.__worksheet.get_col(1)):
            print(f"Element {index} already exists")
            print(values)
            raise ValueError("Element already exists")
        self.__worksheet.append_table(values=(index, *values))

    @staticmethod
    def __generate_id(indexes):
        index = "|".join(indexes)
        encoded_md5 = md5(index.encode()).hexdigest()
        md5_int = int(encoded_md5, 16) % 2 ** 63
        return  f"id-{md5_int}"

    @staticmethod
    def __get_title_values_index(instance:GSheetsModel):
        title_data_options = instance.to_gsheet()

        titles = []
        values = []
        indexes = []
        for title, value, *options in title_data_options:
            titles.append(title)
            values.append(str(value))
            if len(options) == 0 or "skipIndex" not in options:
                indexes.append(str(value))

        return titles, values, indexes
