import argparse
import urls, out, log

def main():
    syntax = {'local' : 0, 'server' : 1, 'hosts' : 2, 'domain' : 3, 'adblock' : 4}
    parser = argparse.ArgumentParser(
        prog='manx',
        description='Combines multiple blocklists into a single dnsmasq configuration file.'
    )
    parser.add_argument('path', type=argparse.FileType('r'), metavar='FILE', help='Required. New-line delimited list of urls. Use # for comments')
    parser.add_argument('-i', '--install', default=False, action='store_true', help='Install the configuration file and restart dnsmasq. Must be run as root.')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), metavar='FILE', default='blacklist.conf', help='Output file name. Defaults to $PWD/blocklist.conf')
    parser.add_argument('-T', default='%Y-%m-%d %H:%M:%S', metavar='FORMAT', help='Set the time stamp formatting using python standard strftime format. Default is ISO8601 format. Not used for -x')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='Print debugging information.')
    parser.add_argument('-x', '--nohead', default=False, action='store_true', help='Do not print header information (program name, version, time, etc.).')
    parser.add_argument('-s', '--syntax', default='local', metavar='KEY', help='Set the output syntax. Options are local, server, hosts, adblock, and domain.')

    wl_arg_grp = parser.add_argument_group('Whitelist', 'Provide a newline-separated list of urls to whitelist')
    wl_group = wl_arg_grp.add_mutually_exclusive_group()
    wl_group.add_argument('-w', default=None, type=argparse.FileType('r'), metavar='FILE', help='Matching lines will be commented out in the output file')
    wl_group.add_argument('-W', default=None, type=argparse.FileType('r'), metavar='FILE', help='Matching lines will be omitted from the output file')

    #Parse those args
    args = parser.parse_args()
    log.verbose = args.verbose
    if(args.syntax not in syntax):
        log.fatal('Invalid syntax.')
    
    #Read blocklist urls
    log.info("Processing lists")
    blocklist_urls = urls.read_blocklist(args.path)

    #Read whitelist urls
    omit = args.W is not None
    whitelist_urls = []
    if args.w is not None:
        whitelist_urls = urls.read_whitelist(args.w)
    elif args.W is not None:
        whitelist_urls = urls.read_whitelist(args.W)

    #Read blacklist urls
    log.info("Processing blacklisted urls")
    blacklist_urls = []
    for url in blocklist_urls:
        blacklist_urls += urls.read_from_remote(url.rstrip())
    blacklist_urls = sorted(set(blacklist_urls))

    #Remove whitelisted urls
    log.info("Processing output lines")
    out_lines = urls.to_lines(blacklist_urls, whitelist_urls, omit, syntax[args.syntax])

    #Write out
    log.info("Writing to disk")
    out.to_file(out_lines, args.output, not args.nohead, args.T)
    if args.install:
        log.error("Install not yet implemented")
        #out.install()

if __name__ == '__main__':
    main()
