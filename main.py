import datetime
import requests
import csv
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# def get_pages(url):
#     user_agent = UserAgent()
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'User_Agent': user_agent.random 
#     }

#     response = requests.get(url=url, headers=headers)

#     with open('index.html', 'w', encoding='utf-8') as file:
#         file.write(response.text)


# def get_json(url):
#     user_agent = UserAgent()
#     headers = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'User_Agent': user_agent.random 
#     }

#     response = requests.get(url=url, headers=headers)

#     with open('result.json', 'w', encoding='utf-8') as file:
#         json.dump(response.json(), file, indent=4, ensure_ascii=False)


def get_data():
    today = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    user_agent = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User_Agent': user_agent.random 
    }

    response = requests.get(url='https://www.lamoda.ru/c/4153/default-women/?is_sale=1&display_locations=outlet&sitelink=topmenuW&l=11&page=1&json=1', headers=headers)
    data = response.json()
    pagination = data.get('payload').get('pagination').get('pages')
    with open(f'{today}.csv', 'w', newline='', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=';')
        
        writer.writerow(
            (
                'Бренд',
                'Название',
                'Старая цена, руб.',
                'Новая цена, руб.',
                'Процент скидки, %',
            )
        )

    for page in range(1, pagination+1):
        url = f'https://www.lamoda.ru/c/4153/default-women/?is_sale=1&display_locations=outlet&sitelink=topmenuW&l=11&page={page}&json=1'
        r = requests.get(url=url, headers=headers)
        data = r.json()
        products = data.get('payload').get('products')
        for product in products:
            brand = product.get('brand').get('name')
            category = product.get('name')
            old_price =  product.get('old_price_amount')
            new_price =  product.get('price_amount')
            discount = product.get('discount')

        print(f'{page}/{pagination}')
    
        with open(f'{today}.csv', 'a', newline='', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    brand,
                    category,
                    old_price,
                    new_price,
                    discount,
                )
            )

def main():
    # get_pages(url='https://www.lamoda.ru/c/4153/default-women/?is_sale=1&display_locations=outlet&sitelink=topmenuW&l=11')
    # get_json(url='https://www.lamoda.ru/c/4153/default-women/?is_sale=1&display_locations=outlet&sitelink=topmenuW&l=11&page=1&json=1')
    get_data()


if __name__ == '__main__':
    main()
