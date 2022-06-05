import twint
import jsonlines
import time
import os
import sqlite3
import nonebot
from nonebot import require
scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('interval', minutes = 3, id = 'twi_checker')

def tweet_check():
    driver = nonebot.get_driver()
    twi_users = getattr(driver.config, "twi_user", list)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "twi.db")
    now_users = 0
    for i in twi_users:    
        now_users = now_users + 1
    if os.path.exists(db_path) == False:
        # 初始化
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tweet(id INTEGER PRIMARY KEY, name TEXT, times INTEGER, tid INTEGER)")
        if twi_users:
            j = 0
            for i in twi_users:
                cur.execute('INSERT INTO tweet VALUES(?,?,?,?)', (j, i, 0, 1111111111111))
                con.commit()
                j = j + 1
    else:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute('select * from tweet')
        users = cur.fetchall()

        for i in range(len(users)):
            uname = users[i][1]
            tid = users[i][3]

            c = twint.Config()
            c.Username = uname
            c.Store_json = True
            c.Hide_output = True
            c.Output = "temp.json"
            t = time.strftime("%Y-%m-%d", time.localtime())
            c.Since = t
            twint.run.Search(c)

            name = "temp.json"
            if os.path.exists(name) == True:
                with jsonlines.open(name) as reader:
                    for obj in reader:
                        if '@' in obj['tweet']:
                            continue
                        else:
                            last_twi = obj['id']
                            if last_twi != tid:
                                sql = f"UPDATE tweet SET tid = '%s' WHERE id = {i}" % last_twi
                                cur.execute(sql)
                                con.commit()
                                sql = f"UPDATE tweet SET times = 1 WHERE id = {i}"
                                cur.execute(sql)
                                con.commit()
                            else:
                                sql = f"UPDATE tweet SET times = 0 WHERE id = {i}"
                                cur.execute(sql)
                                con.commit()
                                print("未发新推!")
                            break
                os.remove(name)
            else:
                continue

