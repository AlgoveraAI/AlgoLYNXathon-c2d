import sys
import os
import json
from pathlib import Path
import zipfile

def get_input(local=False):
    if local:
        print("Reading local directory.")

        # Root directory for dataset
        filename = Path('data/punks/tealpunks')

        return filename

    dids = os.getenv('DIDS', None)

    if not dids:
        print("No DIDs found in environment. Aborting.")
        return

    dids = json.loads(dids)

    cwd = os.getcwd()
    print('cwd', cwd)

    for did in dids:
        print('ls', f'/data/inputs/{did}/0')
        print('ls2', os.listdir(f'/data/inputs/{did}'))
        filename = Path(f'/data/inputs/{did}/0')  # 0 for metadata service
        print(f"Reading asset file {filename}.")
        # print('ls4', os.listdir(filename))

        return filename

def run_bci(local=False):
    print("Getting input...")

    filename = get_input(local)
    if not filename:
        print("Could not retrieve filename.")
        return

    print("Extracting data...")

    data_path = Path('/data/extracted')
    if not data_path.exists():
        data_path.mkdir()

    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(data_path)

    print('ls3', os.listdir(data_path))

    # print(f"Data folder exists: {os.path.exists(str(data))}")

    fns = []
    for root, dirs, files in os.walk(data_path):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            fn = os.path.join(root,file)
            if fn.split('.')[-1] in ['feather']:
                fns.append(fn)
            print(len(path) * '---', file)



if __name__ == "__main__":
    local = (len(sys.argv) == 2 and sys.argv[1] == "local")
    run_bci(local)