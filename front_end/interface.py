import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

import os

from sqlalchemy import create_engine

from datetime import datetime
from datetime import date


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

engine = create_engine('postgresql://'+os.environ["AWS_RDS_POSTGRES_USER"]+\
                        ':'+os.environ["AWS_RDS_POSTGRES_PWD"]+'@'\
                        +os.environ["AWS_RDS_POSTGRES_ENDPT"]+':5432/')

plot_df = pd.read_sql('SELECT posttime,comp,body,score,subreddit FROM kevin_master_sorted',engine)

def moving_average(values,window):
   weights = np.repeat(1.0,window)/window
   smas = np.convolve(values,weights,'valid')
   return smas

colors = {
'background': '#07080a',
'text' : '#d6d8da',
'plotbg' : '#c6c8ca',
'gridline' : '#b6b8ba',
'headertext' : '#df6e22'
}

app.layout =\
 html.Div(children=[
   html.H2('Courtside Sentiment',
           style={'textAlign': 'center','color' : colors['text'], 'font-weight' : 'bold'}),
   html.H5('A front-row seat to the opinions of Reddit',
           style={'textAlign': 'center','color' : colors['text'], 'font-weight' : 'normal','margin-bottom':10}),
   html.Div(id='left_pad_placeholder',style={'width' : '1.25%', 'display' : 'inline-block'}),
   html.Div(children=[
       html.Div('Player selection:',style={'color' : colors['text'], 'fontSize' : 12, 'margin-bottom': 5}),
       dcc.Dropdown(id='player',
           options=[
              {'label' : 'Lebron James', 'value' : 'lebron+james'},
              {'label' : 'Kevin Durant', 'value' : 'kevin+durant'},
              {'label' : 'James Harden', 'value' : 'james+harden'},
              {'label' : 'Anthony Davis', 'value': 'anthony+davis'},
              {'label' : 'Steph Curry', 'value' : 'steph+curry'},
              {'label' : 'Kawhi Leonard', 'value': 'kawhi+leonard'},
           ],
           value='kevin+durant',
           style={'fontSize' : 12, 'fontColor' : colors['text']}),
       html.Div('Sentiment score metric:',style={'color' : colors['text'], 'fontSize' : 12, 'margin-top' : 5,'margin-bottom' : 5}),
       dcc.Dropdown(id='vader_metric',
           options=[
              {'label' : 'Positive', 'value' : 'pos'},
              {'label' : 'Neutral', 'value' : 'neu'},
              {'label' : 'Negative', 'value' : 'neg'},
              {'label' : 'Compound', 'value' : 'comp'}
            ],
            value = 'comp',
            style={'fontSize' : 12, 'fontColor' : colors['text']}
       ),

       html.Div('Selected date range for plot:',style={'color' : colors['text'], 'fontSize' : 12, 'margin-top' : 5,'margin-bottom' : 5}),
       dcc.DatePickerRange(id='date-window-plot',
                              start_date='2017-01-01',
                              end_date='2018-12-31',
                           style={'color' : colors['text'], 'fontSize' : 12},
                          ),

       html.Div('Selected date for getting more info:',style={'color' : colors['text'], 'fontSize' : 12, 'margin-top' : 5, 'margin-bottom' : 5}),

       html.Div(children=[
          dcc.DatePickerSingle(id='querydate',
          style={'fontSize' : 12, 'display':'inline-block'}),

          html.Div(children=[
             html.Button('Get comments',id='get_comments_button',style={'height':41,'fontSize' : 10,'width':160},n_clicks=0)
          ],
          style={'display':'inline-block','margin-left' : 5})

       ]),

       html.Div(id='print-links', style={'color' : colors['text'], 'fontSize' : 12,'margin-top' : 5, 'margin-bottom' : 5})

          ],
          style={'width': '25%','display':'inline-block','vertical-align': 'middle'},
          ),



   html.Div(id='white_space',style={'width' : '1.25%','display':'inline-block'}),

   html.Div(
           dcc.Graph(id='example',figure={
                 'data': [dict(x=(plot_df['posttime'].astype('int')).astype('datetime64[s]'),
                                 y=moving_average(plot_df['comp'],50),
                                 line={'color': '#356d7b','width':'2'}
                         )],
                 'layout': { 'margin' : {'t' : 10,'l' : 70,'r': 10,'b':55},
                             'plot_bgcolor' :  colors['plotbg'],
                             'paper_bgcolor' : colors['background'],
                             'height' : 310,
                             'xaxis' : {'title' : {'text' : 'Date', 'font' : {'size' : 24, 'color' : colors['text']}},
                                        'color' : colors['text'],
                                        'range' : [datetime(2017,1,1),datetime(2018,12,31,23,59,59)],
					'ticklen' : 4,
                                        'tickcolor' : colors['background'],
                                        'showgrid':'true',
                                        'gridcolor' : colors['gridline'],
                                        'gridwidth' : 1,
                                        'zerolinecolor' : colors['gridline'],
                                        'zerolinewidth' : 3,
                             },
                             'yaxis' : {'title' : {'text' : 'Average score', 'font' : {'size' : 24, 'color' : colors['text']}},
                                        'color' : colors['text'],
                                        'range' : [-1,1],
                                        'tickvals' : [-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1],
                                        'ticklen' : 3,
                                        'tickcolor' : colors['background'],
                                        'showgrid':'true',
                                        'gridcolor' : colors['gridline'],
                                        'gridwidth' : 1,
                                        'zerolinecolor' : colors['gridline'],
                                        'zerolinewidth' : 3,
                             }
                           }
           },
           ),
      style={'width' : '70%','display':'inline-block','vertical-align': 'top', 'border' : '3px #00213c solid', 'border-radius' : '2px' }
   ),

   html.Div(
      dash_table.DataTable(
      id='comment_table',
      columns=[{'name' : 'score', 'id' : 'score'},
               {'name' : 'subreddit', 'id' : 'subreddit'},
               {'name' : 'body', 'id' : 'body'}],
      style_table={'overflowY':'scroll','maxHeight':'275px','border' : '3px solid #00213c'},
      style_header={'backgroundColor' : '#356d7b','color':colors['text'],'fontSize':12},
      style_cell={
         'backgroundColor' : colors['plotbg'],'fontSize':10, 'border' : '1px solid #00213c'
      },
      style_data={
        'whiteSpace': 'normal',
      }
      )
      ,style={'width':'96.75%','display':'inline-block','padding-left':'1.25%'}),

   ] #end children
   , style={'backgroundColor':colors['background'],'layout' : {'margin' : 0}}

)

