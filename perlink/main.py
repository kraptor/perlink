# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging

import perlink.config
import perlink.log
import perlink.bot

logger = logging.getLogger(__name__)


def main():
    config = perlink.config.load()
    perlink.log.configure(config.log_format)
    logger.info("Initializing Perlink Bot...")
    bot = perlink.bot.PerlinkBot(config)    
    bot.run()