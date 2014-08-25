#! /usr/bin/env python
import yaml
import MySQLdb
import urllib
import logging
from random import randint
import tweepy, time
from array import array

#get config
with open('/home/will/config.yaml', 'r') as f:
    data = yaml.load(f)
    host = data["host"];
    dbuser = data["user"];
    dbpasswd = data["password"];
    db = data["db"];
    CONSUMER_KEY = data["tCK"];
    CONSUMER_SECRET = data["tCS"];
    ACCESS_KEY = data["tAK"];
    ACCESS_SECRET = data["tAS"]
#will blew

#pxlbin bot auth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth) #do auth

#logging config
logging.basicConfig(filename='pxlbot.log',level=logging.DEBUG)

#connect to db
db = MySQLdb.connect(host=host,user=dbuser,passwd=dbpasswd,db=db)
cur = db.cursor()
cur2 = db.cursor()

#random logic for tweet type
randER = randint(0,1000) 

def RegularTweet():
  #get all
  logging.info('Regular Start!')
  try:
    cur.execute("SELECT FULL,title,site,path,up FROM links WHERE TIME > DATE_SUB(CURDATE(), INTERVAL 2 HOUR) AND nsfw = 0 AND site != 'instagram' AND up > 20 ORDER BY RAND() DESC LIMIT 1")
    links = cur.fetchall ()
    api.update_status(links[0][1] +" " + links[0][0] + " #pxlbin " + "#" + links[0][2] + " #" + links[0][3])
    logging.info("Tweeting regular " + links[0][0])
    quit() #die
  except Exception,e:
    logging.debug(str(e))
  logging.info('Finish!')
def TargetTweet():
  logging.info('Target Start!')
  trendsJ = api.trends_place(23424977)
  data = trendsJ[0] 
  trends = data['trends']
  names = [trend['name'] for trend in trends]
  for name in names:
    try:
      cur2.execute('SELECT * FROM links WHERE TIME > DATE_SUB(CURDATE(), INTERVAL 10 HOUR) AND nsfw = 0 AND site != "instagram" AND title like (%s) ORDER BY RAND() DESC LIMIT 1',("%" + name + "%"))
      if not cur2.rowcount:
        noop = 1
      else:
        for row in cur2:
          logging.info("Tweeting trending " + row[2])
          if name.startswith("#" or "@"):
            noop = ""
          else:
            pre = "#"
            name = pre + name
          api.update_status(name + " " + row[4] + " " + row[2] + " #" + row[1] + " #" + row[3])
          quit() #die!
    except Exception,e:
      logging.debug(str(e))
  logging.info('Finished')

if randER%2==0:
  TargetTweet() #do this and die if needed.
else:
  RegularTweet() #do this if not


