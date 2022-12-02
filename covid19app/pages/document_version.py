from dash_extensions.enrich import DashBlueprint, html, Output, Input, State, dcc, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import json

from covid19app.data import DocumentVersion, Language, Jurisdiction, FileType, Tag, DocumentType


class DashBlueprintWithVariablePaths(DashBlueprint):
    def _layout_value(self, **path_variables):
        if self._layout_is_function:
            layout = self._layout(**path_variables)
        else:
            layout = self._layout

        for transform in self.transforms:
            layout = transform.layout(layout, self._layout_is_function)

        return layout


page = DashBlueprintWithVariablePaths()
page.path = '/document-version'
page.title = 'Document Version'
page.icon = 'carbon:document-export'
page.path_template = '/document-version/<document_version_id>'
page.order = -1

DEFAULT_TAG_COLOR = '#343353'

def generate_input_javascript(component_id):
    return f"""
    (value, data) => {{
        const isInitialCall = data.hasOwnProperty('{component_id}')
        return [
            !isInitialCall,
            Object.assign(data, {{
                ...data,
                '{component_id}': isInitialCall ? value : undefined
            }})
        ]
    }}
    """

@page.callback(
    Output('save-button', 'children'),
    Output('notifications-div', 'children'),
    Input('save-button', 'n_clicks'),
    State('save-data', 'data'),
    prevent_initial_call=True
)
def save_button_handler(n_clicks, data):
    if n_clicks is not None:
        DocumentVersion.update_one(data)

    return no_update, dmc.Notification(
        title='Success!',
        action='show',
        color='lime',
        id='save-success-notification',
        message='The document version has been saved successfully',
        icon=[
            DashIconify(icon='carbon:checkmark-filled')
        ]
    )

for radio_button_id in [
    'has_relevant_information',
    'is_foreign_language',
    'is_malformed',
    'is_empty'
]:
    page.clientside_callback(
        generate_input_javascript(radio_button_id),
        Output('save-button', 'disabled'),
        Output('save-data', 'data'),
        Input(radio_button_id, 'value'),
        State('save-data', 'data')
    )

for multi_select_id in [
    'types',
    'tags',
    'jurisdictions'
]:
    page.clientside_callback(
        generate_input_javascript(multi_select_id),
        Output('save-button', 'disabled'),
        Output('save-data', 'data'),
        Input(multi_select_id, 'value'),
        State('save-data', 'data')
    )

for component_id in [
    'language',
    'file_type',
    'notes',
    'variables',
    'effective-date-input',
    'effective-time-input',
    'termination-date-input',
    'termination-time-input',
    'importance',
    'title',
    'slug',
    'source-input',
    'source_notes'
]:
    page.clientside_callback(
        generate_input_javascript(component_id),
        Output('save-button', 'disabled'),
        Output('save-data', 'data'),
        Input(component_id, 'value'),
        State('save-data', 'data')
    )

for switch_id in [
    'reviewed',
    'flagged_for_review'
]:
    page.clientside_callback(
        generate_input_javascript(switch_id),
        Output('save-button', 'disabled'),
        Output('save-data', 'data'),
        Input(switch_id, 'checked'),
        State('save-data', 'data')
    )

page.clientside_callback(
    """
    color => color
    """,
    Output('add-tag-color-picker-input', 'value'),
    Input('add-tag-color-picker', 'value')
)

@page.callback(
    Output('add-types-chip-modal', 'opened'),
    Output('types', 'data'),
    Output('notifications-div', 'children'),
    Output('add-types-chip-submit-button', 'children'),
    Input('add-types-chip-submit-button', 'n_clicks'),
    State('add-types-chip-label-input', 'value'),
    State('add-types-chip-value-input', 'value')
)
def add_types_chip_submit_button_handler(n_clicks, label, value):
    if n_clicks and n_clicks > 0:
        DocumentType.create(label=label, value=value)
        notification = dmc.Notification(
            title='Success!',
            action='show',
            color='lime',
            id='save-success-notification',
            message='The document type has been added successfully',
            icon=[
                DashIconify(icon='carbon:checkmark')
            ]
        )
    else:
        notification = None

    select_values = DocumentType.get_select_values()

    return False, select_values, notification, no_update

