import sys
import os

local_app_data = os.environ.get('LOCALAPPDATA', 'C:/')
pine_dir = os.path.join(local_app_data, 'Pine')
sys.path.insert(0, pine_dir)

from pine_runtime import PineRuntime

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.path.exists(filename):
            runtime = PineRuntime()
            runtime.run_file(filename)
        else:
            print(f"File not found: {filename}")
    else:
        print("Usage: run_pi.py <filename.pi>")
        print("Or double-click a .pi file to run it")
        input("Press Enter to exit...")
