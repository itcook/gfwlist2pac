GFWList2PAC
===========

[![Build Status](https://travis-ci.org/clowwindy/gfwlist2pac.png?branch=master)](https://travis-ci.org/clowwindy/gfwlist2pac)

Generate O(1) PAC file from gfwlist.

    pip install gfwlist2pac

    usage: gfwlist2pac [-h] -i GFWLIST -f PAC -p PROXY
    
    optional arguments:
      -h, --help            show this help message and exit
      -i GFWLIST, --input GFWLIST
                            path to gfwlist
      -f PAC, --file PAC    path to output pac
      -p PROXY, --proxy PROXY
                            the proxy parameter in the pac file, for example,
                            "SOCKS5 127.0.0.1:1080;"
