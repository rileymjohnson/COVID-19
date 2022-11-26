from dash_extensions.enrich import DashBlueprint, html, callback_context, ALL, Output, Input, State, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import json

from covid19app.data import Document, Language, Jurisdiction, FileType, Tag, DocumentType


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
page.path = '/document'
page.title = 'Document'
page.icon = 'carbon:document-view'
page.path_template = '/document/<document_id>'
page.order = -1

DEFAULT_TAG_COLOR = '#343353'

page.clientside_callback(
    """
    chips => console.log('chips', chips)
    """,
    Input('types-chips', 'value')
)

page.clientside_callback(
    """
    tags => console.log('tags', tags)
    """,
    Input('tag-multi-select', 'value')
)

page.clientside_callback(
    """
    jurisdictions => console.log('jurisdictions', jurisdictions)
    """,
    Input('jurisdiction-multi-select', 'value')
)

page.clientside_callback(
    """
    language => console.log('language', language)
    """,
    Input('language-select', 'value')
)

page.clientside_callback(
    """
    file_type => console.log('file_type', file_type)
    """,
    Input('file-type-select', 'value')
)

page.clientside_callback(
    """
    notes => console.log('notes', notes)
    """,
    Input('notes-input', 'value')
)

page.clientside_callback(
    """
    variables => console.log('variables', variables)
    """,
    Input('variables-input', 'value')
)

page.clientside_callback(
    """
    effective_date => console.log('effective_date', effective_date)
    """,
    Input('effective-date-input', 'value')
)

page.clientside_callback(
    """
    effective_time => console.log('effective_time', effective_time)
    """,
    Input('effective-time-input', 'value')
)

page.clientside_callback(
    """
    termination_date => console.log('termination_date', termination_date)
    """,
    Input('termination-date-input', 'value')
)

page.clientside_callback(
    """
    termination_time => console.log('termination_time', termination_time)
    """,
    Input('termination-time-input', 'value')
)

page.clientside_callback(
    """
    importance => console.log('importance', importance)
    """,
    Input('importance-slider', 'value')
)

page.clientside_callback(
    """
    title => console.log('title', title)
    """,
    Input('title-input', 'value')
)

page.clientside_callback(
    """
    slug => console.log('slug', slug)
    """,
    Input('document-slug-input', 'value')
)

page.clientside_callback(
    """
    source => console.log('source', source)
    """,
    Input('source-input', 'value')
)

page.clientside_callback(
    """
    source_notes => console.log('source_notes', source_notes)
    """,
    Input('source-notes-input', 'value')
)

page.clientside_callback(
    """
    reviewed => console.log('reviewed', reviewed)
    """,
    Input('is-reviewed-switch', 'checked')
)

page.clientside_callback(
    """
    flagged_for_review => console.log('flagged_for_review', flagged_for_review)
    """,
    Input('is-flagged-for-review-switch', 'checked')
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
    Output('types-chips', 'data'),
    Input('add-types-chip-submit-button', 'n_clicks'),
    State('add-types-chip-label-input', 'value'),
    State('add-types-chip-value-input', 'value')
)
def add_types_chip_submit_button_handler(n_clicks, label, value):
    if n_clicks and n_clicks > 0:
        DocumentType.create(label=label, value=value)

    return False, DocumentType.get_select_values()

@page.callback(
    Output('add-tag-modal', 'opened'),
    Output('tag-multi-select', 'data'),
    Input('add-tag-submit-button', 'n_clicks'),
    State('add-tag-color-picker-input', 'value'),
    State('add-tag-text-input', 'value')
)
def add_tag_submit_button_handler(n_clicks, color, text):
    if n_clicks and n_clicks > 0:
        Tag.create(text=text, color=color)

    return False, Tag.get_select_values()

@page.callback(
    Output('add-language-modal', 'opened'),
    Output('language-select', 'data'),
    Input('add-language-submit-button', 'n_clicks'),
    State('add-language-label-input', 'value'),
    State('add-language-value-input', 'value')
)
def add_language_submit_button_handler(n_clicks, label, value):
    if n_clicks and n_clicks > 0:
        Language.create(label=label, value=value)

    return False, Language.get_select_values()

@page.callback(
    Output('add-jurisdiction-modal', 'opened'),
    Output('jurisdiction-multi-select', 'data'),
    Input('add-jurisdiction-submit-button', 'n_clicks'),
    State('add-jurisdiction-label-input', 'value'),
    State('add-jurisdiction-value-input', 'value')
)
def add_jurisdiction_submit_button_handler(n_clicks, label, value):
    if n_clicks and n_clicks > 0:
        Jurisdiction.create(label=label, value=value)

    return False, Jurisdiction.get_select_values()

