import requests


class TVDBClient:
    _api_url = "https://api.thetvdb.com"
    _api_key = "436CB4A29DEF63C1"
    _auth_token = None
    _serie_cache = {}

    def __init__(self):
        self._login()

    def _url(self, path):
        return self._api_url + path

    def _default_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Accept-Language": "en-US",
            "User-Agent": "DDM",
            "Authorization": self._auth_token
        }

    def _login(self):
        if self._auth_token != None:
            return
        print("Executing login in TvDB Api...")
        resp = requests.post(self._url("/login"), json={
            "apikey": self._api_key
        }, headers=self._default_headers())
        if resp.status_code == 200:
            self._auth_token = "Bearer " + resp.json()["token"]
        else:
            print("Error executing login: ", resp.content)

    def search_series(self, name):
        search_name = name.lower()
        if search_name in self._serie_cache:
            return self._serie_cache[search_name]

        print("Searching serie {}".format(name))
        resp = requests.get(self._url("/search/series"), params={
            "name": search_name
        }, headers=self._default_headers())
        if resp.status_code == 200:
            data_array = resp.json()["data"]
            if len(data_array) > 0:
                serie_data = data_array[0]
                self._serie_cache[search_name] = serie_data
                return serie_data
        print("Could not find serie with name: {}, status_code: {}".format(
            name, resp.status_code))
        return None

    def get_serie_id(self, name):
        serie = self.search_series(name)
        if serie == None:
            return None
        return serie["id"]
    def get_serie_name(self, name):
        serie = self.search_series(name)
        if serie == None:
            return None
        return serie["seriesName"]
    def get_episode(self, serie_name, season, episode):
        serie_id = self.get_serie_id(serie_name)
        if serie_id == None:
            return None
        resp = requests.get(self._url("/series/{}/episodes/query".format(serie_id)),
                            params={"airedSeason": season,
                                    "airedEpisode": episode},
                            headers=self._default_headers())
        if resp.status_code == 200:
            data_array = resp.json()["data"]
            if len(data_array) > 0:
                return data_array[0]
        print("Could not find episodename: {}, season: {}, episode: {}".format(
            episode, season, episode))
        return None

    def get_episode_name(self, serie_name, season, episode):
        episode_data = self.get_episode(serie_name, season, episode)
        if episode_data == None:
            return None
        return episode_data["episodeName"]
