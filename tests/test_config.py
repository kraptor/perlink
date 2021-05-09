# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import perlink.config


def fake_environment():
    os.environ["LOG_FORMAT"] = "LOG_FORMAT"
    os.environ["BOT_ID"] = "BOT_ID"
    os.environ["DATABASE_FILE"]  = "DATABASE_FILE"
    os.environ["DISCORD_TOKEN"]  = "DISCORD_TOKEN"
    os.environ["MAX_VOTE_HOURS"] = "666"
    os.environ["ALLOW_NSFW_CHANNELS"] = "false"
    os.environ["DETECT_RAW_LINKS"] = "true"
    os.environ["VALID_LINK_PROTOCOLS"] = "VALID_LINK_PROTOCOLS"
    os.environ["IGNORE_LINKS_WITH_SECRETS"] = "true"

def clear_environment():
    del os.environ["LOG_FORMAT"]
    del os.environ["BOT_ID"]
    del os.environ["DATABASE_FILE"] 
    del os.environ["DISCORD_TOKEN"] 
    del os.environ["MAX_VOTE_HOURS"]
    del os.environ["ALLOW_NSFW_CHANNELS"]
    del os.environ["DETECT_RAW_LINKS"]
    del os.environ["VALID_LINK_PROTOCOLS"]
    del os.environ["IGNORE_LINKS_WITH_SECRETS"]


def test_config():
    fake_environment()
    config = perlink.config.load()
    try:
        assert config.log_format == "LOG_FORMAT"
        assert config.bot_id == "BOT_ID"
        assert config.db_file == "DATABASE_FILE"
        assert config.discord_token == "DISCORD_TOKEN"
        assert config.max_vote_hours == 666
        assert config.allow_nsfw_channels == False
        assert config.detect_raw_links == True
        assert config.valid_link_protocols == {"VALID_LINK_PROTOCOLS"}
        assert config.ignore_links_with_secrets == True
    finally:
        clear_environment()