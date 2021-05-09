<!--
 Copyright (c) 2021 kraptor
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# PerLink Noise Bot

PerLink Noise is a small bot that tracks upvotes to links in discord channels by adding emojis to messages. Users only have to click on the emojis to update/downvote a link.

It uses as database a Google Spreadsheet, so it's easy to extract realtime stats, etc. by administrators.

## Development environment

In order to hack on the project you need `Poetry` installed:

* https://python-poetry.org/

Then you can initialize the development environment:

    > poetry install --no-root
