#!/usr/bin/python
# -*- coding: utf-8 -*-

import pkgutil
import urlparse
import json
import logging
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', required=True,
                      help='path to gfwlist FILE', metavar='FILE')
    parser.add_argument('-f', '--file', dest='output', required=True,
                      help='path to output pac FILE', metavar='FILE')
    parser.add_argument('-p', '--proxy', dest='proxy', required=True,
                        help='proxy parameter in the pac file', metavar='PROXY')
    return parser.parse_args()


def decode_gfwlist(content):
    # decode base64 if have to
    try:
        return content.decode('base64')
    except:
        return content

    
def tlds():
    # return tld list
    pass


def get_hostname(something):
    try:
        # quite enough for GFW
        if not something.startswith('http:'):
            something = 'http://' + something
        r = urlparse.urlparse(something)
        return r.hostname
    except Exception as e:
        logging.error(e) 
        return None


def add_domain_to_set(s, something):
    hostname = get_hostname(something)
    if hostname is not None:
        if hostname.startswith('.'):
            hostname = hostname.lstrip('.')
        if hostname.endswith('/'):
            hostname = hostname.rstrip('/')
        if hostname:
            s.add(hostname)


def parse_gfwlist(content):
    gfwlist = content.splitlines(False)
    domains = set(['google.com', 'wikipedia.org'])
    for line in gfwlist:
        if line.find('.*') >= 0:
            continue
        elif line.find('*') >= 0:
            line = line.replace('*', '/')
        if line.startswith('!'):
            continue
        elif line.startswith('['):
            continue
        elif line.startswith('@'):
            # ignore white list
            continue
        elif line.startswith('||'):
            add_domain_to_set(domains, line.lstrip('||'))
        elif line.startswith('|'):
            add_domain_to_set(domains, line.lstrip('|'))
        elif line.startswith('.'):
            add_domain_to_set(domains, line.lstrip('.'))
        else:
            add_domain_to_set(domains, line)
    # TODO: reduce ['www.google.com', 'google.com'] to ['google.com']
    return domains


def join_pac(domains):
    # the entire tld list is too large. we'll output tlds only appeared in the domain list
    tld_content = pkgutil.get_data('resources', 'tld.txt')
    tlds = set(tld_content.splitlines(False))
    known_domains = set()
    for domain in domains:
        domain_parts = domain.split('.')
        for i in xrange(0, len(domain_parts)):
            known_domain = '.'.join(domain_parts[len(domain_parts) - i - 1:])
            known_domains.add(known_domain)
    return tlds.intersection(known_domains)


def generate_pac(domains, proxy):
    # 1. join tld list with domains appeared in domain list
    # 2. render the pac file
    proxy_content = pkgutil.get_data('resources', 'proxy.pac')
    tlds = join_pac(domains)
    tlds_dict = {}
    for tld in tlds:
        tlds_dict[tld] = 1
    domains_dict = {}
    for domain in domains:
        domains_dict[domain] = 1
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__TLDS__', json.dumps(tlds_dict, indent=2))
    proxy_content = proxy_content.replace('__DOMAINS__', json.dumps(domains_dict, indent=2))
    return proxy_content


def main():
    args = parse_args()
    with open(args.input, 'rb') as f:
        content = f.read()
    content = decode_gfwlist(content)
    domains = parse_gfwlist(content)
    pac_content = generate_pac(domains, args.proxy)
    with open(args.output, 'wb') as f:
        print pac_content
        f.write(pac_content)
        

if __name__ == '__main__':
    main()

