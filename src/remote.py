import requests
import log

def read(remote):
    res = requests.get(remote)
    if res.status_code == 200:
        return res.text.split('\n')
    log.warn(str(res.status_code) + " " + res.reason + ": " + remote)
    return []