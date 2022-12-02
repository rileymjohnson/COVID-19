from dash_extensions.enrich import DashBlueprint, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

page = DashBlueprint()
page.path = '/powershell-search'
page.title = 'Powershell Search'
page.icon = 'carbon:search'
page.order = 4

page.layout = html.Div([
    dmc.Title('Search Results', order=4),
    dmc.Accordion(
        icon=[
            DashIconify(icon='carbon:chevron-down')
        ],
        children=[
            dmc.AccordionItem(
                children=[
                    dmc.Space(h=10),
                    dmc.Timeline(
                        active=3,
                        bulletSize=15,
                        lineWidth=2,
                        children=[
                            dmc.TimelineItem(
                                title=[
                                    dmc.Grid(
                                        [
                                            dmc.Col(
                                                dmc.Stack(
                                                    [
                                                        dmc.Text(
                                                            'Agricultural Employer Checklist for Creating a COVID-19 Assessment and Control Plan',
                                                            weight=500,
                                                            size='sm',
                                                            style={
                                                                'fontStyle': 'italic',
                                                                'fontSize': '13px'
                                                            }
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Badge(
                                                                    'Version #9',
                                                                    variant='outline',
                                                                    color='lime',
                                                                    size='xs',
                                                                    radius='sm'
                                                                ),
                                                                dmc.Badge(
                                                                    'ID: 9405',
                                                                    variant='outline',
                                                                    color='violet',
                                                                    size='xs',
                                                                    radius='sm'
                                                                )
                                                            ],
                                                            spacing='xs',
                                                            style={'gap': '4px'}
                                                        )
                                                    ],
                                                    spacing='xs',
                                                    style={'gap': '2px'}
                                                ),
                                                span=8
                                            ),
                                            dmc.Col(
                                                [
                                                    dmc.Text(
                                                        '2020-03-14 — 2022-04-23',
                                                        color='gray',
                                                        size='sm',
                                                        style={'fontSize': '13px'}
                                                    ),
                                                    dmc.Space(h=5),
                                                    dmc.Group(
                                                        [
                                                            dmc.Button(
                                                                [
                                                                    DashIconify(
                                                                        icon='carbon:view',
                                                                        width=16
                                                                    ),
                                                                    dmc.Space(w=3),
                                                                    'View Document Version'
                                                                ],
                                                                size='xs',
                                                                variant='filled',
                                                                color='orange',
                                                                style={
                                                                    'fontSize': '10px',
                                                                    'height': '20px',
                                                                    'padding': '0 6px',
                                                                    'lineHeight': '9px'
                                                                }
                                                            )
                                                        ],
                                                        position='right',
                                                        spacing='xs',
                                                        style={'gap': '4px'}
                                                    )
                                                ],
                                                style={'textAlign': 'right'},
                                                span=4
                                            )
                                        ]
                                    )
                                ],
                                children=[
                                    dmc.Blockquote(
                                        dmc.Highlight(
                                            'campers during the camp session. Continue to monitor and enforce mask distancing, and healthy hygiene different cohorts are using shared spaces together during the day or Ensure that staff or campers who',
                                            highlight=['cohort'],
                                            color='dimmed',
                                            size='sm'
                                        ),
                                        cite='Characters: 4354 — 5237'
                                    )
                                ],
                            ),
                            dmc.TimelineItem(
                                title="Commits",
                                children=[
                                    dmc.Text(
                                        [
                                            "You've pushed 23 commits to ",
                                            dmc.Anchor("fix-notification", href="#", size="sm"),
                                        ],
                                        color="dimmed",
                                        size="sm",
                                    ),
                                ],
                            ),
                            dmc.TimelineItem(
                                title="Pull Request",
                                lineVariant="dashed",
                                children=[
                                    dmc.Text(
                                        [
                                            "You've submitted a pull request ",
                                            dmc.Anchor(
                                                "Fix incorrect notification message (#178)",
                                                href="#",
                                                size="sm",
                                            ),
                                        ],
                                        color="dimmed",
                                        size="sm",
                                    ),
                                ],
                            ),
                            dmc.TimelineItem(
                                [
                                    dmc.Text(
                                        [
                                            dmc.Anchor(
                                                "Ann Marie Ward",
                                                href="https://github.com/AnnMarieW",
                                                size="sm",
                                            ),
                                            " left a comment on your pull request",
                                        ],
                                        color="dimmed",
                                        size="sm",
                                    ),
                                ],
                                title="Code Review",
                            ),
                        ],
                    )
                ],
                label=[
                    dmc.Grid(
                        [
                            dmc.Col(
                                dmc.Group(
                                    [
                                        dmc.Avatar(
                                            1,
                                            color='blue',
                                            size='sm',
                                            radius='xl'
                                        ),
                                        dmc.Stack(
                                            [
                                                dmc.Text(
                                                    'Agricultural Employer Checklist for Creating a COVID-19 Assessment and Control Plan',
                                                    weight=600,
                                                    size='sm',
                                                    style={'fontStyle': 'italic'}
                                                ),
                                                dmc.Group(
                                                    [
                                                        dmc.Badge(
                                                            'ID: 5948',
                                                            variant='outline',
                                                            color='pink',
                                                            size='xs',
                                                            radius='sm'
                                                        ),
                                                        dmc.Badge(
                                                            'Slug: community_pdf_agricultural-employer-checklist.pdf',
                                                            variant='outline',
                                                            color='lime',
                                                            size='xs',
                                                            radius='sm'
                                                        )
                                                    ],
                                                    spacing='xs',
                                                    style={'gap': '4px'}
                                                ),
                                                dmc.Group(
                                                    [
                                                        dmc.Badge(
                                                            '# Matching Versions: 14',
                                                            variant='outline',
                                                            color='red',
                                                            size='xs',
                                                            radius='sm'
                                                        ),
                                                        dmc.Badge(
                                                            'Issuer: CDC',
                                                            variant='outline',
                                                            color='indigo',
                                                            size='xs',
                                                            radius='sm'
                                                        ),
                                                        dmc.Badge(
                                                            'File Type: .pdf',
                                                            variant='outline',
                                                            color='orange',
                                                            size='xs',
                                                            radius='sm'
                                                        )
                                                    ],
                                                    spacing='xs',
                                                    style={'gap': '4px'}
                                                )
                                            ],
                                            spacing='xs',
                                            style={'gap': '2px'}
                                        )
                                    ]
                                ),
                                span=8
                            ),
                            dmc.Col(
                                [
                                    dmc.Text(
                                        '2020-03-14 — 2022-04-23',
                                        color='gray',
                                        size='sm',
                                    ),
                                    dmc.Space(h=5),
                                    dmc.Button(
                                        [
                                            DashIconify(
                                                icon='carbon:view',
                                                width=20
                                            ),
                                            dmc.Space(w=3),
                                            'View Document'
                                        ],
                                        size='xs',
                                        variant='filled',
                                        color='yellow'
                                    )
                                ],
                                style={'textAlign': 'right'},
                                span=4
                            )
                        ]
                    )
                ],
            ),
            dmc.AccordionItem(
                label="Flexibility",
            ),
            dmc.AccordionItem(
                label="No annoying focus ring",
            ),
        ],
    ),
    dmc.Space(h=10),
    dmc.Grid(
        [
            dmc.Col(
                dmc.NumberInput(
                    id='pagination-num-input',
                    description='Rows per page',
                    value=5,
                    min=2,
                    max=8,
                    step=1,
                ),
                span=2
            ),
            dmc.Col(
                [
                    dmc.Space(h=22),
                    dmc.Pagination(
                        id='pagination-button',
                        total=10,
                        grow=True,
                        align='stretch',
                        siblings=1,
                        page=1
                    )
                ],
                span=5,
                offset=5
            )
        ]
    )
])
