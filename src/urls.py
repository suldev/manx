import requests
from urllib.parse import urlparse
import log

dnsmasq_2_86_prefix = 'local=/'
dnsmasq_2_85_prefix = 'server=/'
dnsmasq_postfix = '/'
hosts_prefix = '0.0.0.0 '
adblock_prefix = '||'
adblock_postfix = '^'

def lines_to_urls(lines, simple):
    urls = []
    for line in lines:
        if line.startswith('#') or line.startswith('!'): 
            continue
        elif simple:
            if urlparse(line).netloc != '':
                urls.append(urlparse(line).geturl())
        elif line.startswith(dnsmasq_2_86_prefix):
            urls.append(line[len(dnsmasq_2_86_prefix):-len(dnsmasq_postfix)])
        elif line.startswith(dnsmasq_2_85_prefix):
            urls.append(line[len(dnsmasq_2_85_prefix):-len(dnsmasq_postfix)])
        elif line.startswith(hosts_prefix):
            urls.append(line[len(hosts_prefix):])
        elif line.startswith(adblock_prefix):
            urls.append(line[len(adblock_prefix):-len(adblock_postfix)])
        elif urlparse(line).netloc != '':
            urls.append(urlparse(line).netloc)
        elif urlparse(line).path != '':
            urls.append(line.rstrip())
    return urls

def read_from_file(file):
    return lines_to_urls(file.readlines(), True)

def read_from_remote(remote):
    urls = []
    res = requests.get(remote)
    if res.status_code == 200:
        lines = res.text.split('\n')
        urls = lines_to_urls(lines, False)
    return urls

def to_lines(blacklist, whitelist, omit, method):
    lines = []
    for url in blacklist:
        line = ''
        for wl in whitelist:
            if url in wl:
                if omit:
                    continue
                line = '#'
        if method == 0:
            line += dnsmasq_2_86_prefix + url + dnsmasq_postfix
        elif method == 1:
            line += dnsmasq_2_85_prefix + url + dnsmasq_postfix
        elif method == 2:
            line += hosts_prefix + url
        elif method == 3:
            line += url
        elif method == 4:
            line += adblock_prefix + url + adblock_postfix
        if len(line) > 1:
            lines.append(line)
    return lines
        