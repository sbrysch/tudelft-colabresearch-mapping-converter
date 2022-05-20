from ast import literal_eval

from project import Project
from project_address import ProjectAddress
from db_definitions import Source


def process_normal_source(data, source):
  '''Process formatted list of projects
  '''

  print(f'Processing {source.name}...')
  projects = []

  for ip in data:
    project = Project(ip[0], source.id)

    project.development_stage = ip[1]
    project.completion_year = ip[2]
    project.dwellings_number = ip[3]

    # Address
    project.address = ProjectAddress(source.country_code)
    project.address.line1 = ip[4]
    project.address.region = ip[5]
    project.address.code = ip[6]

    # housing_tenure
    for ht in literal_eval(ip[7]):
      project.add_housing_tenure(ht)

    # legal form
    for lf in literal_eval(ip[8]):
      project.add_legal_form(lf)

    projects.append(project)

  print(f'Processed: {len(projects)} projects\n')
  return projects
