import sqlite3 as sq
import settings
import parce_helper
from pprint import pprint
import concurrent.futures

# todo если базы нету создать ее
con = sq.connect(settings.DB)
links = [
    'https://passport.yandex.ru/auth?origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru',
    'https://passport.yandex.ru/registration/mail?from=mail&origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru',
    'https://passport.yandex.ru/auth?origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru',
    'https://yabs.yandex.ru/count/WTeejI_zOB81XGu0v1PwAwahzDVCeGK0iW8GW8200J5ivIXW000003ZQZHH094W2ODOOSC2QtfJblDtLgG600GcG0QAAzAauc07aaFYdHxW1Z8Ef-n_00GJO0SYzbI7e0Ou2y0A-meRx0x031EW49VW4lOst0OW5lOst0P05lOst0Q05jUutg0NNnYwm1TV6BhW5ryOkm0N0ZRS1R5aAe3eEleQ2DP5a9cwF-GUm1u20c2ou1_upq0SIoQeB45iilWOraG00C2cz1aYxw0kzZRS1y0i6w0oJGEoogO2gnuFVXe0Gn8-66WZu4FBm4WJW4zV6Bg0KryOkg1IzZRS1w1IC0jWLmOhsxAEFlFnZy90MtG6W5j2R-Fy5oHQ15vWNykcBAQWN2S0Nj0BO5y24FR0O-fgZWGRG627u6FUddTAqa8BZ_m606P0P0Q0PgWEm6RWPqXaIUM5YSrzpPN9sPN8lSZKmCYqqw1c0mWFm6O320u4Q__z3eA1933eV01xRk6Jt4HXAQP6MPyY7o_Q0vWDmxmLM4gpQs6uun4IT15RKzGGd14R0Y5KdhsumFM-mpx7XmBmH4EDy0m4AtVMrs0qPgpYoyWarsDXGVpZ0R_8mkFUYG0_S0HjGQoa0~1',
    'https://yandex.ru/covid19/stat?utm_source=main_graph&utm_source=main_notif&geoId=213',
    'https://yandex.ru/chat/#/join/e8547709-3a39-4584-9168-b83145d0eb44/1613287801002029',
    'https://yandex.ru/covid19/stat?utm_source=main_graph&utm_source=main_notif&geoId=213',
    'https://yandex.ru/covid19/stat?utm_source=main_graph&utm_source=main_notif&geoId=225',
    'https://yabs.yandex.ru/count/WUeejI_zOBC11Gy0v1TwAwah-_f7OWK0im8GW8200J5ivIXW000003ZQZHH014WGOCGISBx-buUE9O012P01sfBpgJYOk06-_fU7igAC8UW1g0Bm0hx2Xli3a0Fmmu1lAlW4WhAI0OW5WhAI0P05WhAI0S05WPb9R5aAe3eEleRP1W0007220000gGSraMGcRe_v1x07W82OBBW7xWc0WC20W8A00VW8dF_BWySI0439gWiGMoo-1ZMH000mARq6IBle2uAoaW7m2mRe39D0xBAfWAh7Wz-6W12PaSR0eX3u4FBW4e606F0I-183u1E2if81e1I2if81g1I2if81q1IamEOzs1JesFFv1UWKZ0BG5UZOy_a5s1N1YlRieu-y_6Fma1Pue1RGc_Z_1SaMWHUe5md05xG2s1V0X3sm6Cwteu46q1WX-1ZtfvtIj922u_y1W1cG6G6W6Qe3i1cu6V__0T8P4dbXOdDVSsLoTcLoBt8rC38jDEWPWC83y1c0mWE16l__rpQo2Ztk7W16otXdzs4MociHZ3KacSi6aUSJU0NDs6gRjk40k43ACm80TGR0KDSJK11O8UzZLU9L695d2CmvXXsOb_zXd6aWG4QxlXnM6RBAnZ9hkpuUeG6wZWTrz3NxqGEUXh87~1',
    'https://yabs.yandex.ru/count/WUeejI_zOBC11Gy0v1TwAwah-_f7OWK0im8GW8200J5ivIXW000003ZQZHH014WGOCGISBx-buUE9O012P01sfBpgJYOk06-_fU7igAC8UW1g0Bm0hx2Xli3a0Fmmu1lAlW4WhAI0OW5WhAI0P05WhAI0S05WPb9R5aAe3eEleRP1W0007220000gGSraMGcRe_v1x07W82OBBW7xWc0WC20W8A00VW8dF_BWySI0439gWiGMoo-1ZMH000mARq6IBle2uAoaW7m2mRe39D0xBAfWAh7Wz-6W12PaSR0eX3u4FBW4e606F0I-183u1E2if81e1I2if81g1I2if81q1IamEOzs1JesFFv1UWKZ0BG5UZOy_a5s1N1YlRieu-y_6Fma1Pue1RGc_Z_1SaMWHUe5md05xG2s1V0X3sm6Cwteu46q1WX-1ZtfvtIj922u_y1W1cG6G6W6Qe3i1cu6V__0T8P4dbXOdDVSsLoTcLoBt8rC38jDEWPWC83y1c0mWE16l__rpQo2Ztk7W16otXdzs4MociHZ3KacSi6aUSJU0NDs6gRjk40k43ACm80TGR0KDSJK11O8UzZLU9L695d2CmvXXsOb_zXd6aWG4QxlXnM6RBAnZ9hkpuUeG6wZWTrz3NxqGEUXh87~1',
    'https://yandex.ru/tune/geo?retpath=https%3A%2F%2Fyandex.ru%2F&nosync=1',
    'https://yandex.ru/time',
    'https://pokupki.market.yandex.ru/my/cart?utm_source=morda_header_icon&clid=956&purchase-referrer=morda_header_icon',
    'https://yandex.ru/collections/',
    'https://yandex.ru/news?mlid=1613292233.glob_225&msid=1613292908.62892.85616.495729&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/region/moscow?mlid=1613292233.geo_213&msid=1613292908.62892.85616.495729&utm_medium=topnews_region&utm_source=morda_desktop',
    'https://yandex.ru/news/rubric/koronavirus?from=main',
    'https://yandex.ru/news/story/Putin_Rossiya_ne_brosit_Donbass--2946eb46117251951d609f27b58e1cf8?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.2946eb46&msid=1613292908.62892.85616.495729&persistent_id=129731646&stid=lOzJX-_P0Wli3Lol0olA&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/Rukovodstvo_Respublikanskoj_partii_osudilo_podderzhavshikh_impichment_Trampa_senatorov--3f059104c397b1204486b69f85578ba5?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.3f059104&msid=1613292908.62892.85616.495729&persistent_id=129724397&stid=CBBedLm_nLOPogICw-GG&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/V_Rossii_zaversheny_ispytaniya_sistemy_preduprezhdeniya_o_raketnom_napadenii--8b44c43fe5ff213d1d2740523707d397?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.8b44c43f&msid=1613292908.62892.85616.495729&persistent_id=130011169&stid=kZqd9Ww0JMcM228wqNM7&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/Uchenye_predupredili_o_riske_ustarevaniya_vakcin_ot_COVID-19--952c0557d18cb529bc30f55de7b7764f?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.952c0557&msid=1613292908.62892.85616.495729&persistent_id=130003586&stid=TwftRvTfvp-t67cuBWvU&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/Mask_priglasil_Putina_pogovorit--5c145817a0a6945d660982c88e004676?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.5c145817&msid=1613292908.62892.85616.495729&persistent_id=129732626&stid=daICqsVY_Qm_sUwejEhj&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/V_rezultate_zemletryaseniya_v_YAponii_postradali_20_chelovek--ca8020dc5439fe4dc1d90ccd7f6e612d?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.ca8020dc&msid=1613292908.62892.85616.495729&persistent_id=129717468&stid=1oIeribx-dGFKtrvfMsa&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/V_SHvecii_prizvali_vlasti_k_davleniyu_na_Germaniyu_po_voprosu_Severnogo_potoka__2--6cdda3ad6a9850b008dc628ba96a7caf?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.6cdda3ad&msid=1613292908.62892.85616.495729&persistent_id=130003372&stid=zLeat9FAmBNHIMw3NhzT&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/Rostrud_napomnil_o_trekhdnevnoj_rabochej_nedele_v_fevrale--666a4eeb4a30587668ef3fb888d9689d?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.666a4eeb&msid=1613292908.62892.85616.495729&persistent_id=128892121&stid=6wGxYa9TELqquUrB_tTF&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/story/Obvinyaemyj_v_gosizmene_v_polzu_Ukrainy_oficer_napal_na_sotrudnika_SIZO_Lefortovo--89e8de3064a610aeac5761f722a1fff9?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.89e8de30&msid=1613292908.62892.85616.495729&persistent_id=130005559&stid=qPNGb8S1zqE8wa6O6dgp&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/sport/story/Usman_pobil_rekord_Sen-Pera_po_chislu_pobed_podryad_v_UFC--3779d8b9282193a784c7663d017b002b?fan=1&from=main_portal&lang=ru&lr=213&mlid=1613292233.glob_225.3779d8b9&msid=1613292908.62892.85616.495729&persistent_id=130008155&stid=22V2xbVr2D1tCs4bFOAS&t=1613292233&utm_medium=topnews_news&utm_source=morda_desktop',
    'https://yandex.ru/news/?lang=ru&msid=1613292908.62892.85616.495729&mlid=1613292233',
    'https://yandex.ru/news/quotes/2002.html',
    'https://yandex.ru/news/quotes/2000.html',
    'https://yandex.ru/news/quotes/1006.html',
    'https://yandex.ru/pogoda/?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home&utm_term=title',
    'https://yandex.ru/pogoda/maps/nowcast?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home&utm_term=nowcast_link',
    'https://yandex.ru/pogoda/?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home&utm_term=main_number',
    'https://yandex.ru/pogoda/?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home&utm_term=next_day_part',
    'https://yandex.ru/pogoda/?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home&utm_term=next_day_part',
    'https://yandex.ru/pogoda/?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home&utm_term=next_day_part',
    'https://yandex.ru/maps/213/moscow/probki',
    'https://yandex.ru/metro/moscow',
    'https://rasp.yandex.ru/?utm_source=yamain&utm_medium=geoblock&utm_campaign=main',
    'https://taxi.yandex.ru/?utm_source=yandex-geoblock&utm_medium=morda&utm_campaign=[YT]DT_UA-goal_RU-ALL-ALL&utm_content=title-taxi',
    'https://yandex.ru/maps/213/moscow/probki',
    'https://yandex.ru/maps/213/moscow/probki',
    'https://o.yandex.ru/?utm_source=main_stripe_big_popup',
    'https://market.yandex.ru/?clid=505&utm_source=main_stripe_big',
    'https://yandex.ru/video/?utm_source=main_stripe_big',
    'https://yandex.ru/images/?utm_source=main_stripe_big',
    'https://yandex.ru/news/?utm_source=main_stripe_big',
    'https://yandex.ru/maps/?utm_source=main_stripe_big',
    'https://translate.yandex.ru/?utm_source=main_stripe_big',
    'https://music.yandex.ru/?utm_source=main_stripe_big',
    'https://tv.yandex.ru/?utm_source=main_stripe_big',
    'https://yandex.ru/all',
    'https://yandex.ru/',
    'https://yabs.yandex.ru/count/WRiejI_zO9C1ZGq0z1HwAwahWYgoC0K0am8GW8200J5ivIXW000003ZQZHH054W2OEeHS8wmWekk9O012P01qjJZcYMOk06Ei8AB3i012DW1zhs31UW1gWBm0hx2Xli3BFW4wwwU0OW5wwwU0P05wwwU0MnP2g0w3hw6WZMHP2PkZ_a7i0U0W9Wik0VwCO20W0e1mGgRklbb6flGFybRBBu6DP40030flGP8k-WBwwwU0V0B1kWCaq3iigc0giU3tuQ04FlUmG88-13oy184u1Fhhfu1e1Jhhfu1g1Jhhfu1w1IC0jWLmOhsxAEFlFnZy90MNA0Mq9lu_mN95e4Nc1SPg1S9m1Uq0jWNm8Gzi1ZPfAE11j0O8VWOzwUTqhIGWkF_0O0Pa1a1e1cg0x0Pk1d__m7I6H9vOM9pNtDbSdPbSYzoDJ0oBJJe6O320_0PWC83WHh__vlayxxGC1y0DSjuPFSv5yfh4Tmp9CbbUy7p0RWd0Ii9Lcs4DXp2dau23kfw0WK28qF4AeLNDoIUD_3cs71WNlg7SPg104hkTAKxcG01goWmOAVj-WAuOg103pndWBxXW3eQduQo1m00~1',
    'https://yabs.yandex.ru/count/WRiejI_zO9C1ZGq0z1HwAwahWYgoC0K0am8GW8200J5ivIXW000003ZQZHH054W2OEeHS8wmWekk9O012P01qjJZcYMOk06Ei8AB3i012DW1zhs31UW1gWBm0hx2Xli3BFW4wwwU0OW5wwwU0P05wwwU0MnP2g0w3hw6WZMHP2PkZ_a7i0U0W9Wik0VwCO20W0e1mGgRklbb6flGFybRBBu6DP40030flGP8k-WBwwwU0V0B1kWCaq3iigc0giU3tuQ04FlUmG88-13oy184u1Fhhfu1e1Jhhfu1g1Jhhfu1w1IC0jWLmOhsxAEFlFnZy90MNA0Mq9lu_mN95e4Nc1SPg1S9m1Uq0jWNm8Gzi1ZPfAE11j0O8VWOzwUTqhIGWkF_0O0Pa1a1e1cg0x0Pk1d__m7I6H9vOM9pNtDbSdPbSYzoDJ0oBJJe6O320_0PWC83WHh__vlayxxGC1y0DSjuPFSv5yfh4Tmp9CbbUy7p0RWd0Ii9Lcs4DXp2dau23kfw0WK28qF4AeLNDoIUD_3cs71WNlg7SPg104hkTAKxcG01goWmOAVj-WAuOg103pndWBxXW3eQduQo1m00~1',
    'https://awaps.yandex.net/1/c1/tx21lszVAoU5Fo8Pyi8d5u0xMsKIfVZMTurqYDkdMUQPsNBYAUGsi6IyofWkW_tQTFGZvoKlvxh+nYgMBFraHG+rTHg8ATBjlZDXLt9SX-P-hlX8ZsIn8OoFpDt_twiP7gw77xWc1rEAIuthSfuQknIHAG4gGH7mQcUeGqE-nkh8co5YubANSVpL9_tsvroABTttk879Z-gUzstdsVr25fyysNoz54I5jpi62N6qydQYhrcLj0q-xe3_t5TgyvLbOf0hnYdFogtiqSBjTLYdI8XzqGq4XugV6Fo72D+xKThrFzQylAwD1_twPca-dV2QqNrlcrx0qp3+YGnsDbYVxI3SJn396T789-NOkI6yAgKr3XdMFEc_aoKu3PqFSir7EnCKzAtquN-QUGkXal50Zi9oA_A_.htm',
    'https://zen.yandex.ru/?clid=101&country_code=ru',
    'https://browser.yandex.ru/desktop/zen/?from=yamain_zen&banerid=0458000000',
    'https://afisha.yandex.ru/moscow?utm_source=yamain&utm_medium=yamain_afisha',
    'https://afisha.yandex.ru/moscow/cinema/dusha-2020?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/rodnye-2020?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/love-2021?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/ponchary?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/privorot-chernoe-venchanie?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/severnyi-veter-2020?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/dyavol-v-detayakh?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/okhotnik-na-monstrov?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/poslednii-bogatyr-koren-zla?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://afisha.yandex.ru/moscow/cinema/fatale?utm_source=yamain&utm_medium=yamain_afisha_kp',
    'https://direct.yandex.ru/?from=maintest_ru_razmestitrekl',
    'https://metrika.yandex.ru/?utm_source=yandexru.v14w&utm_medium=web&utm_campaign=static',
    'https://yandex.ru/adv/?from=main_bottom',
    'https://yandex.ru/jobs',
    'https://yandex.ru/blog/company/',
    'https://yandex.ru/company/',
    'https://yandex.com/company/',
    'https://yandex.ru/legal/confidential/',
    'https://yandex.ru/legal/rules/',
    'https://yandex.ru/support/',
    'https://yandex.ru/support/common/troubleshooting/main.html',
    'https://yandex.ru/tune/search?retpath=https%3A%2F%2Fyandex.ru%2F&nosync=1',
    'https://yandex.ru/tune/geo?retpath=https%3A%2F%2Fyandex.ru%2F&nosync=1',
    'https://yandex.ru/tune/search?retpath=https%3A%2F%2Fyandex.ru%2F&nosync=1']

# сохранить список в базу
# for i in links:
#     parce_helper.save_page(con, i)


# получить список ссылок для обработки
def select(conn):
    cur = conn.cursor()
    cur.execute("""SELECT url FROM page WHERE status_code = 0 """)
    return cur.fetchall()


links = [i for i, in select(con)]
pprint(links)
# обработать полученный список
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(parce_helper.check_page_thread, links)
pprint(parce_helper.responses)
#
# # сохранить полученные данные
for url, response in parce_helper.responses:
    parce_helper.save_page(con, url, response)

con.close()
