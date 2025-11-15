import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Create year list
year_list = [i for i in range(1980, 2024, 1)]

# Initialize app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Automobile Sales Statistics Dashboard'

# Read data
df = pd.read_csv("historical_automobile_sales.csv")

# Layout
app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        placeholder='Select a report type',
        value='Select Statistics',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'textAlignLast': 'center'
        }
    ),
    html.Br(),

    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        placeholder='Select-year',
        value='Select-year',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'textAlignLast': 'center'
        }
    ),
    html.Br(),

    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex', 'flexWrap': 'wrap'}
        )
    ])
])


# --------------------------
# 🔹 Callback 1: Enable/Disable Year Dropdown
# --------------------------
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # Enable dropdown
    else:
        return True   # Disable dropdown


# --------------------------
# 🔹 Callback 2: Update Output Container
# --------------------------
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter data for recession periods
        recession_data = df[df['Recession'] == 1]

        # Create 4 example graphs
        fig1 = px.bar(recession_data, x='Year', y='Automobile_Sales', title='Total Automobile Sales During Recession')
        fig2 = px.line(recession_data, x='Year', y='unemployment_rate', title='Unemployment Rate During Recession')
        fig3 = px.bar(recession_data, x='Vehicle_Type', y='Automobile_Sales', title='Sales by Vehicle Type During Recession')
        fig4 = px.line(recession_data, x='Year', y='GDP', title='GDP During Recession')

    elif selected_statistics == 'Yearly Statistics' and selected_year != 'Select-year':
        # Filter data for selected year
        yearly_data = df[df['Year'] == int(selected_year)]

        # Create 4 example graphs
        fig1 = px.bar(yearly_data, x='Vehicle_Type', y='Automobile_Sales', title=f'Automobile Sales by Vehicle Type in {selected_year}')
        fig2 = px.pie(yearly_data, names='Vehicle_Type', values='Advertising_Expenditure', title='Advertising Expenditure Share')
        fig3 = px.bar(yearly_data, x='Vehicle_Type', y='unemployment_rate', title='Unemployment Rate by Vehicle Type')
        fig4 = px.line(yearly_data, x='Month', y='Automobile_Sales', title=f'Sales Trend by Month in {selected_year}')

    else:
        return []  # No plots if no valid selection

    # Return all four graphs to output container
    return [
        dcc.Graph(figure=fig1, style={'width': '50%'}),
        dcc.Graph(figure=fig2, style={'width': '50%'}),
        dcc.Graph(figure=fig3, style={'width': '50%'}),
        dcc.Graph(figure=fig4, style={'width': '50%'})
    ]


def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter data for recession periods
        recession_data = df[df['Recession'] == 1]

        # 🔹 Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Over Recession Years'
            )
        )

        # 🔹 Plot 2: Average number of vehicles sold by vehicle type (Bar chart)
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type During Recession'
            )
        )

        # 🔹 Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertising Expenditure Share by Vehicle Type During Recession'
            )
        )

        # 🔹 Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        # Return charts in a 2×2 grid
        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                style={'display': 'flex'}
            )
        ]

    # Yearly Statistic Report Plots
    elif (selected_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = df[df['Year'] == int(selected_year)]

        # 🔹 Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Average Automobile Sales (1980–2023)'
            )
        )

        # 🔹 Plot 2: Total Monthly Automobile sales using line chart
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales in {}'.format(selected_year)
            )
        )

        # 🔹 Plot 3: Average number of vehicles sold by vehicle type during the given year (Bar chart)
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in {}'.format(selected_year)
            )
        )

        # 🔹 Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle in {}'.format(selected_year)
            )
        )

        # Return all four charts arranged 2×2
        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                style={'display': 'flex'}
            )
        ]

    else:
        return []


# Run the server
if __name__ == '__main__':
    app.run()
