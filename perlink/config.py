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
    allow_nsfw_channels: bool
    detect_raw_links: bool
    valid_link_protocols: set[str]
    ignore_links_with_secrets: bool


def as_bool(value: str) -> bool:
    return value.lower() in ['true', '1', 't', 'y', 'yes']


def load() -> Configuration:
    dotenv.load_dotenv()

    return Configuration(
        log_format = os.getenv(
            "LOG_FORMAT", 
            "%(asctime)s [%(process)d] %(name)-30s | %(levelname)8s %(message)s"
        ),
        bot_id = os.getenv("BOT_ID", "perlink"),
        db_file = os.getenv("DATABASE_FILE", None),
        discord_token = os.getenv("DISCORD_TOKEN", None),
        max_vote_hours = int(os.getenv("MAX_VOTE_HOURS", 24)),
        allow_nsfw_channels = as_bool(os.getenv("ALLOW_NSFW_CHANNELS", "false")),
        detect_raw_links = as_bool(os.getenv("DETECT_RAW_LINKS", "false")),
        valid_link_protocols = set(os.getenv("VALID_LINK_PROTOCOLS", "http,https,ftp").split(",")),
        ignore_links_with_secrets = as_bool(os.getenv("IGNORE_LINKS_WITH_SECRETS", "true")),
    )