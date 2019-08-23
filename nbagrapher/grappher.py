from sportsreference.nba.roster import Player
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.boxscore import Boxscore
from sportsreference.nba.teams import Teams
import pandas as pd
import io
from os import path
import base64
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import MonthLocator
from matplotlib.dates import DateFormatter
import re
import datetime

save_dir = path.join(path.expanduser("~"), "NBA-Grapher")


def date_format(date, format_as="dash"):
    """
    Util function for formatting season dates as required  by the sportsreference module. Dashed format for a season is the regular way its written, eg "2018-19". Single format only contains the second year of the NBA Season, i.e for the 2018-19 season the single date format is simply 2019
    :param date: Date to be formatted
    :type date: String or Integer
    :param format_as:
    :type: format_as: "dash" or "single"
    """

    if format_as== "dash":
        if re.match("^\d{4}-\d\d", str(date)):
            return date
        else:
            second_year = str(date)[-2:]
            return str(int(date) - 1) + "-" + str(second_year)
    elif format_as == "single":
        if re.match("^\d{4}-\d\d", str(date)):
            return str(int(date[:4]) + 1)
        else:
            return date


def get_player_obj(players):
    """
    Gets a list of bball-reference player ids and returns a sportsreference player object
    :param players: A list of player ids in string format
    :return: A list of sportsreference player objects
    """
    player_obj = []
    for player in players:
        player_obj.append(Player(player))
    return player_obj


def return_plot(stat, fig, ax, return_type):
    if return_type == "fig":
        return (fig, ax)
    elif return_type == "show":
        plt.show()
    elif return_type == "img":
        plt.savefig(path.join(save_dir, stat + ".png"))
    elif return_type == "html":
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        return 'data:image/png;base64,{}'.format(graph_url)


def plot_player_season(players, stat, start_year=0, end_year=3000, xlabel="Year", ylabel=None, scatter=True,
                       return_type="img", cum=False):
    """
    Plots the graphs for seasons of a player or a list of players by seasons. Stats are from the regular season collected at the end of the season.

    :param players: Basketball-reference id of a player
    :type players: String or list of strings
    :param stat: The statistical attribute of the player to plot
    :type stat: String
    :param start_year: Starting year from which to plot
    :type start_year: Integer
    :param end_year: Ending year until which to plot
    :type end_year: Integer
    :param xlabel: The label on the x-axis on the returned plot
    :type xlabel: String
    :param ylabel: The label on the x-axis on the returned plot
    :type ylabel: String
    :param scatter: Whether on not to include a dot for each data point in the graph
    :type scatter: Bool
    :param return_type: Various methods by which the graph can be returned
    :type return_type: "img": png image, "fig":Matplotlib figure and axes,"show": calls the matplotlib show function (appropriate for jupyter notebooks), "html": base64 image useful for rendering in html pages
    :param cum: Whether results are cumulative or not
    :type cum: Bool

    """

    if type(players) is not list:
        players = [players]
    player_obj = get_player_obj(players)

    fig, ax = plt.subplots()
    for player in player_obj:
        x = []
        y = []
        for index, row in player.dataframe.iterrows():
            if not index[0] == "Career" and not pd.isnull(row[stat]):
                if start_year <= int(date_format(index[0], format_as="single")) <= end_year:
                    x.append(int(date_format(index[0], format_as="single")))
                    if cum:
                        try:
                            prev = y[-1]
                        except:
                            prev = 0
                        y.append(row[stat] + prev)
                    else:
                        y.append(row[stat])

        ax.grid()
        ax.plot(x, y, label=player.name)
        if scatter:
            ax.scatter(x, y)
        ax.legend()

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.set_xlabel(xlabel)
    if ylabel == None:
        ylabel = stat
    ax.set_ylabel(ylabel)

    return return_plot(stat, fig, ax, return_type)


