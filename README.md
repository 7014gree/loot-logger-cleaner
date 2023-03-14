# loot-logger-cleaner
Scripts to filter out leagues data from loot logger runelite plugin.

## Problem
- Loot logger runelite plugin tracks all loot received from npcs in runescape
- Tracks based on username (or something equivalent, such as email address or user ID)
- During the Leagues 3 game mode, loot tracked was not differentiated from loot received in the main game
- As a result, the loot logger data contains Leagues 3 data, which we do not want
- Format of this data is .log files, which appears to be in JSON format. See example file `alchemical hydra.log`, extract of a few lines shown below:

`{"name":"Alchemical Hydra","level":426,"killCount":1,"type":"NPC","drops":[{"name":"Blood rune","id":565,"quantity":279,"price":279},{"name":"Ranging potion(3)","id":169,"quantity":1,"price":354},{"name":"Super restore(3)","id":3026,"quantity":1,"price":11704},{"name":"Super restore(3)","id":3026,"quantity":1,"price":11704}],"date":"Feb 4, 2022, 2:01:14 AM"}
{"name":"Alchemical Hydra","level":426,"killCount":2,"type":"NPC","drops":[{"name":"Brimstone key","id":23083,"quantity":1,"price":0},{"name":"Coins","id":995,"quantity":51184,"price":1},{"name":"Ranging potion(3)","id":169,"quantity":1,"price":277},{"name":"Super restore(3)","id":3026,"quantity":1,"price":11677},{"name":"Super restore(3)","id":3026,"quantity":1,"price":11677}],"date":"Feb 4, 2022, 3:19:44 AM"}
{"name":"Alchemical Hydra","level":426,"killCount":3,"type":"NPC","drops":[{"name":"Hydra\u0027s claw","id":22966,"quantity":1,"price":48725000},{"name":"Chaos rune","id":562,"quantity":293,"price":58}],"date":"Feb 4, 2022, 3:22:08 AM"}`

## Approach
- Use `os` to list all .log files within the data folder
- Iterate through all .log files
- Read the data as JSON using `json.load()`
- Convert the `data['date']` value to datetime format using `datetime.strptime()`
- Check if the date value is within the period in which Leagues 3 was running (19th Jan 2022 - 16th March 2022)
- If the date value is within the Leagues 3 timeframe, write it to [name]-leagues.log
- If the date data is outside of the Leagues 3 timeframe, write it [name]-non-leagues.log

## Issues

### Jupyter Notebooks and virtualenv
- In order to speed up development/debugging I wanted to use Jupyter Notebooks
- Also thought I should use a virtual environment as I've been neglecting using them, when it is better practice to use them
- Had issues getting Jupyter Notebooks to run in my virtual environment - eventually ended up creating a new kernel to run the notebook in, '.venv'

### JSON format
- `json.load` did not work for the .log files
- Current solution is to read the data in line by line and convert to JSON format
- Investigated why the .log files were not in the correct format using https://jsonlint.com/
- The cause is that the .log files do not start with `[`, do not end with `]`, and the JSON objects contained are separated with linebreaks instead of commas
- Seems like only way to fix this would involve iterating through the file line by line, which seems like it would be at least as slow as the current approach

## Extensions
- Refactored to use functions
- Added several try-except blocks
- Added script which conencts to s3 bucket
- Added progress bar using tqdm