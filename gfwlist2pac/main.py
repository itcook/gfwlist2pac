#!/usr/bin/python
# -*- coding: utf-8 -*-

import pkgutil
import urlparse
import json
import logging
import urllib2
from argparse import ArgumentParser

__all__ = ['main']


gfwlist_url = 'https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt'


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input',
                        help='path to gfwlist', metavar='GFWLIST')
    parser.add_argument('-f', '--file', dest='output', required=True,
                        help='path to output pac', metavar='PAC')
    parser.add_argument('-p', '--proxy', dest='proxy', required=True,
                        help='the proxy parameter in the pac file, '
                             'for example, "SOCKS5 127.0.0.1:1080;"',
                        metavar='PROXY')
    parser.add_argument('--user-rule', dest='user_rule',
                        help='user rule file, which will be appended to'
                             ' gfwlist')
    parser.add_argument('--precise', dest='precise', action='store_true',
                        help='use adblock plus algorithm instead of O(1)'
                             ' lookup')
    return parser.parse_args()


def decode_gfwlist(content):
    # decode base64 if have to
    try:
        if '.' in content:
            raise Exception()
        return content.decode('base64')
    except:
        return content


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
        s.add(hostname)


def combine_lists(content, user_rule=None):
    builtin_rules = pkgutil.get_data('gfwlist2pac',
                                     'resources/builtin.txt').splitlines(False)
    gfwlist = content.splitlines(False)
    gfwlist.extend(builtin_rules)
    if user_rule:
        gfwlist.extend(user_rule.splitlines(False))
    return gfwlist


def parse_gfwlist(gfwlist):
    domains = set()
    for line in gfwlist:
        if line.find('.*') >= 0:
            continue
        elif line.find('*') >= 0:
            line = line.replace('*', '/')
        if line.startswith('||'):
            line = line.lstrip('||')
        elif line.startswith('|'):
            line = line.lstrip('|')
        elif line.startswith('.'):
            line = line.lstrip('.')
        if line.startswith('!'):
            continue
        elif line.startswith('['):
            continue
        elif line.startswith('@'):
            # ignore white list
            continue
        add_domain_to_set(domains, line)
    return domains


def reduce_domains(domains):
    # reduce 'www.google.com' to 'google.com'
    # remove invalid domains
    tld_content = pkgutil.get_data('gfwlist2pac', 'resources/tld.txt')
    tlds = set(tld_content.splitlines(False))
    new_domains = set()
    for domain in domains:
        domain_parts = domain.split('.')
        last_root_domain = None
        for i in xrange(0, len(domain_parts)):
            root_domain = '.'.join(domain_parts[len(domain_parts) - i - 1:])
            if i == 0:
                if not tlds.__contains__(root_domain):
                    # root_domain is not a valid tld
                    break
            last_root_domain = root_domain
            if tlds.__contains__(root_domain):
                continue
            else:
                break
        if last_root_domain is not None:
            new_domains.add(last_root_domain)

    uni_domains = set()
    for domain in new_domains:
        domain_parts = domain.split('.')
        for i in xrange(0, len(domain_parts)-1):
            root_domain = '.'.join(domain_parts[len(domain_parts) - i - 1:])
            if domains.__contains__(root_domain):
                break
        else:
            uni_domains.add(domain)
    return uni_domains


def generate_pac_fast(domains, proxy):
    # render the pac file
    proxy_content = pkgutil.get_data('gfwlist2pac', 'resources/proxy.pac')
    domains_dict = {}
    for domain in domains:
        domains_dict[domain] = 1
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace(
        '__DOMAINS__',
        json.dumps(domains_dict, indent=2, sort_keys=True)
    )
    return proxy_content


def generate_pac_precise(rules, proxy):
    def grep_rule(rule):
        if rule:
            if rule.startswith('!'):
                return None
            if rule.startswith('['):
                return None
            return rule
        return None
    # render the pac file
    proxy_content = pkgutil.get_data('gfwlist2pac', 'resources/abp.js')
    rules = filter(grep_rule, rules)
    proxy_content = proxy_content.replace('__PROXY__', json.dumps(str(proxy)))
    proxy_content = proxy_content.replace('__RULES__',
                                          json.dumps(rules, indent=2))
    return proxy_content


def main():
    args = parse_args()
    user_rule = None
    if (args.input):
        with open(args.input, 'rb') as f:
            content = f.read()
    else:
        print 'Downloading gfwlist from %s' % gfwlist_url
        content = urllib2.urlopen(gfwlist_url, timeout=10).read()
    if args.user_rule:
        userrule_parts = urlparse.urlsplit(args.user_rule)
        if not userrule_parts.scheme or not userrule_parts.netloc:
            # It's not an URL, deal it as local file
            with open(args.user_rule, 'rb') as f:
                user_rule = f.read()
        else:
            # Yeah, it's an URL, try to download it
            print 'Downloading user rules file from %s' % args.user_rule
            user_rule = urllib2.urlopen(args.user_rule, timeout=10).read()

    content = decode_gfwlist(content)
    gfwlist = combine_lists(content, user_rule)
    if args.precise:
        pac_content = generate_pac_precise(gfwlist, args.proxy)
    else:
        domains = parse_gfwlist(gfwlist)
        domains = reduce_domains(domains)
        pac_content = generate_pac_fast(domains, args.proxy)
    with open(args.output, 'wb') as f:
        f.write(pac_content)


if __name__ == '__main__':
    main()
