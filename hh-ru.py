import requests
from bs4 import BeautifulSoup as bs
import csv



base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=QA&page=0'


def get_hh(base_url):
    session = requests.Session()
    r = session.get(base_url, headers={'accept': '*/*',
                                       'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 '
                                                     'Safari/537.36'})
    if r.status_code == 200:
        jobs = []
        soup = bs(r.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
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
        print(len(divs))
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
    get_hh(base_url)


if __name__ == '__main__':
    main()
