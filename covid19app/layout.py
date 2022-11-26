from dash_extensions.enrich import DashBlueprint, dcc, html, Output, Input, ALL
from dash import page_container, page_registry
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def render_layout(pages):
    layout = DashBlueprint()

    @layout.callback(
        Output('navbar-drawer', 'opened'),
        Input('navbar-menu-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def navbar_menu_toggle(_):
        return True

    @layout.callback(
        Input({'type': 'navbar-link', 'index': ALL}, 'n_clicks'),
        Output('navbar-drawer', 'opened')
    )
    def navbar_link_click(_):
        return False

    pages = [p for p in pages.values() if p['order'] != -1]

    layout.layout = html.Div([
        dmc.Drawer(
            [
                dmc.Navbar(
                    width={"base": 300},
                    height=300,
                    children=[
                        dmc.ScrollArea(
                            offsetScrollbars=True,
                            type='scroll',
                            children=[
                                dmc.Group(
                                    direction='column',
                                    children=[
                                        html.Div(
                                            dcc.Link(
                                                dmc.Group(
                                                    [
                                                        dmc.ThemeIcon(
                                                            DashIconify(icon=page['image'], width=18),
                                                            size=30,
                                                            radius=30,
                                                            variant='light',
                                                        ),
                                                        dmc.Text(page['name'], size='sm', color='gray'),
                                                    ]
                                                ),
                                                href=page['path'],
                                                style={'textDecoration': 'none'},
                                            ),
                                            id={'type': 'navbar-link', 'index': i}
                                        ) for i, page in enumerate(pages)
                                    ],
                                    class_name='navbar-link-group'
                                )
                            ],
                        )
                    ],
                )
            ],
            title='Resources',
            id='navbar-drawer',
            padding='md',
        ),
        dmc.Header(
            height=70,
            fixed=True,
            p='md',
            style={'background': 'rgb(76, 110, 245)'},
            children=[
                dmc.Container(
                    fluid=True,
                    children=dmc.Group(
                        position='apart',
                        align='flex-start',
                        children=[
                            dmc.Group(
                                [
                                    dmc.Button(
                                        [
                                            DashIconify(icon='carbon:menu', width=36)
                                        ],
                                        id='navbar-menu-button',
                                        variant='light',
                                        style={
                                            'padding': '0',
                                            'position': 'relative',
                                            'top': '2px'
                                        }
                                    ),
                                    dmc.Text(
                                        'CDC COVID-19 Guidance Explorer',
                                        size='xl',
                                        color='white',
                                    )
                                ],
                                position='left',
                                align='center',
                                spacing='sm',
                            ),
                            dmc.Group(
                                dmc.TextInput(
                                    style={'width': 250},
                                    placeholder='Search documents',
                                    icon=[DashIconify(icon='carbon:search')],
                                ),
                                position='right',
                                align='center',
                                spacing='xl',
                            ),
                        ],
                    ),
                )
            ],
        ),
        dmc.Container(
            dmc.Stack(
                [
                    dmc.Space(h=50),
                    dmc.Paper(
                        page_container,
                        withBorder=True,
                        radius='md',
                        shadow='xl',
                        p='10px'
                    )
                ]
            ),
            fluid=True
        )
        
    ])

    return layout

def register_layout(app):
    layout = render_layout(page_registry)
    app.layout = layout.layout
    layout.register_callbacks(app)
