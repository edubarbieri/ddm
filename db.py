import sqlite3

_initial_sql = [
        """
		CREATE TABLE IF NOT EXISTS serie (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			tvdbId INTEGER,
			searchKey TEXT
		)
	""",
        """
		CREATE TABLE IF NOT EXISTS feed (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			episodeId INTEGER,
			title TEXT
		)
	"""
]
_db = "ddm.db"
_init = False
def init():
    global _init
    if _init:
        return
    print("initializing sqlite database")
    conn = sqlite3.connect(_db)
    for sql in _initial_sql:
        conn.execute(sql)
    conn.close()
    _init = True

def already_feed_added(episode_id):
    init()
    already = False
    con = sqlite3.connect(_db)
    cursor = con.cursor()
    cursor.execute("SELECT * from feed where episodeId = ?", [episode_id])
    if cursor.fetchone() != None:
        already = True
    cursor.close()
    con.close()
    return already

def add_feed(episode):
    init()
    con = sqlite3.connect(_db)
    cursor = con.cursor()
    cursor.execute("INSERT INTO feed(episodeId, title) VALUES (?, ?)", (
        episode["episode_id"], episode["title"], 
    ))
    con.commit()
    cursor.close()
    con.close()