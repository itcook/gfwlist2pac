#!/bin/bash

pushd .. && \
PYTHONPATH=. python gfwlist2pac/main.py -i test/gfwlist.txt -f test/proxy.pac -p 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;' --user-rule test/user_rule.txt && \
PYTHONPATH=. python gfwlist2pac/main.py --precise -i test/gfwlist.txt -f test/proxy_abp.pac -p 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;' --user-rule test/user_rule.txt && \
popd && \
cat proxy.pac && \
cat proxy.pac test_case.js > /tmp/test.js && \
node /tmp/test.js && \
cat proxy_abp.pac && \
cat proxy_abp.pac test_case.js > /tmp/test.js && \
node /tmp/test.js && \
echo 'Test passed'
