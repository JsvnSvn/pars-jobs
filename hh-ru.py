import requests
from bs4 import BeautifulSoup as bs
import csv
from random import choice


def write_csv(jobs):
    with open('hh.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Название вакансии', 'Зарплата', 'Компания', 'Город', 'Описание', 'Требования', 'Ссылка'))
        for job in jobs:
            writer.writerow((job['title'],
                             job['salary'],
                             job['company'],
                             job['city'],
                             job['description'],
                             job['requirements'],
                             job['url']))


def get_hh(base_url, headers=None, proxy=None):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    r = session.get(base_url, headers=headers, proxies=proxy)
    if r.status_code == 200:
        # r = session.get(base_url, headers=headers, proxies=proxy)
        soup = bs(r.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=QA&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

        for url in urls:
            # r = session.get(base_url, headers=headers, proxies=proxy)
            # soup = bs(r.content, 'html.parser')
            # divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
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
                    salary = 'Ленивые сволочи'

                try:
                    url = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                except:
                    url = ''

                try:
                    description = div.find('div',
                                           attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
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
                print(len(jobs))
    else:
        print('ERROR')
    return jobs


def main():
    base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=QA&page=0'
    useragents = open('useragents.txt').read().split('\n')
    proxies = open('proxies.txt').read().split('\n')
    proxy = {'http': 'http://' + choice(proxies)}
    headers = {'User-Agent': str(choice(useragents))}
    jobs = get_hh(base_url, headers, proxy)
    write_csv(jobs)

if __name__ == '__main__':
    main()