@page.callback(
    Output('add-tag-modal', 'opened'),
    Output('tags', 'data'),
    Output('notifications-div', 'children'),
    Output('add-tag-submit-button', 'children'),
    Input('add-tag-submit-button', 'n_clicks'),
    State('add-tag-color-picker-input', 'value'),
    State('add-tag-text-input', 'value')
)
def add_tag_submit_button_handler(n_clicks, color, text):
    if n_clicks and n_clicks > 0:
        Tag.create(text=text, color=color)
        notification = dmc.Notification(
            title='Success!',
            action='show',
            color='lime',
            id='save-success-notification',
            message='The tag has been added successfully',
            icon=[
                DashIconify(icon='carbon:checkmark')
            ]
        )
    else:
        notification = None

    select_values = Tag.get_select_values()

    return False, select_values, notification, no_update

@page.callback(
    Output('add-language-modal', 'opened'),
    Output('language', 'data'),
    Output('notifications-div', 'children'),
    Output('add-language-submit-button', 'children'),
    Input('add-language-submit-button', 'n_clicks'),
    State('add-language-label-input', 'value'),
    State('add-language-value-input', 'value')
)
def add_language_submit_button_handler(n_clicks, label, value):
    if n_clicks and n_clicks > 0:
        Language.create(label=label, value=value)
        notification = dmc.Notification(
            title='Success!',
            action='show',
            color='lime',
            id='save-success-notification',
            message='The language has been added successfully',
            icon=[
                DashIconify(icon='carbon:checkmark')
            ]
        )
    else:
        notification = None

    select_values = Language.get_select_values()

    return False, select_values, notification, no_update

@page.callback(
    Output('add-jurisdiction-modal', 'opened'),
    Output('jurisdictions', 'data'),
    Output('notifications-div', 'children'),
    Output('add-jurisdiction-submit-button', 'children'),
    Input('add-jurisdiction-submit-button', 'n_clicks'),
    State('add-jurisdiction-label-input', 'value'),
    State('add-jurisdiction-value-input', 'value')
)
def add_jurisdiction_submit_button_handler(n_clicks, label, value):
    if n_clicks and n_clicks > 0:
        Jurisdiction.create(label=label, value=value)
        notification = dmc.Notification(
            title='Success!',
            action='show',
            color='lime',
            id='save-success-notification',
            message='The jurisdiction has been added successfully',
            icon=[
                DashIconify(icon='carbon:checkmark')
            ]
        )
    else:
        notification = None

    select_values = Jurisdiction.get_select_values()

    return False, select_values, notification, no_update

@page.callback(
    Output('add-file-type-modal', 'opened'),
    Output('file_type', 'data'),
    Output('notifications-div', 'children'),
    Output('add-file-type-submit-button', 'children'),
    Input('add-file-type-submit-button', 'n_clicks'),
    State('add-file-type-label-input', 'value'),
    State('add-file-type-mimetype-input', 'value'),
    State('add-file-type-suffix-input', 'value'),
    prevent_initial_call=True
)
def add_file_type_submit_button_handler(n_clicks, label, mimetype, suffix):
    if n_clicks and n_clicks > 0:
        FileType.create(label=label, mimetype=mimetype, suffix=suffix)
        notification = dmc.Notification(
            title='Success!',
            action='show',
            color='lime',
            id='save-success-notification',
            message='The file type has been added successfully',
            icon=[
                DashIconify(icon='carbon:checkmark')
            ]
        )
    else:
        notification = None

    select_values = FileType.get_select_values()

    return False, select_values, notification, no_update

