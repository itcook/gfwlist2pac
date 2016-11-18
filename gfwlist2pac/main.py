#!/usr/bin/python
# -*- coding: utf-8 -*-

import pkgutil
import base64
import urllib.parse
import json
import logging
from argparse import ArgumentParser

__all__ = ['main']


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', required=True,
                        help='path to gfwlist', metavar='GFWLIST')
    parser.add_argument('-f', '--file', dest='output', required=True,
                        help='path to output pac', metavar='PAC')

    parser.add_argument('-p', '--proxy', dest='proxy', required=True,
                        help='the proxy parameter ini the pac file, for example, \
        SOCKS5 127.0.0.1:1080;', metavar='PROXY')
    return parser.parse_args()


def decode_gfwlist(content):
    try:
        return base64.decodebytes(content)
    except Exception as e:
        logging.error(e)
        return content


def get_hostname(element):
    try:
        if not element.startswith(b'http:'):
            element = b'http://' + element
        r = urllib.parse.urlparse(element)
        return r.hostname
    except Exception as e:
        logging.error(e)
        return None


def add_domain_to_set(s, element):
    hostname = get_hostname(element)
    if hostname is not None:
        if hostname.startswith(b'.'):
            hostname = hostname.lstrip(b'.')
        if hostname.endswith(b'/'):
            hostname = hostname.rstrip(b'/')
        if hostname:
            s.add(hostname.decode('utf-8'))


def parse_gfwlist(content):
    builtin_rules = pkgutil.get_data(
        'gfwlist2pac', 'resources/builtin.txt').splitlines(False)
    gfwlist = content.splitlines(False)
    domains = set([domain.decode('utf-8') for domain in builtin_rules])
    for line in gfwlist:
        if line.find(b'.*') >= 0:
            continue
        if line.find(b'*') >= 0:
            line = line.replace(b'*', b'/')
        if line.startswith(b'!'):
            continue
        elif line.startswith(b'['):
            continue
        elif line.startswith(b'@'):
            continue
        elif line.startswith(b'||'):
            add_domain_to_set(domains, line.lstrip(b'||'))
        elif line.startswith(b'|'):
            add_domain_to_set(domains, line.lstrip(b'|'))
        elif line.startswith(b'.'):
            add_domain_to_set(domains, line.lstrip(b'.'))
        else:
            add_domain_to_set(domains, line)
    return domains


def generate_pac(domains, proxy):
    proxy_content = pkgutil.get_data('gfwlist2pac', 'resources/proxy.pac')
    # domains_dict = {}
    # for domain in domains:
    #     domains_dict[domain.decode('utf-8')] = 1
    proxy_content = proxy_content.replace(
        b'__PROXY__', bytes(proxy, encoding='utf-8'))
    proxy_content = proxy_content.replace(
        b'__DOMAINS__', json.dumps(list(domains), indent=4).encode('utf-8'))
    return proxy_content


def main():
    args = parse_args()
    with open(args.input, 'rb') as f:
        content = f.read()
    content = decode_gfwlist(content)
    domains = parse_gfwlist(content)
    pac_content = generate_pac(domains, args.proxy)
    with open(args.output, 'wb') as f:
        f.write(pac_content)


if __name__ == '__main__':
    main()
