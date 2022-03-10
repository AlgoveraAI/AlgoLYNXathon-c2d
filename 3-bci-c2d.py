import sys
import os
import json
from pathlib import Path

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

        return filename

def run_bci(local=False):
    print('testing')
    pass

if __name__ == "__main__":
    local = (len(sys.argv) == 2 and sys.argv[1] == "local")
    run_bci(local)