from dash_extensions.enrich import DashBlueprint, dcc, html, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from covid19app.data import Document


page = DashBlueprint()
page.path = '/documents'
page.title = 'Documents'
page.icon = 'carbon:document'
page.order = 1

badge_colors = [
    'gray', 'red', 'pink', 'grape', 'violet',
    'indigo', 'blue', 'lime', 'yellow', 'orange'
]

def generate_tag_badges(tags):
    tags = ['cleaning', 'testing', 'ppe']

    if len(tags) == 0:
        return [
            dmc.ThemeIcon(
                DashIconify(icon='carbon:error', width=20),
                variant='light',
                color='red',
            )
        ]
    else:
        badges = []

        for i, tag in enumerate(tags):
            badges.extend([
                dmc.Badge(
                    tag,
                    variant='filled',
                    color=badge_colors[i % len(badge_colors)]
                ),
                dmc.Space(w=10)
            ])

        return dmc.Spoiler(
            showLabel='Show',
            hideLabel='Hide',
            maxHeight=25,
            class_name='tags-spoiler',
            children=badges
        )

@page.callback(
    Output('pagination-button', 'total'),
    Input('pagination-num-input', 'value'),
    State('documents-table-search', 'value')
)
def documents_table_pagination_size_change_handler(page_size, search_string):
    if search_string:
        return Document.get_num_pages(page_size, search_string)
    else:
        return Document.get_num_pages(page_size)

@page.callback(
    Output('documents-table-body', 'children'),
    Input('pagination-button', 'page'),
    Input('pagination-num-input', 'value'),
    State('documents-table-search', 'value')
)
def documents_table_pagination_handler(page, page_size, search_string):
    if search_string:
        documents = Document.get_values(
            k=page,
            n=page_size,
            search_string=search_string
        )
    else:
        documents = Document.get_values(
            k=page,
            n=page_size,
        )

    return [
        html.Tr([
            html.Td(document['effective_date'].strftime('%Y-%m-%d')),
            html.Td(
                document['termination_date'].strftime('%Y-%m-%d') \
                    if document.get('termination_date') else 'N/A'
            ),
            html.Td(document['slug']),
            html.Td(document['title']),
            html.Td(document['num_versions']),
            html.Td(
                generate_tag_badges(document['tags'])
            ),
            html.Td(
                dmc.Tooltip(
                    label='View document',
                    position='right',
                    placement='center',
                    withArrow=True,
                    gutter=3,
                    children=[
                        dcc.Link(
                            dmc.Button(
                                [
                                    DashIconify(icon='carbon:view-filled', height=25)
                                ],
                                color='pink',
                                style={'padding': '0 8px'}
                            ),
                            href=f'/document/{document["id"]}'
                        )
                    ]
                )
            )
        ]) for document in documents]

page.clientside_callback(
    """
    debounce(searchString => {
        console.log(searchString)
    }, 500)
    """,
    Input('documents-table-search', 'value')
)

page.layout = html.Div([
    dmc.Grid(
        [
            dmc.Col(
                dmc.Title('Documents', order=3),
                span=6
            ),
            dmc.Col(
                dmc.TextInput(
                    id='documents-table-search',
                    style={'width': 200, 'marginLeft': 'auto'},
                    placeholder='Filter documents',
                    icon=[DashIconify(icon='carbon:search')],
                ),
                span=6,
            )
        ]
    ),
    dmc.Space(h=10),
    dmc.Divider(variant='solid'),
    dmc.Space(h=10),
    dmc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th('Effective Date'),
                        html.Th('Termination Date'),
                        html.Th('Document Slug'),
                        html.Th('Title'),
                        html.Th('# Versions'),
                        html.Th('Tags'),
                        html.Th('')
                    ]
                )
            ),
            html.Tbody(id='documents-table-body')
        ]
    ),
    dmc.Space(h=10),
    dmc.Grid(
        [
            dmc.Col(
                dmc.NumberInput(
                    id='pagination-num-input',
                    description='Rows per page',
                    value=8,
                    min=5,
                    max=20,
                    step=1,
                ),
                span=2
            ),
            dmc.Col(
                [
                    dmc.Space(h=22),
                    dmc.Pagination(
                        id='pagination-button',
                        total=0,
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
