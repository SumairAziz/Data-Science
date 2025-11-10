# # Import required libraries
# import pandas as pd
# import plotly.graph_objects as go
# import dash
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output
# # Read the airline data into the pandas dataframe
# airline_data =  pd.read_csv('airline_data.csv')
# # Create a dash application
# app = dash.Dash(__name__)



# app.layout = html.Div(children=[ html.H1('Airline Performance Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
#                                 html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', 
#                                 type='number', style={'height':'50px', 'font-size': 35}),], 
#                                 style={'font-size': 40}),
#                                 html.Br(),
#                                 html.Br(),
#                                 html.Div(dcc.Graph(id='line-plot')),
#                                 ])
# # add callback decorator
# @app.callback( Output(component_id='line-plot', component_property='figure'),
#                Input(component_id='input-year', component_property='value'))
# # Add computation to callback function and return graph
# def get_graph(entered_year):
#     # Select 2019 data
#     df =  airline_data[airline_data['Year']==int(entered_year)]
    
#     # Group the data by Month and compute average over arrival delay time.
#     line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
#     fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
#     fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
#     return fig
# # Run the app
# if __name__ == '__main__':
#     app.run()


 


import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Read the airline data
airline_data = pd.read_csv('airline_data.csv')

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Total number of flights by reporting airline for selected year',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    html.Div([
        "Input Year: ",
        dcc.Input(id='input-year', value='2010', type='number',
                  style={'height': '50px', 'font-size': 35})
    ], style={'font-size': 40, 'textAlign': 'center'}),

    html.Br(),
    html.Br(),

    html.Div(dcc.Graph(id='bar-plot')),
])

@app.callback(
    Output('bar-plot', 'figure'),
    Input('input-year', 'value')
)
def get_graph(entered_year):
    # Filter data for entered year
    df = airline_data[airline_data['Year'] == int(entered_year)]

    # Group by Reporting_Airline
    bar_data = df.groupby('Reporting_Airline')['Flight_Number_Reporting_Airline'].count().reset_index()
    bar_data.columns = ['Reporting_Airline', 'Flights']

    # Create bar chart
    fig = go.Figure(data=go.Bar(
        x=bar_data['Reporting_Airline'],
        y=bar_data['Flights'],
        marker_color='royalblue'
    ))

    # Chart layout styling
    fig.update_layout(
        title=f'Flights by Airline for Year {entered_year}',
        xaxis_title='Reporting Airline',
        yaxis_title='Number of Flights',
        plot_bgcolor='rgb(245, 245, 255)',
        paper_bgcolor='white',
        font=dict(size=14),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='lightgrey')
    )

    return fig


if __name__ == '__main__':
    app.run()


 
