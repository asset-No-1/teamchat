from teamchat.api.call import save_json, list2df

#def test_save2df():
#    r = save2df('20220101')
#
#    assert r

def test_save_json():
    data = list2df(year='2022')
    r = save_json(data)

    assert True