# When the get comments button is clicked, load the Reddit comments mentioning that player on that day,
# ranked by score (upvotes - downvotes)

@app.callback(Output('comment_table','data'), [Input('get_comments_button','n_clicks')],
   [State('querydate','date'),State('player','value')])

def populate_comment_table(n_clicks,querydate_date,player_value):
   if n_clicks is None or querydate_date is None:
      raise PreventUpdate
   else:
      if n_clicks > 0:
         table_df = pd.read_sql('SELECT posttime,score,subreddit,body FROM %s_master_sorted' % player_value.split('+')[0],engine)
         date_to_match = datetime.strptime(querydate_date,'%Y-%m-%d').date()
         wrongdate = table_df[ pd.to_datetime(table_df['posttime'],unit='s').dt.date != date_to_match].index
         table_df.drop(wrongdate,inplace=True)
         table_df.drop(columns='posttime',inplace=True)
         return table_df.sort_values(by=['score'],ascending=False).to_dict('rows')

# When a date is selected for querying further, print out some useful links. The first
# link is a Google search for the player on the selected date, the second checks if any NBA games are played then

@app.callback(Output('print-links','children'),[Input('querydate','date'),\
      Input('player','value')])

def print_links_on_click(querydate_date,value):
   if querydate_date is None:
      raise PreventUpdate
   else:
        #generate query string
        two = datetime.strptime(querydate_date,"%Y-%m-%d")
        part_two = '%s/%s/%s' % (str(two.month).zfill(2),str(two.day).zfill(2),str(two.year))

        return  html.Div([html.A('Google search',href='https://www.google.com/search?q="%s"+%s'
              % (value,part_two),target='_blank'),
                html.Br(),
                html.A('NBA games played on %s' % part_two,\
                href='https://www.basketball-reference.com/boxscores/?month=%s&day=%s&year=%s'
                     % (str(two.month),str(two.day),str(two.year)),target='_blank')
                ])

# Click on the plot on a date of interest, put that date in the search field

@app.callback(Output('querydate','date'),[Input('example','clickData')] )

def pick_date_from_plot(clickData):
    if clickData is not None:
       try: #sometimes seconds are not there
         date_Clicked = datetime.strptime(clickData['points'][0]['x'],"%Y-%m-%d %H:%M:%S")
       except:
         date_Clicked = datetime.strptime(clickData['points'][0]['x'],"%Y-%m-%d %H:%M")
       #only return day, month, and year
       return date(date_Clicked.year,date_Clicked.month,date_Clicked.day)


# When the player, Vader metric, start date, or end date is updated, change the plot to reflect that.

@app.callback(
   Output('example','figure'),[Input('player','value'), Input('vader_metric','value'),
    Input('date-window-plot','start_date'),Input('date-window-plot','end_date')])

def change_graph_data(player_value,vader_metric_value,start_date,end_date):
   plot_df = pd.read_sql('SELECT posttime,pos,neu,neg,comp FROM %s_master_sorted' % player_value.split('+')[0],engine)
   start_date_conv = datetime.strptime(start_date,'%Y-%m-%d')
   end_date_conv = datetime.strptime(end_date,'%Y-%m-%d')

   return  {
                 'data': [dict(x=(plot_df['posttime'].astype('int')).astype('datetime64[s]'),
                                 y=moving_average(plot_df['%s' % vader_metric_value],50),
                                 line={'color': '#356d7b','width':'2'}
                         )],
                 'layout': { 'margin' : {'t' : 10,'l' : 70,'r': 10,'b':55},
                             'plot_bgcolor' :  colors['plotbg'],
                             'paper_bgcolor' : colors['background'],
                             'height' : 310,
                             'xaxis' : {'title' : {'text' : 'Date', 'font' : {'size' : 24, 'color' : colors['text']}},
                                        'color' : colors['text'],
                                        'range' : [start_date_conv,
                                                   datetime(end_date_conv.year,end_date_conv.month,end_date_conv.day,23,59,59)],
                                        'ticklen' : 4,
                                        'tickcolor' : colors['background'],
                                        'showgrid':'true',
                                        'gridcolor' : colors['gridline'],
                                        'gridwidth' : 1,
                                        'zerolinecolor' : colors['gridline'],
                                        'zerolinewidth' : 3,
                             },
                             'yaxis' : {'title' : {'text' : 'Average score', 'font' : {'size' : 24, 'color' : colors['text']}},
                                        'color' : colors['text'],
                                        'range' : [-1,1],
                                        'tickvals' : [-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1],
                                        'ticklen' : 3,
                                        'tickcolor' : colors['background'],
                                        'showgrid':'true',
                                        'gridcolor' : colors['gridline'],
                                        'gridwidth' : 1,
                                        'zerolinecolor' : colors['gridline'],
                                        'zerolinewidth' : 3,
                             }
                           }
                 }

if __name__ == "__main__":
   app.run_server(host="0.0.0.0",port=8050,debug=False)

