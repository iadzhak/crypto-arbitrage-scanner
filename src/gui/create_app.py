from dash import Dash, html, dash_table, dcc, Input, Output
import dash_bootstrap_components as dbc


def create_app(title, get_data):
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = [
        dbc.Container([
            html.H1(title),
            dash_table.DataTable(id='table', sort_action='native', ilter_action='native')
        ], className='mt-3'),
        dcc.Interval(id='interval', interval=2000)
    ]

    @app.callback(
        Output('table', 'data'),
        Output('table', 'columns'),
        Input('interval', 'n_intervals')
    )
    def update(n):
        """Обновление таблицы."""
        data = get_data()
        if not data:
            return [], []
        columns = [{"name": i, "id": i} for i in data[0].keys()]
        return data, columns

    return app
