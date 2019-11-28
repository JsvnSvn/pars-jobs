import csv


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
