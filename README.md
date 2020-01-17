# SportsSemantics
Sports Analytics with Semantic Analysis using Reddit

## Table of Contents
1. [Project Idea](README.md#project-idea)
1. [Tech Stack](README.md#tech-stack)
1. [Data Source](README.md#data-source)
1. [Engineering Challenge](README.md#engineering-challenge)
1. [Minimum Viable Product](README.md#minimum-viable-product)
1. [Stretch Goals](README.md#stretch-goals)

## Project idea
In the era of social media, an athlete or franchise's social media presence is an important element in developing and maintaining a successful career. With this project, an athlete/franchise or their agent(s) will be able to track the evolution of their sentiment in the post comments of various sports and news-related subreddits over a specified date range, or in response to/in advance of a particular event, like a game against a rival or the start of a season/tournament.

## Tech stack
The data will be stored in Amazon S3, loaded into Spark for parsing. Sentiment analysis will be conducted within Spark or using ElasticSearch, and the data will be visualized in Flask. 

## Data source
The primary data source is 300 GB of Reddit comments stored in JSON format, ranging from Dec. 2005 to Dec. 2017. Player/team data will be obtained from a variety of sources, e.g. Kaggle, but these files will be small and easy to store.

## Engineering challenge
Integration of specific events may be challenging, and an appropriate sentiment analysis library must be selected. More specific challenges are anticipated as the project development proceeds.

## Minimum viable product
The MVP will only consider teams and athletes from a particular sport, e.g. NBA, look at comments in particular subreddits, e.g. r/nba and r/news, and use limited dates, e.g. season schedules.

## Stretch goals
Drawing from additional data sets, e.g. Twitter or sports-specific forums; addition of other sports; allowing filtering of sentiment by location/region; inclusion of some form of streaming





