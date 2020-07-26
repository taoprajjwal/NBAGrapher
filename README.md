# NBAGrapher
[![Documentation Status](https://readthedocs.org/projects/nbagrapher/badge/?version=latest)](https://nbagrapher.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/NBAGrapher.svg)](https://badge.fury.io/py/NBAGrapher)
[![Downloads](https://pepy.tech/badge/nbagrapher)](https://pepy.tech/project/nbagrapher)

![logo](https://taoprajjwal.com/wp-content/uploads/2020/07/d4c017ac-6d49-40e4-bc56-c88c8f541152_200x200.png)

NBA Grapher is a python script that can make plots and graphs of NBA comparing various statistical measures of NBA players and teams

NBA Grapher uses either [sportsreference](https://github.com/roclark/sportsreference) or [basketball_reference_scraper](https://github.com/vishaalagartha/basketball_reference_scraper) for scraping data from [basketball-reference](http://basketball-reference.com) and creates plots using [matplotlib](https://matplotlib.org/)

Currently, scatter plot, shot charts and radial plots are supported. See [Examples](Examples.md) for more details

Details on the functions can be found in the full [documentation](https://nbagrapher.readthedocs.io/en/latest/)

A full list of avaiable statistics for each function can be found [here](https://nbagrapher.readthedocs.io/en/latest/#list-of-available-stats).

---
### Installation
NBAGrapher can be installed from PyPi using PIP. The basketball_reference_scraper dependency is slightly modified from the original, so we will need to install it as well.
```sh
$ pip install nbagrapher
$ pip install git+git://github.com/taoprajjwal/basketball_reference_scraper@master
```
----
License
----

MIT


