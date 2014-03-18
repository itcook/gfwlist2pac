#!/bin/bash

pushd .. && \
PYTHONPATH=. python gfwlist2pac/main.py  -i test/gfwlist.txt -f test/proxy.pac -p 'SOCKS5 127.0.0.1:1080' --user-rule test/user_rule.txt && \
popd && \
cat proxy.pac && \
cat proxy.pac test_case.js > /tmp/test.js && \
node /tmp/test.js && \
echo 'Test passed'