for type_name in [
    'types-chip',
    'tag',
    'language',
    'jurisdiction',
    'file-type'
]:
    page.clientside_callback(
        """
        () => false
        """,
        Output(f'add-{type_name}-modal', 'opened'),
        Input(f'add-{type_name}-cancel-button', 'n_clicks')
    )

    page.clientside_callback(
        """
        n => n !== undefined
        """,
        Output(f'add-{type_name}-modal', 'opened'),
        Input(f'{type_name}-add-button', 'n_clicks')
    )

    if type_name not in ['tag', 'file-type']:
        page.clientside_callback(
            """
            () => ['', '']
            """,
            Input(f'add-{type_name}-modal', 'opened'),
            Output(f'add-{type_name}-label-input', 'value'),
            Output(f'add-{type_name}-value-input', 'value')
        )

page.clientside_callback(
    """
    () => ['#343353', '']
    """,
    Input('add-tag-modal', 'opened'),
    Output('add-tag-color-picker', 'value'),
    Output('add-tag-text-input', 'value')
)

page.clientside_callback(
    """
    () => ['', '', '']
    """,
    Input('add-file-type-modal', 'opened'),
    Output('add-file-type-label-input', 'value'),
    Output('add-file-type-mimetype-input', 'value'),
    Output('add-file-type-suffix-input', 'value')
)

def binary_radio_button_value(value):
    if value == True:
        return 'true'
    elif value == False:
        return 'false'
    else:
        return 'none'

