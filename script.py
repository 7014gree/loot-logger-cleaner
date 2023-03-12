import os
import json
from datetime import datetime


# Three folders are npc (normal kills), event (chests, raids, clues, implings, etc.), and pickpocket
name = "pickpocket"


log_file_paths = os.listdir(f'data/{name}')

# Actually started playing leagues after the first week
start_date = datetime(2022, 1, 26, 0, 0)
end_date = datetime(2022, 3, 16, 23, 59)


# Could expand this to delete and remake folders if they already exist (and hence likely already contain files)
try:
    os.mkdir(f'data/{name}-leagues')
except FileExistsError:
    pass 

try:
    os.mkdir(f'data/{name}-non-leagues')
except FileExistsError:
    pass 

# Read file, split leagues and non-leagues into separate lists, write lists to respective files
for log_name in log_file_paths:
    leagues_list = []
    non_leagues_list = []

    with open(f'data/{name}/{log_name}', 'r') as read_file:
        for line in read_file:
            json_data = json.loads(line)
            if start_date < datetime.strptime(json_data['date'], '%b %d, %Y, %H:%M:%S %p') < end_date:
                leagues_list.append(json_data)
            else:
                non_leagues_list.append(json_data)

    with open(f'data/{name}-leagues/{log_name}', 'w') as leagues_file:
        for entry in leagues_list:
            leagues_file.write(f"{str(entry)}\n")

    with open(f'data/{name}-non-leagues/{log_name}', 'w') as non_leagues_file:
        for entry in non_leagues_list:
            non_leagues_file.write(f"{str(entry)}\n")