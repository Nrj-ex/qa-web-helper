import sqlite3 as sq
import settings
import parce_helper


# todo если базы нету создать ее
con = sq.connect(settings.DB)
link = "https://yandex.ru/"
link1 = "https://www.google.ru/"
link2 = "https://www.banki.ru/insurance3/"
links1 = [link, link1, link2]


# todo сделать запуск параллельным
def check_pages(list_):
    for i in list_:
        response = parce_helper.check_page(i)
        parce_helper.save_page(i, response, con)
        links = parce_helper.get_links_from_content(i, response)
        parce_helper.save_links(i, links, con)


check_pages(links1)


con.close()
