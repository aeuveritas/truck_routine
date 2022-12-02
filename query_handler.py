from datetime import datetime
from http import HTTPStatus
from logging import Logger
from typing import Dict
from retry import retry

import requests


class QueryHandler:
    def __init__(self, config: Dict, target_time: datetime, logger: Logger):
        self.url = (
            "https://apis.openapi.sk.com/tmap/routes/prediction?"
            "version=1&resCoordType=WGS84GEO&reqCoordType=WGS84GEO&sort=index&callback=function"
        )
        self.config = config
        self.headers = self.generate_headers()

        self.target_time = target_time
        self.logger = logger

    def generate_headers(self):
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "appKey": f"{self.config['API_KEY']}",
        }

    @retry(tries=5, delay=5.0)
    def request(self, start, destination):
        payload = self.generate_payload(start, destination)
        response = requests.post(self.url, json=payload, headers=self.headers)
        assert (
            response.status_code == HTTPStatus.OK
        ), "API로부터 예상치 못한 response가 도달하여 재송신합니다."
        return response

    def generate_payload(self, start: Dict, destination: Dict):
        target_time = (
            self.target_time if self.target_time is not None else datetime.now()
        )
        prediction_time = target_time.strftime("%Y-%m-%dT%H:%M:%S") + "+0900"
        return {
            "routesInfo": {
                "departure": {
                    "name": start["name"],
                    "lon": start["long"],
                    "lat": start["lat"],
                },
                "destination": {
                    "name": destination["name"],
                    "lon": destination["long"],
                    "lat": destination["lat"],
                },
                "predictionType": "departure",
                "predictionTime": prediction_time,
                "searchOption": "00",
                "tollgateCarType": self.config["CAR_TYPE"],
                "trafficInfo": "N",
            }
        }
