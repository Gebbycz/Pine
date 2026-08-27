import winreg
import os
import sys
import ctypes

print("Fixing .pi icon...")

if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(script_dir, "Pine.ico")
icon_path = os.path.abspath(icon_path)

print(f"Icon path: {icon_path}")
print(f"Icon exists: {os.path.exists(icon_path)}")

if not os.path.exists(icon_path):
    print("ERROR: Pine.ico not found!")
    sys.exit(1)

print("Deleting old registry entries...")
registry_paths = [
    r"Software\Classes\.pi\DefaultIcon",
    r"Software\Classes\PineScript\DefaultIcon",
    r"Software\Classes\PineFile\DefaultIcon",
    r"Software\Classes\Pine.Script\DefaultIcon",
]

for key_path in registry_paths:
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        print(f"  Deleted: {key_path}")
    except:
        pass

print("Setting icon on .pi extension...")
try:
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pi")
    winreg.SetValue(key, "", winreg.REG_SZ, "PineScript")
    winreg.CloseKey(key)
    
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pi\DefaultIcon")
    winreg.SetValue(key, "", winreg.REG_SZ, icon_path)
    winreg.CloseKey(key)
    print("  Icon set on .pi!")
except Exception as e:
    print(f"  Error: {e}")

print("Setting icon on PineScript...")
try:
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\PineScript")
    winreg.SetValue(key, "", winreg.REG_SZ, "Pine Script")
    winreg.CloseKey(key)
    
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\PineScript\DefaultIcon")
    winreg.SetValue(key, "", winreg.REG_SZ, icon_path)
    winreg.CloseKey(key)
    print("  Icon set on PineScript!")
except Exception as e:
    print(f"  Error: {e}")

print("Refreshing icon cache...")
try:
    os.system("ie4uinit.exe -show")
    ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
    print("  Icon cache refreshed!")
except Exception as e:
    print(f"  Error: {e}")

print("\nDone! Restart Explorer to see changes.")
print("Run: taskkill /f /im explorer.exe && start explorer.exe")
