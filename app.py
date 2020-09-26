from flask import Flask , request ,jsonify

from bs4 import BeautifulSoup

import requests

from fake_useragent import UserAgent

import datetime



ua={"UserAgent":'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}


app =Flask(__name__)

@app.route('/shedule' , methods=['GET'])

def shedule():
    url = "https://www.iplt20.com/matches/schedule/men"
    res = requests.get(url , headers=ua)
    soup = BeautifulSoup(res.content , features='lxml')
    date  = soup.findAll(class_='js-date')
    teams = soup.findAll(class_='fixture__teams')
    time = soup.findAll(class_='fixture__time')
    date_st=[]
    team_name=[]
    time_mat=[]
    for i in range(len(date)):
        date_st.append(date[i].get_text())
        y = teams[i].get_text() #printing date
        y = y.strip()
        y = y.replace('\n',' ')
        team_name.append(y)
        time_mat.append(time[i].get_text())

    all_items = {
        "Date":date_st,"Teams":team_name,"Time":time_mat    
    }    
    return jsonify(all_items)

@app.route('/pointtable' , methods=['GET'])

def point_table():
    url = "https://www.iplt20.com/points-table/2020"

    res = requests.get(url , headers = ua)
    soup = BeautifulSoup(res.content , features='lxml')
    points = soup.findAll(class_='js-points')
    tab = soup.findAll(class_='js-team')
    data = soup.findAll(class_='standings-table__optional')
    k = 0
    j = 1
    y=0
    teams = []
    point = []
    won=[]
    loss=[]
    tied=[]
    nr=[]
    fr=[]
    against=[]
    for i in range(6 ,len(data)):
        if i%6==0:
            y=0
            teams.append(tab[j].get_text())
           
            point.append(points[k].get_text())
            k=k+1
            j=j+2
        if y == 0:
            won.append(data[i].get_text())
            y+=1
            continue
        if y ==1:    
            loss.append(data[i].get_text())
            y+=1
            continue
        if y == 2:    
            tied.append(data[i].get_text())
            y+=1
            continue
        if y ==3:    
            nr.append(data[i].get_text())
            y+=1
            continue
        if y ==4:    
            fr.append(data[i].get_text())
            y+=1
            continue
        if y ==5:    
            against.append(data[i].get_text())
    all_items={
        "Team":teams , "Point":point,"Won":won,"Loss":loss,"Tied":tied
    }
    return jsonify(all_items)

@app.route('/livescore',methods=['GET'])

def score():
    # url ="https://www.cricbuzz.com/cricket-match/live-scores"
    # res = requests.get(url , headers = ua)
    # soup = BeautifulSoup(res.content , features='lxml')
    # data = soup.findAll('a')
    # match = data[98].get_text()
    # team = data[99].get_text()
    # score = data[100].get_text()
    url="https://www.espncricinfo.com/"
    res = requests.get(url , headers = ua)
    soup = BeautifulSoup(res.content , features='lxml')
    head = soup.findAll(class_='text-truncate')
    comp = soup.findAll(class_='competitor')
    win = soup.findAll(class_='text-dark')



    
    all_items={
        "Headline":head[0].get_text() , "Team1":comp[0].get_text(),"Temam2":comp[1].get_text(),"Status":win[0].get_text()
    }
    return jsonify(all_items)

@app.route('/nextmatch',methods=['GET'])

def next():
    
    # url ="https://www.cricbuzz.com/cricket-schedule/upcoming-series/league"
    # res = requests.get(url , headers = ua)
    # soup = BeautifulSoup(res.content , features='lxml')
    # data = soup.findAll(class_='cb-lv-grn-strip')
    # match = soup.findAll(class_='cb-mtchs-dy')
    # team = soup.findAll(class_='cb-adjst-lst')
    # all_items={
    #     "Date":data[0].get_text() ,"League": match[0].get_text() , "Team":team[0].get_text()
    # }
    # return jsonify(all_items)
    url = "https://www.iplt20.com/matches/schedule/men"
    res = requests.get(url , headers = ua)
    soup = BeautifulSoup(res.content , features='lxml')
    date = soup.find(class_='js-date')   
    team = soup.find(class_='fixture__teams')  
    time = soup.find(class_='fixture__time')
    y = team.get_text()
    y= y.strip()
    y = y.replace('\n',' ')
    date = date.get_text()
    time = time.get_text()
    all_items={
        "Date":date , "Team":y , "Time":time
    }
    return jsonify(all_items)

     

if __name__ == "__main__":
    app.run(debug=True)    