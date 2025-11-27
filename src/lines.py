import utils
import log

dnsmasq_2_86_prefix = 'local=/'
dnsmasq_2_85_prefix = 'server=/'
dnsmasq_postfix = '/'
hosts_prefix = '0.0.0.0 '
adblock_prefix = '||'
adblock_postfix = '^'

def strip(lines):
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
                if len(word.rstrip()) > 0 and utils.is_valid_hostname(word):
                    bad_urls.append(word)
                    break
            else:
                log.warn("blacklist line " + line + " was invalid")
    return bad_urls

def add_syntax(blacklist, whitelist, omit, method):
    lines = []
    for url in blacklist:
        line = ''
        for wl in whitelist:
            if url == wl or url.endswith('.' + wl):
                log.info("Whitelist item " + url + " found in blacklist")
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