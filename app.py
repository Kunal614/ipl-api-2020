from flask import Flask , request ,jsonify

from bs4 import BeautifulSoup

import requests

from fake_useragent import UserAgent

import datetime



ua={"UserAgent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}


app =Flask(__name__)

@app.route('/' , methods=['GET'])
def index():
    return jsonify({"Here_You Can Perform 4 Get Request":['livescore','nextmatch','pointtable','schedule']})  

  

@app.route('/schedule' , methods=['GET'])
def shedule():
    url = "https://www.firstpost.com/firstcricket/cricket-schedule/series/ipl-2020.html"
    res = requests.get(url , headers=ua)
    soup = BeautifulSoup(res.content , features='lxml')
    data  =soup.findAll(class_='schedule-head')
    team_name = soup.findAll(class_='sc-match-name')
    time = soup.findAll(class_='sc-label-val')
    date_st=[]
    Team_name=[]
    time_mat=[]
    tm = 0
    for i in team_name:
        Team_name.append(i.get_text().strip())

    for i in  data:
        y = i.get_text().strip()
        y = y.replace('\n' , ' ')
        y = y.replace('\t' , '')
        y = y[:6]  
        date_st.append(y)

    for i in time:
        if tm < len(time):
            p = time[tm].get_text().strip()
            p = p.replace('\n' , ' ')
            p = p.replace('\t' , '')
            r = time[tm+1].get_text().strip()
            r = r.replace('\n' , ' ')
            r = r.replace('\t' , '')
            tm=tm+2   
            time_mat.append(p+"  "+r)

      

    all_items = {
        "Teams":Team_name,"Date":date_st,"Time":time_mat    
    }    
    return jsonify(all_items)

@app.route('/pointtable' , methods=['GET'])

def point_table():
    url = "https://www.espncricinfo.com/series/_/id/8048/season/2020/indian-premier-league"

    res = requests.get(url , headers = ua)
    soup = BeautifulSoup(res.content , features='lxml')
    points = soup.findAll(class_='pr-3')
    team = soup.findAll(class_='text-left')
    teams=[]
    for i in range(1 , 9):
        teams.append(team[i].get_text())
    match =[]
    win=[]
    loss=[]
    point=[]
    nr=[]
    flag = 0
    for i in range(5 , 45):
        y = points[i].get_text()
        # print(y , end=" ")
        if flag == 0:
            match.append(y)
            flag=1
            continue
        if flag ==1:
            win.append(y)
            flag=2
            continue
        if flag == 2:
            loss.append(y)
            flag=3
            continue
        if flag ==3:
            point.append(y)
            flag=4
            continue
        if flag == 4 :
            nr.append(y)
            flag=0

    all_items={
        "Team":teams , "match":match , "Point":point,"Won":win,"Loss":loss,"N/R":nr
    }
    return jsonify(all_items)

@app.route('/livescore',methods=['GET'])

def score():
    url="https://www.espncricinfo.com/"
    res = requests.get(url , headers = ua)
    soup = BeautifulSoup(res.content , features='lxml')
    head = soup.findAll(class_='text-truncate')
    comp = soup.findAll(class_='competitor')
    win = soup.findAll(class_='text-dark')
    all_items={
        "Headline":head[0].get_text() , "Team1":comp[0].get_text(),"Team2":comp[1].get_text(),"Status":win[0].get_text()
    }
    return jsonify(all_items)

@app.route('/nextmatch',methods=['GET'])

def next():
    url = "https://www.firstpost.com/firstcricket/cricket-schedule/series/ipl-2020.html"
    res = requests.get(url , headers=ua)
    soup = BeautifulSoup(res.content , features='lxml')
    data  =soup.findAll(class_='schedule-head')
    team_name = soup.findAll(class_='sc-match-name')
    time = soup.findAll(class_='sc-label-val')
    
    y = data[0].get_text().strip()
    y = y.replace('\n' , ' ')
    y = y.replace('\t' , '')
    Date = y[:6]  
    Team = team_name[0].get_text().strip()
    p= time[0].get_text().strip()
    p = p.replace('\n' , ' ')
    p = p.replace('\t' , '')
    r = time[1].get_text().strip()
    r = r.replace('\n' , ' ')
    r = r.replace('\t' , '')
    Time = p+"  "+r
    all_items={
        "Date":Date , "Team":Team , "Time":Time
    }
    return jsonify(all_items)



@app.errorhandler(404) 

def not_found(e): 
    return "<h1>Invalid Request</h1>"  

          

if __name__ == "__main__":
    app.run(debug=True)    
