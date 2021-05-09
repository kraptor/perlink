<!--
 Copyright (c) 2021 kraptor
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# PerLink Noise Bot

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-ffc200.svg)](https://www.python.org/)
![Tests](https://github.com/kraptor/perlink/workflows/tests/badge.svg)

PerLink Noise is a small bot that tracks upvotes to links in discord channels by adding emojis to messages. Users only have to click on the emojis to update/downvote a link.

It uses as its database a Google Spreadsheet, so it's easy to extract realtime stats, etc. by administrators.

## Development environment

In order to hack on the project you need `Poetry` installed:

* https://python-poetry.org/

Then you can initialize the development environment:

    > poetry install --no-root


To check if tests pass:

    > poetry run pytest -v


## Configuration (TODO)

TODO:
* Configuration class
* Google json auth file

## Deploying (TODO)