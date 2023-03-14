import os
import json
from datetime import datetime, timedelta
from tqdm import tqdm
from time import sleep

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

def date_inputs(filter_kwargs: dict) -> dict:
    if input("Enter 'Y' to input dates: ").upper() == "Y":
        start_str = input("Enter start date in format 'DD/MM/YY': ")
        end_str = input("Enter end date in format 'DD/MM/YY': ")
        try:
            start_date = parse_input_dates(start_str)
            end_date = parse_input_dates(end_str)  + timedelta(hours=24) - timedelta(seconds=1) # To get 23:59:59
            if end_date < start_date:
                raise ValueError(f"end date '{end_date}' is before start date '{start_date}'")
        except (ValueError, TypeError) as e:
            print(f"Enter valid date strings: {str(e)}.")
            return date_inputs()
        filter_kwargs.update({'start_date': start_date, 'end_date': end_date})
        return filter_kwargs
    else:
        print("Default dates used.")
        return filter_kwargs

def parse_input_dates(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d/%m/%y')

def filter_data(name: str, log_name: str, start_date: datetime = datetime(2022, 1, 26, 0, 0), end_date: datetime = datetime(2022, 3, 16, 23, 59)):
    # Ensures file is overwritten by just deleting it
    delete_file(name, log_name)
    delete_file(f'{name}-non', log_name)

    with open(f'data/{name}/{log_name}', 'r') as read_file, open(f'data/{name}-leagues/{log_name}', 'a') as leagues_file, open(f'data/{name}-non-leagues/{log_name}', 'a') as non_leagues_file:
        for i, line in enumerate(read_file):
            try:
                json_data = json.loads(line)
                try:
                    if start_date < datetime.strptime(json_data['date'], '%b %d, %Y, %H:%M:%S %p') < end_date:
                        leagues_file.write(line)
                    else:
                        non_leagues_file.write(line)
                except (ValueError, TypeError):
                    print(f"\nError loading line {i + 1} from '{log_name}': date in unexpected format. Data excluded from output.")
            except json.JSONDecodeError:
                print(f"\nError loading line {i + 1} from '{log_name}': data not in valid JSON format. Data excluded from output.")

def iterate_log_files(log_file_paths: list, filter_kwargs: dict):
    progress_bar = tqdm(log_file_paths, total=len(log_file_paths))
    for log_name in progress_bar:
        progress_bar.set_description(f"Current file: {log_name}")
        filter_data(**filter_kwargs, log_name=log_name)
        sleep(0.1) # File runs too quick to see progress bar


if __name__ == "__main__":
    while True:
        print(os.listdir('data'))
        name = input("Enter a folder name to filter: ")
        while os.path.exists(f'data/{name}') == False:
            name = input("Enter a folder name that exists: ")
        
        make_directory(name)
        make_directory(f'{name}-non')

        log_file_paths = os.listdir(f'data/{name}')
        
        # If user inputs dates, returns dictionary including dates. Otherwise returns dictionary only containing name.
        filter_kwargs = date_inputs({'name': name})

        iterate_log_files(log_file_paths, filter_kwargs)
        
        if input(f"Filter complete for /data/{name}.\nEnter 'Y' to filter another folder: ").upper() != "Y":
            break
    