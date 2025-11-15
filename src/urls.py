from urllib.parse import urlparse
import requests, re, log

dnsmasq_2_86_prefix = 'local=/'
dnsmasq_2_85_prefix = 'server=/'
dnsmasq_postfix = '/'
hosts_prefix = '0.0.0.0 '
adblock_prefix = '||'
adblock_postfix = '^'

def is_valid_hostname(hostname):
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253:
        return False

    labels = hostname.split(".")

    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)

def lines_to_urls(lines):
    bad_urls = []
    for line in lines:
        if line.startswith('#') or line.startswith('!') or len(line.rstrip()) == 0:
            continue
        elif line.startswith(dnsmasq_2_86_prefix):
            bad_urls.append(line[len(dnsmasq_2_86_prefix):-len(dnsmasq_postfix)])
        elif line.startswith(dnsmasq_2_85_prefix):
            bad_urls.append(line[len(dnsmasq_2_85_prefix):-len(dnsmasq_postfix)])
        elif line.startswith(hosts_prefix):
            bad_urls.append(line[len(hosts_prefix):])
        elif line.startswith(adblock_prefix):
            bad_urls.append(line[len(adblock_prefix):-len(adblock_postfix)])
        else:
            words = line.split(' ')
            for word in words:
                if len(word.rstrip()) > 0 and is_valid_hostname(word):
                    bad_urls.append(word)
                    break
            else:
                log.warn("blacklist line " + line + " was invalid")
    return bad_urls

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

def read_from_remote(remote):
    urls = []
    res = requests.get(remote)
    if res.status_code == 200:
        lines = res.text.split('\n')
        urls = lines_to_urls(lines)
    else:
        log.warn(str(res.status_code) + " " + res.reason + ": " + remote)
    return urls

def to_lines(blacklist, whitelist, omit, method):
    lines = []
    for url in blacklist:
        line = ''
        for wl in whitelist:
            if wl in url:
                if omit:
                    break
                line = '#'
        else:
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
        
