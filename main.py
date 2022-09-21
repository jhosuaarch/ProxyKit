import os
import sys
import json
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs

# Color
G = "\033[1;32m"
R = "\033[1;91m"
W = "\033[1;97m"
B = "\033[1;94m"


banner = """{} _____                 _____ _ _   
|  _  |___ ___ _ _ _ _|  |  |_| |_ 
|   __|  _| . |_'_| | |    -| |  _|
|__|  |_| |___|_,_|_  |__|__|_|_|  
                  |___|    {}

{} - {}Author    : {}Jhosua
{} - {}Facebook  : {}https://www.facebook.com/kzdgzr{}
""".format(B,W,G,W,G,G,W,G,W)


URL_BASE = "https://api.proxyscrape.com/v2/?request=proxyinfo&protocol={}&timeout={}&country=all&ssl=all&anonymity=all&simplified=true"
URL_DOWN = "https://api.proxyscrape.com/v2/?request=getproxies&protocol={}&timeout={}&country=all&ssl=all&anonymity=all&simplified=true"
URL_SCRAP = "https://www.freeproxy.world/?type=&anonymity=&country=&speed=&port=&page=500"


def checkerProxy(listProxy,output):
     try:
          for proxyList in listProxy.splitlines():
               with open(output,mode='a') as f:
                    r = requests.post("https://api.proxyscrape.com/v2/online_check.php",data={"ip_addr[]":[proxyList]})
                    data = json.loads(r.text)[0]
                    if(data["working"] == True):
                         print(f"{W}[{data['country']}{W}] [{G}LIVE{W}] {proxyList}")
                         f.write(str(proxyList) + "\n")
                    else:
                         print(f"{W}[UN] [{R}DEAD{W}] {proxyList}")
     except:
          pass


def dumpProxy(protocol,out):
     r = requests.get(URL_BASE.format(protocol,out)).json()
     if(r["proxy_count"] != 0 ):
          print("{}[{}!{}] Proxies found as many as {}{}{}".format(W,G,W,G,r["proxy_count"],W))
          raw = requests.get(URL_DOWN.format(protocol,out))
          ge = requests.get(URL_SCRAP).text
          sop = bs(ge,'lxml')
          tab = sop.find('tbody').find_all('tr')
          proxList = []
          for x in tab:
               if x.texts.replace('\n',''):
                    td = x.find_all('td')
                    prox = td[0].text.replace('\n','')
                    port = td[1].text.replace('\n','')
                    typ = td[5].text.replace('\n','').replace(' ','')
                    if protocol == typ:
                         proxList.append(f"{prox}:{port}")
                    else:
                         proxList.append(f"{prox}:{port}")
          proxList.append(raw.text.replace("\n", ""))
          output = input("{}[{}-{}] Save As : ".format(W,G,W))
          with open(output,'a') as f:
               for res in proxList:
                    f.write(f"{res}\n")

     else:
          print("{}[{}!{}] Proxy Not Found!".format(W,R,W))

def clear_system():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == '__main__':
     clear_system()
     print(banner)
     parser = argparse.ArgumentParser(description="ProxyKit")
     parser.add_argument('-p',type=str,help="Proxy Protocols, Exam : http,socks4,socks5")
     parser.add_argument('-t',type=int,help="Timeout Proxy")
     parser.add_argument('-f',type=str,help="List file proxy")
     parser.add_argument('-o',type=str,help="Output file")

     args = parser.parse_args()

     with ThreadPoolExecutor(max_workers=30) as th:
          if(args.p != None and args.t != None and args.f == None):
               if(args.p in ["http","socks4","socks5"]):
                    th.submit(dumpProxy,args.p,args.t)
               else:
                    print(f"[{R}!{W}] Incorrect Proxy Protocol")
     
          elif(args.f != None and args.t == None and args.p == None):
               if(args.o != None):
                    try:
                         listProxy = open(args.f).read()
                         th.submit(checkerProxy,listProxy,args.o)
                    except FileNotFoundError:
                         print(f"[{R}!{W}] File not found!")
               else:
                    print(f"[{R}!{W}] Enter output file!")

          else:
               print(f"- Download Proxy: {sys.argv[0]} -p socks4 -t 300\n- Checking Proxy: {sys.argv[0]} -f listproxy.txt -o output.txt\n\n")
