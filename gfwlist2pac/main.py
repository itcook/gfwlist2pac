#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', required=True,
                      help='path to gfwlist FILE', metavar='FILE')
    parser.add_argument('-f', '--file', dest='output', required=True,
                      help='path to output pac FILE', metavar='FILE')
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

def parse_gfwlist(content):
    print content
    # TODO:
    # return {domains:[], urls:[]}
    pass

def generate_pac(rules):
    # TODO:
    # 1. join tld list with domains existed in domain list to make tld list smaller
    # 2. render the pac file
    # return pac file content
    pass

if __name__ == '__main__':
    args = parse_args()
    with open(args.input, 'rb') as f:
        content = f.read()
    content = decode_gfwlist(content)
    rules = parse_gfwlist(content)
    pac_content = generate_pac(rules)
    with open(args.output, 'wb') as f:
        f.write(pac_content)
    