@page.callback(
    Output('add-file-type-modal', 'opened'),
    Output('file-type-select', 'data'),
    Input('add-file-type-submit-button', 'n_clicks'),
    State('add-file-type-label-input', 'value'),
    State('add-file-type-mimetype-input', 'value'),
    State('add-file-type-suffix-input', 'value')
)
def add_file_type_submit_button_handler(n_clicks, label, mimetype, suffix):
    if n_clicks and n_clicks > 0:
        FileType.create(label=label, mimetype=mimetype, suffix=suffix)

    return False, FileType.get_select_values()

page.clientside_callback(
    """
    () => false
    """,
    Output('add-types-chip-modal', 'opened'),
    Input('add-types-chip-cancel-button', 'n_clicks')
)

page.clientside_callback(
    """
    () => false
    """,
    Output('add-tag-modal', 'opened'),
    Input('add-tag-cancel-button', 'n_clicks')
)

page.clientside_callback(
    """
    () => false
    """,
    Output('add-language-modal', 'opened'),
    Input('add-language-cancel-button', 'n_clicks')
)

page.clientside_callback(
    """
    () => false
    """,
    Output('add-jurisdiction-modal', 'opened'),
    Input('add-jurisdiction-cancel-button', 'n_clicks')
)

page.clientside_callback(
    """
    () => false
    """,
    Output('add-file-type-modal', 'opened'),
    Input('add-file-type-cancel-button', 'n_clicks')
)

