import requests
import time
from bs4 import BeautifulSoup
from sqllib.database import News, Category
from __init__ import db
import schedule


def craw(url, c_id):
    r = requests.get(url)

    soup = BeautifulSoup(markup=r.text, features="html.parser")

    item = soup.find_all("li", attrs={"class": "item-boxlist"})

    for li in item:
        img = li.find("img").get("src")
        title = li.find("a", attrs={"class": "title"}).text
        href = li.find("a", attrs={"class": "title"}).get("href")
        sapo = li.find("div", attrs={"class": "sapo"}).text
        info = {
            "img": img,
            "title": title,
            "href": "https://danviet.vn/{}".format(href),
            "sapo": sapo,
        }
        new = News(img=info['img'], title=info['title'], href=info['href'], sapo=info['sapo'], category_id=c_id)
        db.session.add(new)
        db.session.commit()

    return {"Success": True}


def solve():
    category = db.session.query(Category.id, Category.url).all()
    for c_id, url in category:
        craw(url, c_id)
        time.sleep(1)
    return {"success": True}


schedule.every().day.at("05:30").do(solve)


if __name__ == "__main__":
    schedule.run_pending()
    time.sleep(1)
