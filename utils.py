from random import choice

useragents = open('useragents.txt').read().split('\n')
proxies = open('proxies.txt').read().split('\n')
proxy = {'http': 'http://' + choice(proxies)}
headers = {'User-Agent': str(choice(useragents))}

