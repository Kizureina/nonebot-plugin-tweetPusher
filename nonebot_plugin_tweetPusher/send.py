import sqlite3
import requests
import nonebot
import json
import os
from nonebot import require, get_bot
scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('interval', minutes = 1, id = 'twisender')
async def twi_sender():
    bot = get_bot()
    driver = nonebot.get_driver()
    pusher_groups = driver.config.pusher_group
    pusher_users = driver.config.pusher_user
    print("start")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "twitest.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("select * from tweet")
    twis = cur.fetchall()
    
    for i in range(len(twis)):
        uname = twis[i][1]
        push_time = twis[i][2]
        tid = twis[i][3]

        if push_time == 1:
            url = 'https://tweetpik.com/api/images'
            h = {
                    'Content-Type': 'application/json',
                    'Authorization':'c9c59ccd-64c3-407f-9be0-8a3bdad07881'
                    }
            tid = str(tid)
            data = {"tweetId":tid}
            r = requests.post(url, headers = h, data = json.dumps(data))
            pic = json.loads(r.text)
            pic_url = pic['url']
            cq_twi = "[CQ:image,file=" + pic_url + ",id=40000]"
            tweet = pic['tweet']['text']

            cq_twi = "[CQ:image,file=" + pic_url + ",id=40000]"
            link = 'https://twitter.com/' + uname + '/status/' + tid
            
            #await bot.send_group_msg(group_id = int(j), message=(f"发推啦!\n推文截图：{cq_twi}\n原推文：{tweet}\n链接：{link}"))
            for i in pusher_users:
                try:
                    await bot.send_private_msg(user_id = int(i), message=(f"你关注的推主发推啦!\n推文截图：{cq_twi}\n原推文：{tweet}\n链接：{link}"))
                except:
                    pass
            for j in pusher_groups:
                try:
                    await bot.send_group_msg(group_id = int(j), message=(f"发推啦!\n推文截图：{cq_twi}\n原推文：{tweet}\n链接：{link}"))
                except:
                    pass
            sql = f"UPDATE tweet SET times = 0 WHERE id = {i}"
            cur.execute(sql)
            con.commit()
        else:
            continue
