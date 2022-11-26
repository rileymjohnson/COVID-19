from importlib import import_module
from pathlib import Path


def register_pages(app, pages_folder='./covid19app/pages/'):
    for page_module_file in Path(pages_folder).glob('*.py'):
        if not page_module_file.stem.startswith('_'):
            page_module_path = '.'.join(
                page_module_file.with_suffix('').parts
            ) 

            module = import_module(page_module_path)

            if hasattr(module, 'page'):
                additional_args = {}

                if hasattr(module.page, 'path_template'):
                    additional_args['path_template'] = module.page.path_template

                if hasattr(module.page, 'order'):
                    additional_args['order'] = module.page.order

                module.page.register(
                    app,
                    module.page.path,
                    module.page.title,
                    name=module.page.title,
                    title=f'{app.title} - {module.page.title}',
                    image=module.page.icon,
                    **additional_args
                )