def layout(document_version_id):
    try:
        document_version = DocumentVersion.get_one(
            int(document_version_id)
        )

        return html.Div([
            html.Div(id='notifications-div'),
            dcc.Store(id='save-data', data={
                'document_version_id': int(document_version_id)
            }),
            dmc.Modal(
                title='Add File Type',
                id='add-file-type-modal',
                centered=True,
                children=[
                    dmc.TextInput(
                        label='Label',
                        placeholder='Enter label here',
                        id='add-file-type-label-input',
                        icon=[
                            DashIconify(icon='carbon:document-unknown')
                        ],
                    ),
                    dmc.TextInput(
                        label='Mimetype',
                        placeholder='Enter mimetype here',
                        id='add-file-type-mimetype-input',
                        icon=[
                            DashIconify(icon='carbon:document-add')
                        ],
                    ),
                    dmc.TextInput(
                        label='Suffix',
                        placeholder='Enter suffix here',
                        id='add-file-type-suffix-input',
                        icon=[
                            DashIconify(icon='carbon:document-blank')
                        ],
                    ),
                    dmc.Space(h=20),
                    dmc.Group(
                        [
                            dmc.Button(
                                'Submit',
                                id='add-file-type-submit-button',
                                color='lime'
                            ),
                            dmc.Button(
                                'Cancel',
                                id='add-file-type-cancel-button',
                                color='orange',
                                variant='outline',
                            ),
                        ],
                        position='right',
                    ),
                ],
            ),
            dmc.Modal(
                title='Add Language',
                id='add-language-modal',
                centered=True,
                children=[
                    dmc.TextInput(
                        label='Label',
                        placeholder='Enter label here',
                        id='add-language-label-input',
                        icon=[
                            DashIconify(icon='carbon:label')
                        ],
                    ),
                    dmc.TextInput(
                        label='Value',
                        placeholder='Enter value here',
                        id='add-language-value-input',
                        icon=[
                            DashIconify(icon='carbon:string-text')
                        ],
                    ),
                    dmc.Space(h=20),
                    dmc.Group(
                        [
                            dmc.Button(
                                'Submit',
                                id='add-language-submit-button',
                                color='lime'
                            ),
                            dmc.Button(
                                'Cancel',
                                id='add-language-cancel-button',
                                color='orange',
                                variant='outline',
                            ),
                        ],
                        position='right',
                    ),
                ],
            ),
            dmc.Modal(
                title='Add Document Type',
                id='add-types-chip-modal',
                centered=True,
                children=[
                    dmc.TextInput(
                        label='Label',
                        placeholder='Enter label here',
                        id='add-types-chip-label-input',
                        icon=[
                            DashIconify(icon='carbon:label')
                        ],
                    ),
                    dmc.TextInput(
                        label='Value',
                        placeholder='Enter value here',
                        id='add-types-chip-value-input',
                        icon=[
                            DashIconify(icon='carbon:string-text')
                        ],
                    ),
                    dmc.Space(h=20),
                    dmc.Group(
                        [
                            dmc.Button(
                                'Submit',
                                id='add-types-chip-submit-button',
                                color='lime'
                            ),
                            dmc.Button(
                                'Cancel',
                                id='add-types-chip-cancel-button',
                                color='orange',
                                variant='outline',
                            ),
                        ],
                        position='right',
                    ),
                ],
            ),
            dmc.Modal(
                title='Add Tag',
                id='add-tag-modal',
                centered=True,
                children=[
                    dmc.TextInput(
                        id='add-tag-text-input',
                        label='Text',
                        placeholder='Enter text here',
                        icon=[
                            DashIconify(icon='carbon:tag')
                        ],
                    ),
                    dmc.Space(h=5),
                    dmc.Center(
                        dmc.Stack(
                            [
                                dmc.Text(
                                    'Color',
                                    weight=500,
                                    size='sm',
                                    style={'marginBottom': '4px'}
                                ),
                                dmc.ColorPicker(
                                    id='add-tag-color-picker',
                                    format='hex',
                                    value=DEFAULT_TAG_COLOR,
                                    swatches=[
                                        '#25262b', '#868e96', '#fa5252', '#e64980', '#be4bdb', '#7950f2',
                                        '#4c6ef5', '#228be6', '#15aabf', '#12b886', '#40c057', '#82c91e',
                                        '#fab005', '#fd7e14'
                                    ]
                                ),
                            ],
                            spacing='sm',
                            style={'gap': '0px', 'textAlign': 'left'}
                        )
                    ),
                    dmc.TextInput(
                        id='add-tag-color-picker-input',
                        label='Color',
                        class_name='disabled-input',
                        icon=[
                            DashIconify(icon='carbon:color-palette')
                        ],
                    ),
                    dmc.Space(h=20),
                    dmc.Group(
                        [
                            dmc.Button(
                                'Submit',
                                id='add-tag-submit-button',
                                color='lime'
                            ),
                            dmc.Button(
                                'Cancel',
                                id='add-tag-cancel-button',
                                color='orange',
                                variant='outline',
                            ),
                        ],
                        position='right',
                    ),
                ],
            ),
            dmc.Modal(
                title='Add Jurisdiction',
                id='add-jurisdiction-modal',
                centered=True,
                children=[
                    dmc.TextInput(
                        label='Label',
                        placeholder='Enter label here',
                        id='add-jurisdiction-label-input',
                        icon=[
                            DashIconify(icon='carbon:label')
                        ],
                    ),
                    dmc.TextInput(
                        label='Value',
                        placeholder='Enter value here',
                        id='add-jurisdiction-value-input',
                        icon=[
                            DashIconify(icon='carbon:string-text')
                        ],
                    ),
                    dmc.Space(h=20),
                    dmc.Group(
                        [
                            dmc.Button(
                                'Submit',
                                id='add-jurisdiction-submit-button',
                                color='lime'
                            ),
                            dmc.Button(
                                'Cancel',
                                id='add-jurisdiction-cancel-button',
                                color='orange',
                                variant='outline',
                            ),
                        ],
                        position='right',
                    ),
                ],
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        [
                                            dmc.TextInput(
                                                label='Title',
                                                value=document_version.title,
                                                id='title'
                                            ),
                                            dmc.Space(h=8),
                                            dmc.Grid(
                                                [
                                                    dmc.Col(
                                                        dmc.DatePicker(
                                                            label='Effective Date',
                                                            value=document_version.effective_date.date(),
                                                            id='effective-date-input',
                                                            class_name='disabled-input'
                                                        ),
                                                        span=9
                                                    ),
                                                    dmc.Col(
                                                        dmc.TimeInput(
                                                            label='_',
                                                            withSeconds=True,
                                                            value=document_version.effective_date,
                                                            id='effective-time-input',
                                                            class_name='disabled-input'
                                                        ),
                                                        span=3
                                                    ),
                                                ],
                                                class_name='date-time-picker'
                                            ),
                                            dmc.Grid(
                                                [
                                                    dmc.Col(
                                                        dmc.DatePicker(
                                                            label='Termination Date',
                                                            value=document_version.termination_date.date(),
                                                            id='termination-date-input',
                                                            class_name='disabled-input'
                                                        ),
                                                        span=9
                                                    ),
                                                    dmc.Col(
                                                        dmc.TimeInput(
                                                            label='_',
                                                            withSeconds=True,
                                                            value=document_version.termination_date,
                                                            id='termination-time-input',
                                                            class_name='disabled-input'
                                                        ),
                                                        span=3
                                                    ),
                                                ],
                                                class_name='date-time-picker'
                                            )
                                        ],
                                        span=7
                                    ),
                                    dmc.Col(
                                        [
                                            dmc.TextInput(
                                                label='Document Version Slug',
                                                value=document_version.slug,
                                                id='slug'
                                            ),
                                            dmc.TextInput(
                                                label='Database ID',
                                                value=str(document_version.id),
                                                class_name='disabled-input',
                                            ),
                                            dmc.NumberInput(
                                                label='Version #',
                                                value=document_version.version_num,
                                                class_name='disabled-input'
                                            )
                                        ],
                                        span=5
                                    )
                                ]
                            ),
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        dmc.TextInput(
                                            label='Document Version Issuer Short Name',
                                            value=document_version.issuer['short_name'],
                                            class_name='disabled-input'
                                        ),
                                        span=6
                                    ),
                                    dmc.Col(
                                        dmc.TextInput(
                                            label='Document Version Issuer Long Name',
                                            value=document_version.issuer['long_name'],
                                            class_name='disabled-input'
                                        ),
                                        span=6
                                    )
                                ]
                            ),
                            html.Div(
                                [
                                    dmc.TextInput(
                                        label='Source',
                                        value=document_version.source,
                                        id='source-input'
                                    ),
                                    dcc.Link(
                                        DashIconify(
                                            icon='carbon:copy-link',
                                            width=20
                                        ),
                                        href=document_version.source,
                                        target='_blank',
                                        style={
                                            'position': 'absolute',
                                            'right': '4px',
                                            'bottom': '4px'
                                        }
                                    )
                                ],
                                style={'position': 'relative'}
                            ),
                            dmc.TextInput(
                                label='Source Notes',
                                value=document_version.source_notes,
                                placeholder='Enter source notes here',
                                id='source_notes'
                            ),
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        html.Div(
                                            [
                                                dmc.Select(
                                                    label='File Type',
                                                    placeholder='Select file type',
                                                    id='file_type',
                                                    value=str(document_version.file_type_id)
                                                ),
                                                dmc.Button(
                                                    DashIconify(
                                                        icon='carbon:add',
                                                        width=30
                                                    ),
                                                    variant='filled',
                                                    color='indigo',
                                                    id='file-type-add-button'
                                                )
                                            ],
                                            className='select-button-group'
                                        ),
                                        span=6
                                    ),
                                    dmc.Col(
                                        html.Div(
                                            [
                                                dmc.Select(
                                                    label='Language',
                                                    placeholder='Select language',
                                                    id='language',
                                                    value=str(document_version.language_id)
                                                ),
                                                dmc.Button(
                                                    DashIconify(
                                                        icon='carbon:add',
                                                        width=30
                                                    ),
                                                    variant='filled',
                                                    color='indigo',
                                                    id='language-add-button'
                                                )
                                            ],
                                            className='select-button-group'
                                        ),
                                        span=6
                                    )
                                ]
                            ),
                            html.Div(
                                [
                                    dmc.MultiSelect(
                                        label='Tags',
                                        searchable=True,
                                        nothingFound='No tags found',
                                        placeholder='Enter tags',
                                        id='tags',
                                        value=[str(t['id']) for t in document_version.tags]
                                    ),
                                    dmc.Button(
                                        DashIconify(
                                            icon='carbon:add',
                                            width=30
                                        ),
                                        variant='filled',
                                        color='indigo',
                                        id='tag-add-button'
                                    )
                                ],
                                className='select-button-group'
                            ),
                            html.Div(
                                [
                                    dmc.MultiSelect(
                                        label='Jurisdictions',
                                        searchable=True,
                                        nothingFound='No jurisdictions found',
                                        placeholder='Enter jurisdictions',
                                        id='jurisdictions',
                                        value=[str(t['id']) for t in document_version.jurisdictions]
                                    ),
                                    dmc.Button(
                                        DashIconify(
                                            icon='carbon:add',
                                            width=30
                                        ),
                                        variant='filled',
                                        color='indigo',
                                        id='jurisdiction-add-button'
                                    )
                                ],
                                className='select-button-group'
                            ),
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        dmc.Textarea(
                                            label='Notes',
                                            placeholder='Add notes here',
                                            autosize=True,
                                            minRows=3,
                                            value=document_version.notes,
                                            id='notes'
                                        ),
                                        span=6
                                    ),
                                    dmc.Col(
                                        dmc.JsonInput(
                                            label='Variables',
                                            placeholder='Put JSON variables here.',
                                            validationError='Invalid JSON',
                                            formatOnBlur=True,
                                            autosize=True,
                                            minRows=3,
                                            class_name='variables-json-input',
                                            value=json.dumps(
                                                document_version.variables,
                                                sort_keys=True,
                                                indent=2
                                            ),
                                            id='variables'
                                        ),
                                        span=6
                                    ),
                                ]
                            )
                        ],
                        span=9
                    ),
                    dmc.Col(
                        [
                            dmc.Stack(
                                [
                                    dmc.Button(
                                        'Save',
                                        size='md',
                                        color='lime',
                                        style={'width': '100%'},
                                        leftIcon=[
                                            DashIconify(icon='carbon:save', width=25)
                                        ],
                                        class_name='document-save-button',
                                        id='save-button',
                                        disabled=True
                                    ),
                                    dmc.Divider(variant='solid'),
                                    dmc.Switch(
                                        size='xl',
                                        radius='xl',
                                        color='lime',
                                        label='Is Reviewed',
                                        offLabel='No',
                                        checked=document_version.reviewed,
                                        id='reviewed'
                                    ),
                                    dmc.Switch(
                                        size='xl',
                                        radius='xl',
                                        color='red',
                                        label='Is Flagged for Review',
                                        offLabel='No',
                                        checked=document_version.flagged_for_review,
                                        id='flagged_for_review'
                                    ),
                                    dmc.Divider(variant='solid'),
                                    dmc.Stack(
                                        [
                                            dmc.Text(
                                                'Importance',
                                                weight=500,
                                                size='sm',
                                                style={'marginBottom': '2px'}
                                            ),
                                            dmc.Slider(
                                                value=document_version.importance,
                                                marks=[{'value': i, 'label': i} for i in range(1, 11)],
                                                min=1,
                                                max=10,
                                                step=1,
                                                size='md',
                                                id='importance'
                                            )
                                        ],
                                        spacing='sm',
                                        style={'gap': '0px', 'textAlign': 'left'}
                                    ),
                                    dmc.Space(h=15),
                                    dmc.Divider(variant='solid'),
                                    dmc.Stack(
                                        [
                                            dmc.Text('Has Relevant Information', weight=500, size='sm'),
                                            dmc.RadioGroup(
                                                data=[
                                                    {'label': 'Unknown', 'value': 'none'},
                                                    {'label': 'Yes', 'value': 'true'},
                                                    {'label': 'No', 'value': 'false'},
                                                ],
                                                size='md',
                                                id='has_relevant_information',
                                                value=binary_radio_button_value(
                                                    document_version.has_relevant_information
                                                )
                                            )
                                        ],
                                        spacing='xs',
                                        style={'gap': '3px', 'textAlign': 'left'}
                                    ),
                                    dmc.Stack(
                                        [
                                            dmc.Text('Is Foreign Language', weight=500, size='sm'),
                                            dmc.RadioGroup(
                                                data=[
                                                    {'label': 'Unknown', 'value': 'none'},
                                                    {'label': 'Yes', 'value': 'true'},
                                                    {'label': 'No', 'value': 'false'},
                                                ],
                                                size='md',
                                                id='is_foreign_language',
                                                value=binary_radio_button_value(
                                                    document_version.is_foreign_language
                                                )
                                            )
                                        ],
                                        spacing='xs',
                                        style={'gap': '6px', 'textAlign': 'left'}
                                    ),
                                    dmc.Stack(
                                        [
                                            dmc.Text('Is Malformed', weight=500, size='sm'),
                                            dmc.RadioGroup(
                                                data=[
                                                    {'label': 'Unknown', 'value': 'none'},
                                                    {'label': 'Yes', 'value': 'true'},
                                                    {'label': 'No', 'value': 'false'},
                                                ],
                                                size='md',
                                                id='is_malformed',
                                                value=binary_radio_button_value(
                                                    document_version.is_malformed
                                                )
                                            )
                                        ],
                                        spacing='xs',
                                        style={'gap': '6px', 'textAlign': 'left'}
                                    ),
                                    dmc.Stack(
                                        [
                                            dmc.Text('Is Empty', weight=500, size='sm'),
                                            dmc.RadioGroup(
                                                data=[
                                                    {'label': 'Unknown', 'value': 'none'},
                                                    {'label': 'Yes', 'value': 'true'},
                                                    {'label': 'No', 'value': 'false'},
                                                ],
                                                size='md',
                                                id='is_empty',
                                                value=binary_radio_button_value(
                                                    document_version.is_empty
                                                )
                                            )
                                        ],
                                        spacing='xs',
                                        style={
                                            'gap': '6px',
                                            'textAlign': 'left',
                                            'marginBottom': '6px'
                                        }
                                    ),
                                    dmc.Divider(variant='solid'),
                                    dmc.Stack(
                                        [
                                            dmc.Grid(
                                                [
                                                    dmc.Col(
                                                        dmc.Text(
                                                            'Document Version Types',
                                                            weight=500,
                                                            size='sm',
                                                            style={'marginBottom': '6px'}
                                                        ),
                                                        span=10
                                                    ),
                                                    dmc.Col(
                                                        dmc.Button(
                                                            DashIconify(
                                                                icon='carbon:add',
                                                                width=30
                                                            ),
                                                            variant='filled',
                                                            color='indigo',
                                                            style={'padding': '0'},
                                                            id='types-chip-add-button'
                                                        ),
                                                        span=2
                                                    )
                                                ]
                                            ),
                                            dmc.Chips(
                                                data=[],
                                                multiple=True,
                                                id='types',
                                                value=[str(t['id']) for t in document_version.types]
                                            )
                                        ],
                                        spacing='sm',
                                        style={'gap': '0px', 'textAlign': 'left'}
                                    )
                                ],
                                class_name='switch-group',
                                spacing='xs'
                            )
                        ],
                        style={'textAlign': 'right'},
                        span=3
                    )
                ]
            )
        ])

    except Exception as e:
        print('error', e)
        return dmc.Alert(
            [
                html.Span('The document version with an ID of '),
                html.Strong(
                    html.Em(f'"{document_version_id}"')
                ),
                html.Span(' does not exist.')
            ],
            title='Document Version Not Found',
            icon=[
                DashIconify(icon='carbon:close-filled', height=36)
            ],
            color='red',
            variant='outline'
        )

page.layout = layout
