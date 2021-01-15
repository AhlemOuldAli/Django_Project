import os
import io
import fnmatch
from json import load, dump
import pandas as pd
from Opticharge.settings import BASE_DIR

def make_dirs_for_file(path):
    '''make dir for files'''
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass

def guess_path_type(path):
    '''guess what type of file'''
    if os.path.isfile(path):
        return 'File'
    if os.path.isdir(path):
        return 'Directory'
    if os.path.islink(path):
        return 'Symbolic Link'
    if os.path.ismount(path):
        return 'Mount Point'
    return 'Path'

def exist(path, overwrite=False, display_info=True):
    if os.path.exists(path):
        if overwrite:
            if display_info:
                print(f'{guess_path_type(path)}: {path} exists. Overwrite.')
            os.remove(path)
            return False
        if display_info:
            print(f'{guess_path_type(path)}: {path} exists.')
        return True
    if display_info:
        print(f'{guess_path_type(path)}: {path} does not exist.')
    return False

def load_instance(json_file):
    if exist(path=json_file, overwrite=False, display_info=True):
        with io.open(json_file, 'rt', newline='') as file_object:
            return load(file_object)
    return None

def calculate_distance(customer1, customer2):
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + \
            (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5

def text2jsonCust(customize=False):
    text_data_dir = os.path.join(BASE_DIR, 'dataC', 'text_customizeC' if customize else 'text')
    json_data_dir = os.path.join(BASE_DIR, 'dataC', 'json_customizeC' if customize else 'json')
    for text_file in map(lambda text_filename: os.path.join(text_data_dir, text_filename),fnmatch.filter(os.listdir(text_data_dir), '*.txt')):
        json_data = {}
        with io.open(text_file, 'rt', newline='') as file_object:
            for line_count, line in enumerate(file_object, start=1):
                if line_count in [2, 3, 4]:
                    #du vide
                    pass
                elif line_count == 1:
                    # <Instance name>
                    json_data['instanceC_name'] = line.strip()
                elif line_count == 5:
                    # Custom number = 0, depart
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <type vehicle>,
                    values = line.strip().split()
                    json_data['depart'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'type vehicle': int(values[4]),
                        #'ready_time': float(values[5]),
                        #'due_time': float(values[6]),
                        #'service_time': float(values[7]),
                    }
                else:
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Type vehicle>
                    values = line.strip().split()
                    json_data[f'customer_{values[0]}'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'type_vehicle': int(values[4]),
                        #'ready_time': float(values[5]),
                        #'due_time': float(values[6]),
                        #'service_time': float(values[7]),
                    }
        customers = ['depart'] + [f'customer_{x}' for x in range(1, 101)]
        json_data['distance_matrix'] = [[calculate_distance(json_data[customer1],
                json_data[customer2]) for customer1 in customers] for customer2 in customers]

        json_file_name = f"{json_data['instanceC_name']}.json"
        json_file = os.path.join(json_data_dir, json_file_name)
        print(f'Write to file: {json_file}')
        make_dirs_for_file(path=json_file)
        with io.open(json_file, 'wt', newline='') as file_object:
            dump(json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))

def text2jsonVehi(customize=False):
    text_data_dir = os.path.join(BASE_DIR, 'dataV', 'text_customizeV' if customize else 'text')
    json_data_dir = os.path.join(BASE_DIR, 'dataV', 'json_customizeV' if customize else 'json')
    for text_file in map(lambda text_filename: os.path.join(text_data_dir, text_filename),fnmatch.filter(os.listdir(text_data_dir), '*.txt')):
        json_data = {}
        with io.open(text_file, 'rt', newline='') as file_object:
            for line_count, line in enumerate(file_object, start=1):
                if line_count in [2,3]:
                    #du vide
                    pass
                elif line_count == 1:
                    # <Instance name>
                    json_data['instanceV_name'] = line.strip()
                else:
                    # <VEHICLE ID>, <VEHICLE NAME>, <VEHICLE CAPACITY>,
                    # ... <ID TYPE VEHICLE>
                    values = line.strip().split()
                    json_data[f'vehicle_{values[0]}'] = {
                        'vehicle_name':values[1],
                        'registration':values[2],
                        'capacity': float(values[3]),
                        'type_vehicle': int(values[4]),
                    }
    vehicles = [f'vehicle_{x}' for x in range(1, 101)]
    json_file_name = f"{json_data['instanceV_name']}.json"
    json_file = os.path.join(json_data_dir, json_file_name)
    print(f'Write to file: {json_file}')
    make_dirs_for_file(path=json_file)
    with io.open(json_file, 'wt', newline='') as file_object:
        dump(json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))