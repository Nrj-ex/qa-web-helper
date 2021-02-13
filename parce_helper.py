import sqlite3 as sq
import settings


def find_links_old(page_url, bd):
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


def check_links_old(bd, retry=1):
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


def check_links_old1(bd, retry=1):
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

# new


def is_internal(parent_url, url):
    if parent_url[:20] in url:
        return 1
    return 0


def save_page(con, url, response=None):
    # сохранение в бд
    cur = con.cursor()
    cur.execute("SELECT id FROM page WHERE url = ?", (url,))
    flag = cur.fetchone()
    if flag is not None:
        print(f"{url} - don't saved")
        return None
    # переменные по умолчанию если нет response
    # todo вынести это говно в отдельную функцию)
    title = None
    description = None
    status_code = 0
    depth = 0
    history = None
    internal = None
    retry = 0
    if response is not None:
        status_code = response.status_code
        depth = response.depth
    values = (url, title, description, status_code, depth, history, internal, retry)
    # values = get_values(url, response) должно так вызываться
    cur.execute(f"""INSERT INTO page(url, title, description, status_code, depth, history, internal, retry) 
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", values)
    con.commit()
    print(f"{url} - response saved.")


# сохранение списка ссылок в links_list
# я могу сохранять все в одном месте: 2 метода которые сохраняют в разные таблицы
# они в одном общем который готовит для них все данные
# на вход все что есть, если данных нету будет сохраняться что то по умолчанию
def save_links(con, parent_url, links_list):
    # todo сделать массовую вставку а не по 1 (executemany)
    if links_list is None:
        return None
    cur = con.cursor()
    cur.execute("SELECT id FROM links_list WHERE url = ?", (parent_url,))
    flag = cur.fetchone()
    if flag is None:
        for i in links_list:
            internal = is_internal(parent_url, i)
            entities = (parent_url, i, internal,)

            cur.execute('INSERT INTO links_list(url, link, internal) '
                        'VALUES(?, ?, ?)', entities)
        con.commit()
        print(f"links saved.")
    else:
        print("links don't saved")


# найти все ссылки в контенте
def get_links_from_content(url, response):
    if response.status_code != 200:
        print(f"{url} не 200!")
        return None
    from bs4 import BeautifulSoup
    content = response.content
    soup = BeautifulSoup(content, 'lxml')
    # блок со всеми ссылками sitemap
    find_a = soup.find_all("a")
    links = []

    for i in find_a:
        link = i.get("href")
        if link.startswith("//"):
            # внешняя ссылка
            link = link[2:]
            if not link.startswith("http"):
                link = "http://" + link
        elif link.startswith("/"):
            link = url[:url.index("/", 8)] + link
        elif link.startswith("http"):
            pass
            # какие еще бывают значения href

        links.append(link)
    print(f"links on {url} found.")
    return links


# получение response по одной странице
def check_page(url):
    from requests import get
    import fake_useragent
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    response = get(url, headers=header)
    # todo add depth in response
    response.depth = 0 # заглушка
    print(f"{url} - checked!")
    return response




