import logging
import yaml
import typer

from typing import Dict
from dotenv import dotenv_values
from logging import Logger
from datetime import datetime

from enums import Mode
from excel_handler import ExcelHandler
from query_handler import QueryHandler
from response_handler import ResponseHandler


def generate_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    return logger


def parse_target_time(config: Dict, logger: Logger) -> datetime:
    target_time_str = config.get("TARGET_TIME")
    assert target_time_str is not None
    target_time = None
    try:
        target_time = datetime.strptime(target_time_str, "%Y/%m/%d %H:%M")
    except Exception as err:
        logger.info(f"TARGET_TIME의 형태가 잘못되었습니다. '%Y/%m/%d %H:%M'")
        logger.info(f"{target_time_str}를 위의 형태에 맞게 수정해주세요.")
        return None
    return target_time


def run(config: Dict, target_time: datetime, logger: Logger):
    query_handler = QueryHandler(config, target_time, logger)

    with open(config["LOCATIONS_FILE"]) as f:
        locations = yaml.load(f, Loader=yaml.FullLoader)
        start_location = locations["start"]

        excel_handler = ExcelHandler(target_time, logger)

        for destination_location in locations["destinations"]:
            try:
                name = destination_location["name"]
                response = query_handler.request(start_location, destination_location)
                response_handler = ResponseHandler(response, logger)
                target_index = response_handler.target_feature_index()
                distance, driving_time, fare = response_handler.results(target_index)
                assert distance is not None
                excel_handler.insert_data(name, distance, driving_time, fare)
            except Exception as err:
                logger.info(f"예상치 못한 에러가 발생했습니다.: {err}")
                logger.info("이로 인해 빈 값을 저장합니다.")
                excel_handler.insert_empty_data(name)
                continue

        excel_handler.save_file()


def main(mode: Mode = Mode.periodic, env_file: str = typer.Option(...)):
    config = dotenv_values(env_file)
    logger = generate_logger()

    if mode == Mode.periodic:
        assert (
            config.get("TARGET_TIME").lower() == "no"
        ), "periodic mode는 TARGET_TIME로 반드시 NO(or no)를 가져야 합니다."
        run(config, None, logger)
    elif mode == Mode.specific:
        target_time = parse_target_time(config, logger)
        if target_time is None:
            return
        run(config, target_time, logger)
    else:
        assert False, f"잘못된 mode를 설정하였습니다.: {mode}\nperiodic 또는 specific을 사용해주세요."


if __name__ == "__main__":
    typer.run(main)
