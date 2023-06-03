import dataclasses
import urllib.parse

trackers = ["http://tracker.trackerfix.com:80/announce",
            "udp://9.rarbg.me:2740",
            "udp://9.rarbg.to:2780",
            "udp://tracker.fatkhoala.org:13720",
            "udp://tracker.tallpenguin.org:15730"]


    

@dataclasses.dataclass
class Torrent:
    title: str
    hash_code: str
    time: str
    size: str
    imdb: str | None

    def build_magnet_link(self):
        res = "magnet:?xt=urn:btih:" + self.hash_code + "&dn=" + self.title
        for tracker in trackers:
            res += "&tr=" + urllib.parse.quote(tracker)
        return res


def torrent_row_factory(_cursor, row):
    return Torrent(*row)