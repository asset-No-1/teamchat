from teamchat.call import save_movies
import os

def test_save_json():
    r = save_movies(2023)

    assert r
