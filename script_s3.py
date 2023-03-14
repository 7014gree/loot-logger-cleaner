import os
import json
from datetime import datetime, timedelta
from tqdm import tqdm
import boto3
from io import TextIOWrapper


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

def date_inputs(filter_kwargs) -> dict:
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
        return filter_kwargs.update({'start_date': start_date, 'end_date': end_date})
    else:
        print("Default dates used.")
        return filter_kwargs

def parse_input_dates(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d/%m/%y')

def filter_data_s3(s3_client, bucket_name: str, name: str, timestamp: 'str', log_name: str, start_date: datetime = datetime(2022, 1, 26, 0, 0), end_date: datetime = datetime(2022, 3, 16, 23, 59)):
    log_file_obj = s3_client.get_object(Bucket=bucket_name, Key=log_name) # Get object from s3 bucket
    log_file_contents = TextIOWrapper(log_file_obj['Body']) # Retrieve text in a format that can be read line by line
    log_name_str = log_name[len(name):] # Removes 'name/' from start of file name

    with open(f'data/{name}-{timestamp}-leagues/{log_name_str}', 'a') as leagues_file, open(f'data/{name}-{timestamp}-non-leagues/{log_name_str}', 'a') as non_leagues_file:
        for i, line in enumerate(log_file_contents):
            line = f'{line.strip()}\n' # For some reason there was an extra line break when reading the file, fixed by removing line breaks then adding one back
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
        progress_bar.set_description(f"Current file: {log_name[len(name) + 1:]}")
        filter_data_s3(**filter_kwargs, log_name=log_name)

if __name__ == "__main__":

    bucket_name = 'loot-logger-data-ea2cbe2a-7ec4-40ae-9480-2423d82c28ca'
    s3_client = boto3.client('s3')

    response = s3_client.list_objects_v2(Bucket=bucket_name,Delimiter='/')
    folder_names = [folder['Prefix'][:-1] for folder in response['CommonPrefixes']]

    while True:
        print(f"Folder names: {folder_names}")
        name = input("Enter a folder name to filter: ")
        while name not in folder_names:
            name = input("Enter a folder name that exists: ")
        
        timestamp = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        make_directory(f"{name}-{timestamp}")
        make_directory(f"{name}-{timestamp}-non")

        log_file_paths = [object['Key'] for object in s3_client.list_objects_v2(Bucket=bucket_name,Prefix=f'{name}/')['Contents']]
        
        filter_kwargs = {'name': name, 'timestamp': timestamp, 's3_client': s3_client, 'bucket_name': bucket_name}

        filter_kwargs = date_inputs(filter_kwargs)

        iterate_log_files(log_file_paths, filter_kwargs)
        
        if input(f"Filter complete for {name}-{timestamp}.\nEnter 'Y' to filter another folder: ").upper() != "Y":
            break
    