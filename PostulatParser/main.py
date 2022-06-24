import requests
from bs4 import BeautifulSoup as bs

"""
Парсер на Python электронного научного журнала Постулат
Собирает авторов и их статьи по указанным выпускам в эксель таблицу
Спасибо: https://habr.com/ru/post/568334/
"""

URL_archive = "http://e-postulat.ru/index.php/Postulat/issue/archive"
r = requests.get(URL_archive)


"""
Искомые данные хранятся в теге <a>
"""

soup = bs(r.text, "html.parser")
releases_names = soup.find_all('a')
del releases_names[0]

stack_of_releases = []
for elem in releases_names:
    temporary_stack = []
    href = elem.get("href")
    if href.find("view") == -1:
        continue
    temporary_stack.append(href)
    text = elem.get_text()
    temporary_stack.append(text)
    stack_of_releases.append(temporary_stack)

"""
Предлагаем пользователю спарсить определённые выпуски
"""
print("Какие выпуски вас интересуют?")

i = 1
for elem in stack_of_releases:
    print(i, ". ", elem[1], sep="")
    i += 1
releases_to_parse = input("Укажите интересующие выпуски через пробел ").split()

"""
Берём только те выпуски, которые нужны пользователю
"""

will_parse = []
for num in releases_to_parse:
    will_parse.append(stack_of_releases[int(num) - 1])

"""
Теперь нужно пробежаться по интересующим выпускам и собрать данные:
1. Выпуск
2. Имя автора
3. Название статьи
4. Ссылка на скачивание статьи данного автора

Этот функционал следует оформлять в функцию (evexile, sorry)
"""


def get_href(tag):     # нужна для нормальной работы функции  authors_n_article()
    tag = str(tag)
    start = tag.find("href")
    tag = str(tag[start::])
    tag_end = tag.find(">")
    tag = str(tag[:tag_end])
    return tag


def authors_n_article(link_name):
    # значит, бужет стэк. [выпуск, автор, название статьи, ссылка для скачивания]
    stack = []

    for elem in link_name:

        URL_of_release = elem[0]
        req = requests.get(URL_of_release)
        soup = bs(req.text, "html.parser")
        tag_author = soup.find_all('td', class_="tocArticleTitleAuthors")
        for tag in tag_author:
            stack_temporary = []
            stack_temporary.append(elem[1])  # выпуск

            name_article = tag.get_text("|", strip=True).split("|")
            for na in name_article:
                stack_temporary.append(na)
            stack_temporary.append(get_href(tag))
            stack.append(stack_temporary)

    return stack


to_save = authors_n_article(will_parse)

"""
Полученная информация будет храниться в TXT файле
"""


def txt_saver(save):
    f = open("output.txt", "w", encoding='utf-8')
    for line in save:
        for string in line:
            f.write(string + ";")
        f.write("\n")


txt_saver(to_save)
