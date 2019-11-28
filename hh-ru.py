import requests
from bs4 import BeautifulSoup as bs
from func import write_csv
from attrs import HeadHunter
import utils


def get_hh(base_url, headers=None, proxy=None):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    r = session.get(base_url, headers=headers, proxies=proxy)
    if r.status_code == 200:
        soup = bs(r.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': HeadHunter.HH_DIVS})
        try:
            pagination = soup.find_all('a', attrs={'data-qa': HeadHunter.HH_PAGINATION})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=QA&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

        for url in urls:
            for div in divs:
                try:
                    title = div.find('a', attrs={'data-qa': HeadHunter.HH_TITLE}).text
                except:
                    title = ''

                try:
                    company = div.find('a', attrs={'data-qa': HeadHunter.HH_COMPANY}).text
                except:
                    company = ''

                try:
                    city = div.find('span', attrs={'data-qa': HeadHunter.HH_CITY}).text
                except:
                    city = ''

                try:
                    salary = div.find('div', attrs={'data-qa': HeadHunter.HH_SALARY}).text
                except:
                    salary = 'Ленивые сволочи'

                try:
                    url = div.find('a', attrs={'data-qa': HeadHunter.HH_URL})['href']
                except:
                    url = ''

                try:
                    description = div.find('div',
                                           attrs={'data-qa': HeadHunter.HH_DESCRIPTION}).text
                except:
                    description = ''

                try:
                    requirements = div.find('div', attrs={'data-qa': HeadHunter.HH_REQUIREMENTS}).text
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
    proxy = utils.proxy
    headers = utils.headers
    jobs = get_hh(base_url, headers, proxy)
    write_csv(jobs)


if __name__ == '__main__':
    main()
