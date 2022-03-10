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
        print('type', type(filename))
        print('ls4', filename)

        return filename

def run_bci(local=False):
    print('testing')

    filename = get_input(local)
    if not filename:
        print("Could not retrieve filename.")
        return

    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('.')

    print('ls3', os.listdir(f'/data/inputs/1F7eEDD29299F6aa33d4711b8e6e122466f199e1/0'))

    # print(f"data folder exists: {os.path.exists(str(data))}")

    # for root, dirs, files in os.walk(str(data)):
    #     path = root.split(os.sep)
    #     print((len(path) - 1) * '---', os.path.basename(root))
    #     for file in files:
    #         fn = os.path.join(root,file)
    #         if fn.split('.')[-1] in ['jpeg', 'jpg', 'png']:
    #             fns.append(fn)
    #         print(len(path) * '---', file)



if __name__ == "__main__":
    local = (len(sys.argv) == 2 and sys.argv[1] == "local")
    run_bci(local)