#coding:utf-8
import requests,redis,time
conRedis = redis.Redis(host='192.168.1.157',port=6379)
# conRedis = redis.Redis(host='127.0.0.1', port=6379)

while True:
    try:
        res = requests.get(
            'ip获取',
            timeout=2).content.decode('utf-8')
        ips = res.replace('\r', '').split('\n')
        print('hasips')

        names = conRedis.smembers('ProxyName')
        for name in names:
            if conRedis.llen(name)>80:
                continue
            else:
                for ip in ips:
                    if ip != "":
                        conRedis.rpush(name, ip)
                conRedis.expire(name, 30)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(3)
        pass
