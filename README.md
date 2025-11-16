# Manx
Download, parse, and filter multiple blocklists and inject them directly into your dnsmasq or hosts configurations. Manx is capable of reading dnsmasq, hosts, adblock, and domain-only entries; it can output any of these types using the syntax argument. See the Syntax section for more information.

## Docker
Build the docker image using the following command in project root directory:

`$ docker build . --tag manx:dev`

Application can be run by using the following command, where /path/to/config points to a directory containing both a blocklist.txt and whitelist.txt file to be consumed. The whitelist can be empty. A combined output file named blacklist.conf will be produced in the same directory if the process completes successfully:

`$ docker run --rm --name manx -v /path/to/config:/manx manx:dev`

## Installation
To install the binary on your computer, run
`$ chmod +x install.sh`
`# ./install.sh`

## Usage
There are several ways to configure this application to produce the requested output.

`$ manx [-h|--help] [-o|--output FILE] [-T FORMAT] [-v] [-x] [-s|--syntax KEY] [-w|-W FILE] FILE`

### Simple
All uses require a list of blocklist urls outlined in an external text file. Urls must be line-delimited.

`$ manx blocklist.txt`

### Whitelist
Similar to the blocklist file, a whitelist text file may be provided that contains urls to omit from the final blacklist. Use -w to comment out matching urls, or -W to remove them from the list completely.

`$ manx -w whitelist.txt blocklist.txt`

### Output
Specify an output configuration file. This file is typically lead by some information about this application and a timestamp. By default, blacklist.conf is produced in the script directory.

`$ manx -o /etc/dnsmasq.d/blacklist.conf -w whitelist.txt blocklist.txt`

### Time Format
By default, manx provides some basic information about the blacklist at the head of the output file, including number of urls and version number of the program. One of these lines includes a time stamp representing when the file was created. By default, the format used is of ISO 8601. However, another format can be selected by passing the `-T` parameter.

`$ manx -w whitelist.txt -T '%Y-%m-%d %H:%M:%S' blocklist.txt`

**Note:** If the -x parameter is passed, no header information is produced. If -T and -x are passed, the program will issue a warning that the custom time formatting will be ignored.

### Syntax
Manx can write the output file in any format that it can interpret. By default, the format used is dnsmasq >= 2.86. Options below are passed with the `-s` or `--syntax` directive

| Format        |  Argument   |
| :---          |       ----: |
| dnsmasq>=2.86 | `local`     |
| dnsmasq<2.86  | `server`    |
| hosts         | `hosts`     |
| adblock       | `adblock`   |
| domain-only   | `domain`    |

## Manx-Daemon
The installer includes manx-daemon, which can be hooked into a systemd unit. This script uses the following command
`$ manx -v -o /etc/dnsmasq.d/blacklist.txt -w /etc/manx/whitelist.txt /etc/manx/blocklist.txt`