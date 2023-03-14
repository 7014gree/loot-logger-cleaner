import os
import json
from datetime import datetime, timedelta

def make_directory(name: str):
    try:
        os.mkdir(f'data/{name}-leagues')
    except FileExistsError:
        print(f'Folder already exists for /data/{name}-leagues.\nAny files which exist in /data/{name} will be overwritten in /data/{name}-leagues.')

def delete_file(name: str, log_name: str):
    try:
        os.remove(f'data/{name}-leagues/{log_name}')
    except FileNotFoundError:
        pass

def date_inputs() -> tuple([datetime, datetime]):
    start_str = input("Enter start date in format 'DD/MM/YY': ")
    end_str = input("Enter end date in format 'DD/MM/YY': ")
    try:
        start_date = parse_input_dates(start_str)
        end_date = parse_input_dates(end_str)  + timedelta(hours=24) - timedelta(seconds=1) # To get 23:59:59
        if end_date < start_date:
            raise ValueError(f"end date '{end_date}' is before start date '{start_date}'")
    except ValueError as e:
        print(f"Enter valid date strings: {str(e)}.")
        return date_inputs()
    except TypeError as e:
        print(f"Enter valid date strings: {str(e)}.")
        return date_inputs()
    
    return start_date, end_date

def parse_input_dates(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d/%m/%y')

def filter_data(name: str, log_name: str, start_date: datetime = datetime(2022, 1, 26, 0, 0), end_date: datetime = datetime(2022, 3, 16, 23, 59)):
    # Ensures file is overwritten by just deleting it
    delete_file(name, log_name)
    delete_file(f'{name}-non', log_name)

    with open(f'data/{name}/{log_name}', 'r') as read_file, open(f'data/{name}-leagues/{log_name}', 'a') as leagues_file, open(f'data/{name}-non-leagues/{log_name}', 'a') as non_leagues_file:
        for line in read_file:
            json_data = json.loads(line)
            if start_date < datetime.strptime(json_data['date'], '%b %d, %Y, %H:%M:%S %p') < end_date:
                leagues_file.write(line) # Automatically adds line break for append mode
            else:
                non_leagues_file.write(line)

if __name__ == "__main__":
    while True:
        print(os.listdir('data'))
        name = input("Enter a folder name to filter: ")
        while os.path.exists(f'data/{name}') == False:
            name = input("Enter a folder name that exists: ")
        
        make_directory(name)
        make_directory(f'{name}-non')

        log_file_paths = os.listdir(f'data/{name}')
        
        kwargs = {'name': name}

        # Optional to take an input here and convert to datetime
        if input("Enter 'Y' to input dates: ").upper() == "Y":
            start_date, end_date = date_inputs()
            kwargs.update({'start_date': start_date, 'end_date': end_date})
        else:
            print('Default dates used.')

        for log_name in log_file_paths:
            filter_data(**kwargs, log_name=log_name)

        if input(f"Filter complete for /data/{name}.\nEnter 'Y' to filter another folder: ").upper() != "Y":
            break
    