from requests import get
from bs4 import BeautifulSoup
import sqlite3 as sq
from settings import *
from pprint import pprint


def find_links(page_url, bd):
    response = get(page_url, verify=False).text
    soup = BeautifulSoup(response, 'lxml')
    # блок со всеми ссылками sitemap
    sitemap_content = soup.find("div", "layout-column-full margin-bottom-large")
    # найти все ссылки
    try:
        find_a = sitemap_content.find_all("a")
        # вставка данных в таблицу
        with sq.connect(bd) as con:
            cur = con.cursor()
            for i in find_a:
                title = i.text
                link = i.get("href")
                if 'http' in link:
                    pass
                elif link.startswith('/'):
                    link = page_url[:page_url.index("/", 8)] + link

                else:
                    link = page_url + link
                entities = (page_url, link, title)
                cur.execute('INSERT INTO links(url, link, title) '
                            'VALUES(?, ?, ?)', entities)
            con.commit()
        print("Links found")
    except AttributeError:
        print('links not found :(')


def check_links(bd, retry=1):
    # Проверяет ссылку если статус не 200
    with sq.connect(bd) as con:
        cur = con.cursor()

        cur.execute("""SELECT id, url, link, status, try FROM links 
        WHERE status <> 200""")
        data = cur.fetchall()

    for id, url, link, status, retry_bd in data:
        # проверяем урлы с переданным статусом
        if status != '200' and retry_bd < retry:



            print(link)
            response = get(link, verify=False)
            status = response.status_code

            with sq.connect(bd) as con:
                cur = con.cursor()
                entities = (status, id)
                cur.execute('UPDATE links SET status=?, try = try + 1'
                                ' WHERE id=? ', entities)
                con.commit()
            if "sitemap" in link and status == 200:
                find_links(link, BD)


def check_links(bd, retry=1):
    # Проверяет ссылку если статус не 200
    with sq.connect(bd) as con:
        cur = con.cursor()

        cur.execute("""SELECT id, url, link, status, try FROM links 
        WHERE status <> 200""")
        data = cur.fetchall()

    for id, url, link, status, retry_bd in data:
        # проверяем урлы с переданным статусом
        if status != '200' and retry_bd < retry:



            print(link)
            response = get(link, verify=False)
            status = response.status_code

            with sq.connect(bd) as con:
                cur = con.cursor()
                entities = (status, id)
                cur.execute('UPDATE links SET status=?, try = try + 1'
                                ' WHERE id=? ', entities)
                con.commit()
            if "sitemap" in link and status == 200:
                find_links(link, BD)
# find_links(MAIN_URL, BD)
# check_links(BD)