def plot_player_game(players, season, stat, start_date=datetime.date(1900, 1, 1), end_date=datetime.date(3000, 1, 1),
                     only_month=False, xlabel="Time", ylabel=None, scatter=True, return_type="img", cum=False):
    """
    Plots the graphs of players according to their performance in particular games.

    :param players: Basketball-reference id of a player or list of players
    :type players: String or list of strings
    :param season: The season in which the games are played
    :type season: Either in dashed form (2018-19) or single form (2019 means the season 2018-19)
    :param stat: The statistical attribute of the player to plot
    :type stat: String
    :param start_date: The date from which the data is plotted
    :type start_date: datetime.date format
    :param end_date: The date untill which data is plotted
    :type end_date: datetime.date format
    :param only_month: Wheter or not the ticks on the x-axis only contain months. (Recommended when plotting dates extending across dates more than a couple of months)
    :type only_month: Bool
    :param xlabel: The label on the x-axis on the returned plot
    :type xlabel: String
    :param ylabel: The label on the x-axis on the returned plot
    :type ylabel: String
    :param scatter: Wheter on not to include a dot for each data point in the graph
    :type scatter: Bool
    :param return_type: Various methods by which the graph can be returned
    :type return_type: "img": png image, "fig":Matplotlib figure and axes,"show": calls the matplotlib show function (appropriate for jupyter notebooks), "html": base64 image useful for rendering in html pages
    :param cum: Wheter results are cumulative or not
    :type cum: Bool

    """
    if type(players) is not list:
        players = [players]

    player_obj = get_player_obj(players)

    fig, ax = plt.subplots()
    for player in player_obj:
        season = date_format(season)
        team = player(season).team_abbreviation
        sch = Schedule(team, date_format(season, format_as="single"))
        sch_df = sch.dataframe
        x = []
        y = []
        for index, row in sch_df.iterrows():
            if start_date <= row['datetime'].date() <= end_date:
                box = Boxscore(index)
                if row['location'] == "Home":
                    for boxplay in box.home_players:
                        if boxplay.player_id == player.player_id:
                            x.append(row['datetime'].date())
                            if cum:
                                try:
                                    prev = y[-1]
                                except:
                                    prev = 0
                                y.append(boxplay.dataframe[stat] + prev)
                            else:
                                y.append(boxplay.dataframe[stat])
                elif row['location'] == "Away":
                    for boxplay in box.away_players:
                        if boxplay.player_id == player.player_id:
                            x.append(row['datetime'].date())
                            if cum:
                                try:
                                    prev = y[-1]
                                except:
                                    prev = 0
                                y.append(boxplay.dataframe[stat] + prev)
                            else:
                                y.append(boxplay.dataframe[stat])
        ax.plot(x, y, label=player.name)
        if scatter:
            ax.scatter(x, y)
        ax.legend()
        if only_month:
            ax.xaxis.set_major_locator(MonthLocator())
            ax.xaxis.set_major_formatter(DateFormatter("%y-%m"))

    fig.autofmt_xdate()

    ax.set_xlabel(xlabel)
    if ylabel == None:
        ylabel = stat
    ax.set_ylabel(ylabel)

    return return_plot(stat, fig, ax, return_type)


