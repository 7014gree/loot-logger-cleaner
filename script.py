import os
import json
from datetime import datetime

log_file_paths = os.listdir('data/npc')
start_date = datetime(2022, 1, 19, 0, 0)
end_date = datetime(2022, 3, 16, 23, 59)


for log_name in log_file_paths:
    leagues_list = []
    non_leagues_list = []

    with open(f'data/npc/{log_name}', 'r') as read_file:
        for line in read_file:
            json_data = json.loads(line)
            if start_date < datetime.strptime(json_data['date'], '%b %d, %Y, %H:%M:%S %p') < end_date:
                leagues_list.append(json_data)
            else:
                non_leagues_list.append(json_data)

    with open(f'data/leagues/{log_name}', 'w') as leagues_file:
        for entry in leagues_list:
            leagues_file.write(f"{str(entry)}\n")

    with open(f'data/non-leagues/{log_name}', 'w') as non_leagues_file:
        for entry in non_leagues_list:
            non_leagues_file.write(f"{str(entry)}\n")