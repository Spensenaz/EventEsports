from django.shortcuts import render
from home.models import Team, Match, Tournament
import requests
import aiohttp
import asyncio
import logging
import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
import sys

def getUpcomingMatches(matches, matchDatas):
    x = 0
    for matchData in matchDatas:
        if len(matches) < 8:
            if matchData['original_scheduled_at'] != None:
                    match = Match()
                    match.name = matchData['name']
                    match.rescheduled = matchData['rescheduled']
                    match.league_id = matchData['league']['id']
                    match.league_image_url = matchData['league']['image_url']
                    match.league_modified_at = matchData['league']['modified_at']
                    match.league_name = matchData['league']['name']
                    match.league_url = matchData['league']['url']
                    match.league_slug = matchData['league']['slug']
                    match.opponent1_name = "TBD"
                    match.opponent2_name = "TBD"
                    match.opponent1_image_url = None
                    match.opponent2_image_url = None
                    if len(matchData['opponents']) > 0:
                        if len(matchData['opponents']) >= 1:
                            match.opponent1_acronym = matchData['opponents'][0]['opponent']['acronym']
                            match.opponent1_id = matchData['opponents'][0]['opponent']['id']
                            match.opponent1_image_url = matchData['opponents'][0]['opponent']['image_url']
                            match.opponent1_location = matchData['opponents'][0]['opponent']['location']
                            match.opponent1_modified_at = matchData['opponents'][0]['opponent']['modified_at']
                            match.opponent1_name = matchData['opponents'][0]['opponent']['name']
                            if matchData['opponents'][0]['opponent']['acronym'] != None:
                                match.opponent1_name = matchData['opponents'][0]['opponent']['acronym']
                            match.opponent1_slug = matchData['opponents'][0]['opponent']['slug']
                        if len(matchData['opponents']) == 2:
                            match.opponent2_acronym = matchData['opponents'][1]['opponent']['acronym']
                            match.opponent2_id = matchData['opponents'][1]['opponent']['id']
                            match.opponent2_image_url = matchData['opponents'][1]['opponent']['image_url']
                            match.opponent2_location = matchData['opponents'][1]['opponent']['location']
                            match.opponent2_modified_at = matchData['opponents'][1]['opponent']['modified_at']
                            match.opponent2_name = matchData['opponents'][1]['opponent']['name']
                            if matchData['opponents'][1]['opponent']['acronym'] != None:
                                match.opponent2_name = matchData['opponents'][1]['opponent']['acronym']
                            match.opponent2_slug = matchData['opponents'][1]['opponent']['slug']
                    
                    match.forfeit = matchData['forfeit']
                    match.live_embed_url = matchData['live_embed_url']
                    match.winner = matchData['winner']
                    match.official_stream_url =matchData['official_stream_url']
                    match.videogame_slug = matchData['videogame']['slug']
                    match.videogame_name = matchData['videogame']['name']
                    match.begins_at = matchData['begin_at']
                    if not match.begins_at:
                        match.begins_at = matchData['original_scheduled_at']
                    match.begins_in = None
                    if match.begins_at:
                        dateTimeMatch = datetime.datetime.strptime(match.begins_at, '%Y-%m-%dT%H:%M:%SZ')
                        match.begins_in = str(dateTimeMatch - datetime.datetime.now() - datetime.timedelta(hours=4))
                        index = match.begins_in.rindex('.')
                        match.formatted_begins_in = match.begins_in[0:index]
                    if match.formatted_begins_in[0] != '-':
                        matches.append(match)
    return matches

    
def getLiveMatches(matches, matchDatas):
    for matchData in matchDatas:
        if len(matches) < 8:
            if matchData['original_scheduled_at'] != None:
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
                    if matchData['opponents'][0]['opponent']['name'] != None:
                        match.opponent1_name = matchData['opponents'][0]['opponent']['name']
                    else:
                        match.opponent1_name = "TBD"
                    match.opponent1_slug = matchData['opponents'][0]['opponent']['slug']
                    match.opponent2_acronym = matchData['opponents'][1]['opponent']['acronym']
                    match.opponent2_id = matchData['opponents'][1]['opponent']['id']
                    match.opponent2_image_url = matchData['opponents'][1]['opponent']['image_url']
                    match.opponent2_location = matchData['opponents'][1]['opponent']['location']
                    match.opponent2_modified_at = matchData['opponents'][1]['opponent']['modified_at']
                    if matchData['opponents'][1]['opponent']['name'] != None:
                        match.opponent2_name = matchData['opponents'][1]['opponent']['name']
                    else:
                        match.opponent2_name = "TBD"
                    match.opponent2_slug = matchData['opponents'][1]['opponent']['slug']
                    match.forfeit = matchData['forfeit']
                    match.live_embed_url = matchData['live_embed_url']
                    match.winner = matchData['winner']
                    match.official_stream_url =matchData['official_stream_url']
                    match.videogame_slug = matchData['videogame']['slug']
                    match.videogame_name = matchData['videogame']['name']
                    match.score_team_1 = matchData['results'][0]['score']
                    match.score_team_2 = matchData['results'][1]['score']
                    match.begins_at = matchData['begin_at']
                    if not match.begins_at:
                        match.begins_at = matchData['original_scheduled_at']
                    match.begins_in = None
                    if match.begins_at:
                        dateTimeMatch = datetime.datetime.strptime(match.begins_at, '%Y-%m-%dT%H:%M:%SZ')
                        match.begins_in = str(dateTimeMatch - datetime.datetime.now() - datetime.timedelta(hours=4))
                        index = match.begins_in.rindex('.')
                        match.formatted_begins_in = match.begins_in[0:index]
                    matches.append(match)
    return matches

