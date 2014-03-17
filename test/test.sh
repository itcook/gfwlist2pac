#!/bin/bash

pushd .. && \
python gfwlist2pac/main.py  -i test/gfwlist.txt -f proxy.pac -p 'SOCKS5 127.0.0.1:1080' && \
popd && \
cat ../proxy.pac test_case.js > /tmp/test.js && \
node /tmp/test.js