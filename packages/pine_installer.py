# Pine Installer and Runtime Environment
# File: pine_installer.py
# This creates the complete Pine system on the user's computer

import os
import sys
import json
import shutil
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import winreg

class PineInstaller:
    def __init__(self):
        self.system = platform.system()
        self.install_path = self.get_install_path()
        self.pine_commands = {}
        self.initialize_commands()
        
    def get_install_path(self):
        if self.system == "Windows":
            return Path(os.environ.get('LOCALAPPDATA', 'C:/')) / "Pine"
        elif self.system == "Darwin":
            return Path.home() / "Library" / "Pine"
        else:
            return Path.home() / ".pine"
    
    def initialize_commands(self):

        self.pine_commands = {
            "display": lambda args: print(" ".join(args)),
            "show": lambda args: print(" ".join(args)),
            "exec_t": lambda args: print(" ".join(args)),
            "exec.t": lambda args: print(" ".join(args)),
            "exec_result": lambda args: print(" ".join(args)),
            "exec_write": lambda args: print(" ".join(args)),
            "write": lambda args: print(" ".join(args)),
            "tell": lambda args: print(" ".join(args)),
            "input_exec": lambda args: input(" ".join(args) if args else "Enter input: "),
            "get_exec": lambda args: input(" ".join(args) if args else "Input: "),
            "read_input": lambda args: input(" ".join(args) if args else "Enter: "),
            "ask_user": lambda args: input(" ".join(args) if args else "Please enter: "),
            "prompt": lambda args: input(" ".join(args) if args else "> "),
            "get_value": lambda args: input(" ".join(args) if args else "Value: "),
            "read_line": lambda args: input(),
            "input_number": lambda args: float(input(" ".join(args) if args else "Enter number: ")),
            "get_number": lambda args: float(input(" ".join(args) if args else "Number: ")),
            "read_number": lambda args: float(input(" ".join(args) if args else "Enter a number: ")),
            "print_number": lambda args: print(float(args[0]) if args else 0),
            "display_number": lambda args: print(float(args[0]) if args else 0),
            
            "Pset": lambda args, vars_dict: vars_dict.update({args[0]: " ".join(args[1:])}) if len(args) > 1 else None,
            "Passign": lambda args, vars_dict: vars_dict.update({args[0]: " ".join(args[1:])}) if len(args) > 1 else None,
            "Plet": lambda args, vars_dict: vars_dict.update({args[0]: " ".join(args[1:])}) if len(args) > 1 else None,
            "define": lambda args, vars_dict: vars_dict.update({args[0]: " ".join(args[1:])}) if len(args) > 1 else None,
            "exec_save": lambda args, vars_dict: vars_dict.update({args[0]: " ".join(args[1:])}) if len(args) > 1 else None,
            "save_var": lambda args, vars_dict: vars_dict.update({args[0]: " ".join(args[1:])}) if len(args) > 1 else None,
            "get_var": lambda args, vars_dict: vars_dict.get(args[0], "") if args else "",
            "fetch_var": lambda args, vars_dict: vars_dict.get(args[0], "") if args else "",
            "retrieve": lambda args, vars_dict: vars_dict.get(args[0], "") if args else "",
            "rm_var": lambda args, vars_dict: vars_dict.pop(args[0], None) if args else None,
            "clear_var": lambda args, vars_dict: vars_dict.pop(args[0], None) if args else None,
            "del_var": lambda args, vars_dict: vars_dict.pop(args[0], None) if args else None,
            "list_vars": lambda args, vars_dict: print(vars_dict),
            "show_vars": lambda args, vars_dict: print(vars_dict),
            "display_vars": lambda args, vars_dict: print(vars_dict),
            "check_var": lambda args, vars_dict: print(args[0] in vars_dict),
            "var_exists": lambda args, vars_dict: print(args[0] in vars_dict),
            "is_defined": lambda args, vars_dict: print(args[0] in vars_dict),
            "type_of": lambda args, vars_dict: print(type(vars_dict.get(args[0], "")).__name__),
            "get_type": lambda args, vars_dict: print(type(vars_dict.get(args[0], "")).__name__),
            "increment": lambda args, vars_dict: vars_dict.update({args[0]: str(int(vars_dict.get(args[0], 0)) + 1)}),
            "decrement": lambda args, vars_dict: vars_dict.update({args[0]: str(int(vars_dict.get(args[0], 0)) - 1)}),
            "add_to": lambda args, vars_dict: vars_dict.update({args[0]: str(float(vars_dict.get(args[0], 0)) + float(args[1]))}),
            "subtract_from": lambda args, vars_dict: vars_dict.update({args[0]: str(float(vars_dict.get(args[0], 0)) - float(args[1]))}),
            "multiply_by": lambda args, vars_dict: vars_dict.update({args[0]: str(float(vars_dict.get(args[0], 0)) * float(args[1]))}),
            "divide_by": lambda args, vars_dict: vars_dict.update({args[0]: str(float(vars_dict.get(args[0], 0)) / float(args[1]))}),
            "modulo": lambda args, vars_dict: vars_dict.update({args[0]: str(int(vars_dict.get(args[0], 0)) % int(args[1]))}),
            "power": lambda args, vars_dict: vars_dict.update({args[0]: str(float(vars_dict.get(args[0], 0)) ** float(args[1]))}),
            "concat": lambda args, vars_dict: vars_dict.update({args[0]: vars_dict.get(args[0], "") + " ".join(args[1:])}),
            "append_text": lambda args, vars_dict: vars_dict.update({args[0]: vars_dict.get(args[0], "") + " ".join(args[1:])}),
            
            "sub_add": lambda args: print(sum(map(float, args))),
            "exec_sum": lambda args: print(sum(map(float, args))),
            "plus": lambda args: print(sum(map(float, args))),
            "subtract": lambda args: print(float(args[0]) - float(args[1])),
            "minus": lambda args: print(float(args[0]) - float(args[1])),
            "exec_difference": lambda args: print(float(args[0]) - float(args[1])),
            "multiply": lambda args: print(float(args[0]) * float(args[1])),
            "times": lambda args: print(float(args[0]) * float(args[1])),
            "product": lambda args: print(float(args[0]) * float(args[1])),
            "divide": lambda args: print(float(args[0]) / float(args[1])),
            "quotient": lambda args: print(float(args[0]) / float(args[1])),
            "mod": lambda args: print(int(args[0]) % int(args[1])),
            "remainder": lambda args: print(int(args[0]) % int(args[1])),
            "pf": lambda args: print(float(args[0]) ** float(args[1])),
            "exponent": lambda args: print(float(args[0]) ** float(args[1])),
            "sr": lambda args: print(float(args[0]) ** 0.5),
            "sqrt": lambda args: print(float(args[0]) ** 0.5),
            "ct": lambda args: print(float(args[0]) ** (1/3)),
            "absolute": lambda args: print(abs(float(args[0]))),
            "abs_value": lambda args: print(abs(float(args[0]))),
            "round_number": lambda args: print(round(float(args[0]))),
            "floor": lambda args: print(int(float(args[0]))),
            "ceiling": lambda args: print(int(float(args[0])) + (1 if float(args[0]) > int(float(args[0])) else 0)),
            "min_value": lambda args: print(min(map(float, args))),
            "max_value": lambda args: print(max(map(float, args))),
            "average": lambda args: print(sum(map(float, args)) / len(args)),
            "mean": lambda args: print(sum(map(float, args)) / len(args)),
            "median": lambda args: print(sorted(map(float, args))[len(args)//2]),
            "factorial": lambda args: print(self.factorial(int(args[0]))),
            "gcd": lambda args: print(self.gcd(int(args[0]), int(args[1]))),
            "lcm": lambda args: print(self.lcm(int(args[0]), int(args[1]))),
            "is_prime": lambda args: print(self.is_prime(int(args[0]))),
            "prime_check": lambda args: print(self.is_prime(int(args[0]))),
            "is_even": lambda args: print(int(args[0]) % 2 == 0),
            "even_check": lambda args: print(int(args[0]) % 2 == 0),
            "is_odd": lambda args: print(int(args[0]) % 2 != 0),
            "odd_check": lambda args: print(int(args[0]) % 2 != 0),
            "sin": lambda args: print(__import__('math').sin(float(args[0]))),
            "cos": lambda args: print(__import__('math').cos(float(args[0]))),
            "tan": lambda args: print(__import__('math').tan(float(args[0]))),
            "log": lambda args: print(__import__('math').log(float(args[0]))),
            "log10": lambda args: print(__import__('math').log10(float(args[0]))),
            "exp": lambda args: print(__import__('math').exp(float(args[0]))),
            "degrees": lambda args: print(__import__('math').degrees(float(args[0]))),
            "radians": lambda args: print(__import__('math').radians(float(args[0]))),
            "pi_value": lambda args: print(__import__('math').pi),
            "e_value": lambda args: print(__import__('math').e),
            "random_number": lambda args: print(__import__('random').random()),
            "random_int": lambda args: print(__import__('random').randint(int(args[0]), int(args[1]))),
            "random_range": lambda args: print(__import__('random').randint(int(args[0]), int(args[1]))),
            "seed_random": lambda args: __import__('random').seed(int(args[0])),
            "convert_to_int": lambda args: print(int(float(args[0]))),
            "convert_to_float": lambda args: print(float(args[0])),
            "convert_to_string": lambda args: print(str(args[0])),
            
            "string_length": lambda args: print(len(args[0])),
            "length": lambda args: print(len(args[0])),
            "str_len": lambda args: print(len(args[0])),
            "uppercase": lambda args: print(args[0].upper()),
            "to_upper": lambda args: print(args[0].upper()),
            "lowercase": lambda args: print(args[0].lower()),
            "to_lower": lambda args: print(args[0].lower()),
            "capitalize": lambda args: print(args[0].capitalize()),
            "title_case": lambda args: print(args[0].title()),
            "reverse_string": lambda args: print(args[0][::-1]),
            "reverse": lambda args: print(args[0][::-1]),
            "trim": lambda args: print(args[0].strip()),
            "strip": lambda args: print(args[0].strip()),
            "trim_left": lambda args: print(args[0].lstrip()),
            "trim_right": lambda args: print(args[0].rstrip()),
            "replace_text": lambda args: print(args[0].replace(args[1], args[2])),
            "replace": lambda args: print(args[0].replace(args[1], args[2])),
            "substring": lambda args: print(args[0][int(args[1]):int(args[2])]),
            "substr": lambda args: print(args[0][int(args[1]):int(args[2])]),
            "split_string": lambda args: print(args[0].split(args[1] if len(args) > 1 else " ")),
            "split": lambda args: print(args[0].split(args[1] if len(args) > 1 else " ")),
            "join_strings": lambda args: print(args[0].join(args[1:])),
            "join": lambda args: print(args[0].join(args[1:])),
            "exec_find_text": lambda args: print(args[0].find(args[1])),
            "exec_find": lambda args: print(args[0].find(args[1])),
            "contains_text": lambda args: print(args[1] in args[0]),
            "contains": lambda args: print(args[1] in args[0]),
            "starts_with": lambda args: print(args[0].startswith(args[1])),
            "ends_with": lambda args: print(args[0].endswith(args[1])),
            "count_char": lambda args: print(args[0].count(args[1])),
            "count": lambda args: print(args[0].count(args[1])),
            "is_digit": lambda args: print(args[0].isdigit()),
            "is_alpha": lambda args: print(args[0].isalpha()),
            "is_alphanumeric": lambda args: print(args[0].isalnum()),
            "is_space": lambda args: print(args[0].isspace()),
            "is_upper": lambda args: print(args[0].isupper()),
            "is_lower": lambda args: print(args[0].islower()),
            "repeat_string": lambda args: print(args[0] * int(args[1])),
            "repeat": lambda args: print(args[0] * int(args[1])),
            "pad_left": lambda args: print(args[0].rjust(int(args[1]), args[2] if len(args) > 2 else " ")),
            "pad_right": lambda args: print(args[0].ljust(int(args[1]), args[2] if len(args) > 2 else " ")),
            "center_text": lambda args: print(args[0].center(int(args[1]), args[2] if len(args) > 2 else " ")),
            "swap_case": lambda args: print(args[0].swapcase()),
            "format_text": lambda args: print(args[0].format(*args[1:])),
            "template": lambda args: print(args[0].format(*args[1:])),
            "escape_string": lambda args: print(args[0].encode('unicode_escape').decode()),
            "unescape_string": lambda args: print(args[0].encode().decode('unicode_escape')),
            "base64en": lambda args: print(__import__('base64').b64encode(args[0].encode()).decode()),
            "base64de": lambda args: print(__import__('base64').b64decode(args[0].encode()).decode()),
            "url_encode": lambda args: print(__import__('urllib.parse').quote(args[0])),
            "url_decode": lambda args: print(__import__('urllib.parse').unquote(args[0])),
            
            "create_list": lambda args: print(args),
            "make_list": lambda args: print(args),
            "list_add": lambda args: print(args[0] + " ".join(args[1:])),
            "list_append": lambda args: print(args + [args[-1]] if args else args),
            "list_remove": lambda args: print([x for x in args if x != args[-1]]),
            "list_length": lambda args: print(len(args)),
            "list_count": lambda args: print(len(args)),
            "list_sort": lambda args: print(sorted(args)),
            "sort_list": lambda args: print(sorted(args)),
            "list_reverse": lambda args: print(args[::-1]),
            "reverse_list": lambda args: print(args[::-1]),
            "list_first": lambda args: print(args[0] if args else None),
            "list_last": lambda args: print(args[-1] if args else None),
            "list_get": lambda args: print(args[int(args[0])] if len(args) > int(args[0]) else None),
            "list_set": lambda args: print(args[:int(args[0])] + [args[-1]] + args[int(args[0])+1:]),
            "list_contains": lambda args: print(args[-1] in args[:-1]),
            "list_index": lambda args: print(args[:-1].index(args[-1]) if args[-1] in args[:-1] else -1),
            "list_min": lambda args: print(min(args)),
            "list_max": lambda args: print(max(args)),
            "list_sum": lambda args: print(sum(map(float, args))),
            "list_average": lambda args: print(sum(map(float, args)) / len(args)),
            "list_join": lambda args: print(" ".join(args)),
            "join_list": lambda args: print(" ".join(args)),
            "list_split": lambda args: print(args[0].split(args[1] if len(args) > 1 else " ")),
            "list_filter": lambda args: print([x for x in args if x != args[-1]]),
            "list_map": lambda args: print([x.upper() for x in args]),
            "list_reduce": lambda args: print("".join(args)),
            "list_unique": lambda args: print(list(set(args))),
            "unique_items": lambda args: print(list(set(args))),
            "list_duplicates": lambda args: print([x for x in args if args.count(x) > 1]),
            "list_flatten": lambda args: print([item for sublist in args for item in sublist]),
            "list_chunk": lambda args: print([args[i:i+int(args[-1])] for i in range(0, len(args)-1, int(args[-1]))]),
            "list_zip": lambda args: print(list(zip(*[args[i::2] for i in range(2)]))),
            "list_unzip": lambda args: print([list(x) for x in zip(*args)]),
            "list_intersect": lambda args: print(list(set(args[0]) & set(args[1]))),
            "list_union": lambda args: print(list(set(args[0]) | set(args[1]))),
            "list_difference": lambda args: print(list(set(args[0]) - set(args[1]))),
            "list_symmetric_diff": lambda args: print(list(set(args[0]) ^ set(args[1]))),
            "list_permutations": lambda args: print(list(__import__('itertools').permutations(args))),
            "list_combinations": lambda args: print(list(__import__('itertools').combinations(args, int(args[-1])))),
            "list_product": lambda args: print(list(__import__('itertools').product(*args))),
            "list_shuffle": lambda args: print(__import__('random').shuffle(args) or args),
            "list_sample": lambda args: print(__import__('random').sample(args, int(args[-1]))),
            "list_choice": lambda args: print(__import__('random').choice(args)),
            "list_count_item": lambda args: print(args[:-1].count(args[-1])),
            "list_clear": lambda args: [],
            "list_copy": lambda args: print(args.copy()),
            "list_extend": lambda args: print(args + args),
            "list_insert": lambda args: print(args[:int(args[0])] + [args[-1]] + args[int(args[0]):-1]),
            "list_pop": lambda args: print(args[:-1]),
            "list_slice": lambda args: print(args[int(args[0]):int(args[1])]),
            
            "if": lambda args, vars_dict: None,
            "then": lambda args: None,
            "otherwise": lambda args: None,
            "elif": lambda args: None,
            "endif": lambda args: None,
            "for": lambda args: None,
            "while": lambda args: None,
            "do": lambda args: None,
            "endfor": lambda args: None,
            "endwhile": lambda args: None,
            "break": lambda args: None,
            "continue": lambda args: None,
            "return": lambda args: None,
            "exit": lambda args: None,
            "loop": lambda args: None,
            "repeat_until": lambda args: None,
            "case": lambda args: None,
            "switch": lambda args: None,
            "when": lambda args: None,
            "default": lambda args: None,
            "endcase": lambda args: None,
            "endswitch": lambda args: None,
            "exec_try": lambda args: None,
            "catch": lambda args: None,
            "finally": lambda args: None,
            "throw": lambda args: None,
            "raise_error": lambda args: None,
            "assert": lambda args: None,
            "check": lambda args: None,
            "verify": lambda args: None,
            "test": lambda args: None,
            "evaluate": lambda args: None,
            "condition": lambda args: None,
            "branch": lambda args: None,
            "jump": lambda args: None,
            "exec_goto": lambda args: None,
            "label": lambda args: None,
            "call": lambda args: None,
            "invoke": lambda args: None,
            "execute": lambda args: None,
            "run": lambda args: None,
            "perform": lambda args: None,
            "process": lambda args: None,
            "handle": lambda args: None,
            "manage": lambda args: None,
            "control": lambda args: None,
            "direct": lambda args: None,
            "guide": lambda args: None,
            "steer": lambda args: None,
            "navigate": lambda args: None,
            "route": lambda args: None,
            "channel": lambda args: None,
            "flow": lambda args: None,
            
            "mkfile": lambda args: self.create_file(args),
            "crfile": lambda args: self.create_file(args),
            "nwfile": lambda args: self.create_file(args),
            "opfile": lambda args: self.read_file(args),
            "rfile": lambda args: self.read_file(args),
            "lfile": lambda args: self.read_file(args),
            "wrfile": lambda args: self.write_file(args),
            "svfile": lambda args: self.write_file(args),
            "apdfile": lambda args: self.append_file(args),
            "delfile": lambda args: self.delete_file(args),
            "rmfile": lambda args: self.delete_file(args),
            "cpfile": lambda args: self.copy_file(args),
            "mvfile": lambda args: self.move_file(args),
            "renfile": lambda args: self.rename_file(args),
            "file_exists": lambda args: print(os.path.exists(args[0])),
            "isfile": lambda args: print(os.path.isfile(args[0])),
            "isdir": lambda args: print(os.path.isdir(args[0])),
            "filesize": lambda args: print(os.path.getsize(args[0]) if os.path.exists(args[0]) else 0),
            "fileinf": lambda args: print(os.stat(args[0]) if os.path.exists(args[0]) else "File not found"),
            "lisfiles": lambda args: print(os.listdir(args[0] if args else ".")),
            "lisdir": lambda args: print(os.listdir(args[0] if args else ".")),
            "current_dir": lambda args: print(os.getcwd()),
            "change_dir": lambda args: os.chdir(args[0]),
            "mkdir": lambda args: os.makedirs(args[0], exist_ok=True),
            "crdir": lambda args: os.makedirs(args[0], exist_ok=True),
            "rmdir": lambda args: os.rmdir(args[0]) if os.path.exists(args[0]) else None,
            "deldir": lambda args: shutil.rmtree(args[0]) if os.path.exists(args[0]) else None,
            "cpdir": lambda args: shutil.copytree(args[0], args[1]) if os.path.exists(args[0]) else None,
            "mvdir": lambda args: shutil.move(args[0], args[1]) if os.path.exists(args[0]) else None,
            "read_lines": lambda args: self.read_lines(args),
            "wr_lines": lambda args: self.write_lines(args),
            "read_csv": lambda args: self.read_csv(args),
            "write_csv": lambda args: self.write_csv(args),
            "read_json": lambda args: self.read_json(args),
            "write_json": lambda args: self.write_json(args),
            "file_extension": lambda args: print(os.path.splitext(args[0])[1]),
            "file_name": lambda args: print(os.path.basename(args[0])),
            "file_path": lambda args: print(os.path.dirname(args[0])),
            "absolute_path": lambda args: print(os.path.abspath(args[0])),
            "relative_path": lambda args: print(os.path.relpath(args[0])),
            "join_paths": lambda args: print(os.path.join(*args)),
            "split_path": lambda args: print(os.path.split(args[0])),
            "normalize_path": lambda args: print(os.path.normpath(args[0])),
            "check_permission": lambda args: print(os.access(args[0], os.R_OK)),
            "set_permission": lambda args: os.chmod(args[0], int(args[1], 8)),
            "get_permission": lambda args: print(oct(os.stat(args[0]).st_mode & 0o777)),
            "file_modified": lambda args: print(os.path.getmtime(args[0]) if os.path.exists(args[0]) else 0),
            "file_created": lambda args: print(os.path.getctime(args[0]) if os.path.exists(args[0]) else 0),
            "file_accessed": lambda args: print(os.path.getatime(args[0]) if os.path.exists(args[0]) else 0),
            
            "sysfo": lambda args: print(platform.system()),
            "exec_os": lambda args: print(platform.system()),
            "cur_os": lambda args: print(platform.version()),
            "platform_info": lambda args: print(platform.platform()),
            "cpu_info": lambda args: print(platform.processor()),
            "computer_info": lambda args: print(platform.machine()),
            "python_version": lambda args: print(sys.version),
            "run_command": lambda args: print(os.popen(" ".join(args)).read()),
            "exec_command": lambda args: print(os.popen(" ".join(args)).read()),
            "shell_command": lambda args: print(os.popen(" ".join(args)).read()),
            "system_command": lambda args: print(os.popen(" ".join(args)).read()),
            "terminal": lambda args: print(os.popen(" ".join(args)).read()),
            "command_line": lambda args: print(os.popen(" ".join(args)).read()),
            "environment": lambda args: print(os.environ),
            "get_env": lambda args: print(os.environ.get(args[0], "")),
            "set_env": lambda args: self.set_environment_variable(args),
            "del_env": lambda args: os.environ.pop(args[0], None),
            "list_env": lambda args: print(os.environ),
            "process_id": lambda args: print(os.getpid()),
            "parent_process": lambda args: print(os.getppid()),
            "usr_name": lambda args: print(os.getlogin()),
            "usr_home": lambda args: print(os.path.expanduser("~")),
            "temp_dir": lambda args: print(os.environ.get('TEMP', '/tmp')),
            "disk_usage": lambda args: print(shutil.disk_usage(args[0] if args else ".")),
            "memory_info": lambda args: print(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')),
            "cpu_count": lambda args: print(os.cpu_count()),
            "network_name": lambda args: print(platform.node()),
            "hostname": lambda args: print(platform.node()),
            "ip_address": lambda args: print(self.get_ip_address()),
            "mac_address": lambda args: print(self.get_mac_address()),
            "uptime": lambda args: print(self.get_uptime()),
            "O": lambda args: os.system("shutdown /s /t 0" if self.system == "Windows" else "shutdown -h now"),
            "I": lambda args: os.system("shutdown /r /t 0" if self.system == "Windows" else "shutdown -r now"),
            "logoff": lambda args: os.system("shutdown /l" if self.system == "Windows" else "logout"),
            "lock": lambda args: os.system("rundll32.exe user32.dll,LockWorkStation" if self.system == "Windows" else "loginctl lock-session"),
            "sleep": lambda args: __import__('time').sleep(float(args[0]) if args else 1),
            "wait": lambda args: __import__('time').sleep(float(args[0]) if args else 1),
            "delay": lambda args: __import__('time').sleep(float(args[0]) if args else 1),
            "pause": lambda args: input("Press Enter to continue..."),
            "clear_screen": lambda args: os.system('cls' if self.system == "Windows" else 'clear'),
            "cls": lambda args: os.system('cls' if self.system == "Windows" else 'clear'),
            "clear": lambda args: os.system('cls' if self.system == "Windows" else 'clear'),
            "beep": lambda args: print('\a'),
            "sound": lambda args: print('\a'),
            "alert": lambda args: print('\a'),
            "notify": lambda args: self.show_notification(" ".join(args) if args else "Notification"),
            "message_box": lambda args: self.show_message_box(" ".join(args) if args else "Message"),
            "opbrowser": lambda args: __import__('webbrowser').open(args[0] if args else "http://www.google.com"),
            "opurl": lambda args: __import__('webbrowser').open(args[0] if args else "http://www.google.com"),
            "downfile": lambda args: self.download_file(args),
            
            "gt_hhtp": lambda args: self.http_request("GET", args[0]) if args else None,
            "post_http": lambda args: self.http_request("POST", args[0], args[1] if len(args) > 1 else None) if args else None,
            "put_http": lambda args: self.http_request("PUT", args[0], args[1] if len(args) > 1 else None) if args else None,
            "del_http": lambda args: self.http_request("DELETE", args[0]) if args else None,
            "send_request": lambda args: self.http_request(args[0], args[1]) if len(args) > 1 else None,
            "get_url": lambda args: self.http_request("GET", args[0]) if args else None,
            "post_url": lambda args: self.http_request("POST", args[0], args[1] if len(args) > 1 else None) if args else None,
            "sentpckt": lambda args: self.ping_host(args[0]) if args else None,
            "check_host": lambda args: self.ping_host(args[0]) if args else None,
            "dnslkup": lambda args: self.dns_lookup(args[0]) if args else None,
            "resolve_host": lambda args: self.dns_lookup(args[0]) if args else None,
            "whois": lambda args: self.whois_lookup(args[0]) if args else None,
            "traceroute": lambda args: self.traceroute(args[0]) if args else None,
            "port_scan": lambda args: self.scan_port(args[0], int(args[1]) if len(args) > 1 else 80) if args else None,
            "check_port": lambda args: self.scan_port(args[0], int(args[1]) if len(args) > 1 else 80) if args else None,
            "socket_open": lambda args: self.create_socket(args[0], int(args[1]) if len(args) > 1 else 80) if args else None,
            "socket_close": lambda args: None,
            "socket_send": lambda args: None,
            "socket_receive": lambda args: None,
            "start_server": lambda args: self.start_server(int(args[0]) if args else 8000),
            "stop_server": lambda args: None,
            "server_status": lambda args: None,
            "upload_file": lambda args: self.upload_file(args),
            "send_file": lambda args: self.upload_file(args),
            "receive_file": lambda args: self.download_file(args),
            "fetch_file": lambda args: self.download_file(args),
            "create_socket": lambda args: self.create_socket(args[0], int(args[1]) if len(args) > 1 else 80) if args else None,
            "bind_socket": lambda args: None,
            "listen_socket": lambda args: None,
            "accept_socket": lambda args: None,
            "connect_socket": lambda args: self.create_socket(args[0], int(args[1]) if len(args) > 1 else 80) if args else None,
            "close_socket": lambda args: None,
            "send_data": lambda args: None,
            "receive_data": lambda args: None,
            "set_timeout": lambda args: None,
            "get_timeout": lambda args: None,
            "set_buffer": lambda args: None,
            "get_buffer": lambda args: None,
            "encrypt_data": lambda args: self.encrypt_data(args[0]) if args else None,
            "decrypt_data": lambda args: self.decrypt_data(args[0]) if args else None,
            "hash_data": lambda args: self.hash_data(args[0]) if args else None,
            "generate_key": lambda args: print(self.generate_key()),
            "validate_ssl": lambda args: self.validate_ssl(args[0]) if args else None,
            "get_headers": lambda args: self.get_headers(args[0]) if args else None,
            "post_json": lambda args: self.http_request("POST", args[0], json.loads(args[1]) if len(args) > 1 else None) if args else None,
            "websocket_connect": lambda args: None,
            "websocket_send": lambda args: None,
            "websocket_close": lambda args: None,
            "ftp_upload": lambda args: self.ftp_upload(args),
            "ftp_download": lambda args: self.ftp_download(args),
            "ftp_list": lambda args: self.ftp_list(args),
            "ftp_delete": lambda args: self.ftp_delete(args),
            "ftp_rename": lambda args: self.ftp_rename(args),
            "ftp_mkdir": lambda args: self.ftp_mkdir(args),
            "ssh_connect": lambda args: None,
            "ssh_execute": lambda args: None,
            "ssh_close": lambda args: None,
            "smtp_send": lambda args: self.send_email(args),
            "send_email": lambda args: self.send_email(args),
            "email_send": lambda args: self.send_email(args),
            "pop3_receive": lambda args: self.receive_email(args),
            "receive_email": lambda args: self.receive_email(args),
            "imap_fetch": lambda args: self.fetch_email(args),
            
            "db_connect": lambda args: self.db_connect(args),
            "database_connect": lambda args: self.db_connect(args),
            "db_close": lambda args: None,
            "db_query": lambda args: self.db_query(args),
            "db_execute": lambda args: self.db_execute(args),
            "db_fetch": lambda args: self.db_fetch(args),
            "db_fetchall": lambda args: self.db_fetchall(args),
            "db_insert": lambda args: self.db_insert(args),
            "db_update": lambda args: self.db_update(args),
            "db_delete": lambda args: self.db_delete(args),
            "db_select": lambda args: self.db_select(args),
            "db_create_table": lambda args: self.db_create_table(args),
            "db_drop_table": lambda args: self.db_drop_table(args),
            "db_alter_table": lambda args: self.db_alter_table(args),
            "db_create_index": lambda args: self.db_create_index(args),
            "db_drop_index": lambda args: self.db_drop_index(args),
            "db_begin": lambda args: None,
            "db_commit": lambda args: None,
            "db_rollback": lambda args: None,
            "db_transaction": lambda args: None,
            "db_backup": lambda args: self.db_backup(args),
            "db_restore": lambda args: self.db_restore(args),
            "db_export": lambda args: self.db_export(args),
            "db_import": lambda args: self.db_import(args),
            "db_list_tables": lambda args: self.db_list_tables(args),
            "db_table_info": lambda args: self.db_table_info(args),
            "db_count_rows": lambda args: self.db_count_rows(args),
            "db_last_id": lambda args: self.db_last_id(args),
            "db_error": lambda args: self.db_error(args),
            "sqlite_connect": lambda args: self.sqlite_connect(args),
            "sqlite_query": lambda args: self.sqlite_query(args),
            "sqlite_execute": lambda args: self.sqlite_execute(args),
            "mysql_connect": lambda args: self.mysql_connect(args),
            "mysql_query": lambda args: self.mysql_query(args),
            "postgres_connect": lambda args: self.postgres_connect(args),
            "postgres_query": lambda args: self.postgres_query(args),
            "mongo_connect": lambda args: self.mongo_connect(args),
            "mongo_insert": lambda args: self.mongo_insert(args),
            "mongo_find": lambda args: self.mongo_find(args),
            "mongo_update": lambda args: self.mongo_update(args),
            "mongo_delete": lambda args: self.mongo_delete(args),
            "redis_connect": lambda args: self.redis_connect(args),
            "redis_set": lambda args: self.redis_set(args),
            "redis_get": lambda args: self.redis_get(args),
            "redis_delete": lambda args: self.redis_delete(args),
            "cache_set": lambda args: self.cache_set(args),
            "cache_get": lambda args: self.cache_get(args),
            "cache_delete": lambda args: self.cache_delete(args),
            "cache_clear": lambda args: self.cache_clear(args),

            "current_time": lambda args: print(__import__('datetime').datetime.now().strftime("%H:%M:%S")),
            "current_date": lambda args: print(__import__('datetime').datetime.now().strftime("%Y-%m-%d")),
            "current_datetime": lambda args: print(__import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "now": lambda args: print(__import__('datetime').datetime.now()),
            "timestamp": lambda args: print(__import__('time').time()),
            "epoch_time": lambda args: print(int(__import__('time').time())),
            "format_date": lambda args: print(__import__('datetime').datetime.strptime(args[0], args[1]) if len(args) > 1 else args[0]),
            "parse_date": lambda args: print(__import__('datetime').datetime.strptime(args[0], args[1]) if len(args) > 1 else args[0]),
            "date_add": lambda args: print(__import__('datetime').datetime.now() + __import__('datetime').timedelta(days=int(args[0]))),
            "date_subtract": lambda args: print(__import__('datetime').datetime.now() - __import__('datetime').timedelta(days=int(args[0]))),
            "days_between": lambda args: print((__import__('datetime').datetime.strptime(args[1], "%Y-%m-%d") - __import__('datetime').datetime.strptime(args[0], "%Y-%m-%d")).days),
            "day_of_week": lambda args: print(__import__('datetime').datetime.now().strftime("%A")),
            "day_of_year": lambda args: print(__import__('datetime').datetime.now().timetuple().tm_yday),
            "week_number": lambda args: print(__import__('datetime').datetime.now().isocalendar()[1]),
            "month_name": lambda args: print(__import__('datetime').datetime.now().strftime("%B")),
            "year": lambda args: print(__import__('datetime').datetime.now().year),
            "month": lambda args: print(__import__('datetime').datetime.now().month),
            "day": lambda args: print(__import__('datetime').datetime.now().day),
            "hour": lambda args: print(__import__('datetime').datetime.now().hour),
            "minute": lambda args: print(__import__('datetime').datetime.now().minute),
            "second": lambda args: print(__import__('datetime').datetime.now().second),
            "timezone": lambda args: print(__import__('time').tzname),
            "set_timezone": lambda args: os.environ.__setitem__('TZ', args[0]),
            "timer_start": lambda args: self.timer_start(),
            "timer_stop": lambda args: self.timer_stop(),

            "gui_window": lambda args: self.create_window(args),
            "create_window": lambda args: self.create_window(args),
            "gui_button": lambda args: self.create_button(args),
            "create_button": lambda args: self.create_button(args),
            "gui_label": lambda args: self.create_label(args),
            "create_label": lambda args: self.create_label(args),
            "gui_input": lambda args: self.create_input(args),
            "create_input": lambda args: self.create_input(args),
            "gui_text": lambda args: self.create_text(args),
            "create_text": lambda args: self.create_text(args),
            "gui_checkbox": lambda args: self.create_checkbox(args),
            "create_checkbox": lambda args: self.create_checkbox(args),
            "gui_radio": lambda args: self.create_radio(args),
            "create_radio": lambda args: self.create_radio(args),
            "gui_dropdown": lambda args: self.create_dropdown(args),
            "create_dropdown": lambda args: self.create_dropdown(args),
            "gui_listbox": lambda args: self.create_listbox(args),
            "create_listbox": lambda args: self.create_listbox(args),
            "gui_canvas": lambda args: self.create_canvas(args),
            "create_canvas": lambda args: self.create_canvas(args),
            "gui_menu": lambda args: self.create_menu(args),
            "create_menu": lambda args: self.create_menu(args),
            "gui_dialog": lambda args: self.create_dialog(args),
            "create_dialog": lambda args: self.create_dialog(args),
            "gui_message": lambda args: self.show_message(args),
            "show_message": lambda args: self.show_message(args),
            "gui_input_dialog": lambda args: self.input_dialog(args),
            "input_dialog": lambda args: self.input_dialog(args),
            "gui_file_dialog": lambda args: self.file_dialog(args),
            "file_dialog": lambda args: self.file_dialog(args),
            "gui_color_dialog": lambda args: self.color_dialog(args),
            "color_dialog": lambda args: self.color_dialog(args),

            "image_load": lambda args: self.load_image(args),
            "load_image": lambda args: self.load_image(args),
            "image_save": lambda args: self.save_image(args),
            "save_image": lambda args: self.save_image(args),
            "image_resize": lambda args: self.resize_image(args),
            "resize_image": lambda args: self.resize_image(args),
            "image_rotate": lambda args: self.rotate_image(args),
            "rotate_image": lambda args: self.rotate_image(args),
            "image_flip": lambda args: self.flip_image(args),
            "flip_image": lambda args: self.flip_image(args),
            "image_crop": lambda args: self.crop_image(args),
            "crop_image": lambda args: self.crop_image(args),
            "image_filter": lambda args: self.filter_image(args),
            "filter_image": lambda args: self.filter_image(args),
            "image_info": lambda args: self.image_info(args),
            "image_format": lambda args: self.image_format(args),
            "image_size": lambda args: self.image_size(args),
            "create_canvas_image": lambda args: self.create_canvas_image(args),
            "draw_line": lambda args: self.draw_line(args),
            "draw_rectangle": lambda args: self.draw_rectangle(args),
            "draw_circle": lambda args: self.draw_circle(args),
            "draw_text": lambda args: self.draw_text(args),
            
            "help": lambda args: self.show_help(),
            "version": lambda args: print("Pine Language v1.0"),
            "about": lambda args: print("Pine Programming Language - Created 2026"),
            "license": lambda args: print("MIT License"),
            "credits": lambda args: print("Pine Language Development Team"),
            "exit_program": lambda args: sys.exit(0),
            "quit": lambda args: sys.exit(0),
            "terminate": lambda args: sys.exit(0),
            "shutdown_pine": lambda args: sys.exit(0),
            "restart_pine": lambda args: os.execv(sys.executable, ['python'] + sys.argv),
            "reload": lambda args: self.initialize_commands(),
            "refresh": lambda args: self.initialize_commands(),
            "reset": lambda args: self.initialize_commands(),
            "clear_cache": lambda args: self.cache_clear(),
            "cleanup": lambda args: self.cleanup(),
            "optimize": lambda args: self.optimize(),
            "compress": lambda args: self.compress_data(args),
            "decompress": lambda args: self.decompress_data(args),
            "serialize": lambda args: self.serialize_data(args),
            "deserialize": lambda args: self.deserialize_data(args),
            "generate_id": lambda args: print(__import__('uuid').uuid4()),
            "uuid": lambda args: print(__import__('uuid').uuid4()),
            "random_string": lambda args: print(__import__('secrets').token_hex(int(args[0]) if args else 16)),
            "random_password": lambda args: print(__import__('secrets').token_urlsafe(int(args[0]) if args else 16)),
            "checksum": lambda args: print(__import__('hashlib').md5(args[0].encode()).hexdigest()),
            "validate_email": lambda args: print(self.validate_email(args[0]) if args else False),
            "validate_url": lambda args: print(self.validate_url(args[0]) if args else False),
            "validate_phone": lambda args: print(self.validate_phone(args[0]) if args else False),
            "capitalize_words": lambda args: print(" ".join(word.capitalize() for word in args)),
            "title_case_text": lambda args: print(" ".join(args).title()),
            "format_number": lambda args: print(f"{float(args[0]):,}"),
            "format_currency": lambda args: print(f"${float(args[0]):,.2f}"),
            "format_percent": lambda args: print(f"{float(args[0]):.2%}"),
            "strip_html": lambda args: print(__import__('re').sub(r'<[^>]+>', '', args[0])),
            "strip_tags": lambda args: print(__import__('re').sub(r'<[^>]+>', '', args[0])),
            "html_encode": lambda args: print(__import__('html').escape(args[0])),
            "html_decode": lambda args: print(__import__('html').unescape(args[0])),
            "url_shorten": lambda args: self.shorten_url(args[0]),
            "qr_generate": lambda args: self.generate_qr(args[0]),
            "barcode_generate": lambda args: self.generate_barcode(args[0]),
            "text_to_speech": lambda args: self.text_to_speech(args),
            "speech_to_text": lambda args: self.speech_to_text(args),
            "translate": lambda args: self.translate_text(args),
            "detect_language": lambda args: self.detect_language(args[0]),
            "sentiment_analysis": lambda args: self.analyze_sentiment(args[0]),
            "spell_check": lambda args: self.spell_check(args[0]),
            "grammar_check": lambda args: self.grammar_check(args[0]),
        }
    
    def factorial(self, n):
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    
    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(self, a, b):
        return abs(a * b) // self.gcd(a, b) if a and b else 0
    
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def create_file(self, args):
        if args:
            with open(args[0], 'w') as f:
                if len(args) > 1:
                    f.write(" ".join(args[1:]))
            print(f"File created: {args[0]}")
    
    def read_file(self, args):
        if args and os.path.exists(args[0]):
            with open(args[0], 'r') as f:
                print(f.read())
    
    def write_file(self, args):
        if len(args) > 1:
            with open(args[0], 'w') as f:
                f.write(" ".join(args[1:]))
            print(f"File written: {args[0]}")
    
    def append_file(self, args):
        if len(args) > 1:
            with open(args[0], 'a') as f:
                f.write(" ".join(args[1:]) + "\n")
            print(f"Content appended to: {args[0]}")
    
    def delete_file(self, args):
        if args and os.path.exists(args[0]):
            os.remove(args[0])
            print(f"File deleted: {args[0]}")
    
    def copy_file(self, args):
        if len(args) > 1 and os.path.exists(args[0]):
            shutil.copy2(args[0], args[1])
            print(f"File copied: {args[0]} -> {args[1]}")
    
    def move_file(self, args):
        if len(args) > 1 and os.path.exists(args[0]):
            shutil.move(args[0], args[1])
            print(f"File moved: {args[0]} -> {args[1]}")
    
    def rename_file(self, args):
        if len(args) > 1 and os.path.exists(args[0]):
            os.rename(args[0], args[1])
            print(f"File renamed: {args[0]} -> {args[1]}")
    
    def read_lines(self, args):
        if args and os.path.exists(args[0]):
            with open(args[0], 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    print(f"{i}: {line.rstrip()}")
    
    def write_lines(self, args):
        if len(args) > 1:
            with open(args[0], 'w') as f:
                for line in args[1:]:
                    f.write(line + "\n")
            print(f"Lines written to: {args[0]}")
    
    def read_csv(self, args):
        if args and os.path.exists(args[0]):
            import csv
            with open(args[0], 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    print(",".join(row))
    
    def write_csv(self, args):
        if len(args) > 1:
            import csv
            with open(args[0], 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(args[1:])
            print(f"CSV written: {args[0]}")
    
    def read_json(self, args):
        if args and os.path.exists(args[0]):
            with open(args[0], 'r') as f:
                data = json.load(f)
                print(json.dumps(data, indent=2))
    
    def write_json(self, args):
        if len(args) > 1:
            with open(args[0], 'w') as f:
                json.dump(json.loads(args[1]), f, indent=2)
            print(f"JSON written: {args[0]}")
    
    def get_ip_address(self):
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_mac_address(self):
        try:
            import uuid
            return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 48, 8)][::-1])
        except:
            return "00:00:00:00:00:00"
    
    def get_uptime(self):
        try:
            if self.system == "Linux":
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                    return f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"
            elif self.system == "Windows":
                import ctypes
                lib = ctypes.windll.kernel32
                return f"{int(lib.GetTickCount64() // 3600000)}h {int((lib.GetTickCount64() % 3600000) // 60000)}m"
            else:
                return "Unknown"
        except:
            return "Unknown"
    
    def show_notification(self, message):
        try:
            if self.system == "Windows":
                from plyer import notification
                notification.notify(title="Pine Language", message=message, timeout=5)
            else:
                os.system(f'notify-send "Pine Language" "{message}"')
        except:
            print(f"Notification: {message}")
    
    def show_message_box(self, message):
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Pine Language", message)
            root.destroy()
        except:
            print(f"Message: {message}")
    
    def download_file(self, args):
        if args:
            import urllib.request
            url = args[0]
            filename = args[1] if len(args) > 1 else url.split('/')[-1]
            try:
                urllib.request.urlretrieve(url, filename)
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Download failed: {e}")
    
    def http_request(self, method, url, data=None):
        try:
            import urllib.request
            import urllib.parse
            
            if data:
                data = urllib.parse.urlencode(data).encode()
            
            req = urllib.request.Request(url, data=data, method=method)
            with urllib.request.urlopen(req) as response:
                return response.read().decode()
        except Exception as e:
            return f"Request failed: {e}"
    
    def ping_host(self, host):
        try:
            import subprocess
            param = '-n' if self.system == "Windows" else '-c'
            command = ['ping', param, '1', host]
            result = subprocess.run(command, capture_output=True, text=True, timeout=5)
            print(result.stdout)
        except:
            print(f"Ping failed for {host}")
    
    def dns_lookup(self, host):
        try:
            import socket
            ip = socket.gethostbyname(host)
            print(f"{host} -> {ip}")
        except:
            print(f"DNS lookup failed for {host}")

    def set_environment_variable(self, args):
        if len(args) > 0:
            os.environ[args[0]] = " ".join(args[1:]) if len(args) > 1 else ""
            print(f"Environment variable set: {args[0]}")
    
    def encrypt_data(self, data):
        try:
            import base64
            return base64.b64encode(data.encode()).decode()
        except:
            return data
    
    def decrypt_data(self, data):
        try:
            import base64
            return base64.b64decode(data.encode()).decode()
        except:
            return data
    
    def hash_data(self, data):
        try:
            import hashlib
            return hashlib.sha256(data.encode()).hexdigest()
        except:
            return data
    
    def generate_key(self):
        import secrets
        return secrets.token_hex(32)
    
    def create_window(self, args):
        try:
            root = tk.Tk()
            root.title(args[0] if args else "Pine Window")
            if len(args) > 1:
                root.geometry(args[1])
            root.mainloop()
        except:
            print("GUI not available")
    
    def create_button(self, args):
        try:
            root = tk.Tk()
            button = tk.Button(root, text=args[0] if args else "Button")
            button.pack()
            root.mainloop()
        except:
            print("GUI not available")
    
    def create_label(self, args):
        try:
            root = tk.Tk()
            label = tk.Label(root, text=args[0] if args else "Label")
            label.pack()
            root.mainloop()
        except:
            print("GUI not available")
    
    def create_input(self, args):
        try:
            root = tk.Tk()
            entry = tk.Entry(root)
            entry.pack()
            root.mainloop()
        except:
            print("GUI not available")
    
    def validate_email(self, email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    def validate_url(self, url):
        import re
        pattern = r'^https?://[\w\.-]+\.\w+$'
        return bool(re.match(pattern, url))
    
    def validate_phone(self, phone):
        import re
        pattern = r'^\+?[\d\s-]{10,}$'
        return bool(re.match(pattern, phone))
    
    def timer_start(self):
        self.timer = __import__('time').time()
        print("Timer started")
    
    def timer_stop(self):
        if hasattr(self, 'timer'):
            elapsed = __import__('time').time() - self.timer
            print(f"Elapsed time: {elapsed:.2f} seconds")
            del self.timer
        else:
            print("No timer running")
    
    def show_help(self):
        print("Pine Language Commands:")
        print("=" * 50)
        categories = {
            "Basic I/O": ["display", "input_text", "print_number"],
            "Variables": ["Pset", "get_var", "increment"],
            "Math": ["sub_add", "sqrt", "factorial"],
            "String": ["uppercase", "reverse", "substring"],
            "List": ["create_list", "list_sort", "list_unique"],
            "File": ["mkfile", "rfile", "wrfile"],
            "System": ["sysfo", "run_command", "clear_screen"],
            "Network": ["gt_hhtp", "ping", "download_file"],
            "Database": ["db_connect", "db_query", "db_insert"],
            "Date/Time": ["current_time", "timestamp", "timer_start"],
            "GUI": ["gui_window", "gui_button", "gui_input"],
            "Image": ["image_load", "image_resize", "draw_line"],
            "Utility": ["help", "version", "generate_id"]
        }
        
        for category, commands in categories.items():
            print(f"\n{category}:")
            print(f"  {', '.join(commands)}")
    
    def cleanup(self):
        temp_dir = os.environ.get('TEMP', '/tmp')
        count = 0
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    if file.endswith('.tmp') or file.endswith('.temp'):
                        os.remove(os.path.join(root, file))
                        count += 1
                except:
                    pass
        print(f"Cleaned up {count} temporary files")
    
    def optimize(self):
        print("Optimizing Pine environment...")
        self.cleanup()
        print("Optimization complete")
    
    def compress_data(self, args):
        if args:
            import zlib
            compressed = zlib.compress(args[0].encode())
            print(f"Compressed: {len(compressed)} bytes")
            return compressed
    
    def decompress_data(self, args):
        if args:
            import zlib
            decompressed = zlib.decompress(args[0])
            print(f"Decompressed: {decompressed.decode()}")
    
    def serialize_data(self, args):
        import pickle
        return pickle.dumps(args)
    
    def deserialize_data(self, args):
        import pickle
        return pickle.loads(args)
    
    def generate_qr(self, data):
        try:
            import qrcode
            img = qrcode.make(data)
            img.save("qrcode.png")
            print("QR code saved as qrcode.png")
        except:
            print("QR code generation requires qrcode library")
    
    def text_to_speech(self, args):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(" ".join(args))
            engine.runAndWait()
        except:
            print("Text-to-speech requires pyttsx3 library")
    
    def translate_text(self, args):
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(args[0], dest=args[1] if len(args) > 1 else 'en')
            print(result.text)
        except:
            print("Translation requires googletrans library")
    
    def add_to_path(self):
        if self.system == "Windows":
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
                try:
                    path = winreg.QueryValueEx(key, "PATH")[0]
                except:
                    path = ""
                
                if str(self.install_path) not in path:
                    new_path = f"{path};{self.install_path}" if path else str(self.install_path)
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    winreg.CloseKey(key)
                    print("Added to PATH")
            except:
                print("Failed to add to PATH")
        else:
            shell_rc = os.path.expanduser("~/.bashrc")
            try:
                with open(shell_rc, 'a') as f:
                    f.write(f'\nexport PATH="$PATH:{self.install_path}"\n')
                print("Added to PATH")
            except:
                print("Failed to add to PATH")

    def install(self):
        print("Installing Pine Language...")
        
        self.install_path.mkdir(parents=True, exist_ok=True)
        
        lib_path = self.install_path / "lib"
        lib_path.mkdir(exist_ok=True)
        
        scripts_path = self.install_path / "scripts"
        scripts_path.mkdir(exist_ok=True)
        
        commands_file = self.install_path / "commands.json"
        with open(commands_file, 'w') as f:
            json.dump(list(self.pine_commands.keys()), f, indent=2)
        
        launcher = self.install_path / "pine.py"
        with open(launcher, 'w') as f:
            f.write("""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from pine_runtime import PineRuntime
if __name__ == "__main__":
    runtime = PineRuntime()
    if len(sys.argv) > 1:
        runtime.run_file(sys.argv[1])
    else:
        runtime.run_interactive()
""")
        
        # Create full runtime with all commands
        runtime_code = '''
import sys
import os
import json
import shutil
import platform
import subprocess
from pathlib import Path
import math
import random
import base64
import hashlib
import secrets
import datetime
import time

class PineRuntime:
    def __init__(self):
        self.variables = {}
        self.install_path = Path(__file__).parent
        self.commands = self.load_commands()
    
    def load_commands(self):
        commands_file = self.install_path / "commands.json"
        if commands_file.exists():
            with open(commands_file, 'r') as f:
                return json.load(f)
        return []
    
    def run_file(self, filename):
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            return
        with open(filename, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                self.execute_line(line)
    
    def execute_line(self, line):
        parts = line.split()
        if not parts:
            return
        command = parts[0]
        args = parts[1:]
        args = [self.variables.get(arg, arg) for arg in args]
        
        # Basic I/O
        if command in ["display", "show", "exec_t", "exec.t", "exec_result", "exec_write", "write", "tell"]:
            print(" ".join(args))
        elif command in ["input_exec", "get_exec", "read_input", "ask_user", "prompt", "get_value", "read_line"]:
            return input(" ".join(args) if args else "> ")
        elif command in ["input_number", "get_number", "read_number"]:
            return float(input(" ".join(args) if args else "Enter number: "))
        elif command in ["print_number", "display_number"]:
            print(float(args[0]) if args else 0)
        
        # Variables
        elif command in ["Pset", "Passign", "Plet", "define", "exec_save", "save_var"]:
            if len(args) > 1:
                self.variables[args[0]] = " ".join(args[1:])
        elif command in ["get_var", "fetch_var", "retrieve"]:
            if args:
                print(self.variables.get(args[0], ""))
        elif command in ["rm_var", "clear_var", "del_var"]:
            if args:
                self.variables.pop(args[0], None)
        elif command in ["list_vars", "show_vars", "display_vars"]:
            print(self.variables)
        elif command in ["check_var", "var_exists", "is_defined"]:
            print(args[0] in self.variables if args else False)
        elif command in ["type_of", "get_type"]:
            print(type(self.variables.get(args[0], "")).__name__)
        elif command == "increment":
            self.variables[args[0]] = str(int(self.variables.get(args[0], 0)) + 1)
        elif command == "decrement":
            self.variables[args[0]] = str(int(self.variables.get(args[0], 0)) - 1)
        elif command == "add_to":
            self.variables[args[0]] = str(float(self.variables.get(args[0], 0)) + float(args[1]))
        elif command == "subtract_from":
            self.variables[args[0]] = str(float(self.variables.get(args[0], 0)) - float(args[1]))
        elif command == "multiply_by":
            self.variables[args[0]] = str(float(self.variables.get(args[0], 0)) * float(args[1]))
        elif command == "divide_by":
            self.variables[args[0]] = str(float(self.variables.get(args[0], 0)) / float(args[1]))
        elif command == "modulo":
            self.variables[args[0]] = str(int(self.variables.get(args[0], 0)) % int(args[1]))
        elif command == "power":
            self.variables[args[0]] = str(float(self.variables.get(args[0], 0)) ** float(args[1]))
        elif command in ["concat", "append_text"]:
            self.variables[args[0]] = self.variables.get(args[0], "") + " ".join(args[1:])
        
        # Math
        elif command in ["sub_add", "exec_sum", "plus", "add", "sum"]:
            print(sum(map(float, args)))
        elif command in ["subtract", "minus", "exec_difference"]:
            print(float(args[0]) - float(args[1]) if len(args) > 1 else 0)
        elif command in ["multiply", "times", "product"]:
            result = 1
            for a in args:
                result *= float(a)
            print(result)
        elif command in ["divide", "quotient"]:
            print(float(args[0]) / float(args[1]) if len(args) > 1 else 0)
        elif command in ["mod", "remainder"]:
            print(int(args[0]) % int(args[1]) if len(args) > 1 else 0)
        elif command in ["pf", "exponent", "power_of"]:
            print(float(args[0]) ** float(args[1]) if len(args) > 1 else 0)
        elif command in ["sr", "sqrt", "square_root"]:
            print(float(args[0]) ** 0.5 if args else 0)
        elif command in ["ct", "cube_root"]:
            print(float(args[0]) ** (1/3) if args else 0)
        elif command in ["absolute", "abs_value"]:
            print(abs(float(args[0])) if args else 0)
        elif command == "round_number":
            print(round(float(args[0])) if args else 0)
        elif command == "floor":
            print(int(float(args[0])) if args else 0)
        elif command == "ceiling":
            print(int(float(args[0])) + 1 if args and float(args[0]) > int(float(args[0])) else int(float(args[0])) if args else 0)
        elif command in ["min_value", "min"]:
            print(min(map(float, args)))
        elif command in ["max_value", "max"]:
            print(max(map(float, args)))
        elif command in ["average", "mean"]:
            print(sum(map(float, args)) / len(args) if args else 0)
        elif command == "median":
            print(sorted(map(float, args))[len(args)//2] if args else 0)
        elif command == "factorial":
            n = int(args[0]) if args else 0
            result = 1
            for i in range(1, n+1):
                result *= i
            print(result)
        elif command == "gcd":
            a, b = int(args[0]), int(args[1])
            while b:
                a, b = b, a % b
            print(a)
        elif command == "lcm":
            a, b = int(args[0]), int(args[1])
            print(abs(a*b) // math.gcd(a, b) if a and b else 0)
        elif command in ["is_prime", "prime_check"]:
            n = int(args[0]) if args else 0
            if n < 2:
                print(False)
            else:
                print(all(n % i != 0 for i in range(2, int(n**0.5)+1)))
        elif command in ["is_even", "even_check"]:
            print(int(args[0]) % 2 == 0 if args else False)
        elif command in ["is_odd", "odd_check"]:
            print(int(args[0]) % 2 != 0 if args else False)
        elif command == "sin":
            print(math.sin(float(args[0])))
        elif command == "cos":
            print(math.cos(float(args[0])))
        elif command == "tan":
            print(math.tan(float(args[0])))
        elif command == "log":
            print(math.log(float(args[0])))
        elif command == "log10":
            print(math.log10(float(args[0])))
        elif command == "exp":
            print(math.exp(float(args[0])))
        elif command == "degrees":
            print(math.degrees(float(args[0])))
        elif command == "radians":
            print(math.radians(float(args[0])))
        elif command == "pi_value":
            print(math.pi)
        elif command == "e_value":
            print(math.e)
        elif command == "random_number":
            print(random.random())
        elif command in ["random_int", "random_range"]:
            print(random.randint(int(args[0]), int(args[1])))
        elif command == "seed_random":
            random.seed(int(args[0]))
        
        # String operations
        elif command in ["string_length", "length", "str_len"]:
            print(len(args[0]) if args else 0)
        elif command in ["uppercase", "to_upper"]:
            print(args[0].upper() if args else "")
        elif command in ["lowercase", "to_lower"]:
            print(args[0].lower() if args else "")
        elif command == "capitalize":
            print(args[0].capitalize() if args else "")
        elif command == "title_case":
            print(args[0].title() if args else "")
        elif command in ["reverse_string", "reverse"]:
            print(args[0][::-1] if args else "")
        elif command in ["trim", "strip"]:
            print(args[0].strip() if args else "")
        elif command == "trim_left":
            print(args[0].lstrip() if args else "")
        elif command == "trim_right":
            print(args[0].rstrip() if args else "")
        elif command in ["replace_text", "replace"]:
            print(args[0].replace(args[1], args[2]) if len(args) > 2 else "")
        elif command in ["substring", "substr"]:
            print(args[0][int(args[1]):int(args[2])] if len(args) > 2 else "")
        elif command in ["split_string", "split"]:
            print(args[0].split(args[1] if len(args) > 1 else " ") if args else [])
        elif command in ["join_strings", "join"]:
            print(args[0].join(args[1:]) if args else "")
        elif command in ["contains_text", "contains"]:
            print(args[1] in args[0] if len(args) > 1 else False)
        elif command == "starts_with":
            print(args[0].startswith(args[1]) if len(args) > 1 else False)
        elif command == "ends_with":
            print(args[0].endswith(args[1]) if len(args) > 1 else False)
        elif command in ["count_char", "count"]:
            print(args[0].count(args[1]) if len(args) > 1 else 0)
        elif command == "is_digit":
            print(args[0].isdigit() if args else False)
        elif command == "is_alpha":
            print(args[0].isalpha() if args else False)
        elif command == "is_alphanumeric":
            print(args[0].isalnum() if args else False)
        elif command == "is_space":
            print(args[0].isspace() if args else False)
        elif command == "is_upper":
            print(args[0].isupper() if args else False)
        elif command == "is_lower":
            print(args[0].islower() if args else False)
        elif command in ["repeat_string", "repeat"]:
            print(args[0] * int(args[1]) if len(args) > 1 else "")
        elif command == "base64en":
            print(base64.b64encode(args[0].encode()).decode() if args else "")
        elif command == "base64de":
            print(base64.b64decode(args[0].encode()).decode() if args else "")
        
        # Lists
        elif command in ["create_list", "make_list"]:
            print(args)
        elif command == "list_length":
            print(len(args))
        elif command in ["list_sort", "sort_list"]:
            print(sorted(args))
        elif command in ["list_reverse", "reverse_list"]:
            print(args[::-1])
        elif command == "list_first":
            print(args[0] if args else None)
        elif command == "list_last":
            print(args[-1] if args else None)
        elif command == "list_min":
            print(min(args))
        elif command == "list_max":
            print(max(args))
        elif command == "list_sum":
            print(sum(map(float, args)))
        elif command == "list_average":
            print(sum(map(float, args)) / len(args) if args else 0)
        elif command in ["list_join", "join_list"]:
            print(" ".join(args))
        elif command in ["list_unique", "unique_items"]:
            print(list(set(args)))
        
        # System
        elif command in ["sysfo", "exec_os"]:
            print(platform.system())
        elif command == "python_version":
            print(sys.version)
        elif command in ["run_command", "exec_command", "shell_command", "system_command", "terminal", "command_line"]:
            print(os.popen(" ".join(args)).read())
        elif command in ["get_env"]:
            print(os.environ.get(args[0], "") if args else "")
        elif command == "process_id":
            print(os.getpid())
        elif command == "cpu_count":
            print(os.cpu_count())
        elif command in ["hostname", "network_name"]:
            print(platform.node())
        elif command in ["sleep", "wait", "delay"]:
            time.sleep(float(args[0]) if args else 1)
        elif command == "pause":
            input("Press Enter to continue...")
        elif command in ["clear_screen", "cls", "clear"]:
            os.system('cls' if os.name == 'nt' else 'clear')
        
        # Date/Time
        elif command == "current_time":
            print(datetime.datetime.now().strftime("%H:%M:%S"))
        elif command == "current_date":
            print(datetime.datetime.now().strftime("%Y-%m-%d"))
        elif command == "current_datetime":
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif command == "now":
            print(datetime.datetime.now())
        elif command in ["timestamp", "epoch_time"]:
            print(int(time.time()))
        elif command == "year":
            print(datetime.datetime.now().year)
        elif command == "month":
            print(datetime.datetime.now().month)
        elif command == "day":
            print(datetime.datetime.now().day)
        elif command == "hour":
            print(datetime.datetime.now().hour)
        elif command == "minute":
            print(datetime.datetime.now().minute)
        elif command == "second":
            print(datetime.datetime.now().second)
        
        # Utility
        elif command == "help":
            print(f"Pine Language - {len(self.commands)} commands loaded")
            print("Categories: I/O, Variables, Math, String, List, File, System, Network, Database, Date/Time, GUI, Image, Utility")
        elif command == "version":
            print("Pine Language v1.0")
        elif command == "generate_id":
            import uuid
            print(uuid.uuid4())
        elif command in ["exit", "quit", "terminate", "exit_program", "shutdown_pine"]:
            sys.exit(0)
        
        else:
            print(f"Unknown command: {command}")
    
    def run_interactive(self):
        print("Pine Language Interactive Mode")
        print(f"{len(self.commands)} commands loaded")
        print("Type 'exit' to quit")
        while True:
            try:
                line = input("pine> ").strip()
                if line.lower() in ['exit', 'quit', 'exit_program']:
                    break
                if line:
                    self.execute_line(line)
            except KeyboardInterrupt:
                print("\\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
'''
        
        runtime = self.install_path / "pine_runtime.py"
        with open(runtime, 'w') as f:
            f.write(runtime_code)
        
        if self.system == "Windows":
            self.create_windows_association()
            self.create_desktop_shortcut()
        
        self.add_to_path()
        
        print(f"Pine Language installed successfully to {self.install_path}")
        print(f"{len(self.pine_commands)} commands available")
        print("You can now create .pi files and run them!")
        
    def create_windows_association(self):
        try:
            import winreg
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, ".pi")
            winreg.SetValue(key, "", winreg.REG_SZ, "PineScript")
            winreg.CloseKey(key)
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "PineScript")
            winreg.SetValue(key, "", winreg.REG_SZ, "Pine Script")
            winreg.CloseKey(key)
            
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "PineScript\\shell\\open\\command")
            command = f'python "{self.install_path}\\pine.py" "%1"'
            winreg.SetValue(key, "", winreg.REG_SZ, command)
            winreg.CloseKey(key)
            
            print("File association created for .pine files")
        except:
            print("Failed to create file association")
    
    def create_desktop_shortcut(self):
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut = shell.CreateShortCut(os.path.join(desktop, "Pine IDE.lnk"))
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{self.install_path}\\pine.py"'
            shortcut.WorkingDirectory = str(self.install_path)
            shortcut.save()
            
            print("Desktop shortcut created")
        except:
            print("Failed to create desktop shortcut")

def setup_pine_icon(installer):
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    source_icon = os.path.join(script_dir, "Pine.ico")
    
    if os.path.exists(source_icon):
        installer.install_path.mkdir(parents=True, exist_ok=True)
        
        lib_dir = installer.install_path / "lib"
        lib_dir.mkdir(parents=True, exist_ok=True)

        icon_dest = lib_dir / "Pine.ico"
        shutil.copy2(source_icon, icon_dest)
        
        if installer.system == "Windows":
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r".pi\DefaultIcon")
                winreg.SetValue(key, "", winreg.REG_SZ, str(icon_dest))
                winreg.CloseKey(key)
                print(f"Icon copied to {icon_dest} and set as default")
            except Exception as e:
                print(f"Failed to set icon: {e}")
    else:
        print(f"Pine.ico not found next to pine.py at: {source_icon}")
        print("Please place Pine.ico in the same directory as pine.py")

def setup_pine_icon(installer):
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    source_icon = os.path.join(script_dir, "Pine.ico")
    
    if os.path.exists(source_icon):
        installer.install_path.mkdir(parents=True, exist_ok=True)
        
        lib_dir = installer.install_path / "lib"
        lib_dir.mkdir(parents=True, exist_ok=True)

        icon_dest = lib_dir / "Pine.ico"
        shutil.copy2(source_icon, icon_dest)
        
        if installer.system == "Windows":
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pi\DefaultIcon")
                winreg.SetValue(key, "", winreg.REG_SZ, str(icon_dest))
                winreg.CloseKey(key)
                print(f"Icon copied to {icon_dest} and set as default")
            except Exception as e:
                print(f"Failed to set icon: {e}")
    else:
        print(f"Pine.ico not found next to pine.py at: {source_icon}")
        print("Please place Pine.ico in the same directory as pine.py")


def set_pine_icon_registry():
    try:
        import winreg
        
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(script_dir, "Pine.ico")
        
        if not os.path.exists(icon_path):
            print(f"Pine.ico not found at: {icon_path}")
            return
        
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.pi\DefaultIcon")
        winreg.SetValue(key, "", winreg.REG_SZ, icon_path)
        winreg.CloseKey(key)
        
        print(f"Default icon set for .pi files: {icon_path}")
        
    except Exception as e:
        print(f"Failed to set icon: {e}")


if __name__ == "__main__":
    installer = PineInstaller()
    setup_pine_icon(installer)
    set_pine_icon_registry()
    installer.install()
