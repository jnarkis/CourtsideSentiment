# Courtside Sentiment
A front-row seat to the opinions of Reddit!

## Table of Contents
1. [Project Idea](README.md#project-idea)
1. [Tech Stack](README.md#tech-stack)
1. [Engineering Challenge](README.md#engineering-challenge)
1. [Minimum Viable Product](README.md#minimum-viable-product)
1. [Stretch Goals](README.md#stretch-goals)

## Project idea
Courtside Sentiment is a web application designed for the PR representative of a particular person of people, that allows them to investigate how the perception of their client changes over time according to Reddit comments.  If a client is interested in selling a new product, the release date can have a significant impact on overall sales. 

Much of the decision-making process can be done by looking at previous sales data of similar products.  For example, an NBA player will probably sell more jerseys and other products for die-hard fans around the start of the postseason championships, but around the holidays they might be more likely to sell novelty items like pet outfits to casual fans.

There may occasionally be instances in which sales of some or many products increase or decrease without any apparent cause.  It could be due to a discrete event in the news unrelated to the time of year or athletic performance, like a public statement on Twitter about current events. CourtsideSentiment helps the user identify these discrete events by looking at Reddit comment data. Combining CourtsideSentiment with sales data will then help the user advise their client on whether such discrete events are helpful or harmful to their brand, and use that information to boost sales and visibility during a product release.

## Tech stack
The tech stack for this project is shown below. The data source for this project is over 660 GB of Reddit comment dated hosted by [pushshift](https://files.pushshift.io/reddit/comments/) in compressed JSON format.  There's one data file per month, compressed in `.bz2`, `.xz`, or `.zst` format. The files are converted to compressed `.parquet` format (see [here](https://github.com/jnarkis/CourtsideSentiment/tree/master/file_conversion) for more info), and stored in an Amazon S3 bucket along with the raw data files. For each comment file, the comments are queried for the person of interest (popular NBA players are used for the MVP), and sentiment analysis is performed on them using the [VADER](https://github.com/cjhutto/vaderSentiment) package.  This is done with distributed computing using a Spark cluster of 4 workers using [AWS EC2](https://aws.amazon.com/ec2/) instances (m4.large). The results are saved to a PostgreSQL database hosted by [AWS RDS](https://aws.amazon.com/rds/), which is then queried by the front end using [Dash](https://dash.plot.ly/).
![](techstack.png)

## Engineering challenge
Integration of specific events may be challenging, and an appropriate sentiment analysis library must be selected. More specific challenges are anticipated as the project development proceeds.

## Minimum viable product
The MVP will only consider teams and athletes from a particular sport, e.g. NBA, look at comments in particular subreddits, e.g. r/nba and r/news, and use limited dates, e.g. season schedules.

## Stretch goals
Drawing from additional data sets, e.g. Twitter or sports-specific forums; addition of other sports; allowing filtering of sentiment by location/region; inclusion of some form of streaming





