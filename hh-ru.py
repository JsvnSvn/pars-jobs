import requests
from bs4 import BeautifulSoup as bs
import csv
from random import choice


def get_hh(base_url, headers=None, proxy=None):
    session = requests.Session()
    r = session.get(base_url, headers=headers, proxies=proxy)
    print(headers)
    print(proxy)
    if r.status_code == 200:
        jobs = []
        soup = bs(r.content, 'html.parser')
        #h2 = soup.find_all('h2', class_='position')
        divs = soup.find_all('div', class_='vacancy-serp-item')
        #divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            except:
                title = ''

            try:
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            except:
                company = ''

            try:
                city = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            except:
                city = ''

            try:
                salary = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            except:
                salary = ''

            try:
                url = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            except:
                url = ''

            try:
                description = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            except:
                description = ''

            try:
                requirements = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            except:
                requirements = ''

            jobs.append({'title': title,
                         'salary': salary,
                         'company': company,
                         'city': city,
                         'description': description,
                         'requirements': requirements,
                         'url': url})
        print(jobs)
    else:
        print('ERROR')







def write_csv(data):
    with open('hh.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['zarplata'],
                         data['vacancy_date'],
                         data['url']))





def main():
    #base_url = 'https://ru.jooble.org/%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0?salary=20000'
    base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=QA&page=0'
    useragents = open('useragents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')
    proxy = {'http': 'http://' + choice(proxies)}
    headers = {'User-Agent': str(choice(useragents))}
    get_hh(base_url, headers, proxy)



if __name__ == '__main__':
    main()
