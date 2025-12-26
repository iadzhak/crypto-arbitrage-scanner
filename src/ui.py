from dash import Dash, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc

from components import navbar, progress_bar, checklist, toggle

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

opts = [('bybit', False), ('binance', False)]
list_exchanges = checklist('exchanges', 'Выберите биржу', *opts)
buttons = [('Настройки', 'btn_settings')]
table_columns = ['updated', 'exchanges', 'symbols', 'amount', 'margin']

app.layout = [html.Div(children=[
    navbar(*buttons),
    progress_bar(value=12, value_max=15),
    toggle('settings', list_exchanges),
    dash_table.DataTable(id='table', columns=[{"name": i, "id": i} for i in table_columns])
])]


# Меню настроек.
@app.callback(
    Output('settings', 'is_open'),
    [Input('btn_settings', 'n_clicks')],
    [State('settings', 'is_open')]
)
def toggle_settings(n, is_open):
    return not is_open if n else is_open


if __name__ == '__main__':
    app.run(debug=True)
