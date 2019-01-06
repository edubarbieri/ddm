
import requests
import xml.etree.ElementTree as ET
import db
import config
import transmissionrpc

def get_pending():
    resp = requests.get(config.get_config()["feedURL"])
    if resp.status_code != 200:
        print("Erro getting feed data {}".format(resp.status_code))
        return
    raw_xml = resp.content
    rss = ET.fromstring(raw_xml)
    episodes = []
    for item in rss.iter("item"):
        episodes.append({
                "title": item.find("title").text,
                "link": item.find("link").text,
                "show_id": item.find("{http://showrss.info}show_id").text,
                "episode_id": int(item.find("{http://showrss.info}episode_id").text),
                "show_name": item.find("{http://showrss.info}show_name").text
        })
    return filter(_already_added, episodes)

def _already_added(episode):
    return not db.already_feed_added(episode["episode_id"])

def _get_tr_client():
    tr_conf = config.get_config()["transmission"]
    host, port = tr_conf["host"].split(":")
    return transmissionrpc.Client(host, port=port, user=tr_conf["user"], password=tr_conf["password"])


def _add_in_transmission(ep):
    tc = _get_tr_client()
    tor_resp = tc.add_torrent(ep["link"])
    if tor_resp == None:
        return
    db.add_feed(ep)

def remove_completes():
    tc = _get_tr_client()
    for t in tc.get_torrents():
        if t.isFinished:
            tc.remove_torrent(t.id)

def process():
    for ep in get_pending():
        print("Adding to download queue {}".format(ep["title"]))
        _add_in_transmission(ep)
