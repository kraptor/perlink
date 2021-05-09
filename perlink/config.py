# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import dataclasses

import dotenv


@dataclasses.dataclass
class Configuration:
    log_format: str
    bot_id: str
    db_file: str
    discord_token: str
    max_vote_hours: int


def load() -> Configuration:
    dotenv.load_dotenv()

    return Configuration(
        log_format = os.getenv(
            "LOG_FORMAT", 
            "%(asctime)s [%(process)d] %(name)-30s | %(levelname)8s %(message)s"
        ),
        bot_id = "perlink",
        db_file = os.getenv("DATABASE_FILE", None),
        discord_token = os.getenv("DISCORD_TOKEN", None),
        max_vote_hours = int(os.getenv("MAX_VOTE_HOURS", 24)),
    )