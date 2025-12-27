from dash import Input, Output, State


def register_callbacks(app):
    # Меню настроек.
    @app.callback(
        Output('settings', 'is_open'),
        Input('btn_settings', 'n_clicks'),
        State('settings', 'is_open')
    )
    def toggle_settings(n, is_open):
        return not is_open if n else is_open
