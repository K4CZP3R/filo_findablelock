import app_config
from filoModules.Tools import Tools
log_file = app_config.LOG_FILE_PATH


def read_from_line(start_line):
    f = open(log_file, 'r')
    lines = f.readlines()

    for i in range(start_line, len(lines)):
        start_line += 1
        width = Tools.get_terminal_size()[0]
        print(lines[i].strip()[:width])
    return start_line


s=0
while True:
    s = read_from_line(s)