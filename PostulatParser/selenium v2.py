import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3
import pandas as pd

URL_ARCHIVE = "https://e-postulat.ru/index.php/Postulat/issue/archive"
DB_NAME = "journal_data.db"


def get_page_source(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return page_source


def extract_releases(page_source):
    soup = bs(page_source, "html.parser")
    releases_names = soup.find_all('a')
    stack_of_releases = []
    for elem in releases_names:
        href = elem.get("href")
        if href and "view" in href:
            stack_of_releases.append((href, elem.get_text()))
    return stack_of_releases


def prompt_user_for_releases(releases):
    print("Какие выпуски вас интересуют?")
    for i, (href, name) in enumerate(releases, start=1):
        print(f"{i}. {name}")
    releases_to_parse = input("Укажите интересующие выпуски через пробел ").split()
    return [releases[int(num) - 1] for num in releases_to_parse]


def get_href(tag):
    href = tag.find("a", href=True)
    return href["href"] if href else ""


def authors_and_articles(link_names):
    stack = []
    for link, name in link_names:
        page_source = get_page_source(link)
        soup = bs(page_source, "html.parser")
        for tag in soup.find_all('td', class_="tocArticleTitleAuthors"):
            article_info = [name]
            article_info.extend(tag.get_text("|", strip=True).split("|"))
            article_info.append(get_href(tag))
            stack.append(article_info)
    return stack


def save_to_txt(data, filename="output.txt"):
    with open(filename, "w", encoding='utf-8') as f:
        for line in data:
            f.write(";".join(line) + "\n")


def save_to_excel(data, filename="output.xlsx"):
    df = pd.DataFrame(data, columns=["Выпуск", "Название статьи", "Имя автора", "Ссылка"])
    df.to_excel(filename, index=False)


def insert_data_to_db(conn, data):
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO articles (issue, title, author, link)
        VALUES (?, ?, ?, ?)
    ''', data)
    conn.commit()


def save_chooser(data):
    print("В каком формате вы хотите сохранить данные? \n 1. В .txt (old version) \n 2. В .xlsx")
    resp_ans = int(input())
    if resp_ans == 1:
        save_to_txt(data)
    elif resp_ans == 2:
        save_to_excel(data)
    else:
        print("команда не распознана, даные будут сохранены в .txt")
        save_to_txt(data)


def main():
    page_source = get_page_source(URL_ARCHIVE)
    releases = extract_releases(page_source)
    selected_releases = prompt_user_for_releases(releases)
    data = authors_and_articles(selected_releases)
    save_chooser(data)


if __name__ == "__main__":
    main()
