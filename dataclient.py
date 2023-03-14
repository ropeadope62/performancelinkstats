import datetime
from iracingdataapi.client import irDataClient

def dataclient(): 
    irclient = irDataClient(username='davechadwick@gmail.com', password='@Finnegan2022@')
    global api
    api = irclient


def convtime(ms):
    delta = datetime.timedelta(milliseconds=(ms)).total_seconds()
    return delta

def lookup_driver(displayname):
    driver_id = api.lookup_drivers(displayname)[0]['cust_id']
    return driver_id   

def recentincidents(displayname):
    driver_id = lookup_driver(displayname)
    recentraces = api.stats_member_recent_races(driver_id)
    incidents = 0
    for race in recentraces['races']:
        incidents += race['incidents']
    return incidents

def get_roster(league_id=8804): 
    roster = []
    for eachdriver in api.league_get(league_id)['roster']:
        roster.append(tuple((eachdriver['display_name'], eachdriver['car_number'])))
    return roster
        
def get_seasons(league_id=8804):
    seasons = []
    for eachseason in api.league_seasons(league_id)['seasons']:
        seasons.append(tuple((eachseason['season_name'], eachseason['season_id'])))
    return seasons