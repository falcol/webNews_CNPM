import requests
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from bs4 import BeautifulSoup
from sqllib.database import Corona, Corona_VN
from __init__ import db
import time
import schedule


class BadRequest(Exception):
    pass


def get_corona_data():
    r = requests.get('https://baomoi.com/events/coronavirus.epi')
    soup = BeautifulSoup(markup=r.text, features='html.parser')

    tbody = soup.find('tbody')
    for tr in tbody.find_all('tr'):
        data = []
        for td in tr.find_all('td'):
            data.append(td.text)
        info = {'territory': data[0],
                'infection': data[1],
                'dead': data[2],
                'serious': data[3],
                'cured': data[4]}
        detail = Corona(territory=info['territory'], infection=info['infection'], death=info['dead'], serious=info['serious'], cure=info['cured'])
        db.session.add(detail)
        try:
            db.session.commit()
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)  # proves the original exception
            raise BadRequest from e

    return {'Success': True}


def corona_in_vietnam():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0', 'Content-Type': 'text/html; charset=utf-8'}
    r = requests.get("https://www.ntdvn.com/corona/thong-ke", headers=headers)
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(markup=r.text, features='html.parser')

    for tr in soup.find_all('tbody')[2].find_all('tr'):
        data = []
        for td in tr.find_all('td'):
            data.append(td.text)
        info = {'place': data[0],
                'infection': data[1],
                'death': data[2],
                'cured': data[3]}
        detail = Corona_VN(place=info['place'], infection=info['infection'], death=info['death'], cured=info['cured'])
        db.session.add(detail)
        db.session.commit()

    return {"Success": True}


def solve():
    get_corona_data()
    time.sleep(1)
    corona_in_vietnam()

    return {'Success': True}


schedule.every().day.at("05:30").do(solve)


if __name__ == "__main__":
    schedule.run_pending()
    time.sleep(1)
