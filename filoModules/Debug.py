from pathlib import Path
from enum import Enum
import colorama, traceback
from filoModules.Tools import Tools
import config

class DebugTypes(Enum):
    VERBOSE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

class Debug:
    def __init__(self, module_name, allowed_debug_types = [DebugTypes.INFO, DebugTypes.VERBOSE, DebugTypes.DEBUG, DebugTypes.WARNING, DebugTypes.ERROR], enabled=True):
        self.module_name = module_name
        self.allowed_debug_types = allowed_debug_types
        self.enabled = enabled
        colorama.init()
    def reset_log(self):
        if self.debug_file_exists():
            f = open(config.get_log_file_name(), 'w')
            f.write("Log cleared.\n")
            f.close()


    def debug_file_exists(self):
        try:
            f = open(config.get_log_file_name())
        except IOError:
            return False
        f.close()
        return True

    def append_to_log_file(self, content):
        if not self.debug_file_exists():
            f = open(config.get_log_file_name(), 'w')
            f.write("Log init.\n")
            f.close()
        
        f = open(config.get_log_file_name(), 'a+')
        f.write(f"{content}\n")
        f.close()
        


    def print_v(self, content):
        self.out(DebugTypes.VERBOSE, content)
    def print_d(self, content):
        self.out(DebugTypes.DEBUG, content)
    def print_e(self, content):
        self.out(DebugTypes.ERROR, content)
    def print_w(self, content):
        self.out(DebugTypes.WARNING, content)
    def print_i(self, content):
        self.out(DebugTypes.INFO, content)
    def out(self, log_type: DebugTypes, content):
        if log_type not in self.allowed_debug_types or not self.enabled:
            return

        content_plain = content
        if log_type == DebugTypes.ERROR:
            content_plain = f"{content}"
            content = f"{colorama.Fore.RED}{content}{colorama.Fore.RESET}"
        if log_type == DebugTypes.WARNING:
            content_plain = f"{content}"
            content = f"{colorama.Fore.YELLOW}{content}{colorama.Fore.RESET}"
            
        log_type = log_type.name
        stack = traceback.extract_stack(None, 3)[0]
        code_file = Tools.find_between_r(stack[0], "\\",".py")
        code_line = stack[1]
        code_func = stack[2]
        str_to_print = f"{colorama.Fore.YELLOW}[0] {colorama.Fore.GREEN}<{code_file}/{code_func}:{code_line}> {colorama.Fore.CYAN}({log_type}): {colorama.Fore.RESET}{str(content)}"
        str_to_print_plain = f"[0] <{code_file}/{code_func}:{code_line}> ({log_type}): {content_plain}"
        self.append_to_log_file(str_to_print_plain)
        print(str_to_print_plain)