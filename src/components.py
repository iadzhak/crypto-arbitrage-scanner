from dash import html
import dash_bootstrap_components as dbc


def make_nav_button(btn_id: str, btn_name: str):
    btn = dbc.Button(btn_name, outline=True, color='light', className='me-1', id=btn_id, n_clicks=0)
    return dbc.NavItem(btn)


def navbar(*buttons: tuple[str, str]):
    # Создание кнопок и добавление их в панель управления
    btn_s = [make_nav_button(btn_id, btn_name) for btn_name, btn_id in buttons]

    # Панель управления с кнопками
    return dbc.NavbarSimple(children=btn_s, brand='Crypto Arbitrage Scanner', color='primary', dark=True)


def progress_bar(bar_id: str = 'progress_bar', value: int = 0, value_max: int = 100):
    # Индикатор загрузки.
    bar = dbc.Progress(
        value=value, max=value_max, animated=True, striped=True,
        style={'height': '5px', 'margin-top': '5px'}, id=bar_id)

    return bar


def checklist(list_id: str, header: str = None, *options: tuple[str, bool]):
    # Создание списка опций
    options_list = [
        {'label': opt_name, 'value': opt_name, 'disabled': opt_disabled}
        for opt_name, opt_disabled in options
    ]

    # Формирование контейнера с заголовком и чек листом
    children = [dbc.Label(header)] if header else []
    children.append(dbc.Checklist(options=options_list, id=list_id, inline=True))

    return html.Div(children)


def toggle(toggle_id: str, children, is_open: bool = False):
    container = dbc.Collapse(dbc.Card(dbc.CardBody(children)), id=toggle_id, is_open=is_open)
    return container
