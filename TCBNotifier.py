import requests
from bs4 import BeautifulSoup
from time import sleep
from PIL import Image
from io import BytesIO
from numpy import array,sum

async def check_website(url_name, word):
    try:
        response = requests.get(url=url_name)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            component = soup.select_one("body > main > div.overflow-hidden > div.container.mx-auto.text-center.p-4 > h1")
            if word in component.get_text():
                return component.get_text()[-4:]
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

async def check_cover(url_name, temp, number):
    try:
        response = requests.get(url=url_name)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image = soup.find('img', alt=lambda x: x and f'One Piece  Chapter {temp} Page {number}' in x)
            if image:
                return image['src']
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

async def check_continuous_chapters(known_chapter_url): 
    if len(known_chapter_url) > 60:
        subdomain_number = int(known_chapter_url[:-23][-4:])
        chapter_number = subdomain_number
        url_base = known_chapter_url[:-27]
    else:
        subdomain_number = int(known_chapter_url[-4:])
        chapter_number = subdomain_number
        url_base = known_chapter_url[:41]
    count = 0
    cover = None
    while count <= 20:
        subdomain_number += 1
        url_name = url_base + str(subdomain_number)
        #print(url_name)
        temp = await check_website(url_name, 'One Piece  - Chapter')
        if(temp):
            cover = await check_cover(url_name,temp,1)
            #print(temp,'exists neu:',url_name,'alt:',known_chapter_url)
            known_chapter_url = url_name
            chapter_number = temp
            count = 0
        count += 1
        sleep(0.2)
    i = 1
    while cover != None:
        if  not await image_color(cover):
            break
        else:
            i+=1
            cover = await check_cover(known_chapter_url,chapter_number,i)
        if i >= 3: break
    return [known_chapter_url,chapter_number,cover]

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
