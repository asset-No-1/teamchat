from teamchat.call import save_json, list2df
import os

#def test_save2df():
#    r = save2df('20220101')
#
#    assert r

def test_save_json():
    data = list2df(year=2022)
    home_path = os.path.expanduser("~")
    file_path = f"{home_path}/data/mov_data/year=2022/data.json"
    r = save_json(data, file_path)

    assert True
