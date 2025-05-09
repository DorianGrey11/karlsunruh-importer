import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from services.sync_service import run_sync

if __name__ == "__main__":
    run_sync()
