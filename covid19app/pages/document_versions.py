from dash_extensions.enrich import DashBlueprint, dcc, html, Input, Output, ALL
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from covid19app.data import DocumentVersion


page = DashBlueprint()
page.path = '/document-versions'
page.title = 'Document Versions'
page.icon = 'carbon:version'
page.order = 2

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
    Input('document-versions-table-search', 'value'),
    Input('pagination-num-input', 'value'),
    Output('pagination-button', 'total')
)
def document_versions_table_pagination_size_change_handler(search_string, page_size):
    if search_string:
        return DocumentVersion.get_num_pages(page_size, search_string)
    else:
        return DocumentVersion.get_num_pages(page_size)

@page.callback(
    Input('pagination-button', 'page'),
    Input('pagination-num-input', 'value'),
    Input('document-versions-table-search', 'value'),
    Output('document-versions-table-body', 'children')
)
def document_versions_table_pagination_handler(page, page_size, search_string):
    if search_string:
        document_versions = DocumentVersion.get_values(
            k=page,
            n=page_size,
            search_string=search_string
        )
    else:
        document_versions = DocumentVersion.get_values(
            k=page,
            n=page_size
        )

    return [
        html.Tr([
            html.Td(document_version['effective_date'].strftime('%Y-%m-%d')),
            html.Td(
                document_version['termination_date'].strftime('%Y-%m-%d') \
                    if document_version.get('termination_date') else 'N/A'
            ),
            html.Td(document_version['slug']),
            html.Td(document_version['title']),
            html.Td('1'),
            html.Td(
                generate_tag_badges(document_version['tags'])
            ),
            html.Td(
                dmc.Tooltip(
                    label='View document version',
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
                                color='orange',
                                style={'padding': '0 8px'}
                            ),
                            href=f'/document-version/{document_version["id"]}'
                        )
                    ]
                )
            )
        ]) for document_version in document_versions]

page.layout = html.Div([
    dmc.Grid(
        [
            dmc.Col(
                dmc.Title('Document Versions', order=3),
                span=6
            ),
            dmc.Col(
                dmc.TextInput(
                    id='document-versions-table-search',
                    style={'width': 200, 'marginLeft': 'auto'},
                    placeholder='Filter document versions',
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
                        html.Th('Version #'),
                        html.Th('Tags'),
                        html.Th('')
                    ]
                )
            ),
            html.Tbody(id='document-versions-table-body')
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
