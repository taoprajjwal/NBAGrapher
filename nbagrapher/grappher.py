from sportsreference.nba.roster import Player
from sportsreference.nba.schedule import Schedule
from sportsreference.nba.boxscore import Boxscore
from sportsreference.nba.teams import Teams
import pandas as pd
import io
import os
import base64
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import MonthLocator
from matplotlib.dates import DateFormatter
import re
import datetime
import basketball_reference_scraper.players as bball_players
from nbagrapher import shot_scraper,custom_plots

save_dir = os.path.join(os.path.expanduser("~"), "NBA-Grapher")
if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

stat_type_str={
    "PER_GAME":"_Per Game",
    "PER_MINUTE": "_Per 36 Minutes",
    "PER_POSS":"_Per 100 Possessions",
    "ADVANCED": ""
}

radar_templates={
"splits":["AST","STL","PTS","FG%","BLK","TOV"],
"advanced":["PER","WS/48","VORP","TS%","BPM"],
"advanced_metrics":["3PAr","FTr","TRB%","AST%","STL%","BLK%","TOV%","USG%"]

}

templates_stat_type={

    "splits":"PER_GAME",
    "advanced":"ADVANCED",
    "advanced_rates":"ADVANCED"
}

ranges_dict={"PER_GAME":{"G":[6,78],"GS":[0,68],"MP":[7.0,31.63],"FG":[0.8,6.0],"FGA":[2.0,13.3],"FG%":[0.33299999999999996,0.5587],"3P":[0,2],"3PA":[0.1,5.4],"3P%":[0.125,0.41],"2P":[0.5,4.8],"2PA":[1.2,9.1],"2P%":[0.3922,0.607],"eFG%":[0.395,0.594],"FT":[0.2,2.8],"FTA":[0.3,3.6],"FT%":[0.5752,0.875],"ORB":[0.1,1.7],"DRB":[0.7,5.230000000000009],"TRB":[1.0,6.9300000000000095],"AST":[0.4,4.0],"STL":[0.17,1.2],"BLK":[0.0,0.8],"TOV":[2.0,0.3,],"PF":[2.7,0.6],"PTS":[2.0,16.63]},
             "PER_MINUTE":{"G":[6,78],"GS":[0,68],"MP":[46.4,2189.5],"FG":[3.2,8.03000000000001],"FGA":[8.3,17.2],"FG%":[0.33299999999999996,0.5587],"3P":[0.0,2.8],"3PA":[0.3,7.8],"3P%":[0.125,0.41],"2P":[1.5,6.8],"2PA":[3.47,12.73],"2P%":[0.3922,0.607],"FT":[0.6,4.1],"FTA":[0.9,5.5],"FT%":[0.5752,0.875],"ORB":[0.3,3.6300000000000097],"DRB":[2.5,8.4],"TRB":[3.1,12.0],"AST":[1.2,6.13000000000001],"STL":[0.4,1.8],"BLK":[0.0,1.6],"TOV":[3.1,0.9],"PF":[5.2,1.9],"PTS":[8.77,21.03]},
             "PER_POSS":{"G":[6,78],"GS":[0,68],"MP":[46.4,2189.5],"FG":[4.3,10.6],"FGA":[10.97,23.03],"FG%":[0.33299999999999996,0.5587],"3P":[0.0,3.7300000000000098],"3PA":[0.4,10.4],"3P%":[0.125,0.41],"2P":[1.97,9.0],"2PA":[4.6,16.9],"2P%":[0.3922,0.607],"FT":[0.77,5.4],"FTA":[1.2,7.4300000000000095],"FT%":[0.5752,0.875],"ORB":[0.47,4.83000000000001],"DRB":[3.3,11.1],"TRB":[4.2,15.8],"AST":[1.6,8.23000000000001],"STL":[0.6,2.4],"BLK":[0.0,2.1],"TOV":[1.2,4.1],"PF":[2.6,7.0],"PTS":[11.7,27.83],"ORtg":[91,122],"DRtg":[105.0,116.3]},
             "ADVANCED":{"G":[6,78],"MP":[46.4,2189.5],"PER":[5.8,20.5],"TS%":[0.4322,0.622],"3PAr":[0.0331,0.6467],"FTr":[0.0923,0.4256],"ORB%":[1.0,10.9],"DRB%":[7.57,25.23],"TRB%":[4.6,17.7],"AST%":[4.77,24.83],"STL%":[0.6,2.4],"BLK%":[0.0,3.7],"TOV%":[6.8,17.69],"USG%":[12.57,25.1],"OWS":[-0.2,3.2],"DWS":[0.0,2.5],"WS":[0.0,5.63000000000001],"WS/48":[-0.022000000000000002,0.17300000000000001],"OBPM":[-5.4,2.2],"DBPM":[-2.1,1.6],"BPM":[-6.4,2.5],"VORP":[-0.3,1.7]}
             }

