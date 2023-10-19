import requests
from bs4 import BeautifulSoup
import time
from os import system, name
from collections import namedtuple 

Score = namedtuple('Score', ['Team1', 'Team2', 'Score1', 'Score2'])

def getScore(url = 'https://www.cricbuzz.com/cricket-match/live-scores') -> Score:

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    dats = soup.find_all(class_ = 'cb-ovr-flo cb-hmscg-tm-nm')
    scores = soup.find_all(class_ = 'cb-ovr-flo')
    start = int(len(scores) - (len(dats)/2)*5) + 1
    curr_score = Score(scores[start].get_text(), scores[start + 2].get_text(), scores[start + 1].get_text(), scores[start + 3].get_text())

    return curr_score

def getNews(url = 'https://www.cricbuzz.com/cricket-news'):
    
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    output = soup.find_all(class_ = 'cb-nws-intr')

    news = []

    for n in output:
        news.append(n.get_text())
    return news

def getICCRanking(player_type = 'batting', match_format = 'test'):
    
    url = f'https://www.cricbuzz.com/cricket-stats/icc-rankings/men/{player_type}'

    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    output = soup.find_all(class_ = 'text-hvr-underline text-bold cb-font-16')
    
    test_rankings = []
    odi_rankings = []
    t20_rankings = []

    for i in range(10):
        test_rankings.append(output[i].get_text())
    for i in range(10, 20):
        odi_rankings.append(output[i].get_text())
    for i in range(20, 30):
        t20_rankings.append(output[i].get_text())

    if match_format == 'odi':
        return odi_rankings
    if match_format == 't20':
        return t20_rankings
    else:
        return test_rankings

def printScore(curr_score):

    now = time.localtime()

    system('clear')

    print("-------------------------------")
    print(f"Current Score at time: {now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}")
    print("-------------------------------")
    print(curr_score.Team1 + ": " + curr_score.Score1)
    print(curr_score.Team2 + ": " + curr_score.Score2)
    print("-------------------------------")

def liveScore(url = 'https://www.cricbuzz.com/cricket-match/live-scores'):
    while True:
        printScore(getScore(url))
        time.sleep(5)

def team1Score(url = 'https://www.cricbuzz.com/cricket-match/live-scores'):
    
    return [getScore(url).Team1, getScore(url).Score1]

def team2Score(url = 'https://www.cricbuzz.com/cricket-match/live-scores'):
    
    return [getScore(url).Team2, getScore(url).Score2]

def team1Runs(url = 'https://www.cricbuzz.com/cricket-match/live-scores'):
    return int(getScore(url).Score1.split(" ")[0].split('-')[0])

def team2Runs(url = 'https://www.cricbuzz.com/cricket-match/live-scores'):
    return int(getScore(url).Score2.split(" ")[0].split('-')[0])

def runDiff(url = 'https://www.cricbuzz.com/cricket-match/live-scores'):
    return abs(team1Runs(url) - team2Runs(url))

def getTime():
    now = time.localtime()
    return str(f"{now.tm_hour:02}:{now.tm_min:02}:{now.tm_sec:02}")