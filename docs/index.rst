.. NBAGrapher documentation master file, created by
   sphinx-quickstart on Wed Aug 21 23:35:03 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NBAGrapher's documentation!
======================================
NBA Grapher is a small utility tool that automates the process of scraping data from basketball-reference and uses matplotlib to create frequenty used graphs.

Graphing Functions
======================================
For the stats supported by each function see :ref:`List of available stats`

.. automodule:: nbagrapher.grappher
   :members: plot_player_season, plot_player_game,plot_team_season,plot_team_game

List of available stats
=======================
Each of the function has a varying degree of statistical measurements available to it. Some measures that are available on the per-season basis are applicable on game-to-game basic. This document outlines the possible stats by each of the function. Each of the following stats should be provided to the function as a string.

plot_player_season()
--------------------
All attributes available from the `sportsreference.NBA.Player <https://sportsreference.readthedocs.io/en/stable/nba.html#sportsreference.nba.roster.Player>`_ and `sportsreference.NBA.AbstractPlayer <https://sportsreference.readthedocs.io/en/stable/nba.html#sportsreference.nba.player.AbstractPlayer>`_. Details can be found in these pages.

- and_ones
- assist_percentage
- assists
- block_percentage
- blocking_fouls
- blocks
- box_plus_minus
- center_percentage
- defensive_box_plus_minus
- defensive_rebound_percentage
- defensive_rebounds
- defensive_win_shares
- dunks
- effective_field_goal_percentage
- field_goal_attempts
- field_goal_perc_sixteen_foot_plus_two_pointers
- field_goal_perc_ten_to_sixteen_feet
- field_goal_perc_three_to_ten_feet
- field_goal_perc_zero_to_three_feet
- field_goal_percentage
- field_goals
- free_throw_attempt_rate
- free_throw_attempts
- free_throw_percentage
- free_throws
- games_played
- games_started
- half_court_heaves
- half_court_heaves_made
- height
- lost_ball_turnovers
- minutes_played
- nationality
- net_plus_minus
- offensive_box_plus_minus
- offensive_fouls
- offensive_rebound_percentage
- offensive_rebounds
- offensive_win_shares
- on_court_plus_minus
- other_turnovers
- passing_turnovers
- percentage_field_goals_as_dunks
- percentage_of_three_pointers_from_corner
- percentage_shots_three_pointers
- percentage_shots_two_pointers
- percentage_sixteen_foot_plus_two_pointers
- percentage_ten_to_sixteen_footers
- percentage_three_to_ten_footers
- percentage_zero_to_three_footers
- personal_fouls
- player_efficiency_rating
- player_id
- point_guard_percentage
- points
- points_generated_by_assists
- position
- power_forward_percentage
- salary
- shooting_distance
- shooting_fouls
- shooting_fouls_drawn
- shooting_guard_percentage
- shots_blocked
- small_forward_percentage
- steal_percentage
- steals
- take_fouls
- team_abbreviation
- three_point_attempt_rate
- three_point_attempts
- three_point_percentage
- three_point_shot_percentage_from_corner
- three_pointers
- three_pointers_assisted_percentage
- total_rebound_percentage
- total_rebounds
- true_shooting_percentage
- turnover_percentage
- turnovers
- two_point_attempts
- two_point_percentage
- two_pointers
- two_pointers_assisted_percentage
- usage_percentage
- value_over_replacement_player
- weight
- win_shares
- win_shares_per_48_minutes

plot_player_game()
--------------------
All attributes available from the `sportsreference.NBA.AbstractPlayer <https://sportsreference.readthedocs.io/en/stable/nba.html#sportsreference.nba.player.AbstractPlayer>`_ and `sportsreference.NBA.BoxScorePlayer <https://sportsreference.readthedocs.io/en/stable/nba.html#sportsreference.nba.boxscore.BoxscorePlayer>`_

- assist_percentage
- assists
- block_percentage
- blocks
- box_plus_minus
- defensive_rating
- defensive_rebound_percentage
- defensive_rebounds
- effective_field_goal_percentage
- field_goal_attempts
- field_goal_percentage
- field_goals
- free_throw_attempt_rate
- free_throw_attempts
- free_throw_percentage
- free_throws
- minutes_played
- offensive_rating
- offensive_rebound_percentage
- offensive_rebounds
- personal_fouls
- points
- steal_percentage
- steals
- three_point_attempt_rate
- three_point_attempts
- three_point_percentage
- three_pointers
- total_rebound_percentage
- total_rebounds
- true_shooting_percentage
- turnover_percentage
- turnovers
- two_point_attempts
- two_point_percentage
- two_pointers
- usage_percentage

plot_team_season()
-------------------
All attributes from `sportsreference.NBA.teams.Teams <https://sportsreference.readthedocs.io/en/stable/nba.html#sportsreference.nba.teams.Team>`_. The attributes starting with "opp" refer to the value of the stat but for the opposing team. While these attributes can be used as well, if opposition stat is required it is recommend to use the opp=True parameter in the function.

- abbreviation
- assists
- blocks
- defensive_rebounds
- field_goal_attempts
- field_goal_percentage
- field_goals
- free_throw_attempts
- free_throw_percentage
- free_throws
- games_played
- minutes_played
- name
- offensive_rebounds
- personal_fouls
- points
- rank
- steals
- three_point_field_goal_attempts
- three_point_field_goal_percentage
- three_point_field_goals
- total_rebounds
- turnovers
- two_point_field_goal_attempts
- two_point_field_goal_percentage
- two_point_field_goals

plot_team_game()
----------------

- assist_percentage
- assists
- block_percentage
- blocks
- defensive_rating
- defensive_rebound_percentage
- defensive_rebounds
- effective_field_goal_percentage
- field_goal_attempts
- field_goal_percentage
- field_goals
- free_throw_attempt_rate
- free_throw_attempts
- free_throw_percentage
- free_throws
- losses
- minutes_played
- offensive_rating
- offensive_rebound_percentage
- offensive_rebounds
- personal_fouls
- points
- steal_percentage
- steals
- three_point_attempt_rate
- three_point_field_goal_attempts
- three_point_field_goal_percentage
- three_point_field_goals
- total_rebound_percentage
- total_rebounds
- true_shooting_percentage
- turnover_percentage
- turnovers
- two_point_field_goal_attempts
- two_point_field_goal_percentage
- two_point_field_goals
- wins

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
