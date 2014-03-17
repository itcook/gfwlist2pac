
// 1. Test if url matches url dictionary
// 2. Split host into ['www', 'google.co.jp']. If the host itself is a tld, just output it.
// 3. Build a reversal list ['google.co.jp', 'www.google.co.jp']
// 4. Test each host in the host dictionary

// https://wiki.mozilla.org/TLD_List
// http://publicsuffix.org/
var tlds = __TLDS__;

var domainDict = __DOMAINS__;

function FindProxyForURL(url, host) {
    // TODO
}
