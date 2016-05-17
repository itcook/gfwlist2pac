#!/bin/bash

pushd ..
coverage erase
PYTHONPATH=. coverage run -a gfwlist2pac/main.py -i test/gfwlist.txt -f test/proxy.pac -p 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;' --user-rule https://raw.githubusercontent.com/clowwindy/gfwlist2pac/master/test/user_rule.txt && \
PYTHONPATH=. coverage run -a gfwlist2pac/main.py -f test/proxy.pac -p 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;' --user-rule test/user_rule.txt && \
PYTHONPATH=. coverage run -a gfwlist2pac/main.py -i test/gfwlist.txt -f test/proxy.pac -p 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;' --user-rule test/user_rule.txt && \
cat test/gfwlist.txt | base64 -d | PYTHONPATH=. coverage run -a gfwlist2pac/main.py -i /dev/stdin -f test/proxy_nobase64.pac -p 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;' --user-rule test/user_rule.txt && \
PYTHONPATH=. coverage run -a gfwlist2pac/main.py --precise -i test/gfwlist.txt -f test/proxy_abp.pac -p 'SOCKS5 127.0.0.1:1080; SOCKS 127.0.0.1:1080; DIRECT;' --user-rule test/user_rule.txt && \
diff test/proxy.pac test/proxy_nobase64.pac && \
popd && \
cat proxy.pac test_case.js > /tmp/test.js && \
node /tmp/test.js && \
cat proxy_abp.pac test_case.js > /tmp/test.js && \
node /tmp/test.js && \
cd .. && coverage report --include=gfwlist2pac/* && \
rm -rf htmlcov && \
coverage html --include=gfwlist2pac/* && \
coverage report --include=gfwlist2pac/* | tail -n1 | rev | cut -d' ' -f 1 | rev > /tmp/gfwlist2pac-coverage && \
echo 'Test passed'
