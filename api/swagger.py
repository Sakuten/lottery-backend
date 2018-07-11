import os
from flasgger import Swagger, swag_from
import yaml
import api

with open('api/spec/template.yml') as f:
    template = yaml.load(f)
swag = Swagger(template=template)


def spec(path, methods=None):
    spec_path = os.path.join(api.__path__[0], 'spec/routes', path)
    return swag_from(spec_path, methods=methods)
