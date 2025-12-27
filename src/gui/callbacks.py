from dash import Input, Output, State
from .scanner_model import ScannerModel


def register_callbacks(app, scanner: ScannerModel):
    # Меню настроек.
    @app.callback(
        Output('settings', 'is_open'),
        Input('btn_settings', 'n_clicks'),
        State('settings', 'is_open')
    )
    def toggle_settings(n, is_open):
        return not is_open if n else is_open

    @app.callback(
        Input('exchanges', 'value')
    )
    def update_exchange(exchanges):
        scanner.set_watchlist(exchanges)

    @app.callback()
    def update():
        pass
