import sqlite3

bd = sqlite3.connect("2048.sqlite")
cur = bd.cursor()
cur.execute("""
create table if not exists RECORDS (
    name text,
    score integer
)""")


def inser_result(name, score):
    cur.execute("""
    insert into RECORDS Values (?, ?)
    """, (name, score))
    bd.commit()


def get_best():
    cur.execute("""
    SELECT name gamer, max(score) score from RECORDS
    GROUP by name
    ORDER by score DESC
    LIMIT 3
    """)
    return cur.fetchall()


inser_result("qqq", 888)
