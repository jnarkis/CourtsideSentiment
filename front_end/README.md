# CourtsideSentiment Interface
The CourtsideSentiment interface is written using [Dash](https://dash.plot.ly/), a Python framework written on top of Flask designed for data visualization web applications. Within the `assets` directory is a short `.css` file that adds minor formatting improvements to the frontend.

There are three main sections of the interface: the parameter selection, the plot window, and the comment table. See below for a screenshot of the interface 'in-action' and, subsequently, description of each part of the interface.

![](screenshot.png)

## Table of Contents

1. [Parameter selection](README.md#parameter_selection)
1. [Plot window](README.md#plot_window)
1. [Comment table](README.md#comment_table)

## Parameter selection
There are several parameters available to the user for selecting what data to explore. Player selection includes a list of popular NBA players: Lebron James, Kevin Durant, James Harden, Anthony Davis, Steph Curry, and Kawhi Leonard.  The sentiment score metric is one of the scores obtained from the [VADER sentiment analysis](https://github.com/cjhutto/vaderSentiment).  Each reddit comment contains positive, neutral, and negative words of varying sentimal strength.  A corresponding score for each type of word is assigned to each comment, as well as a 'compound' score that is an aggregate metric. 
Users can also select a date range for the plot window, discussed in the next section.
Finally, the user can select a certain date of interest on the plot, and then click 'Get comments' to get all the Reddit comments that mention a particular player on a particular day, and populate the comment table. In addition, two links for more information are generated: the first is a Google search of the player and date, and the second is a link to all NBA games played on the selected date.

## Plot window
The plot window displays the moving average of the sentiment score (with a window of 50) for the selected player, metric, and date range. The plot is a [Dash graph object](https://dash.plot.ly/dash-core-components/graph) that has many useful features, like zooming and point selection.

## Comment table
The comment table is initially empty, so to populate the list select a player and date and click 'Get Comments'. The table is then populated by the list of all Reddit comments that mention the selected player on the selected date, sorted in descending order by score. If the user has identified a date of interest where many Reddit users expressed strong sentiment about a player, then reading through the comments might provide some insight as to a particular event they are discussing.
