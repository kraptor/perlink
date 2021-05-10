# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
import logging

import discord
import discord.ext.commands
import urlextract
import uri

import perlink.db
import perlink.config
import perlink.emojis as emojis


logger = logging.getLogger(__name__)


class PerlinkBot(discord.ext.commands.Bot):

    def __init__(self, config: perlink.config.Configuration) -> None:
        super().__init__(">!")
        self.id = config.bot_id
        self._config = config
        self._db = perlink.db.Database(self)
        logger.info(f"Bot created: {self.id}")

        self._url_extractor = urlextract.URLExtract(
            extract_email=False,
            extract_localhost=False,
        )

    @property
    def config(self) -> perlink.config.Configuration:
        return self._config

    def run(self) -> None:
        logger.info(f"Bot running: {self.id}")
        super(PerlinkBot, self).run(self.config.discord_token)
        logger.info(f"Bot stopped: {self.id}")


    async def process_mention(self, msg: discord.Message) -> None:
        # TODO: add bot commands and answers here
        ch: discord.TextChannel = msg.channel
        await ch.send("ein???")


    async def on_message(self, msg: discord.Message) -> None:
        if msg.channel is discord.DMChannel:
            # ignore direct messages to bot
            return

        if self.user in msg.mentions and msg.author != self.user:
            # only process mentions in real-time
            await self.process_mention(msg)
            return

        if await self.can_process_message(msg):
            await self.inspect_and_process_message(msg)
    

    async def can_process_message(self, msg: discord.Message) -> bool:
        if msg.channel is discord.DMChannel:
            # ignore direct messages to bot
            return False

        if not isinstance(msg.channel, discord.TextChannel):
            return False

        if msg.author == self.user:
            # ignore my own messages :)
            return False

        if msg.channel.is_nsfw():
            # only process nsfw channels if allowed
            return self.config.allow_nsfw_channels

        return True


    def find_urls(self, text: typing.Optional[str]) -> typing.Iterable[str]:
        if text is None:
            return

        detect_raw_links = self.config.detect_raw_links
        valid_schemes = self.config.valid_link_protocols
        ban_secrets = self.config.ignore_links_with_secrets

        if detect_raw_links:
            valid_schemes.add(None)
        
        for url in self._url_extractor.find_urls(text):
            link: uri.URI = uri.URI(url)

            scheme_name = None if link.scheme is None else link.scheme.name
            
            if scheme_name not in valid_schemes:
                continue

            if ban_secrets:
                if link.user is not None \
                    or link.username is not None\
                    or link.password is not None:
                    continue

            yield url


    async def inspect_and_process_message(self, msg: discord.Message) -> None:
        vote_up   = 0
        vote_down = 0
        vote_fun  = 0
        vote_old  = 0
        vote_all  = 0

        for r in msg.reactions:
            vote_all += r.count
            if   r.emoji == emojis.ARROW_UP  : vote_up   = r.count
            elif r.emoji == emojis.ARROW_DOWN: vote_down = r.count
            elif r.emoji == emojis.ROFL      : vote_fun  = r.count
            elif r.emoji == emojis.OLD_MAN   : vote_old  = r.count

        has_urls = False
        for url in self.find_urls(msg.content):
            has_urls = True
            self._db.store_entry(
                perlink.db.DbEntry(
                    False,
                    msg.channel.id,
                    msg.channel.name,
                    msg.author.id,
                    msg.author.name,
                    msg.id,
                    url, 
                    msg.created_at.isoformat(),
                    vote_up, 
                    vote_down,
                    vote_old,
                    vote_fun,
                    vote_all
                )
            )

        if has_urls:
            # add voting reactions to message
            await msg.add_reaction(emojis.ARROW_UP)
            await msg.add_reaction(emojis.ARROW_DOWN)
            await msg.add_reaction(emojis.ROFL)
            await msg.add_reaction(emojis.OLD_MAN)