def df_format(df,stats):
    if type(stats)!=list:
        stats=list(stats)
    df=df[~df['SEASON'].duplicated()]

    for stat in stats:
        df.loc[:,stat]=pd.to_numeric(df[stat],errors="coerce")
        df=df[df[stat].notnull()]

    return  df

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

def get_player_df(players,stat_type,stat,playoffs,player_labels):
    """
    Get dataframe from basketball_scraper
    :param players: list of player names
    :return:
    """
    if not player_labels:
        player_labels=players

    players_df=[]
    for player,player_label in zip(players,player_labels):
        player_df=bball_players.get_stats(player,stat_type,playoffs)
        player_df=df_format(player_df,stat)
        players_df.append((player_df,player_label))

    return players_df

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

def get_range(stats,players_df,season,stat_type):

    ranges=[]

    for stat in stats:
        ranges.append(ranges_dict[stat_type][stat])

    for df,player in players_df:
        df = df[df['SEASON'] == date_format(season)]
        df = df[[c for c in stats if c in df.columns]]
        for i,stat in enumerate(stats):
            if ranges[i][0]<ranges[i][1]: #range is noraml
                ranges[i][0]=min(ranges[i][0],df.iloc[0][stat])
                ranges[i][1]=max(ranges[i][1],df.iloc[0][stat])
            else:
                ranges[i][0] = max(ranges[i][0], df.iloc[0][stat])
                ranges[i][1] = min(ranges[i][1], df.iloc[0][stat])
    return ranges

def return_plot(stat, fig, ax, return_type):
    if return_type == "fig":
        return (fig, ax)
    elif return_type == "show":
        plt.show()
    elif return_type == "img":
        plt.savefig(os.path.join(save_dir, stat + ".png"))
    elif return_type == "html":
        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        return 'data:image/png;base64,{}'.format(graph_url)

