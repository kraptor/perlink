# Copyright (c) 2021 kraptor
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import perlink.config
import perlink.bot


def test_allow_raw_uris():
    config = perlink.config.load()
    config.detect_raw_links = True
    bot = perlink.bot.PerlinkBot(config)

    MESSAGES = [
        ("itch.io", ["itch.io"]),
        ("itch.io youtube.com", ["itch.io", "youtube.com"]),
        ("http://itch.io", ["http://itch.io"]),
        ("", []),
        (None, []),
    ]

    for msg, expected in MESSAGES:
        urls = list(bot.find_urls(msg))
        assert urls == expected


def test_only_non_raw_uris():
    config = perlink.config.load()
    config.detect_raw_links = False
    bot = perlink.bot.PerlinkBot(config)

    MESSAGES = [
        ("itch.io", []),
        ("itch.io http://youtube.com", ["http://youtube.com"]),
        ("", []),
        (None, []),
    ]

    for msg, expected in MESSAGES:
        urls = list(bot.find_urls(msg))
        assert urls == expected  


def test_ignore_links_with_secrets():
    config = perlink.config.load()
    config.detect_raw_links = True
    config.ignore_links_with_secrets = True
    config.valid_link_protocols.add("http")
    bot = perlink.bot.PerlinkBot(config)

    MESSAGES = [
        ("a:a@itch.io", []),
        ("http://theuser:thepassword@example.com", []),
        ("http://:thepassword@example.com", []),
        ("http://theuser:@example.com", []),
        ("", []),
        (None, []),
    ]

    for msg, expected in MESSAGES:
        urls = list(bot.find_urls(msg))
        assert urls == expected
    

def test_keep_links_with_secrets():
    config = perlink.config.load()
    config.detect_raw_links = True
    config.ignore_links_with_secrets = False
    config.valid_link_protocols.add("http")
    bot = perlink.bot.PerlinkBot(config)

    MESSAGES = [
        ("http://theuser:thepassword@example.com", ["http://theuser:thepassword@example.com"]),
        ("http://:thepassword@example.com", ["http://:thepassword@example.com"]),
        ("http://theuser:@example.com", ["http://theuser:@example.com"]),
        ("", []),
        (None, []),
    ]

    for msg, expected in MESSAGES:
        urls = list(bot.find_urls(msg))
        assert urls == expected

