import re
import requests
from bs4 import BeautifulSoup
import os
import datetime
import requests
import base64
import random
from pystyle import Write,Colors
from pystyle import Colors, Colorate
listwebsite  = [
            'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http',
            'https://www.freeproxychecker.com/result/http_proxies.txt',
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://www.freeproxychecker.com/result/https_proxies.txt',
' https://www.proxy-list.download/api/v1/get?type=http',

'https://www.proxyscan.io/download?type=https',
             'https://spys.me/proxy.txt',
             'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt',
             'https://api.openproxylist.xyz/http.txt',
             'https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt',
             'http://alexa.lr2b.com/proxylist.txt',
             'http://rootjazz.com/proxies/proxies.txt',
             'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
             'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt',
             'https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt',
             'https://proxy-spider.com/api/proxies.example.txt',
             'https://multiproxy.org/txt_all/proxy.txt',
             'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt'
             'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/free.txt',
             'https://raw.githubusercontent.com/saisuiu/Lionkings-Http-Proxys-Proxies/main/cnfree.txt',
             'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt',
             'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt',
              'https://free-proxy.pro/proxy.txt',
'https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt',
'https://sunny9577.github.io/proxy-scraper/proxies.txt',
'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt',
'https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt',
		"https://openproxylist.xyz/http.txt",
		"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
		"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
		"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
		"https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
		"https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt",
		"https://raw.githubusercontent.com/andigwandi/free-proxy/main/proxy_list.txt",
		"https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
		"https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
		"https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
		"https://raw.githubusercontent.com/zloi-user/hideip.me/main/connect.txt",
		"https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
		"https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
		"https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt",
      "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
     "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
   "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
   "https://raw.githubusercontent.com/TuanMinPay/live-proxy/refs/heads/master/all.txt",
  "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/HTTPS_RAW.txt",  "https://spys.me/socks.txt",
 "https://spys.one/free-proxy-list/",
 "https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country=US",
 "https://www.proxy-list.download/api/v1/get?type=http&anon=transparent&country=US",
"https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/http.txt",
"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt","https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/https.txt",
"https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/socks4.txt",
"https://raw.githubusercontent.com/Simatwa/free-proxies/master/files/http.json",
"https://raw.githubusercontent.com/Simatwa/free-proxies/master/files/socks5.json",
"https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
"https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/http_checked.txt","https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/http.txt",
"https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/socks5_checked.txt",
"https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
"https://raw.githubusercontent.com/tuanminpay/live-proxy/master/socks4.txt",
'https://raw.githubusercontent.com/jepluk/PROXYLIST/main/all.json',
'https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt',
'https://raw.githubusercontent.com/Isloka/proxyscraper/refs/heads/main/proxies/http.txt',
'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt',
'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt',
'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/http.txt',
'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/https.txt',
'https://raw.githubusercontent.com/MrMarble/proxy-list/refs/heads/main/all.txt',
'https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/refs/heads/main/proxies.txt',
]
def clear():
    os.system("cls" if os.name == "nt" else "clear")
def banner():
    Write.Print("""
 \033[32m██████╗ ██╗   ██╗██╗   ██╗    ██████╗ ███████╗ ██████╗     ██████╗ ███████╗██╗   ██╗\033[0m
\033[32m██╔═══██╗██║   ██║╚██╗ ██╔╝    ██╔══██╗██╔════╝██╔═══██╗    ██╔══██╗██╔════╝██║   ██║\033[0m
\033[32m██║   ██║██║   ██║ ╚████╔╝     ██████╔╝█████╗  ██║   ██║    ██║  ██║█████╗  ██║   ██║\033[0m
\033[32m██║▄▄ ██║██║   ██║  ╚██╔╝      ██╔══██╗██╔══╝  ██║   ██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝\033[0m
\033[32m╚██████╔╝╚██████╔╝   ██║       ██████╔╝███████╗╚██████╔╝    ██████╔╝███████╗ ╚████╔╝ \033[0m
 \033[32m╚══▀▀═╝  ╚═════╝    ╚═╝       ╚═════╝ ╚══════╝ ╚═════╝     ╚═════╝ ╚══════╝  ╚═══╝  """+'\n', Colors.green_to_red, interval=0.0001)
def get_proxies_from_website(url):
	try:
	    response = requests.get(url)
	    try:
	        if response.status_code == 200:
	            try:
	                pattern = r'\b(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)\b'
	                proxy_matches = re.findall(pattern, response.text)
	                return proxy_matches
	            except:
	                data = response.json()['data']
	                proxy_matches = []
	                for entry in data:
	                    ip = entry.get('ip')
	                    port = entry.get('port')
	                    if ip and port:
	                        proxy_matches.append(ip + ':' + port)
	                return proxy_matches
	        else:
	            return []
	    except:
	        return []
	except:
		return []
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
output_file = "proxy.txt"
i = 0
with open(output_file, 'w') as file:
    for web in listwebsite:
        result = get_proxies_from_website(web)
        for proxy in result:
            i += 1
            file.write(proxy + '\n')
            print(f"[{i}] - [BANNGUVC] | {proxy}")





