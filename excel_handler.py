from datetime import datetime
from logging import Logger
from pathlib import Path
from openpyxl.workbook import Workbook


class ExcelHandler:
    def __init__(self, target_time: datetime, logger: Logger):
        self.workbook = Workbook()
        self.sheet = self.workbook.create_sheet("sheet1")

        self.sheet = self.workbook.active
        self.sheet["A1"] = "목적지"
        self.sheet["B1"] = "거리 (km)"
        self.sheet["C1"] = "시간 (분)"
        self.sheet["D1"] = "요금 (원)"

        self.output_directory = Path("outputs")

        self.target_time = target_time if target_time is not None else datetime.now()
        self.logger = logger

    def insert_data(self, name, distance, driving_time, fare):
        self.logger.info(
            f"목적지: {name}, 거리: {distance} km, 시간: {driving_time} 분, 요금: {fare} 원"
        )
        self.sheet.append([name, distance, driving_time, fare])

    def insert_empty_data(self, name):
        self.logger.info(f"Skip 목적지: {name}")
        self.sheet.append([name, "N/A", "N/A", "N/A"])

    def save_file(self):
        self.workbook.save(
            self.output_directory
            / f"{self.target_time.strftime('%Y-%m-%d-%H-%M')}.xlsx"
        )
