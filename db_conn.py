import aiosqlite
import torrent


CATEGORIES = {
    35: 'ebooks',
    27: 'games_pc_iso',
    28: 'games_pc_rip',
    40: 'games_ps3',
    53: 'games_ps4',
    32: 'games_xbox',
    14: 'movies_xvid',
    42: 'movies_bd_full',
    46: 'movies_bd_remux',
    17: 'movies_x264',
    44: 'movies_x264',
    47: 'movies_x264_3d',
    50: 'movies_x264_4k',
    45: 'movies_x264_720p',
    54: 'movies_x265',
    51: 'movies_x265_4k',
    52: 'movies_x265_4k_hdr',
    48: 'movies_xvid_720p',
    25: 'music_flac',
    23: 'music_mp3',
    41: 'tv',
    18: 'tv_sd',
    49: 'tv_uhd',
    4: 'xxx',
}

class RarbgDatabase:
    conn: aiosqlite.Connection

    def __init__(self):
        self.conn = None
    
    async def close(self):
        await self.conn.close()

    async def connect(self, db_path: str):
        self.conn = await aiosqlite.connect(db_path)
        self.conn.row_factory = torrent.torrent_row_factory
    
    async def list_from_categories(self, list_of_categories: list[int], limit: int = 100) -> list[torrent.Torrent]:
        """_summary_

        Args:
            list_of_categories (list[int]): _description_
            limit (int, optional): _description_. Defaults to 100.

        Returns:
            list[tuple]: (title, hash, time, size, imdb)
        """
        cats = [CATEGORIES[cat] for cat in list_of_categories]
        cur = await self.conn.execute("SELECT title, hash, dt, size, imdb FROM items WHERE cat IN (" + "?,"*(len(list_of_categories)-1) + "?) ORDER BY id DESC LIMIT (?)", (*cats, limit))
        return list(await cur.fetchall())
    
    async def search(self, list_of_categories: list[int]= None, limit: int = 100, imdb: str = None, search_string: str = None) -> list[torrent.Torrent]:
        sql = "SELECT title, hash, dt, size, imdb FROM items WHERE "
        categ = None
        if list_of_categories is not None:
            categ = [CATEGORIES[cat] for cat in list_of_categories]
            sql += "cat IN (" + "?,"*(len(list_of_categories)-1) + "?) AND "
        if imdb is not None:
            sql += "imdb = ? AND "
        if search_string is not None:
            sql += "title LIKE ? "

        if sql.endswith("AND "):
            sql = sql[:-4]

        sql += "ORDER BY id DESC LIMIT (?)"


        params = (*categ, imdb, search_string, limit)
        params = tuple([param for param in params if param is not None])

        cur = await self.conn.execute(sql, params)
        
        return list(await cur.fetchall())