def plot_team_season(teams, stat, start_season, end_season, opp=False, xlabel="Year", ylabel=None, scatter=True,
                     return_type='img', cum=False):
    """
     Plots the graph of a team or a list of teams by seasons. Stats are from the regular season collected at the end of the season.
    :param teams: Basketball-reference id for team
    :type teams: String or list of strings
    :param stat: The statistical attribute of the player to plot
    :type stat: String
    :param start_season: Starting season from which to plot
    :type start_season: Integer
    :param end_season: Last season until which to plot
    :type end_season: Integer
    :param opp: Whether the stat is for the opponent
    :type opp: Bool
    :param xlabel: The label on the x-axis on the returned plot
    :type xlabel: String
    :param ylabel: The label on the y-axis on the returned plot
    :type ylabel: String
    :param scatter: Whether on not to include a dot for each data point in the graph
    :type scatter: Bool
    :param return_type: Various methods by which the graph can be returned
    :type return_type: "img": png image, "fig":Matplotlib figure and axes,"show": calls the matplotlib show function (appropriate for jupyter notebooks), "html": base64 image useful for rendering in html pages
    :param cum: Whether results are cumulative or not
    :type cum: Bool
    """
    if type(teams) is not list:
        teams = [teams]
    fig, ax = plt.subplots()
    tm_dict = {}
    if opp:
        stat = "opp_" + stat

    for year in range(start_season, end_season):
        tm = Teams(year)
        tm_dict[year] = tm

    for team in teams:
        x = []
        y = []
        for year in range(start_season, end_season):
            tm = tm_dict[year]
            x.append(year)
            if cum:
                try:
                    prev = y[-1]
                except:
                    prev = 0
                y.append(tm.dataframes.loc[team][stat] + prev)
            else:
                y.append(tm.dataframes.loc[team][stat])
        ax.plot(x, y, label=team)
        if scatter:
            ax.scatter(x, y)
        ax.legend()

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(xlabel)
    if ylabel == None:
        ylabel = stat
    ax.set_ylabel(ylabel)

    return return_plot(stat, fig, ax, return_type)


def plot_team_game(teams, stat, season, start_date, end_date, opp=False, xlabel="Time", ylabel=None, only_month=False,
                    scatter=True, return_type="img", cum=False):

    """
    :param teams: Basketball-reference id for team
    :type teams: String or list of strings
    :param stat: The statistical attribute of the player to plot
    :type stat: String
    :param season: The season in which the games are played
    :type season: Either in dashed form (2018-19) or single form (2019 means the season 2018-19)
    :param start_date: The date from which the data is plotted
    :type start_date: datetime.date format
    :param end_date: The date untill which data is plotted
    :type end_date: datetime.date format
    :param opp: Whether the stat is for the opponent
    :type opp: Bool
    :param xlabel: The label on the x-axis on the returned plot
    :type xlabel: String
    :param ylabel: The label on the Y-axis on the returned plot
    :type ylabel: String
    :param scatter: Whether on not to include a dot for each data point in the graph
    :type scatter: Bool
    :param return_type: Various methods by which the graph can be returned
    :type return_type: "img": png image, "fig":Matplotlib figure and axes,"show": calls the matplotlib show function (appropriate for jupyter notebooks), "html": base64 image useful for rendering in html pages
    :param cum: Whether results are cumulative or not
    :type cum: Bool
    """
    fig, ax = plt.subplots()
    if type(teams) is not list:
        teams = [teams]
    for team in teams:
        x = []
        y = []
        sch = Schedule(team, season)
        for index, row in sch.dataframe.iterrows():
            if start_date <= row['datetime'].date() <= end_date:
                box = Boxscore(index)
                stat_prefix = ""
                stat_prefix_reversal = {"home_": "away_", "away_": "home_"}

                if row['location'] == "Home":
                    stat_prefix = "home_"
                elif row['location'] == "Away":
                    stat_prefix = "away_"

                if opp:
                    stat_prefix = stat_prefix_reversal[stat_prefix]

                x.append(row['datetime'].date())
                if cum:
                    try:
                        prev = y[-1]
                    except:
                        prev = 0

                    y.append(int(box.dataframe[stat_prefix + stat]) + prev)

                else:
                    y.append(int(box.dataframe[stat_prefix + stat]))

        ax.plot(x, y, label=team)
        if scatter:
            ax.scatter(x, y)
        ax.legend()
        if only_month:
            ax.xaxis.set_major_locator(MonthLocator())
            ax.xaxis.set_major_formatter(DateFormatter("%y-%m"))

    fig.autofmt_xdate()
    ax.set_xlabel(xlabel)
    if ylabel == None:
        if opp:
            ax.set_ylabel("opp_" + stat)
        else:
            ax.set_ylabel(stat)

    return return_plot(stat, fig, ax, return_type)
