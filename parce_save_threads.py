import requests
import fake_useragent
from bs4 import BeautifulSoup
import concurrent.futures


user = fake_useragent.UserAgent().random
header = {'user-agent': user}
base_url = 'https://www.goodfon.ru'
img_page_links = []


def get_img_links(id):
    print(f"{id} - start")
    response = requests.get(f"{base_url}/index-{id}.html", verify=False).text
    soup = BeautifulSoup(response, "lxml")
    links = soup.find_all(class_="wallpapers__item")
    for i in links:
        link = i.a['href']
        img_page_links.append(link)
    print(f"{id} - done")


def download_img(url):
    print(url)
    response = requests.get(url, verify=False).text
    soup = BeautifulSoup(response, "lxml")
    img_link = f"""{base_url}{soup.find(class_="wallpaper__download").a["href"]}"""
    print(img_link)
    response = requests.get(img_link, verify=False).text
    soup = BeautifulSoup(response, "lxml")
    img_content = soup.find(class_="text_center").a["href"]
    print(img_content)
    image_byte = requests.get(img_content, verify=False).content
    img_name = img_content[img_content.rfind("/") + 1:]
    with open(f"img//{img_name}", "wb") as f:
        f.write(image_byte)
    print(f"{img_name} - save.")



with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(get_img_links, [i for i in range(1, 20)])


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_img, img_page_links)
