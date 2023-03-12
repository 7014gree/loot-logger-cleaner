# Given path for folder containing .log files
# Writes paths for .log files to a list
# Iterates through each .log file
# Reads json
# If date for a line is within leagues timeframe (19th Jan - 16th March), writes to [name]-leagues.log
# If date is not in that time frame, writes to [name].log
# Know that first week was skipped, so 19th Jan - 26th Jan also written to a [nane]-leagues-exception.log

import os
import json