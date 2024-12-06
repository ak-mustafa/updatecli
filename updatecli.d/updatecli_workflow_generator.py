import os
import yaml
from jinja2 import Template


ENVIRONMENTS = ['mgmt', 'dev', 'stg', 'prd']
TOOLS = {
    'azure-workload-identity': {
        'url' : 'https://azure.github.io/azure-workload-identity/charts',
        'name' : 'workload-identity-webhook'
    },
}

for env in ENVIRONMENTS:
    for tool in TOOLS:
        input_file = f'./charts/argocd/utils/{tool}.yaml'
        output_file = f'/tmp/workflows/{tool}-{env}-helm.yaml'
      
        if os.path.exists(input_file):
            with open(input_file, 'r') as file:
                yaml_data = yaml.safe_load(file)
                if env == 'dev':
                    row = 1
                elif env == 'stg':
                    row = 2
                elif env == 'prd':
                    row = 3
                elif env == 'mgmt':
                    row = 0
                elements = yaml_data['spec']['generators'][0]['list']['elements'][row]

            with open('./updatecli.d/updatecli_helm_utils.j2', 'r') as template_file:
                template_str = template_file.read()

            template = Template(template_str)
            rendered_output = template.render(elements=elements, tool=tool, environment=env, url=TOOLS[tool]['url'], chart_name=TOOLS[tool]['name'])

            with open(output_file, 'w') as output_file:
                output_file.write(rendered_output)            
