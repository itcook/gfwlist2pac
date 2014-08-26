
// This test case should run after the pac script

proxy = 'PROXY';

console.assert('PROXY' == FindProxyForURL('http://www.google.com/search?q=helloworld', 'www.google.com'));
console.assert('PROXY' == FindProxyForURL('https://smtp.google.com/', 'smtp.google.com'));
console.assert('PROXY' == FindProxyForURL('https://a.google.com/', 'a.google.com'));
console.assert('PROXY' == FindProxyForURL('https://a.b.google.com/', 'a.b.google.com'));
console.assert('PROXY' == FindProxyForURL('https://a.b.c.google.com/', 'a.b.c.google.com'));
console.assert('PROXY' == FindProxyForURL('https://www.twitter.com/', 'www.twitter.com'));
console.assert('PROXY' == FindProxyForURL('http://www.facebook.com/', 'www.facebook.com'));
console.assert('PROXY' == FindProxyForURL('http://www.google.co.jp/', 'www.google.co.jp'));
console.assert('PROXY' == FindProxyForURL('http://www.facebook.com/', 'www.facebook.com'));
console.assert('PROXY' == FindProxyForURL('http://www.youtube.com/', 'www.youtube.com'));
console.assert('PROXY' == FindProxyForURL('http://s.ytimg.com/', 's.ytimg.com'));
console.assert('PROXY' == FindProxyForURL('https://r1---sn-a5m7zu7l.googlevideo.com/videoplayback?expire=1395089125&fexp=931919%2C936903%2C943103%2C916625%2C910834%2C937417%2C913434%2C936910%2C936913%2C934022%2C3300001%2C3300101%2C3300130%2C3300137%2C3300161%2C3310623%2C3310649&id=cb048f5eb94374cb&requiressl=yes&signature=AA0F7DB3A18F4D376BBD224E27124CF17291D7FF.38C0D47ECEFE8EBE13941024D6E0C2C8F60FA028&clen=1843858&sparams=clen%2Cdur%2Cgir%2Cid%2Cip%2Cipbits%2Citag%2Clmt%2Crequiressl%2Csource%2Cupn%2Cexpire&ipbits=0&upn=oj-aQXhXwbw&itag=243&dur=74.520&lmt=1395027800917214&ip=106.187.46.253&key=yt5&gir=yes&sver=3&source=youtube&cpn=vm3zeV79pZjco-re&alr=yes&mime=video%2Fwebm&ratebypass=yes&redirect_counter=1&cms_redirect=yes&ms=tsu&mt=1395068116&mv=m&range=255812-336599&keepalive=yes', 'r1---sn-a5m7zu7l.googlevideo.com'));
console.assert('PROXY' == FindProxyForURL('http://appspot.com/', 'appspot.com'));
console.assert('PROXY' == FindProxyForURL('http://my.appspot.com/', 'my.appspot.com'));

console.assert('PROXY' == FindProxyForURL('http://www.userdefined.com/', 'www.userdefined.com'));

console.assert('DIRECT;' == FindProxyForURL('http://www.baidu.com', 'www.baidu.com'));
console.assert('DIRECT;' == FindProxyForURL('http://www.youku.com', 'www.youku.com'));
console.assert('DIRECT;' == FindProxyForURL('http://www.taobao.com', 'www.taobao.com'));
console.assert('DIRECT;' == FindProxyForURL('http://www.baidu.com', '.com'));
console.assert('DIRECT;' == FindProxyForURL('http://www.baidu.com', '.'));
