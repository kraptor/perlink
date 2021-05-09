# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
import logging
import datetime
import recordclass

import gspread
import gspread.models
import gspread_asyncio
import discord
import discord.ext.tasks
import discord.ext.commands
import google.oauth2.service_account

import perlink.config


log = logging.getLogger(__name__)


DbEntry = recordclass.recordclass("DbEntry", [
    "is_saved", "ch_id", "channel", "auth_id", "author", "msg_id", 
    "url", "created", "upvotes", "downvotes", "oldvotes", "funnyvotes", 
    "allvotes"
])


VOTE_COLLECT_INTERVAL_SECONDS=60*3
VOTE_SAVE_INTERVAL_SECONDS=60*5


class Database(discord.ext.commands.Cog):
    def __init__(self, bot) -> None:
        log.debug("Initializing database...")
        super().__init__()
        self._bot: "perlink.bot.PerlinkBot" = bot
        self._gspread_manager = gspread_asyncio.AsyncioGspreadClientManager(self._authenticate)
        self._cached_messages: typing.Mapping[str, DbEntry] = {}
        self._database_file_id = bot.config.db_file
        self._max_vote_hours = bot.config.max_vote_hours
        self.save_messages.start()
        self.collect_votes.start()


    def _authenticate(self):
        log.debug("Authenticating bot against Google...")
        filename = self._bot.config.google_auth_file
        creds = google.oauth2.service_account.Credentials.from_service_account_file(filename)
        scoped = creds.with_scopes([
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ])
        log.debug("Auth ok!")
        return scoped


    def cog_unload(self):
        self.save_messages.cancel()
        self.collect_votes.cancel()


    @discord.ext.tasks.loop(seconds=VOTE_SAVE_INTERVAL_SECONDS)
    async def save_messages(self):
        if len(self._cached_messages) == 0:
            return

        log.info("Saving pending messages...")
        start  = datetime.datetime.utcnow()
        client = await self._gspread_manager.authorize()
        file   = await client.open_by_key(self._database_file_id)
        sheet  = await file.get_worksheet(0)

        # store as a list, so the dict is still mutable while we perform the
        # save operation, therefore other coroutines can add items in the
        # meating if they want to :)
        items = list(self._cached_messages.items())
        
        for msg_id, entry in items:
            entry: DbEntry
            if entry.is_saved: continue
            
            row  = await self.find_row_for_message(str(msg_id), sheet=sheet)
            data = list(entry)[1:] # skip 'is_saved' field
            entry.is_saved = True

            try:
                if row:                
                    first = gspread.utils.rowcol_to_a1(row, 1)
                    last  = gspread.utils.rowcol_to_a1(row, len(data))
                    range = await sheet.range(f"{first}:{last}")
                    index = 0
                    for c in range:
                        c: gspread.models.Cell
                        v = data[index]
                        if isinstance(v, datetime.datetime):
                            v = v.isoformat()
                        c.value = v
                        index += 1
                    await sheet.update_cells(range)
                else:
                    await sheet.append_row(data)
            except Exception as e:
                entry.is_saved = False
                raise e

        delta = datetime.datetime.utcnow() - start
        log.debug(f"Saved messages in {delta.total_seconds()} seconds.")
        self.clear_expired_and_saved()


    @discord.ext.tasks.loop(seconds=VOTE_COLLECT_INTERVAL_SECONDS)
    async def collect_votes(self):
        bot = self._bot
        inspected = 0
        processed = 0

        start = datetime.datetime.utcnow()
        max_time = datetime.datetime.utcnow() - datetime.timedelta(hours=self._max_vote_hours)
        log.info(f"Collecting votes since: {max_time.isoformat()}")

        for channel in bot.get_all_channels():
            if not isinstance(channel, discord.TextChannel): continue
            if channel.is_nsfw(): continue # do not include NSFW channels
            
            async for message in channel.history(limit=None, after=max_time, oldest_first=True):
                message: discord.Message
                inspected += 1
                if bot.can_process_message(message):
                    await bot.inspect_and_process_message(message)
                    processed += 1

        if processed > 0:
            delta = datetime.datetime.utcnow() - start
            log.info(f"Collecting votes stats: {processed} processed of {inspected} inspected messages in {delta.total_seconds()} seconds.")


    async def find_row_for_message(self, msg_id: str, *, sheet: gspread_asyncio.AsyncioGspreadWorksheet) -> typing.Optional[int]:
        try:
            cell = await sheet.find(msg_id)
            return cell.row
        except gspread.exceptions.CellNotFound:
            return None


    def clear_expired_and_saved(self):
        to_delete = []

        for item, entry in self._cached_messages.items():
            entry: DbEntry
            if not entry.is_saved:
                continue
            created = datetime.datetime.fromisoformat(entry.created)
            max_time = datetime.datetime.utcnow() - datetime.timedelta(hours=self._max_vote_hours)
            if created < max_time:
                to_delete.append(item)

        for item in to_delete:
            del self._cached_messages[item]

        log.debug(f"{len(to_delete)} cache entries evicted. In cache: {len(self._cached_messages)}")


    def store_entry(self, entry: DbEntry):
        log.debug(f"Storing entry: {entry}")

        if entry.msg_id in self._cached_messages:
            # only add if current saved entry is the same as the current one (except for is_saved)
            current_entry = self._cached_messages[entry.msg_id]
            state = entry.is_saved
            entry.is_saved = True
            if entry == current_entry:
                return
            entry.is_saved = state

        entry.ch_id = str(entry.ch_id)
        entry.msg_id = str(entry.msg_id)
        entry.auth_id = str(entry.auth_id)
        self._cached_messages[entry.msg_id] = entry