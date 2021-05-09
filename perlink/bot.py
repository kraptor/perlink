# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import logging
import discord.ext.commands

import perlink.config


logger = logging.getLogger(__name__)


class PerlinkBot(discord.ext.commands.Bot):

    def __init__(self, config: perlink.config.Configuration) -> None:
        super().__init__(">!")
        self.id = config.bot_id
        self._token = config.discord_token
        logger.info(f"Bot created: {self.id}")


    def run(self) -> None:
        logger.info(f"Bot running: {self.id}")
        super(PerlinkBot, self).run(self._token)
        logger.info(f"Bot stopped: {self.id}")