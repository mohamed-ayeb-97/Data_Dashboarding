from dash import Dash, dash_table, dcc, html, Input, Output, State, callback
import pandas as pd
import plotly.express as px

app = Dash(__name__)

server = app.server

df = pd.read_excel('data_file.xlsx')

# Background image style
background_image_style = {
    'background-image': 'url(" https://www.tunisie-direct.com/wp-content/uploads/2021/11/oaca_1547656075.jpg")',
    'background-size': '530px 230px',
    'background-repeat': 'no-repeat',
    'background-position': 'top right',
    'min-height': '100vh',
}

app.layout = html.Div(
    style=background_image_style,
    
    children=[
        html.Div([
            html.Br(),

            dcc.Input(
            id='name',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-rows-button', n_clicks=0)
    ], style={'height': 50}),
    html.Br(),
    html.Br(),
    html.Br(),

        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i, "deletable": True, "selectable": True, 'renamable': True} for i in df.columns],
        id='table',
        editable=True,
        row_deletable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        export_format='xlsx',
        export_headers='display',
        merge_duplicate_headers=True,
        page_size= 50
    ),
    dcc.RadioItems(options=['FlightType', 'AircraftType', 'Destination'], value='Destination', id='controls-and-radio-item1'),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),

    dcc.Graph(figure={}, id='graph1'),

    dcc.RadioItems(options=['FlightType', 'AircraftType', 'Destination'], value='Destination', id='controls-and-radio-item2'),

    dcc.Graph(figure={}, id='graph2')
])


@callback(
    Output('table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('table', 'data'),
    State('table', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@callback(
    Output('table', 'columns'),
    Input('adding-rows-button', 'n_clicks'),
    State('name', 'value'),
    State('table', 'columns'))

def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns

@callback(
    Output('graph1', 'figure'),
    Input('controls-and-radio-item1', 'value'))
def display_output(col_chosen):
    fig = px.bar(df, x=df['Origin'], y=col_chosen, color=col_chosen, title=f"Origin X {col_chosen}")
    return fig

@callback(
    Output('graph2', 'figure'),
    Input('controls-and-radio-item2', 'value'))
def display_output(col_chosen):
    fig = px.bar(df, x=df['CallSign'], y=col_chosen, color=col_chosen, title=f"CallSign X {col_chosen}")
    return fig


if __name__ == '__main__':
    app.run(debug=True)
