import requests
from bs4 import BeautifulSoup
import json

def parse_data():
    base_url = 'http://quotes.toscrape.com'
    json_qoutes = []
    json_authors = []
    all_authors = []
    page = 1

    while True:
        url = f"{base_url}/page/{page}/"
        html_doc = requests.get(url)

        if html_doc.status_code == 200:    
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            author = soup.find_all('small', class_='author')
            quote = soup.find_all('span', class_='text')
            tags = soup.find_all('div', class_='tags')
            
            if not quote:
                break
            
            for i in range(0, len(quote)):
                quote_dict = dict()
                tagsfourqoute = tags[i].find_all('a', class_='tag')
                quote_dict['tags'] = [tag.text for tag in tagsfourqoute]
                quote_dict['author'] = author[i].text
                quote_dict['quote'] = quote[i].text
                json_qoutes.append(quote_dict)

                if author[i].text not in all_authors:
                    all_authors.append(author[i].text)
                    link = author[i].find_next_sibling("a")
                    author_dict = parse_author(link['href'])
                    json_authors.append(author_dict)
            page += 1
                
    return json_qoutes, json_authors

    

def parse_author(link: str) -> dict:
    url = f'http://quotes.toscrape.com{link}'
    html_doc = requests.get(url)

    if html_doc.status_code == 200:

        soup = BeautifulSoup(html_doc.content, 'html.parser')
        fullname = soup.find('h3', class_='author-title')
        born_date = soup.find('span', class_='author-born-date')
        born_location = soup.find('span', class_='author-born-location')
        description = soup.find('div', class_='author-description')

        author_dict = dict()
        author_dict['fullname'] = fullname.text
        author_dict['born_date'] = born_date.text
        author_dict['born_location'] = born_location.text
        author_dict['description'] = description.text.strip()
        return author_dict



if __name__ == "__main__":
    qoute, author = parse_data()
    
    with open("qoutes.json", 'w') as f:
        json.dump(qoute, f, indent=4)

    with open('authors.json', 'w') as f:
        json.dump(author, f, indent=4)