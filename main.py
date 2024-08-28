import argparse
import urls, out, log

def main():
    parser = argparse.ArgumentParser(
        prog='Update Blocklist',
        description='Combines multiple blocklist files into a single dnsmasq configuration file. This program is limited to dnsmasq blocklists since 2.86'
    )
    parser.add_argument('path', type=argparse.FileType('r'), metavar='FILE', help='Required. New-line delimited list of urls. Use # for comments')
    parser.add_argument('-i', '--install', default=False, action='store_true', help='Install the configuration file and restart dnsmasq. Must be run as root.')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), metavar='FILE', default='blacklist.conf', help='Output file name. Defaults to blocklist.conf')
    parser.add_argument('-T', default='%Y-%m-%d %H:%M:%S', metavar='FORMAT', help='Set the time stamp formatting using python standard strftime format')

    wl_arg_grp = parser.add_argument_group('Whitelist', 'Provide a newline-separated list of urls to whitelist')
    wl_group = wl_arg_grp.add_mutually_exclusive_group()
    wl_group.add_argument('-w', default=None, type=argparse.FileType('r'), metavar='FILE', help='Matching lines will be commented out in the output file')
    wl_group.add_argument('-W', default=None, type=argparse.FileType('r'), metavar='FILE', help='Matching lines will be omitted from the output file')

    #Parse those args
    args = parser.parse_args()
    
    #Read blocklist urls
    log.info("Processing lists")
    blocklist_urls = urls.read_from_file(args.path)

    #Read whitelist urls
    omit = args.W is not None
    whitelist_urls = []
    if args.w is not None:
        whitelist_urls = urls.read_from_file(args.w)
    elif args.W is not None:
        whitelist_urls = urls.read_from_file(args.W)

    #Read blacklist urls
    log.info("Processing blacklisted urls")
    blacklist_urls = []
    for url in blocklist_urls:
        blacklist_urls += urls.read_from_remote(url.rstrip())
    blacklist_urls = sorted(set(blacklist_urls))

    #Remove whitelisted urls
    log.info("Processing output lines")
    out_lines = urls.to_lines(blacklist_urls, whitelist_urls, omit, 0)

    #Write out
    log.info("Writing to disk")
    out.to_file(out_lines, args.output, args.T)
    if args.install:
        log.error("Install not yet implemented")
        #out.install()

if __name__ == '__main__':
    main()