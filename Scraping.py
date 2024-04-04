import requests
from bs4 import BeautifulSoup
import json

def parse_data():
    # Базовий URL для скрапінгу
    base_url = 'http://quotes.toscrape.com'

    # Списки зберігання цитат, авторів
    json_qoutes = []
    json_authors = []
    # Список для запобігання дублювання
    all_authors = []
    page = 1

    while True:
        # Формування URL поточної сторінки
        url = f"{base_url}/page/{page}/"
        html_doc = requests.get(url)

        # Перевірка успішності отримання сторінки
        if html_doc.status_code == 200:
            # Розбір HTML-коду сторінки за допомогою BeautifulSoup
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            author = soup.find_all('small', class_='author')
            quote = soup.find_all('span', class_='text')
            tags = soup.find_all('div', class_='tags')
            
            # Перевірка наявності цитат на сторінці
            if not quote:
                break
            
            # Проходження по кожній знайденій цитаті
            for i in range(0, len(quote)):
                # Створення словника для зберігання інформації про цитату
                quote_dict = dict()

                tagsfourqoute = tags[i].find_all('a', class_='tag')
                quote_dict['tags'] = [tag.text for tag in tagsfourqoute]
                quote_dict['author'] = author[i].text
                quote_dict['quote'] = quote[i].text

                # Додавання словника цитати до списку цитат у форматі JSON
                json_qoutes.append(quote_dict)

                # Перевірка, чи автор ще не доданий до списку всіх авторів
                if author[i].text not in all_authors:
                    all_authors.append(author[i].text)
                    # Знаходження посилання на сторінку автора та парсинг інформації про нього
                    link = author[i].find_next_sibling("a")
                    author_dict = parse_author(link['href'])
                    # Додавання словника автора до списку авторів у форматі JSON
                    json_authors.append(author_dict)

            # Збільшення номера сторінки для переходу на наступну сторінку
            page += 1
                
    return json_qoutes, json_authors

    

def parse_author(link: str) -> dict:
    # Формування URL сторінки автора
    url = f'http://quotes.toscrape.com{link}'
    html_doc = requests.get(url)

    if html_doc.status_code == 200:

        soup = BeautifulSoup(html_doc.content, 'html.parser')
        fullname = soup.find('h3', class_='author-title')
        born_date = soup.find('span', class_='author-born-date')
        born_location = soup.find('span', class_='author-born-location')
        description = soup.find('div', class_='author-description')

        # Створення словника для зберігання інформації про автора
        author_dict = dict()
        # Додавання інформації про автора до словника
        author_dict['fullname'] = fullname.text
        author_dict['born_date'] = born_date.text
        author_dict['born_location'] = born_location.text
        author_dict['description'] = description.text.strip()
        return author_dict



if __name__ == "__main__":
    qoute, author = parse_data()
    
    # Запис списку цитат у JSON-файл
    with open("qoutes.json", 'w') as f:
        json.dump(qoute, f, indent=4)

    # Запис списку авторів у JSON-файл
    with open('authors.json', 'w') as f:
        json.dump(author, f, indent=4)