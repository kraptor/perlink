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

import perlink.emojis as emojis
import perlink.config


logger = logging.getLogger(__name__)


class PerlinkBot(discord.ext.commands.Bot):

    def __init__(self, config: perlink.config.Configuration) -> None:
        super().__init__(">!")
        self.id = config.bot_id
        self.config = config
        logger.info(f"Bot created: {self.id}")

        self.url_extractor = urlextract.URLExtract(
            extract_email=False,
            extract_localhost=False,
        )


    def run(self) -> None:
        logger.info(f"Bot running: {self.id}")
        super(PerlinkBot, self).run(self.config.discord_token)
        logger.info(f"Bot stopped: {self.id}")

    
    async def on_message(self, msg: discord.Message) -> None:
        if msg.channel is discord.DMChannel:
            # ignore direct messages to bot
            return

        if await self.can_process_message(msg):
            await self.inspect_and_process_message(msg)


    async def process_mention(self, msg: discord.Message) -> None:
        # TODO: add bot commands and answers here
        ch: discord.TextChannel = msg.channel
        await ch.send("ein???")
    

    async def can_process_message(self, msg: discord.Message) -> bool:
        if msg.channel is discord.DMChannel:
            # ignore direct messages to bot
            return

        if not isinstance(msg.channel, discord.TextChannel):
            return False

        if msg.author == self.user:
            # ignore my own messages :)
            return False

        if self.user in msg.mentions:
            await self.process_mention(msg)
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
        
        for url in self.url_extractor.find_urls(text):
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
            
        if has_urls:
            # add voting reactions to message
            await msg.add_reaction(emojis.ARROW_UP)
            await msg.add_reaction(emojis.ARROW_DOWN)
            await msg.add_reaction(emojis.ROFL)
            await msg.add_reaction(emojis.OLD_MAN)
