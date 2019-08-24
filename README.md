# NBAGrapher

NBA Grapher is a python script that can make plots and graphs of NBA comparing various statistical measures of NBA players and teams

NBA Grapher uses [sportsreference](https://github.com/roclark/sportsreference) for scraping data from [basketball-reference](http://basketball-reference.com) and creates plots using [matplotlib](https://matplotlib.org/)

Currently, four types of graphs are supported.

- Player stat by season
- Player stat by game
- Team stat by season
- Team stat by game

Details on each of these functions can be found in the full [documentation](https://nbagrapher.readthedocs.io/en/latest/)

A full list of avaiable statistics for each function can be found here.

---
### Installation
NBAGrapher can be installed from PyPi using PIP
```sh
$ pip install nbagrapher
```
----
### Examples

##### Season based

- VORP of two players throughout their career


```python
nbagrapher.plot_player_season(['iversal01','bryanko01'],"value_over_replacement_player")
```

![vorp](https://raw.githubusercontent.com/taoprajjwal/NBAGrapher/master/graphs/value_over_replacement_player.png)

- PER of the last five MVPs over the last five years

```python
nbagrapher.plot_player_season(['antetgi01','hardeja01','westbru01','curryst01','duranke01'],"player_efficiency_rating",start_year=2014,end_year=2019)
```
![per](https://raw.githubusercontent.com/taoprajjwal/NBAGrapher/master/graphs/player_efficiency_rating.png)

- Cumulative points of the five top points scorers over the last decade

```python
nbagrapher.plot_player_season(['jamesle01','duranke01','hardeja01','westbru01','curryst01'],"points",start_year=2010,cum=True)
```
![points](https://raw.githubusercontent.com/taoprajjwal/NBAGrapher/master/graphs/points.png)
##### Game based
- Win Shares for January 2019
```python
nbagrapher.plot_player_game(['embiijo01','antetgi01'],2019,"true_shooting_percentage",start_date=datetime.date(2019,1,1),end_date=datetime.date(2019,2,1))
```
![ts](https://raw.githubusercontent.com/taoprajjwal/NBAGrapher/master/graphs/true_shooting_percentage.png)
-----
License
----

MIT


