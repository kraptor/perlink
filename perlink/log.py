# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import coloredlogs
import logging


def configure(log_format: str):
    coloredlogs.install(fmt=log_format, level="DEBUG")
    log = logging.getLogger(__name__)

    for logger, level in {
        "discord.gateway": logging.CRITICAL,
        "discord.client" : logging.CRITICAL,
        "discord.http"   : logging.CRITICAL,
        # "asyncio"        : logging.CRITICAL,
        "filelock": logging.CRITICAL,
        "urllib3.connectionpool": logging.CRITICAL,
    }.items(): logging.getLogger(logger).setLevel(level)