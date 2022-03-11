import json
import numpy as np
import os
import pandas as pd
from pathlib import Path
import sys
import zipfile

def get_input(
    local: bool=False, # Flag to indicate local vs C2D
):
    if local:
        print("Reading local bci data directory...")

        # Root directory for dataset
        data_dir = Path('data/bci')

        return data_dir

    print("Reading from C2D container...")

    dids = os.getenv('DIDS', None) # decentralized identifiers representing data assets

    if not dids:
        print("No DIDs found in environment. Aborting.")
        return

    dids = json.loads(dids)

    did = dids[0]
    print(f"DID: {did}")

    cwd = os.getcwd()
    print('cwd', cwd)

    filename = Path(f'/data/inputs/{did}/0')  # 0 for metadata service
    print(f"Asset file {filename} exists: {os.path.exists(filename)}")

    print('ls2', os.listdir(f'/data/inputs/{did}'))

    try:
        with open(filename) as datafile:
            print('check if its a html')
            print(type(datafile))
            data = datafile.read()
            print(data)
            print('_____________________________________________')
    except:
        print('except - check if its a html')
        print('_____________________________________________')
        pass

    try:
        print('lets see if its unzipped')
        print(type(filename))
        fns = []
        for root, dirs, files in os.walk(str(filename)):
            path = root.split(os.sep)
            print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                fn = os.path.join(root,file)
                if fn.split('.')[-1] in ['jpeg', 'jpg', 'png']:
                    fns.append(fn)
                print(len(path) * '---', file)

    print("Extracting data...")

    data_dir = Path('/data/extracted')
    if not data_dir.exists():
        data_dir.mkdir()

    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(data_dir)

    return data_dir

def run_bci(local=False):

    print("Getting input...")
    data_dir = get_input(local)

    print("Listing files...")
    data_path = []
    for root, dirs, files in os.walk(data_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            fn = os.path.join(root,file)
            if fn.split('.')[-1] in ['feather']:
                data_path.append(fn)
            print(len(path) * '---', file)

    print("Reading files...")
    datas = []
    for path in data_path:
        datas.append(np.array(pd.read_feather(data_path[0])))
    data = np.stack(datas)

    print("Data shape:", data.shape)

    return data

if __name__ == "__main__":
    local = (len(sys.argv) == 2 and sys.argv[1] == "local")
    run_bci(local)