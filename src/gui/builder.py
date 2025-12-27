from dash import Dash, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc

from .components import build_navbar, build_progress_bar, build_checklist, build_toggle_container
from .callbacks import register_callbacks
from .scanner_model import ScannerModel


def create_app(scanner: ScannerModel):
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Создание элементов.
    # Навигация.
    navbar_buttons = [('Настройки', 'btn_settings')]
    navbar = build_navbar(*navbar_buttons)

    # Полоса загрузки.
    value_max = len(scanner.available_exchanges())
    progress_bar = build_progress_bar(value_max=value_max)

    # Панель настроек.
    opts = scanner.available_exchanges()
    checklist_exchanges = build_checklist('exchanges', 'Выберите биржу', *opts)
    toggle_settings = build_toggle_container('settings', checklist_exchanges)

    # Таблица сканера.
    columns = ['updated', 'exchanges', 'symbols', 'amount', 'margin']
    table_columns = [{"name": i, "id": i} for i in columns]
    table = dash_table.DataTable(id='table', columns=table_columns)

    # Расположение элементов на странице.
    app.layout = [html.Div(children=[
        navbar,
        progress_bar,
        toggle_settings,
        table
    ])]

    # Регистрация обработчиков событий.
    register_callbacks(app, scanner)

    return app
