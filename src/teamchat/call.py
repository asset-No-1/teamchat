import requests
import os
import json

def req(year='2022'):
    url = gen_url(year)
    r = requests.get(url)
    code = r.status_code
    data = r.json()
    
    return code, data

def gen_url(year="2022"):
    base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    key = get_key()
    url = f"{base_url}?key={key}&openStartDt={year}&openEndDt={year}"

    return url

def get_key():
    key = os.getenv('MOVIE_API_KEY')
    return key

def req2list(year='2022'):
    _, data = req(year)
    l = data['movieListResult']['movieList']
    return l

def list2df(year='2022'):
    l = req2list(year)

    return l

def save_json(data, year='2022'):
    data = list2df(year='2022')
    home_path = os.path.expanduser("~")
    file_path = f"{home_path}/data/mov_data/year={year}/data.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    pass

