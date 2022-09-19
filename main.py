import os
import sys
import json
import requests
import argparse

# Color
G = "\033[1;32m"
R = "\033[1;91m"
W = "\033[1;97m"

URL_BASE = "https://api.proxyscrape.com/v2/?request=proxyinfo&protocol={}&timeout={}&country=all&ssl=all&anonymity=all&simplified=true"
URL_DOWN = "https://api.proxyscrape.com/v2/?request=getproxies&protocol={}&timeout={}&country=all&ssl=all&anonymity=all&simplified=true"


def getProxy(tproxy,pproxy):
     raw = requests.get(URL_BASE.format(tproxy,pproxy))
     total = json.loads(raw.text)["proxy_count"]
     if(total == 0):
          print("{}[{}!{}] Proxy Not Found!".format(W,R,W))
     else:
          print("{}[{}!{}] Proxies found as many as {}{}{}".format(W,G,W,G,total,W))
          r = requests.get(URL_DOWN.format(tproxy,pproxy))
          output = input("{}[{}-{}] Save As : ".format(W,G,W))
          if os.path.exists(output):
               with open(output,mode="a") as f: f.write(r.text)
          
          if not os.path.exists(output):
               with open(output,mode="w") as f: f.write(r.text)
          
          print("{}[{}!{}] Successfully saved as {}{}{}".format(W,G,W,G,output,W))


if __name__ == '__main__':
     parser = argparse.ArgumentParser(description="Proxy Downloader\n\nCreated By Jhosua\n\n")
     parser.add_argument('-t',type=str,help="Enter type proxy http,socks4,socks5")
     parser.add_argument('-p',type=int,help="Enter Time Respone Exm : 200")
     args = parser.parse_args()
     
     if(args.t == None):
          print(f"Sorry the format you entered is wrong, \nplease enter the command: python {sys.argv[0]} -h\n\nUsage examples: python3 {sys.argv[0]} -t socks4 -p 300")
     else:
          if args.t in ["http","socks4","socks5"]:
               getProxy(args.t,args.p)
          else:
               print("The supported proxy types are http,socks4 and socks5")
