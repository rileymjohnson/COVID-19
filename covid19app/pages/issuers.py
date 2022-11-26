from dash_extensions.enrich import DashBlueprint, dcc, html, Input, Output, ALL
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from covid19app.data import DocumentIssuer


page = DashBlueprint()
page.path = '/document-issuers'
page.title = 'Document Issuers'
page.icon = 'carbon:license-draft'
page.order = 3

def layout():
    document_issuers = DocumentIssuer.get_values()

    return html.Div([
        dmc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th('Database ID'),
                            html.Th('Issuer Short Name'),
                            html.Th('Issuer Long Name'),
                            html.Th('# Documents'),
                            html.Th('# Document Versions')
                        ]
                    )
                ),
                html.Tbody(
                    [
                    html.Tr([
                        html.Td(issuer['id']),
                        html.Td(issuer['short_name']),
                        html.Td(issuer['long_name']),
                        html.Td(f'{issuer["num_documents"]:,}'),
                        html.Td(f'{issuer["num_document_versions"]:,}')
                    ]) for issuer in document_issuers]
                )
            ]
        )
    ])

page.layout = layout
