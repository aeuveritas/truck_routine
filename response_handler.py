from logging import Logger
from requests import Response


class ResponseHandler:
    def __init__(self, response: Response, logger: Logger):
        json = response.json()
        self.features = json["features"]

        self.logger = logger

    def target_feature_index(self) -> int:
        target_index = None
        for idx, feature in enumerate(self.features):
            properties = feature.get("properties")
            if properties is None:
                break
            total_distance = properties.get("totalDistance")
            if total_distance is None:
                break
            target_index = idx
            break
        assert target_index is not None, "properties를 찾을 수 없습니다."
        return target_index

    def results(self, target_index: int):
        feature = self.features[target_index]
        properties = feature["properties"]
        total_distance = properties.get("totalDistance")
        if total_distance is None:
            return None, None, None
        distance = round(total_distance / 1000, 2)
        driving_time = round(properties["totalTime"] / 60, 2)
        fare = properties["totalFare"]

        return distance, driving_time, fare