page.clientside_callback(
    """
    () => ['', '']
    """,
    Input('add-types-chip-modal', 'opened'),
    Output('add-types-chip-label-input', 'value'),
    Output('add-types-chip-value-input', 'value')
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
    () => ['', '']
    """,
    Input('add-language-modal', 'opened'),
    Output('add-language-label-input', 'value'),
    Output('add-language-value-input', 'value')
)

page.clientside_callback(
    """
    () => ['', '']
    """,
    Input('add-jurisdiction-modal', 'opened'),
    Output('add-jurisdiction-label-input', 'value'),
    Output('add-jurisdiction-value-input', 'value')
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

@page.callback(
    Output({'type': 'multi-switch-is-guidance-document', 'index': ALL}, 'variant'),
    Input({'type': 'multi-switch-is-guidance-document', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def multi_switch_has_relevant_information_handler(_):
    button_id = callback_context.triggered_id
    value = [None, True, False][button_id['index']]

    print('has_relevant_information', value)

    return [
        'filled' if i['id'] == button_id else 'outline' \
            for i in callback_context.args_grouping
    ]

@page.callback(
    Output({'type': 'multi-switch-is-foreign-language', 'index': ALL}, 'variant'),
    Input({'type': 'multi-switch-is-foreign-language', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def multi_switch_is_foreign_language_handler(_):
    button_id = callback_context.triggered_id
    value = [None, True, False][button_id['index']]

    print('is_foreign_language', value)

    return [
        'filled' if i['id'] == button_id else 'outline' \
            for i in callback_context.args_grouping
    ]

@page.callback(
    Output({'type': 'multi-switch-is-malformed', 'index': ALL}, 'variant'),
    Input({'type': 'multi-switch-is-malformed', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def multi_switch_is_malformed_handler(_):
    button_id = callback_context.triggered_id
    value = [None, True, False][button_id['index']]

    print('is_malformed', value)

    return [
        'filled' if i['id'] == button_id else 'outline' \
            for i in callback_context.args_grouping
    ]

@page.callback(
    Output({'type': 'multi-switch-is-empty', 'index': ALL}, 'variant'),
    Input({'type': 'multi-switch-is-empty', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def multi_switch_is_empty_handler(_):
    button_id = callback_context.triggered_id
    value = [None, True, False][button_id['index']]

    print('is_empty', value)

    return [
        'filled' if i['id'] == button_id else 'outline' \
            for i in callback_context.args_grouping
    ]

page.clientside_callback(
    """
    n => n !== undefined
    """,
    Output('add-types-chip-modal', 'opened'),
    Input('types-chips-add-button', 'n_clicks')
)

page.clientside_callback(
    """
    n => n !== undefined
    """,
    Output('add-file-type-modal', 'opened'),
    Input('file-type-add-button', 'n_clicks')
)

page.clientside_callback(
    """
    n => n !== undefined
    """,
    Output('add-language-modal', 'opened'),
    Input('language-add-button', 'n_clicks')
)

page.clientside_callback(
    """
    n => n !== undefined
    """,
    Output('add-tag-modal', 'opened'),
    Input('tag-add-button', 'n_clicks')
)

page.clientside_callback(
    """
    n => n !== undefined
    """,
    Output('add-jurisdiction-modal', 'opened'),
    Input('jurisdiction-add-button', 'n_clicks')
)

def layout(document_id):
    try:
        document = Document.get_one(int(document_id))

        return html.Div([
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
                        class_name='disabled-text-input',
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
                                                value=document.title,
                                                id='title-input'
                                            ),
                                            dmc.Space(h=8),
                                            dmc.Grid(
                                                [
                                                    dmc.Col(
                                                        dmc.DatePicker(
                                                            label='Effective Date',
                                                            value=document.effective_date.date(),
                                                            id='effective-date-input'
                                                        ),
                                                        span=9
                                                    ),
                                                    dmc.Col(
                                                        dmc.TimeInput(
                                                            label='_',
                                                            withSeconds=True,
                                                            value=document.effective_date,
                                                            id='effective-time-input'
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
                                                            value=document.termination_date.date(),
                                                            id='termination-date-input'
                                                        ),
                                                        span=9
                                                    ),
                                                    dmc.Col(
                                                        dmc.TimeInput(
                                                            label='_',
                                                            withSeconds=True,
                                                            value=document.termination_date,
                                                            id='termination-time-input'
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
                                                label='Document Slug',
                                                value=document.slug,
                                                id='document-slug-input'
                                            ),
                                            dmc.TextInput(
                                                label='Database ID',
                                                value=str(document.id),
                                                class_name='disabled-text-input',
                                            ),
                                            dmc.NumberInput(
                                                label='# Versions',
                                                value=document.num_versions,
                                                class_name='disabled-number-input'
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
                                            label='Document Issuer Short Name',
                                            value=document.issuer.short_name,
                                            class_name='disabled-text-input'
                                        ),
                                        span=6
                                    ),
                                    dmc.Col(
                                        dmc.TextInput(
                                            label='Document Issuer Long Name',
                                            value=document.issuer.long_name,
                                            class_name='disabled-text-input'
                                        ),
                                        span=6
                                    )
                                ]
                            ),
                            html.Div(
                                [
                                    dmc.TextInput(
                                        label='Source',
                                        value=document.source,
                                        id='source-input'
                                    ),
                                    dcc.Link(
                                        DashIconify(
                                            icon='carbon:copy-link',
                                            width=20
                                        ),
                                        href=document.source,
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
                                value=document.source_notes,
                                placeholder='Enter source notes here',
                                id='source-notes-input'
                            ),
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        html.Div(
                                            [
                                                dmc.Select(
                                                    label='File Type',
                                                    placeholder='Select file type',
                                                    id='file-type-select',
                                                    value=str(document.file_type_id)
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
                                                    id='language-select',
                                                    value=str(document.language_id)
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
                                        id='tag-multi-select',
                                        value=[str(t['id']) for t in document.tags]
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
                                        id='jurisdiction-multi-select',
                                        value=[str(t['id']) for t in document.jurisdictions]
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
                                            value=document.notes,
                                            id='notes-input'
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
                                            value=json.dumps(document.variables),
                                            id='variables-input'
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
                                        disabled=True
                                    ),
                                    dmc.Divider(variant='solid'),
                                    dmc.Switch(
                                        size='xl',
                                        radius='xl',
                                        color='lime',
                                        label='Is Reviewed',
                                        offLabel='No',
                                        checked=document.reviewed,
                                        id='is-reviewed-switch'
                                    ),
                                    dmc.Switch(
                                        size='xl',
                                        radius='xl',
                                        color='red',
                                        label='Is Flagged for Review',
                                        offLabel='No',
                                        checked=document.flagged_for_review,
                                        id='is-flagged-for-review-switch'
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
                                                value=document.importance,
                                                marks=[{'value': i, 'label': i} for i in range(1, 11)],
                                                min=1,
                                                max=10,
                                                step=1,
                                                size='md',
                                                id='importance-slider'
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
                                            dmc.Group(
                                                [
                                                    dmc.Button(
                                                        'None',
                                                        variant='filled' if document.has_relevant_information is None else 'outline',
                                                        color='indigo',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-guidance-document', 'index': 0}
                                                    ),
                                                    dmc.Button(
                                                        'True',
                                                        variant='filled' if document.has_relevant_information == True else 'outline',
                                                        color='lime',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-guidance-document', 'index': 1}
                                                    ),
                                                    dmc.Button(
                                                        'False',
                                                        variant='filled' if document.has_relevant_information == False else 'outline',
                                                        color='red',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-guidance-document', 'index': 2}
                                                    ),
                                                ],
                                                style={'width': '100%'},
                                                spacing='xs',
                                                class_name='button-group'
                                            )
                                        ],
                                        spacing='xs',
                                        style={'gap': '6px', 'textAlign': 'left'}
                                    ),
                                    dmc.Stack(
                                        [
                                            dmc.Text('Is Foreign Language', weight=500, size='sm'),
                                            dmc.Group(
                                                [
                                                    dmc.Button(
                                                        'None',
                                                        variant='filled' if document.is_foreign_language is None else 'outline',
                                                        color='indigo',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-foreign-language', 'index': 0}
                                                    ),
                                                    dmc.Button(
                                                        'True',
                                                        variant='filled' if document.is_foreign_language == True else 'outline',
                                                        color='lime',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-foreign-language', 'index': 1}
                                                    ),
                                                    dmc.Button(
                                                        'False',
                                                        variant='filled' if document.is_foreign_language == False else 'outline',
                                                        color='red',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-foreign-language', 'index': 2}
                                                    ),
                                                ],
                                                style={'width': '100%'},
                                                spacing='xs',
                                                class_name='button-group'
                                            )
                                        ],
                                        spacing='xs',
                                        style={'gap': '6px', 'textAlign': 'left'}
                                    ),
                                    dmc.Stack(
                                        [
                                            dmc.Text('Is Malformed', weight=500, size='sm'),
                                            dmc.Group(
                                                [
                                                    dmc.Button(
                                                        'None',
                                                        variant='filled' if document.is_malformed is None else 'outline',
                                                        color='indigo',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-malformed', 'index': 0}
                                                    ),
                                                    dmc.Button(
                                                        'True',
                                                        variant='filled' if document.is_malformed == True else 'outline',
                                                        color='lime',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-malformed', 'index': 1}
                                                    ),
                                                    dmc.Button(
                                                        'False',
                                                        variant='filled' if document.is_malformed == False else 'outline',
                                                        color='red',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-malformed', 'index': 2}
                                                    ),
                                                ],
                                                style={'width': '100%'},
                                                spacing='xs',
                                                class_name='button-group'
                                            )
                                        ],
                                        spacing='xs',
                                        style={'gap': '6px', 'textAlign': 'left'}
                                    ),
                                    dmc.Stack(
                                        [
                                            dmc.Text('Is Empty', weight=500, size='sm'),
                                            dmc.Group(
                                                [
                                                    dmc.Button(
                                                        'None',
                                                        variant='filled' if document.is_empty is None else 'outline',
                                                        color='indigo',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-empty', 'index': 0}
                                                    ),
                                                    dmc.Button(
                                                        'True',
                                                        variant='filled' if document.is_empty == True else 'outline',
                                                        color='lime',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-empty', 'index': 1}
                                                    ),
                                                    dmc.Button(
                                                        'False',
                                                        variant='filled' if document.is_empty == False else 'outline',
                                                        color='red',
                                                        size='xs',
                                                        id={'type': 'multi-switch-is-empty', 'index': 2}
                                                    ),
                                                ],
                                                style={'width': '100%'},
                                                spacing='xs',
                                                class_name='button-group'
                                            )
                                        ],
                                        spacing='xs',
                                        style={'gap': '6px', 'textAlign': 'left'}
                                    ),
                                    dmc.Divider(variant='solid'),
                                    dmc.Stack(
                                        [
                                            dmc.Grid(
                                                [
                                                    dmc.Col(
                                                        dmc.Text(
                                                            'Document Types',
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
                                                            id='types-chips-add-button'
                                                        ),
                                                        span=2
                                                    )
                                                ]
                                            ),
                                            dmc.Chips(
                                                data=[],
                                                multiple=True,
                                                id='types-chips',
                                                value=[str(t['id']) for t in document.types]
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
                html.Span('The document with an ID of '),
                html.Strong(
                    html.Em(f'"{document_id}"')
                ),
                html.Span(' does not exist.')
            ],
            title='Document Not Found',
            icon=[
                DashIconify(icon='carbon:close-filled', height=36)
            ],
            color='red',
            variant='outline'
        )

page.layout = layout
