from dash_extensions.enrich import DashBlueprint, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash_extensions import Lottie


page = DashBlueprint()
page.path = '/'
page.title = 'Home'
page.icon = 'carbon:home'
page.order = 0

page.layout = html.Div([
    Lottie(
        isClickToPauseDisabled=True,
        options={
            'loop': True,
            'autoplay': True,
            'rendererSettings': {
                'preserveAspectRatio': 'xMidYMid slice'
            }
        },
        width='60%',
        url='/assets/lottie-animation-document-search.json'
    ),
    dmc.Center(
        dcc.Link(
            dmc.Button(
                'Explore the documents',
                size='lg',
                color='violet',
                variant='filled',
                leftIcon=[
                    DashIconify(
                        icon='carbon:search-locate',
                        width=25
                    )
                ]
            ),
            href='/documents'
        )
    ),
    dmc.Space(h=20)
])
