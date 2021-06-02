from django.shortcuts import render
from home.models import Team, Match
import requests
import logging
import datetime
from django.core.paginator import Paginator
from django.shortcuts import render

def getMatches(matches, matchDatas):
    for matchData in matchDatas:
        if len(matchData['opponents']) == 2:
            match = Match()
            match.name = matchData['name']
            match.rescheduled = matchData['rescheduled']
            match.league_id = matchData['league']['id']
            match.league_image_url = matchData['league']['image_url']
            match.league_modified_at = matchData['league']['modified_at']
            match.league_name = matchData['league']['name']
            match.league_url = matchData['league']['url']
            match.league_slug = matchData['league']['slug']
            match.opponent1_acronym = matchData['opponents'][0]['opponent']['acronym']
            match.opponent1_id = matchData['opponents'][0]['opponent']['id']
            match.opponent1_image_url = matchData['opponents'][0]['opponent']['image_url']
            match.opponent1_location = matchData['opponents'][0]['opponent']['location']
            match.opponent1_modified_at = matchData['opponents'][0]['opponent']['modified_at']
            match.opponent1_name = matchData['opponents'][0]['opponent']['name']
            match.opponent1_slug = matchData['opponents'][0]['opponent']['slug']
            match.opponent2_acronym = matchData['opponents'][1]['opponent']['acronym']
            match.opponent2_id = matchData['opponents'][1]['opponent']['id']
            match.opponent2_image_url = matchData['opponents'][1]['opponent']['image_url']
            match.opponent2_location = matchData['opponents'][1]['opponent']['location']
            match.opponent2_modified_at = matchData['opponents'][1]['opponent']['modified_at']
            match.opponent2_name = matchData['opponents'][1]['opponent']['name']
            match.opponent2_slug = matchData['opponents'][1]['opponent']['slug']
            match.forfeit = matchData['forfeit']
            match.live_embed_url = matchData['live_embed_url']
            match.winner = matchData['winner']
            match.official_stream_url =matchData['official_stream_url']
            match.videogame_slug = matchData['videogame']['slug']
            match.videogame_name = matchData['videogame']['name']
            match.begins_at = matchData['original_scheduled_at']
            match.begins_in = None
            if match.begins_at:
                dateTimeMatch = datetime.datetime.strptime(match.begins_at, '%Y-%m-%dT%H:%M:%SZ')
                match.begins_in = str(dateTimeMatch - datetime.datetime.now())
                index = match.begins_in.rindex('.')
                match.formatted_begins_in = match.begins_in[0:index]
            matches.append(match)

    return matches

def getTeams(teams, teamDatas):
    for teamData in teamDatas:
        team = Team()
        team.id = teamData['id']
        team.acronym = teamData['acronym']
        team.current_videogame_id = teamData['current_videogame']['id']
        team.current_videogame_name = teamData['current_videogame']['name']
        team.current_videogame_slug = teamData['current_videogame']['slug']
        team.image_url = teamData['image_url']
        team.location = teamData['location']
        team.modified_at = teamData['modified_at']
        team.name = teamData['name']
        team.slug = teamData['slug']
        teams.append(team)
    return teams

def getData(request):
    teams = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/teams?' + myToken)
    teamDatas = response.json()
    
    teams = getTeams(teams, teamDatas)

    matches = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/matches?' + myToken)
    matchDatas = response.json()

    matches = getMatches(matches, matchDatas)

    return render(request, 'home/index.html', {
        'teamDatas': teams,
        'matchDatas': matches
    })

    
def getDotaData(request):
    dotaTeams = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/dota2/teams?' + myToken)
    dotaTeamDatas = response.json()
    dotaTeams = getTeams(dotaTeams, dotaTeamDatas)
    dotaMatches = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/dota2/matches?' + myToken)
    matchDatas = response.json()

    dotaMatches = getMatches(dotaMatches, matchDatas)

    return render(request, 'home/dota2.html', {
        'dotaTeamDatas': dotaTeams,
        'dotaMatchDatas': dotaMatches
    })

def getLoLData(request):
    lolTeams = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/lol/teams?' + myToken)
    lolTeamDatas = response.json()
    lolTeams = getTeams(lolTeams, lolTeamDatas)

    lolMatches = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/lol/matches?' + myToken)
    matchDatas = response.json()

    lolMatches = getMatches(lolMatches, matchDatas)

    return render(request, 'home/lol.html', {
        'lolTeamDatas': lolTeams,
        'lolMatchDatas': lolMatches
    })


def getSiegeData(request):
    siegeTeams = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/r6siege/teams?' + myToken)
    siegeTeamDatas = response.json()
    siegeTeams = getTeams(siegeTeams, siegeTeamDatas)

    siegeMatches = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/r6siege/matches?' + myToken)
    matchDatas = response.json()

    siegeMatches = getMatches(siegeMatches, matchDatas)

    return render(request, 'home/siege.html', {
        'siegeTeamDatas': siegeTeams,
        'siegeMatchDatas': siegeMatches
    })


def getCsgoData(request):
    csgoTeams = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/csgo/teams?' + myToken)
    csgoTeamDatas = response.json()
    csgoTeams = getTeams(csgoTeams, csgoTeamDatas)

    csgoMatches = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/csgo/matches?' + myToken)
    matchDatas = response.json()

    csgoMatches = getMatches(csgoMatches, matchDatas)

    return render(request, 'home/csgo.html', {
        'csgoTeamDatas': csgoTeams,
        'csgoMatchDatas': csgoMatches
    })

def getValorantData(request):
    valorantTeams = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/valorant/teams?' + myToken)
    valorantTeamDatas = response.json()
    valorantTeams = getTeams(valorantTeams, valorantTeamDatas)

    valorantMatches = []
    valorantLives = []
    valorantUpcomings = []
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    response = requests.get('https://api.pandascore.co/valorant/matches?' + myToken)
    matchDatas = response.json()
    repsonseLives = requests.get('https://api.pandascore.co/valorant/matches/running?' + myToken)
    livesDatas = repsonseLives.json()
    repsonseUpcoming = requests.get('https://api.pandascore.co/valorant/matches/upcoming?' + myToken)
    upcomingDatas = repsonseUpcoming.json()

    valorantLives = getMatches(valorantLives, livesDatas)
    valorantUpcomings = getMatches(valorantUpcomings, upcomingDatas)
    valorantMatches = getMatches(valorantMatches, matchDatas)


    return render(request, 'home/valorant.html', {
        'valorantTeamDatas': valorantTeams,
        'valorantMatchDatas': valorantMatches,
        'valorantLiveMatchDatas': valorantLives,
        'valorantUpcomingMatchDatas': valorantUpcomings,
        'allMatchData': matchDatas
    })