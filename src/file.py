from urllib.parse import urlparse
from datetime import datetime
import log

def read_blocklist(file):
    urls = []
    iline = 0
    for line in file.readlines():
        iline = iline + 1
        if line.startswith('#') or len(line.rstrip()) == 0:
            continue
        elif urlparse(line).netloc != '':
            urls.append(urlparse(line).geturl())
        else:
            log.warn("blocklist line " + str(iline) + " contains an invalid url")
    return urls

def read_whitelist(file):
    urls = []
    for line in file.readlines():
        if line.startswith('#'):
            continue
        urls.append(line)
    return urls

def write(lines, file, head, time_format):
    if head:
        file.write("# Manx v0.2\n")
        file.write(f"# Published: {datetime.now().strftime(time_format)}\n")
        file.write(f"# Unique Entries: {len(lines)}\n")
    for line in lines:
        file.write(f"{line}\n")