from dash_extensions.enrich import DashProxy, NoOutputTransform, MultiplexerTransform

from covid19app.layout import register_layout
from covid19app.pages import register_pages

app = DashProxy(
    title='CDC COVID-19 Guidance Explorer',
    pages_folder='./covid19app/pages',
    assets_folder='./covid19app/assets',
    suppress_callback_exceptions=True,
    use_pages=True,
    transforms=[
        MultiplexerTransform(),
        NoOutputTransform()
    ]
)

register_pages(app)
register_layout(app)

if __name__ == '__main__':
    app.run_server()
