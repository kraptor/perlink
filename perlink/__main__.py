# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import dotenv
import logging
import coloredlogs

import perlink.config


def configure_logger(config: perlink.config.Configuration):
    coloredlogs.install(fmt=config.log_format, level="DEBUG")
    log = logging.getLogger(__name__)

    for logger, level in {
        "discord.gateway": logging.CRITICAL,
        "discord.client" : logging.CRITICAL,
        "discord.http"   : logging.CRITICAL,
        # "asyncio"        : logging.CRITICAL,
        "filelock": logging.CRITICAL,
        "urllib3.connectionpool": logging.CRITICAL,
    }.items(): logging.getLogger(logger).setLevel(level)


def main():
    config = perlink.config.load_configuration()
    configure_logger(config)
    print(config)


if __name__ == "__main__":
    main()