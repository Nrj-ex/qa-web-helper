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
#  количество потоков равно количеству проверяемых страниц
#  после получения всех результатов записывать их в базу
def check_pages(list_):
    # todo в зависимости от глубины продолжать работу, брать страницы из базы
    # todo добавить retry

    # todo добавить метод выбора n ссылок из базы page удовлетворяющий параметрам:
    #  status, retry, depth, internal

    # ДЕЛАЮ ЭТО!
    # todo list_ сразу записывать в базу а затем брать ссылки на проверку из базы
    #  так будет только один поставщик ссылок
    for i in list_:
        response = parce_helper.check_page(i)
        parce_helper.save_page(con, i, response)
        links = parce_helper.get_links_from_content(i, response)
        parce_helper.save_links(con, i, links)


check_pages(links1)


con.close()
