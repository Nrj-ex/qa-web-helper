import requests
import fake_useragent
from bs4 import BeautifulSoup
import json

# пример использования/сохранения сессии
session = requests.Session()

user = fake_useragent.UserAgent().random
header = {'user-agent': user}

link = 'https://www.banki.ru/ng-auth/auth/?backurl=%2F'
param = {
    "utf": 1,
    "AUTH_FORM": "Y",
    "TYPE": "AUTH",
    "FORM_TYPE": "FORM_TYPE",
    "USER_LOGIN": "",
    "USER_PASSWORD": "",
    "USER_REMEMBER": "true"

}

response = session.post(link, headers=header, verify=False, data=param)
with open('test_file.html', 'w', encoding="utf-8") as f:
    f.write(response.text)


# формирование списка с куками
cookies_dict = [
    {"domain": key.domain, "name": key.name, "path": key.path, "value": key.value}
    for key in session.cookies
]

# Сохранение кук в файл
with open('cookies_dict.json', 'w', encoding="utf-8") as f:
    json.dump(cookies_dict, f, sort_keys=True, indent=4, ensure_ascii=False)


with open("cookies_dict.json") as f:
    cookies_from_file = json.load(f)
session2 = requests.Session()

for cookies in cookies_from_file:
    session2.cookies.set(**cookies)



profile = "https://www.banki.ru/profile/?UID=3741536"
response2 = session2.get(profile, headers=header, verify=False)


with open('test_file2.html', 'w', encoding="utf-8") as f:
    f.write(response2.text)