def getPreviousMatches(matches, matchDatas):
    x = 0
    for matchData in matchDatas:
        if len(matches) < 8:
            if matchData['original_scheduled_at'] != None:
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
                    match.score_team_1 = matchData['results'][0]['score']
                    match.score_team_2 = matchData['results'][1]['score']
                    match.begins_at = matchData['begin_at']
                    if not match.begins_at:
                        match.begins_at = matchData['original_scheduled_at']
                    match.begins_in = None
                    if match.begins_at:
                        dateTimeMatch = datetime.datetime.strptime(match.begins_at, '%Y-%m-%dT%H:%M:%SZ')
                        match.begins_in = str(dateTimeMatch - datetime.datetime.now() - datetime.timedelta(hours=4))
                        index = match.begins_in.rindex('.')
                        match.formatted_begins_in = match.begins_in[0:index]
                    matches.append(match)
    return matches

def getTourneys(tourneys, tourneyDatas):
    for tourneyData in tourneyDatas:
        tourney = Tournament()
        tourney.league_name = tourneyData['league']['name']
        tourney.league_url = tourneyData['league']['url']
        tourney.name = tourneyData['name']
        tourney.serie_name = tourneyData['serie']['name']
        tourney.tier = tourneyData['serie']['tier']
        tourney.begin_at = tourneyData['begin_at']
        tourney.end_at = tourneyData['end_at']
        tourney.image_url = tourneyData['league']['image_url']
        tourney.id = tourneyData['id']
        tourney.slug = tourneyData['slug']
        tourney.standings = []
        if tourney.begin_at:
            dateTimeMatch = datetime.datetime.strptime(tourney.begin_at, '%Y-%m-%dT%H:%M:%SZ')
            tourney.begins_in = str(dateTimeMatch - datetime.datetime.now() - datetime.timedelta(hours=4))
            index = tourney.begins_in.rindex('.')
            tourney.formatted_begins_in = tourney.begins_in[0:index]
        tourneys.append(tourney)
    return tourneys

def getStandings(standings, tourneyStandingDatas):
    for standingData in tourneyStandingDatas:
        for team in standingData:
            team = Team()


async def getDataAsync(game):
    urls = ['https://api.pandascore.co/'+ game +'/tournaments/running?',
            'https://api.pandascore.co/'+ game +'/tournaments/upcoming?',
            'https://api.pandascore.co/'+ game +'/matches/running?',
            'https://api.pandascore.co/'+ game +'/matches/upcoming?',
            'https://api.pandascore.co/'+ game +'/matches/past?'
            ]
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(getRequest(session, url))
            tasks.append(task)
        tourneys = await asyncio.gather(*tasks)
        return tourneys

