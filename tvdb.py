import requests

_api_url = "https://api.thetvdb.com"
_api_key = "436CB4A29DEF63C1"
_auth_token = None
_serie_cache = {}

def _url(path):
    return _api_url + path

def _default_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "en-US",
        "User-Agent": "DudaDownloadManager",
        "Authorization": _auth_token
    }

def _login():
    global _auth_token
    if _auth_token != None:
        return
    print("Executing login in TvDB Api...")
    resp = requests.post(_url("/login"), json={
        "apikey": _api_key
    }, headers=_default_headers())
    if resp.status_code == 200:
        _auth_token = "Bearer " + resp.json()["token"]
    else:
        print("Error executing login: ", resp.content)

def search_series(name):
    _login()
    search_name = name.lower()
    if search_name in _serie_cache:
        return _serie_cache[search_name]

    print("Searching serie {}".format(name))
    resp = requests.get(_url("/search/series"), params={
        "name": search_name
    }, headers=_default_headers())
    if resp.status_code == 200:
        data_array = resp.json()["data"]
        if len(data_array) > 0:
            serie_data = data_array[0]
            _serie_cache[search_name] = serie_data
            return serie_data
    print("Could not find serie with name: {}, status_code: {}".format(
        name, resp.status_code))
    return None

def get_serie_id(name):
    serie = search_series(name)
    if serie == None:
        return None
    return serie["id"]

def get_serie_name(name):
    serie = search_series(name)
    if serie == None:
        return None
    return serie["seriesName"]

def get_episode(serie_name, season, episode):
    _login()
    serie_id = get_serie_id(serie_name)
    if serie_id == None:
        return None
    resp = requests.get(_url("/series/{}/episodes/query".format(serie_id)),
                        params={"airedSeason": season,
                                "airedEpisode": episode},
                        headers=_default_headers())
    if resp.status_code == 200:
        data_array = resp.json()["data"]
        if len(data_array) > 0:
            return data_array[0]
    print("Could not find episodename: {}, season: {}, episode: {}".format(
        episode, season, episode))
    return None

def get_episode_name(serie_name, season, episode):
    episode_data = get_episode(serie_name, season, episode)
    if episode_data == None:
        return None
    return episode_data["episodeName"]