def plot_player_season(players, stat, start_year=0, end_year=3000, xlabel="Year", ylabel=None, scatter=True,
                       return_type="img", cum=False):
    """
    Uses sportsreference

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
    Uses Sportsreference
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
    Uses Sportsreference
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
    Uses Sportsreference

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

def player_season(players,stat,stat_type="PER_GAME",players_label=None,playoffs=False,start_year=0, end_year=3000, xlabel="Year", ylabel=None, scatter=True,
                       return_type="img", cum=False):
    """
    Uses Basketball_reference_scraper

    Plots the graphs for seasons of a player or a list of players by seasons. Can specify whether to use the regular season only or regular season+playoffs

    :param players: Basketball-reference id of a player or list of players
    :type players: String or list of strings
    :param stat: Statisitc to use
    :type stat: String
    :param stat_type: Type of statistic. PER_GAME by default
    :type stat_type: "PER_GAME", "PER_MINUTE","PER_POSS","ADVANCED"    :param stat:
    :param start_year: Starting year from which to plot
    :type start_year: Integer
    :param end_year: Ending year until which to plot
    :type end_year:Integer
    :param xlabel:The label on the x-axis on the returned plot
    :type xlabel: String
    :param ylabel:The label on the x-axis on the returned plot
    :type ylabel:String
    :param scatter:Whether on not to include a dot for each data point in the graph
    :type scatter:Boolean
    :param return_type:Various methods by which the graph can be returned
    :type return_type:"img": png image, "fig":Matplotlib figure and axes,"show": calls the matplotlib show function (appropriate for jupyter notebooks), "html": base64 image useful for rendering in html pages)
    :param cum:Whether results are cumulative or not
    :type cum:Boolean
    """
    if type(players) is not list:
        players=[players]

    players_df=get_player_df(players,stat_type,stat,playoffs,players_label)

    fig,ax=plt.subplots()
    for player,player_name in players_df:
        x=[]
        y=[]
        for index,row in player.iterrows():
            if start_year<=int(date_format(row.SEASON,format_as="single"))<=end_year:
                x.append(int(date_format(row.SEASON,format_as="single")))
                if cum:
                    try:
                        prev=y[-1]
                    except:
                        prev=0
                    y.append(row[stat]+prev)
                else:
                    y.append(row[stat])

        ax.grid()
        ax.plot(x,y,label=player_name)
        if scatter:
            ax.scatter(x,y)
        ax.legend()

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel(xlabel)
    if ylabel==None:
        ylabel=stat+stat_type_str[stat_type]
    ax.set_ylabel(ylabel)


    return return_plot(stat,fig,ax,return_type)

def player_shot_chart_season(player,season,playoffs=False,fig_type='scatter',hex_C="makes",hex_binsize=(30,30),hex_minshots=10,return_type="img",figsize=(5,4)):
    """
    Uses basketball_reference_scraper
    Create a shot chart for a player from a particular season

    :param player: Basketball-reference id of a player
    :type player: String
    :param season: Season to get the shots from
    :type season: Integer
    :param playoffs: Wheter or not to include the playoffs
    :type playoffs: Boolean
    :param fig_type: Scatter plots every shot event as point. Hex creates bins of a certain size and counts the shots inside the point.
    :type fig_type: "scatter","hex"
    :param hex_C: The statistic that gives magnitude to the hexbins. Makes and misses simply count makes and misses in each hexbin. fg% is the field goal percentage in each bin. fg%_adj is similar to TS%, it accounts for 3 pointers being more valuable than 2 pointers
    :type hex_C: "makes","miss","fg%","fg%_adj"
    :param hex_binsize: Number of hexbins in x and y directions. A greater value of hexbins means that each bins becomes smaller
    :type hex_binsize: Tuple, (Integer,Integer)
    :param hex_minshots: Minimum shots needed to count a hexbin. Prevents bins with a small shot sample from diluting the data. Default is 10
    :type hex_minshots: Integer
    :param figsize: Size of the matplotlib figure
    :type figsize: Tuple containing size in inches
    :param return_type: Various methods by which the graph can be returned
    :type return_type: "img": png image, "fig":Matplotlib figure and axes,"show": calls the matplotlib show function (appropriate for jupyter notebooks), "html": base64 image useful for rendering in html pages
    """
    fig,ax=custom_plots.prepare_shot_chart(figsize)
    shots_df=shot_scraper.scrape_season_shot(player,season,playoffs,)
    if fig_type=="scatter":
        for index,row in shots_df.iterrows():
            if row['Shot Made']:
                ax.scatter(row['X-Coordinate'], row['Y-Coordinate'], color='green')
            else:
                ax.scatter(row['X-Coordinate'], row['Y-Coordinate'], color='red')
        return return_plot("{}-{}-Shot-Chart".format(player,season),fig,ax,return_type)

    elif fig_type=="hex":
        if hex_C=="makes":
            shots_df=shots_df[shots_df['Shot Made']]
            x=ax.hexbin(shots_df['X-Coordinate'], shots_df['Y-Coordinate'], gridsize=hex_binsize, cmap='OrRd', bins='log',
                      extent=(-300, 300, 0, 940),mincnt=hex_minshots)
        elif hex_C=="miss":
            shots_df=shots_df[~shots_df['Shot Made']]
            x=ax.hexbin(shots_df['X-Coordinate'], shots_df['Y-Coordinate'], gridsize=hex_binsize, cmap='OrRd', bins='log',
                      extent=(-300, 300, 0, 940),mincnt=hex_minshots)
        elif hex_C=="fg%":
            x=ax.hexbin(shots_df['X-Coordinate'], shots_df['Y-Coordinate'],C=shots_df['Shot Value'], gridsize=hex_binsize, cmap='OrRd',
                      extent=(-300, 300, 0, 940),mincnt=hex_minshots)

        elif hex_C=="fg%_adj":
            x = ax.hexbin(shots_df['X-Coordinate'], shots_df['Y-Coordinate'], C=shots_df['Shot Value Adj'],
                          gridsize=hex_binsize, cmap='OrRd',extent=(-300, 300, 0, 940),mincnt=hex_minshots)

        else:
            x = ax.hexbin(shots_df['X-Coordinate'], shots_df['Y-Coordinate'], gridsize=hex_binsize, cmap='OrRd',
                          bins='log',
                          extent=(-300, 300, 0, 940), mincnt=hex_minshots)
        fig.colorbar(x,ax=ax)
        return return_plot("{}-{}-Shot-Chart".format(player,season),fig,ax,return_type)

def player_season_radar(players,season,player_labels=None,template="splits",playoffs=False,stat_type=None,stats=None,range=None,figsize=(8,6),return_type="img"):
    """
    Create a radar chart for a season of one or multiple players. You can customize the stats to include in the radar chart.

    :param players: Basketball-reference id of a player
    :type players: String or list of strings
    :param season: Season to gets stat from
    :type season: Integer
    :param player_labels: Player labels to show in the legend, None to use Basketball-reference id
    :type player_labels: List of strings
    :param template: Pre-defined statistics chosen on the based of templates.
    :type template: "splits","advanced","advanced_metrics"
    :param playoffs: Include the playoffs or not
    :type playoffs: Boolean
    :param stat_type: Type of statistic. "PER_GAME" by default
    :type stat_type: "PER_GAME", "PER_MINUTE","PER_POSS","ADVANCED"
    :param stats: If the stats you need are not defined by a template, you can use stats to get a new radar chart
    :type stats: List of strings
    :param range: Range on the radar chart. By default, the lower range is the 10th percentile and upper range is 90th percentile of the stat in the 2019 NBA Season
    :type range: List of integers, eg [(0,10),(5,20)...]
    :param figsize: Size of the matplotlib figure
    :type figsize: Tuple containing size in inches
    :param return_type: Various methods by which the graph can be returned
    :type return_type:"img": png image, "fig":Matplotlib figure and axes,"show": calls the matplotlib show function (appropriate for jupyter notebooks), "html": base64 image useful for rendering in html pages
    """
    if type(players) is not list:
        players=[players]

    if not stats:
        stats=radar_templates[template]

    if not stat_type:
        stat_type=templates_stat_type[template]
    players_df=get_player_df(players,stat_type,stats,playoffs,player_labels)
    if not range:
        range = get_range(stats, players_df, season, stat_type)

    fig=plt.figure(figsize=figsize)
    ax = custom_plots.ComplexRadar(fig, variables=stats, ranges=range, n_ordinate_levels=5)
    for player_df,player in players_df:
        player_df=player_df[player_df['SEASON']==date_format(season)]
        player_df=player_df[[c for c in stats if c in player_df.columns]]
        ax.plot(list(player_df.iloc[0]),label=player)
        ax.fill(list(player_df.iloc[0]),alpha=0.2)

    return return_plot("radarplot",fig,ax,return_type)