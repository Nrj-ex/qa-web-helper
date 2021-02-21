import sqlite3 as sq
import settings
import parce_helper
from pprint import pprint
import concurrent.futures

# todo если базы нету создать ее
con = sq.connect(settings.DB)
links = [
    'https://yandex.ru/time',
    'https://yandex.ru/collections/',
    'https://yandex.ru/news/quotes/2000.html',
    'https://yandex.ru/video/',
    'https://yandex.ru/images/',
    'https://yandex.ru/news/',
    'https://yandex.ru/maps/',
    'https://yandex.ru/all',
    'https://yandex.ru/',
    'https://yandex.ru/jobs',
    'https://yandex.ru/blog/company/',
    'https://yandex.ru/company/',
    'https://yandex.com/company/',
    'https://yandex.ru/legal/confidential/',
    'https://yandex.ru/legal/rules/',
    'https://yandex.ru/support/']

# сохранить список в базу
for i in links:
    parce_helper.save_page(con, i)


# получить список ссылок для обработки
def get_links_list(conn, retry=1, ):
    cur = conn.cursor()
    cur.execute("SELECT url FROM page WHERE status_code != 200 AND retry < ?", (retry,))
    return cur.fetchall()


links = [i for i, in get_links_list(con)]
pprint(links)
while links:
    # обработать полученный список
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(parce_helper.check_page_thread, links)
    pprint(parce_helper.responses)

    # # сохранить полученные данные
    for url, response in parce_helper.responses:
        parce_helper.save_page(con, url, response)

    # получить список ссылок
    links = [i for i, in get_links_list(con)]
    pprint(links)




con.close()
