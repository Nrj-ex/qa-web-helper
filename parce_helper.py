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
# find_links(MAIN_URL, BD)
# check_links(BD)


#new
def save_page(url, response, con):
    # сохранение в бд
    cur = con.cursor()
    cur.execute("SELECT id FROM page WHERE url = ?", (url,))
    flag = cur.fetchone()
    if flag is None:
        values = (url, response.status_code)
        cur.execute(f"""INSERT INTO page(url, status_code) 
            VALUES(?, ?)""", values)
        con.commit()
        print(f"{url} - response saved.")
    else:
        print("page don't saved")


# сохранение списка ссылок в links_list
def save_links(parent_url, links_list, con):
    # todo если parent_url есть в таблице, ничего не сохранять
    #  значит данные повторяются
    # todo сделать массовую вставку а не по 1 (executemany)
    if links_list is None:
        return None
    cur = con.cursor()
    cur.execute("SELECT id FROM links_list WHERE url = ?", (parent_url,))
    flag = cur.fetchone()
    if flag is None:
        for i in links_list:
            internal = 0
            if parent_url[:20] in i:
                internal = 1
            entities = (parent_url, i, internal,)

            cur.execute('INSERT INTO links_list(url, link, internal) '
                        'VALUES(?, ?, ?)', entities)
        con.commit()
        print(f"links saved.")
    else:
        print("links don't saved")


# найти ссылки в контенте
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
        links.append(link)
    print(f"links on {url} found.")
    return links
        # какие еще бывают значения href


#
def check_page(url):
    # получение response по одной странице
    from requests import get
    import fake_useragent
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    response = get(url, headers=header)
    print(response.url)
    print(f"{url} - checked!")
    return response




