from urllib.request import urlopen
import pandas as pd
import re
from bs4 import BeautifulSoup, Comment

def get_shot_events(URL):
    page = urlopen(URL)
    soup = BeautifulSoup(page, "html.parser")
    if soup.find("div", {"id": "all_shooting"}):  # filters seasons players didnt play/no playoffs etc
        comments = soup.find_all(string=lambda text: isinstance(text,
                                                                Comment))  ##bf-ref stores shooting data as comments for some reason idk
        for comment in comments:
            bs_com = BeautifulSoup(comment, "html.parser")
            if bs_com.find("div", {"class": "shot-area"}):
                return bs_com.find_all("div", {"class": "tooltip"})

def get_shot_df(shot_events):
  shot_list=[]
  for shot_event in shot_events:
    shot_coordinate_xy=re.compile(r'top:(.*)px;left:(.*)px')
    coordinates=shot_coordinate_xy.search(shot_event['style'])
    top,left=coordinates.groups()
    top=(int(top))
    left=int(left)-250
    info=shot_event['tip'].split("<br>")
    date=info[0].split(",")[0]
    teams=info[0].split(",")[2]
    time=info[1]
    shot_details=info[2].split()
    made=True if shot_details[0]=="Made" else False
    shot_type=shot_details[1]
    distance=shot_details[3]
    score_status=info[3]
    value=1 if made else 0
    value_adj=int(shot_type.split("-")[0]) if made else 0
    shot_list.append([date,teams,time,top,left,made,shot_type,distance,score_status,value,value_adj])
  df=pd.DataFrame(shot_list,columns=['Date',"Teams","Time","Y-Coordinate","X-Coordinate","Shot Made","Shot Type","Distance","Score Status","Shot Value","Shot Value Adj"])
  return df

def scrape_season_shot(player,season,include_playoffs=False):
    URL = "https://www.basketball-reference.com/play-index/shooting.fcgi?player_id={}&year_id={}&is_playoffs={}"
    shots=get_shot_events(URL.format(player,season,0))
    if include_playoffs:
        shots_playoff=get_shot_events(URL.format(player,season,1))
        shots=shots+shots_playoff

    return get_shot_df(shots)