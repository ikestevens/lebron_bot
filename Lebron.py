'''
Bron Bron Bot Bot
@author Isaac Stevens
'''

import tweepy
import math
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

class Bron():
    def __init__(self):
        # points section
        self.kareem = 38387
        self.karl = 36928
        self.lebron = self.get_lebron_total_points()

        # lebron points average
        self.today = datetime.datetime.today()
        if self.today.month >= 7:
            self.nba_year = self.today.year + 1
        else:
            self.nba_year = self.today.year
        self.source = requests.get('https://www.basketball-reference.com/players/j/jamesle01/gamelog/' + str(self.nba_year)).text
        self.soup = BeautifulSoup(self.source, 'lxml')
        self.table = self.soup.find('tbody')
        if len(self.table.findAll('tr')) < 10:
            self.recent_games = self.table.findAll('tr')
        else:
            self.recent_games = self.table.findAll('tr')[-10:]

        self.get_lebron_avg_points()
        self.games_to_pass()

        # lakers schedule
        self.lakers_full_schedule_df = self.get_lakers_schedule()
        self.lakers_schedule_df = self.lakers_full_schedule_df[self.lakers_full_schedule_df['already_happened']==False]
        self.games_left_this_season = len(self.lakers_schedule_df)

        #calulate games projected date
        self.projected_kareem_pass_date, self.projected_kareem_opponent, self.projected_kareem_home = self.calculate_game_pass(self.games_to_pass_kareem)
        self.projected_karl_pass_date, self.projected_karl_opponent, self.projected_karl_home = self.calculate_game_pass(self.games_to_pass_karl)


    def get_lebron_total_points(self):
        source = requests.get('https://www.basketball-reference.com/leaders/pts_career.html').text
        soup = BeautifulSoup(source, 'lxml')
        table = soup.find('table', class_="suppress_glossary suppress_csv sortable stats_table")
        for player in table.findAll('tr')[:5]:
            if 'lebron james' in str(player).lower():
                lebron_points = int(player.findAll('td')[2].contents[0])
        return lebron_points

    def get_lebron_avg_points(self):
        self.game_points = []
        for game in self.recent_games:
            self.game_points.append(int(game.find(attrs={"data-stat": "pts"}).contents[0]))
        self.points_avg = round(sum(self.game_points) / len(self.game_points), 2)

    def games_to_pass(self):
        self.kareem_diff = self.kareem - self.lebron
        self.karl_diff = self.karl - self.lebron
        self.games_to_pass_kareem = int(math.ceil(self.kareem_diff/self.points_avg))
        self.games_to_pass_karl = int(math.ceil(self.karl_diff/self.points_avg))

    def get_lakers_schedule(self):
        schedule = {
        "game_num": [],
        "full_date_string": [],
        "day_of_week": [],
        "date": [],
        "already_happened": [],
        "opponent": [],
        "at_home": [],
        }
        source = requests.get('https://www.basketball-reference.com/teams/LAL/' + str(self.nba_year) + '_games.html').text
        soup = BeautifulSoup(source, 'lxml')
        table = soup.find('table', id="games")
        count = 0
        for game in table.findAll('tr'):
            if game.findAll('td'):
                schedule['game_num'].append(count)
                date_string = game.findAll('td')[0].contents[0].contents[0]
                schedule['full_date_string'].append(date_string)
                schedule['day_of_week'].append(date_string.split(",")[0])
                schedule['date'].append((date_string.split(",")[1] + "," + date_string.split(",")[2]).lstrip())
                no_comma_date_string = (date_string.split(",")[1] + date_string.split(",")[2]).lstrip()
                date_object = datetime.datetime.strptime(no_comma_date_string, '%b %d %Y')
                if self.today >= date_object:
                    schedule['already_happened'].append(True)
                else:
                    schedule['already_happened'].append(False)
                schedule['opponent'].append(game.findAll('td')[5].contents[0].contents[0])
                if len(game.findAll('td')[4].contents) == 0:
                    schedule['at_home'].append(True)
                else:
                    schedule['at_home'].append(False)
                count += 1
        return pd.DataFrame(schedule)

    def calculate_game_pass(self, games_needed_to_pass):
        if games_needed_to_pass > self.games_left_this_season:
            years_away = 1
            games_into_next_season = games_needed_to_pass - self.games_left_this_season
            while games_into_next_season > 82:
                games_into_next_season = games_into_next_season - 82
                years_away += 1
            year_digit = int(self.lakers_full_schedule_df.iloc[games_into_next_season]['date'][-1])
            new_year = year_digit + int(years_away)
            projected_date = self.lakers_full_schedule_df.iloc[games_into_next_season]['date'][:-1] + str(new_year)
            opponent = None
            home = None
        else:
            projected_date = self.lakers_schedule_df.iloc[games_needed_to_pass]['date']
            opponent = self.lakers_schedule_df.iloc[games_needed_to_pass]['opponent']
            home = self.lakers_schedule_df.iloc[games_needed_to_pass]['at_home']
        return projected_date, opponent, home

if __name__ == "__main__":
    bron = Bron()

    print("Lebron is averaging " + str(bron.points_avg) + " points over the last 10 games. With this pace, he'll pass Kareem in " + str(bron.games_to_pass_kareem) + " games on around " + bron.projected_kareem_pass_date + ". He's " + str(bron.kareem_diff) + " points behind Kareem.")

    print('\n')

    print("Lebron is averaging " + str(bron.points_avg) + " points over the last 10 games. With this pace, he'll pass Karl Malone in " + str(bron.games_to_pass_karl) + " games on around " + bron.projected_karl_pass_date + ". He's " + str(bron.karl_diff) + " points behind Karl.")
