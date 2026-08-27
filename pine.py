import os
import sys
import subprocess
from pathlib import Path

if getattr(sys, 'frozen', False):
    script_dir = Path(os.path.dirname(sys.executable))
else:
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))

packages_dir = script_dir / "packages"

print("=" * 50)
print("Pine Language Installer")
print("=" * 50)

if not packages_dir.exists():
    print(f"ERROR: packages folder not found at: {packages_dir}")
    input("Press Enter to exit...")
    sys.exit(1)

files_to_run = ["fix_icon.py", "pine_installer.py", "run_pi.py"]

for file_name in files_to_run:
    file_path = packages_dir / file_name
    if file_path.exists():
        print(f"\nExecuting: {file_name}")
        print("-" * 30)
        subprocess.run([sys.executable, str(file_path)])
    else:
        print(f"\nWARNING: {file_name} not found in packages folder")

print("\n" + "=" * 50)
print("Installation complete!")
print("=" * 50)
input("Press Enter to exit...")
