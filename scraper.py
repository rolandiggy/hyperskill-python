import re

import requests

import string

import os

from bs4 import BeautifulSoup


def create_directories(number):
    print("Creating directories ...")
    for i in range(number):
        try:
            os.mkdir('Page_' + str(i + 1))
        except FileExistsError:
            print('Directory Page_' + str(i + 1) + ' already exists. Continuing ...')
    return


def write_to_disk(filename, content):
    file = open(filename + '.txt', 'wb')
    print('Writing to ' + os.getcwd() + '/' + filename + '.txt ...')
    file.write(content)
    file.close()
    print("Content saved.")
    return


def parse(main_url, article_type, response):
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('span', {'class': 'c-meta__type'})

    found = False
    for article in articles:
        if article.string == article_type:
            found = True
            article_title = article.parent.parent.parent.parent.a.string
            print("Article found: " + article_title)
            filename = article_title.translate(str.maketrans(' ', '_', string.punctuation))
            article_url = article.parent.parent.parent.parent.a.get('href')
            article_page = requests.get(main_url + article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            page_soup = BeautifulSoup(article_page.content, 'html.parser')
            regex = re.compile(".*body.*")
            content = bytes(page_soup.find('div', attrs={'class': regex}).get_text(), encoding='utf-8')
            write_to_disk(filename, content)

    if not found:
        print("No articles found.")
    else:
        print("Articles saved to directory.")
    return


def main():
    pages = int(input("Input how many pages to scrape: "))
    article_type = input("Input type of articles to save: ")

    main_url = 'https://www.nature.com'
    url = '/nature/articles?searchType=journalSearch&sort=PubDate&page='

    create_directories(pages)
    for i in range(pages):
        os.chdir('Page_' + str(i + 1))
        print('Getting ' + article_type + ' articles from page ' + str(i + 1) + ' ...')

        r = requests.get(main_url + url + str(i + 1), headers={'Accept-Language': 'en-US,en;q=0.5'})
        if r:
            parse(main_url, article_type, r)
        else:
            print("The URL returned a " + str(r.status_code) + " error!")

        os.chdir(os.path.dirname(os.getcwd()))

    print("All tasks completed.")


if __name__ == "__main__":
    main()
