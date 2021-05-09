# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import dataclasses

import dotenv


@dataclasses.dataclass
class Configuration:
    discord_token: str
    db_file: str
    max_vote_hours: int
    log_format: str


def load_configuration() -> Configuration:
    dotenv.load_dotenv()

    return Configuration(
        discord_token = os.getenv("DISCORD_TOKEN", None),
        db_file = os.getenv("DATABASE_FILE", None),
        max_vote_hours = int(os.getenv("MAX_VOTE_HOURS", 24)),
        log_format = os.getenv(
            "LOG_FORMAT", 
            "%(asctime)s [%(process)d] %(name)-30s | %(levelname)8s %(message)s"
        )
    )