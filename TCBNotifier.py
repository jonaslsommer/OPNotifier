import requests
from bs4 import BeautifulSoup
from time import sleep
from PIL import Image
from io import BytesIO
from numpy import array,sum

async def check_cover(url_name, temp, number):
    try:
        response = requests.get(url=url_name)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image = soup.find('img', alt=lambda x: x and f'One Piece  Chapter {temp} Page {number}' in x)
            print(f'One Piece  Chapter {temp} Page {number}')
            if image:
                print("found")
                return image['src']
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

async def check_button(url_base,url_name):
    try:
        response = requests.get(url=url_name)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            component = soup.select_one("body > main > div.overflow-hidden > div.container.mx-auto.text-center.p-4 > div.flex.items-center.justify-center.my-6.gap-2.text-sm.font-bold > a:nth-child(3)")
            if component:
                print("next rec on" + str(url_base + str(component.get("href")[10:14])))
                return url_base + str(component.get("href")[10:14]),str(component.get("href")[-4:])
            else:
                return None,None
        else:
            return None,None
    except requests.exceptions.RequestException as e:
        return None,None

async def check_contiuous_button(known_chapter_url, number = 0):
    if len(known_chapter_url) > 60:
        subdomain_number = int(known_chapter_url[:-23][-4:])
        chapter_number = subdomain_number
        url_base = known_chapter_url[:-27]
    else:
        subdomain_number = int(known_chapter_url[-4:])
        chapter_number = subdomain_number
        url_base = known_chapter_url[:41]
    cover = None
    url_name = url_base + str(subdomain_number)
    while True:
        _url_name, _chapter_number = await check_button(url_base,url_name)
        if _url_name:
            url_name = _url_name
            chapter_number = _chapter_number
        else:
            break
    print(url_name,chapter_number)
    if url_name == url_base + str(subdomain_number):
        return [url_name,chapter_number,cover]
    else:
        i = 1
        cover = await check_cover(url_name,chapter_number,1)
        while cover != None:
            if  not await image_color(cover):
                break
            else:
                i+=1
                cover = await check_cover(url_name,chapter_number,i)
            if i >= 3: break
        return [url_name,chapter_number,cover]

async def image_color(picture_url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tcbonepiecechapters.com/"
    }
    response = requests.get(picture_url, headers=headers)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img_array = array(img)

    r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
    color_pixels = sum((r != g) | (g != b))
    total_pixels = img_array.shape[0] * img_array.shape[1]

    return (color_pixels/total_pixels) > 0.05
