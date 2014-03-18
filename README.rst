GFWList2PAC
===========

|Build Status|

Generate O(1) PAC file from gfwlist.

::

    pip install gfwlist2pac

    usage: gfwlist2pac [-h] -i GFWLIST -f PAC -p PROXY [--user-rule USER_RULE]

    optional arguments:
      -h, --help            show this help message and exit
      -i GFWLIST, --input GFWLIST
                            path to gfwlist
      -f PAC, --file PAC    path to output pac
      -p PROXY, --proxy PROXY
                            the proxy parameter in the pac file, for example,
                            "SOCKS5 127.0.0.1:1080;"
      --user-rule USER_RULE
                            user rule file, which will be appended to gfwlist

.. |Build Status| image:: https://travis-ci.org/clowwindy/gfwlist2pac.png?branch=master
   :target: https://travis-ci.org/clowwindy/gfwlist2pac
