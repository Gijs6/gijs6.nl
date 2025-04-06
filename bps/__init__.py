import os
import importlib

def load_blueprints():
    blueprints = []
    base_path = os.path.dirname(__file__)

    for file_item in os.scandir(base_path):
        if file_item.is_dir():
            routes_path = os.path.join(file_item.path, 'routes.py')
            if os.path.isfile(routes_path):
                module_path = f'bps.{file_item.name}.routes'
                module = importlib.import_module(module_path)

                for attr in dir(module):
                    if attr.endswith('_bp'):
                        bp = getattr(module, attr)
                        blueprints.append((bp, f'/{file_item.name}'))

    return blueprints
