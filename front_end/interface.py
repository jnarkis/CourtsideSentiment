import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import DataFrameReader

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np

import sys

from datetime import datetime

app = dash.Dash()

spark = SparkSession.builder.appName("DashSpark").config("spark.jars","/home/ubuntu/postgresql-42.2.9.jar").getOrCreate()
#app.layout = html.Div(children=[ dcc.Input(id='input', value='Enter something', type='text'),
#   html.Div(id='output')
#   ])

#@app.callback(
#   Output(component_id='output', component_property='children'),
#   [Input(component_id='input', component_property='value')])

#def update_value(input_data):
#   try:
#      return str(float(input_data)**2)
#   except:
#      return "error"

conf = pyspark.SparkConf()
sc = pyspark.SparkContext.getOrCreate(conf=conf)
sqlContext = SQLContext(sc)

in_df_properties = {"user" : "postgres", "password" : "API5tl5VktcxEaJk1HMX", "driver":"org.postgresql.Driver"}

in_df = DataFrameReader(sqlContext).jdbc(url="jdbc:postgresql://database-1.c9z5u98esvku.us-west-2.rds.amazonaws.com:5432/",table="lebron_2018",properties=in_df_properties)

in_dfc = in_df.select("posttime","comp","body")
in_dfc = in_dfc.filter(in_dfc.comp != 0).orderBy("posttime").collect()

posttimes = [datetime.fromtimestamp(int(row.posttime)) for row in in_dfc]
scores = [row.comp for row in in_dfc]
body = [row.body for row in in_dfc]

def moving_average(values,window):
   weights = np.repeat(1.0,window)/window
   smas = np.convolve(values,weights,'valid')
   return smas


#in_df.show()

#fig = go.Figure(data=[go.Scatter(x=posttimes, y=scores)])

#data = px.data.gapminder()
#fig = px.scatter(x=posttimes,y=scores,hovertext=body)
fig = go.Figure(data=go.Scatter(x=posttimes,y=scores,mode='markers')) # ,layout={'yaxis' : [Range,(-1,1)] }) #,hovertext=body))
#fig.update_yaxes(range[-1,1])

fig.update_layout(yaxis = dict(range = [-1,1], constrain = 'domain'))

#fig.update_layout(yaxis = dict(range[-1,1]))

app.layout = html.Div(children=[html.H1('Sports Sentiment Analysis'),
   dcc.Dropdown(id='wow',
      options=[
         {'label' : 'Lebron James', 'value' : 'lebron'},
         {'label' : 'Kevin Durant', 'value' : 'kevin'},
      ],
      value='lebron'
   ),
   dcc.Dropdown(id='year',
      options=[
        {'label' : '2005', 'value' : '2005'},
        {'label' : '2006', 'value' : '2006'},
        {'label' : '2007', 'value' : '2007'},
        {'label' : '2008', 'value' : '2008'},
        {'label' : '2009', 'value' : '2009'},
        {'label' : '2010', 'value' : '2010'},
        {'label' : '2011', 'value' : '2011'},
        {'label' : '2012', 'value' : '2012'},
        {'label' : '2013', 'value' : '2013'},
        {'label' : '2014', 'value' : '2014'},
        {'label' : '2015', 'value' : '2015'},
        {'label' : '2016', 'value' : '2016'},
        {'label' : '2017', 'value' : '2017'},
        {'label' : '2018', 'value' : '2018'},
        {'label' : '2019', 'value' : '2019'},
      ],
      value='2017',
   ),
   dcc.Dropdown(id='vader_metric',
      options=[
        {'label' : 'Positive', 'value' : 'pos'},
        {'label' : 'Neutral', 'value' : 'neu'},
        {'label' : 'Negative', 'value' : 'neg'},
        {'label' : 'Compound', 'value' : 'comp'}
      ],
      value = 'comp'
   ),
   dcc.Dropdown(id='plot_type',
      options=[
        {'label' : 'Scatter plot', 'value' : 'scatter'},
        {'label' : 'Moving average', 'value' : 'mov_avg'},
      ],
      value = 'mov_avg'
   ),
   dcc.Graph(id='example',
      figure=fig)
   ])

@app.callback(
   Output('example','figure'),[Input('wow','value'), Input('year','value'), Input('vader_metric','value'),\
      Input('plot_type','value')
   ])

def update_graph(wow_value,year_value,vader_metric_value,plot_type_value):
   in_df = DataFrameReader(sqlContext).jdbc(url="jdbc:postgresql://database-1.c9z5u98esvku.us-west-2.rds.amazonaws.com:5432/",\
      table="%s_%s" % (wow_value,year_value),properties=in_df_properties)

   in_dfc = in_df.select("posttime","pos","neu","neg","comp","body")

   in_dfc = in_dfc.filter(in_dfc.comp != 0).orderBy("posttime").collect()

   posttimes = [datetime.fromtimestamp(int(row.posttime)) for row in in_dfc]
   scores = [row[vader_metric_value] for row in in_dfc]
   body = [row.body for row in in_dfc]
   #fig.update_layout(
   #yax/is = dict(
   #   range[-1,1]
   #   )
   #)

   #fig.update_layout(yaxis = dict(range = [-1,1], constrain = 'domain'))

   if (plot_type_value == 'scatter'):
      return {'data': [{'x': posttimes, 'y': scores, 'mode': 'markers'}]} #, 'hovertext' :  body}]}
   else:
      return {'data': [{'x': posttimes, 'y': moving_average(scores,50),'mode' : 'lines'}]}

#go.Scatter(x=posttimes,y=scores,mode='markers',hovertext=body)}

#def update_graph(wow_value,year_value):
#     type(wow_value)
#     type(year_value)
#     in_df = DataFrameReader(sqlContext).jdbc(url="jdbc:postgresql://database-1.c9z5u98esvku.us-west-2.rds.amazonaws.com:5432/",table="%s_%s" % (wow_value,year_value),properties=in_df_properties)
#     in_dfc = in_df.select("posttime","comp","body").collect()
#     posttimes = [datetime.fromtimestamp(int(row.posttime)) for row in in_dfc]
#     scores = [row.comp for row in in_dfc]
#     body = [row.body for row in in_dfc]

#     return {}

#go.Scatter(x=posttimes,y=scores,mode='markers',hovertext=body)}

#     print("query redone")

#     fig = go.Figure(data=go.Scatter(x=posttimes,y=scores,mode='markers',hovertext=body))
#     dcc.Graph(id='example',figure=fig)

     
#   dash.dependencies.Output('container','children'),
#   [dash.dependencies.Input('wow','value')])
#def update_output(value):
#   return 'You have selected "{}"'.format(value)

#fig.update_layout(
#   updatemenus=[
#)

if __name__ == "__main__":
   app.run_server(host="0.0.0.0",port=8050,debug=False)

