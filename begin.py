import settings
import sqlite_driver


# создать таблицу page
sqlite_driver.create_table(settings.DB)

sqlite_driver.truncate_table(settings.DB, "page")
sqlite_driver.truncate_table(settings.DB, "links_list")