async def getDataAsyncStandings(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(getRequest(session, url))
            tasks.append(task)
        standings = await asyncio.gather(*tasks)
        return standings

async def getRequest(session, url):
    myToken = '&token=YMjgWp44V9BDfS4-F8T0zdkmDvjIQ63xQdUosX4Na0V-TPF5pZ0'
    async with session.get(url + myToken) as response:
        result_data = await response.json()
        return result_data
    
def getDotaData(request):
    dotaLiveTourneys = []
    dotaUpcomingTourneys = []
    dotaData = asyncio.run(getDataAsync('dota2'))
    dotaLiveTourneyDatas = dotaData[0]
    dotaUpcomingTourneyDatas = dotaData[1]
    dotaLiveTourneys = getTourneys(dotaLiveTourneys, dotaLiveTourneyDatas)
    dotaUpcomingTourneys = getTourneys(dotaUpcomingTourneys, dotaUpcomingTourneyDatas)
    urls = []
    for tourney in dotaLiveTourneys:
            urls.append('https://api.pandascore.co/tournaments/' + str(tourney.slug) +'/standings?')
    allTourneyStandings = asyncio.run(getDataAsyncStandings(urls))
    i = 0
    for tourneyStandings in allTourneyStandings:
        if len(tourneyStandings) > 1:
            for team in tourneyStandings:
                    standings = []
                    standings.append(team['team']['name'])
                    standings.append(team['rank'])
                    standings.append(team['team']['image_url'])
                    if 'wins' in team:
                        standings.append(team['wins'])
                        standings.append(team['losses'])
                        standings.append(team['total'])
                    dotaLiveTourneys[i].standings.append(standings)
        i+=1
    dotaPrevMatches = []
    dotaLives = []
    dotaUpcomings = []
    livesDatas = dotaData[2]
    upcomingDatas = dotaData[3]
    pastDatas = dotaData[4]

    dotaPrevMatches = getPreviousMatches(dotaPrevMatches, pastDatas)
    dotaLives = getLiveMatches(dotaLives, livesDatas)
    dotaUpcomings = getUpcomingMatches(dotaUpcomings, upcomingDatas)


    return render(request, 'home/dota2.html', {
        'dotaLiveMatchDatas': dotaLives,
        'dotaUpcomingMatchDatas': dotaUpcomings,
        'dotaLiveTourneyDatas': dotaLiveTourneys,
        'dotaUpcomingTourneyDatas': dotaUpcomingTourneys,
        'dotaPrevMatchDatas': dotaPrevMatches,
    })



def getLoLData(request):
    lolLiveTourneys = []
    lolUpcomingTourneys = []
    lolData = asyncio.run(getDataAsync('lol'))
    lolLiveTourneyDatas = lolData[0]
    lolUpcomingTourneyDatas = lolData[1]
    lolLiveTourneys = getTourneys(lolLiveTourneys, lolLiveTourneyDatas)
    lolUpcomingTourneys = getTourneys(lolUpcomingTourneys, lolUpcomingTourneyDatas)
    urls = []
    for tourney in lolLiveTourneys:
            urls.append('https://api.pandascore.co/tournaments/' + str(tourney.slug) +'/standings?')
    allTourneyStandings = asyncio.run(getDataAsyncStandings(urls))
    i = 0
    for tourneyStandings in allTourneyStandings:
        if len(tourneyStandings) > 1:
            for team in tourneyStandings:
                    standings = []
                    standings.append(team['team']['name'])
                    standings.append(team['rank'])
                    standings.append(team['team']['image_url'])
                    if 'wins' in team:
                        standings.append(team['wins'])
                        standings.append(team['losses'])
                        standings.append(team['total'])
                    lolLiveTourneys[i].standings.append(standings)
        i+=1
    lolPrevMatches = []
    lolLives = []
    lolUpcomings = []
    livesDatas = lolData[2]
    upcomingDatas = lolData[3]
    pastDatas = lolData[4]

    lolPrevMatches = getPreviousMatches(lolPrevMatches, pastDatas)
    lolLives = getLiveMatches(lolLives, livesDatas)
    lolUpcomings = getUpcomingMatches(lolUpcomings, upcomingDatas)


    return render(request, 'home/lol.html', {
        'lolLiveMatchDatas': lolLives,
        'lolUpcomingMatchDatas': lolUpcomings,
        'lolLiveTourneyDatas': lolLiveTourneys,
        'lolUpcomingTourneyDatas': lolUpcomingTourneys,
        'lolPrevMatchDatas': lolPrevMatches
    })



def getSiegeData(request):
    siegeLiveTourneys = []
    siegeUpcomingTourneys = []
    siegeData = asyncio.run(getDataAsync('r6siege'))
    siegeLiveTourneyDatas = siegeData[0]
    siegeUpcomingTourneyDatas = siegeData[1]
    siegeLiveTourneys = getTourneys(siegeLiveTourneys, siegeLiveTourneyDatas)
    siegeUpcomingTourneys = getTourneys(siegeUpcomingTourneys, siegeUpcomingTourneyDatas)
    urls = []
    for tourney in siegeLiveTourneys:
            urls.append('https://api.pandascore.co/tournaments/' + str(tourney.slug) +'/standings?')
    allTourneyStandings = asyncio.run(getDataAsyncStandings(urls))
    i = 0
    for tourneyStandings in allTourneyStandings:
        if len(tourneyStandings) > 1:
            for team in tourneyStandings:
                    standings = []
                    standings.append(team['team']['name'])
                    standings.append(team['rank'])
                    standings.append(team['team']['image_url'])
                    if 'wins' in team:
                        standings.append(team['wins'])
                        standings.append(team['losses'])
                        standings.append(team['total'])
                    siegeLiveTourneys[i].standings.append(standings)
        i+=1
    siegePrevMatches = []
    siegeLives = []
    siegeUpcomings = []
    livesDatas = siegeData[2]
    upcomingDatas = siegeData[3]
    pastDatas = siegeData[4]

    siegePrevMatches = getPreviousMatches(siegePrevMatches, pastDatas)
    siegeLives = getLiveMatches(siegeLives, livesDatas)
    siegeUpcomings = getUpcomingMatches(siegeUpcomings, upcomingDatas)


    return render(request, 'home/siege.html', {
        'siegeLiveMatchDatas': siegeLives,
        'siegeUpcomingMatchDatas': siegeUpcomings,
        'siegeLiveTourneyDatas': siegeLiveTourneys,
        'siegeUpcomingTourneyDatas': siegeUpcomingTourneys,
        'siegePrevMatchDatas': siegePrevMatches
    })


def getCsgoData(request):
    csgoLiveTourneys = []
    csgoUpcomingTourneys = []
    csgoData = asyncio.run(getDataAsync('csgo'))
    csgoLiveTourneyDatas = csgoData[0]
    csgoUpcomingTourneyDatas = csgoData[1]
    csgoLiveTourneys = getTourneys(csgoLiveTourneys, csgoLiveTourneyDatas)
    csgoUpcomingTourneys = getTourneys(csgoUpcomingTourneys, csgoUpcomingTourneyDatas)
    urls = []
    for tourney in csgoLiveTourneys:
            urls.append('https://api.pandascore.co/tournaments/' + str(tourney.slug) +'/standings?')
    allTourneyStandings = asyncio.run(getDataAsyncStandings(urls))
    i = 0
    for tourneyStandings in allTourneyStandings:
        if len(tourneyStandings) > 1:
            for team in tourneyStandings:
                    standings = []
                    standings.append(team['team']['name'])
                    standings.append(team['rank'])
                    standings.append(team['team']['image_url'])
                    if 'wins' in team:
                        standings.append(team['wins'])
                        standings.append(team['losses'])
                        standings.append(team['total'])
                    csgoLiveTourneys[i].standings.append(standings)
        i+=1
    csgoPrevMatches = []
    csgoLives = []
    csgoUpcomings = []
    livesDatas = csgoData[2]
    upcomingDatas = csgoData[3]
    pastDatas = csgoData[4]

    csgoPrevMatches = getPreviousMatches(csgoPrevMatches, pastDatas)
    csgoLives = getLiveMatches(csgoLives, livesDatas)
    csgoUpcomings = getUpcomingMatches(csgoUpcomings, upcomingDatas)


    return render(request, 'home/csgo.html', {
        'csgoLiveMatchDatas': csgoLives,
        'csgoUpcomingMatchDatas': csgoUpcomings,
        'csgoLiveTourneyDatas': csgoLiveTourneys,
        'csgoUpcomingTourneyDatas': csgoUpcomingTourneys,
        'csgoPrevMatchDatas': csgoPrevMatches
    })

def getValorantData(request):
    valorantLiveTourneys = []
    valorantUpcomingTourneys = []
    valorantData = asyncio.run(getDataAsync('valorant'))
    valorantLiveTourneyDatas = valorantData[0]
    valorantUpcomingTourneyDatas = valorantData[1]
    valorantLiveTourneys = getTourneys(valorantLiveTourneys, valorantLiveTourneyDatas)
    valorantUpcomingTourneys = getTourneys(valorantUpcomingTourneys, valorantUpcomingTourneyDatas)
    urls = []
    for tourney in valorantLiveTourneys:
            urls.append('https://api.pandascore.co/tournaments/' + str(tourney.slug) +'/standings?')
    allTourneyStandings = asyncio.run(getDataAsyncStandings(urls))
    i = 0
    for tourneyStandings in allTourneyStandings:
        if len(tourneyStandings) > 1:
            for team in tourneyStandings:
                    standings = []
                    standings.append(team['team']['name'])
                    standings.append(team['rank'])
                    standings.append(team['team']['image_url'])
                    if 'wins' in team:
                        standings.append(team['wins'])
                        standings.append(team['losses'])
                        standings.append(team['total'])
                    valorantLiveTourneys[i].standings.append(standings)
        i+=1
    valorantPrevMatches = []
    valorantLives = []
    valorantUpcomings = []
    livesDatas = valorantData[2]
    upcomingDatas = valorantData[3]
    pastDatas = valorantData[4]

    valorantPrevMatches = getPreviousMatches(valorantPrevMatches, pastDatas)
    valorantLives = getLiveMatches(valorantLives, livesDatas)
    valorantUpcomings = getUpcomingMatches(valorantUpcomings, upcomingDatas)


    return render(request, 'home/valorant.html', {
        'valorantLiveMatchDatas': valorantLives,
        'valorantUpcomingMatchDatas': valorantUpcomings,
        'valorantLiveTourneyDatas': valorantLiveTourneys,
        'valorantUpcomingTourneyDatas': valorantUpcomingTourneys,
        'valorantPrevMatchDatas': valorantPrevMatches
    })