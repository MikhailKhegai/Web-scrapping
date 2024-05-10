import json
import requests
import bs4
from fake_headers import Headers

def get_fake_headers():
    return Headers(browser="chrome", os="win").generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_fake_headers())

main_page = bs4.BeautifulSoup(response.text, features='lxml')

vacancy_tags = main_page.findAll('div', class_="vacancy-serp-item__layout")
parsed_data = []

for vacancy_tag in vacancy_tags:
    link = vacancy_tag.find('a', class_ = 'bloko-link')['href']
    salary = vacancy_tag.find('span', class_="bloko-header-section-2")
    company_tag = vacancy_tag.find('a', class_ = 'bloko-link bloko-link_kind-tertiary')
    company = company_tag.find('span').text
    city_tag = vacancy_tag.findAll('div', class_ = 'bloko-text')[1]
    city = city_tag.text.split(',')[0]

    # description_response = requests.get(link)
    # description_data = bs4.BeautifulSoup(description_response.text, features='lxml')

    if salary == None:
        salary = 'ЗП не указана'
    else:
        salary = salary.text

    parsed_data.append({
        'link' : link,
        'salary' : salary,
        'company' : company,
        'city' : city
    })

with open('vacancy.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(parsed_data, ensure_ascii=False, indent=4))






