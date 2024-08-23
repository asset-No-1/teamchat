import requests
import os
import pandas as pd


def req(load_dt='20220101', url_param={}):
    url = gen_url(load_dt, url_param)
    r = requests.get(url)
    code = r.status_code
    data = r.json()
    
    return code, data

def gen_url(load_dt="20220101", url_param = {}):
    base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    key = os.getenv('MOVIE_API_KEY')
    url = f"{base_url}?key={key}&targetDt={load_dt}"
    for k,v in url_param.items():
        url = url + f"&{k}={v}"

    return url                 

def req2list(load_dt='20220101', url_param={}):
    _, data = req(load_dt, url_param)
    l = data['movieListResult']['movieList']

    return l

def list2df(load_dt='20220101', url_param={}):
    l = req2list(load_dt, url_param)
    df = pd.DataFrame(l)
    
    return df

def save2df(load_dt='20220101', url_param={}):
    df = list2df(url_param=url_param, load_dt=load_dt)
    df['load_dt'] = load_dt
    df.to_parquet(f'~/data/api/{load_dt}.parquet')
    
    return df
