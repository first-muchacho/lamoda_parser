import datetime
import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_data():
    today = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    us_agent = UserAgent()
    url = 'https://www.lamoda.ru/c/4153/default-women/?is_sale=1&display_locations=outlet&sitelink=topmenuW&l=11&page=1'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User_Agent': us_agent.random 
    }

    response = requests.get(url=url, headers=headers)

    with open('data.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    with open('data.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    gender = soup.find('h1', class_='d-catalog-header__title-text').text.strip()
    cards = soup.find_all('div', class_='x-product-card__card')
    
    with open(f'{gender}-{today}.csv', 'w', newline='', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=';')
        
        writer.writerow(
            (
                'Название',
                'Бренд',
                'Старая цена, руб.',
                'Новая цена, руб.',
                'Процент скидки, %',
                'Ссылка на товара'
            )
        )

    for card in cards:
        title = card.find('div', class_='x-product-card-description__product-name').text.strip()
        brand = card.find('div', class_='x-product-card-description__brand-name').text.strip()
        try:
            old_price = card.find('span', class_='x-product-card-description__price-old').text.strip().replace(' ₽', '').replace(' ', '')
            new_price = card.find('span', class_='x-product-card-description__price-new').text.strip().replace(' ₽', '').replace(' ', '')
        except AttributeError:
            continue
        discount = int(100 - int(new_price) * 100 / int(old_price))
        link = card.find(class_='x-product-card__link', href=True)

        with open(f'{gender}-{today}.csv', 'a', newline='', encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    title,
                    brand,
                    old_price,
                    new_price,
                    discount,
                    f'https://www.lamoda.ru{link["href"]}'
                )
            )


def main():
    get_data()


if __name__ == '__main__':
    main()
