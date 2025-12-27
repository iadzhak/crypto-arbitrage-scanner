from logging import disable

from dash import Input, Output, State
from .scanner_model import ScannerModel


def register_callbacks(app, scanner: ScannerModel):
    # Загрузка.
    @app.callback(
        Output('progress_bar', 'value'),
        Output('exchanges', 'options'),
        Output('loader_interval', 'disabled'),
        Output('progress_bar', 'style'),
        Input('loader_interval', 'n_intervals'),
        State('progress_bar', 'style')
    )
    def update_progress(_, style):
        load = scanner.load_status()
        loaded_exchanges = scanner.loaded_exchanges()
        value_max = len(loaded_exchanges)
        options_list = [
            {'label': opt_name, 'value': opt_name, 'disabled': opt_disabled}
            for opt_name, opt_disabled in loaded_exchanges
        ]
        disabled = False if load < value_max else True
        if disabled:
            style = {'display': 'none'}
        return load, options_list, disabled, style

    # Меню настроек.
    @app.callback(
        Output('settings', 'is_open'),
        Input('btn_settings', 'n_clicks'),
        State('settings', 'is_open')
    )
    def toggle_settings(n, is_open):
        return not is_open if n else is_open

    # Выбор бирж.
    @app.callback(
        Input('exchanges', 'value')
    )
    def update_exchange(exchanges):
        scanner.set_watchlist(exchanges)

    # Обновление таблицы данных.
    ...
