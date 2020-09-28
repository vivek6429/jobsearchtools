# Script to notfy me for any changes on a lsit of webpages
# shows what changed during this time
# will be adding to cron jobs to run on every system startup


import yaml
import hashlib
import random,time,os
from requests_html import HTMLSession

def load_config():
    with open("config.yaml", "r") as stream:
        try :
            cfg = yaml.safe_load(stream)
            # print(cfg)
        except yaml.YAMLError as err :
            print(err)
            exit()
        return cfg

def generateHash():
    pass

def write_hashes():
    pass



cfg=load_config()
nonjsurls=cfg["urls"]["nonjs"]
jsurls=cfg["urls"]["js"]
useragents=random.choice(cfg["useragents"])

print(*nonjsurls,sep="\n")
print("\n\n")
print(*jsurls,sep="\n")

for url in nonjsurls:
    pass














