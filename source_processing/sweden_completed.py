import re

from project import Project
from project_address import ProjectAddress


def process_se_completed(data, source_name):
  '''Process list of completed projects from Sweden
  '''
  print('Processing Sweden (completed projects)...')
  projects = []

  for ip in data:
    project = Project(ip[2], source_name)

    # Address
    project.address = ProjectAddress('Sweden', 'SE')
    project.address.region = ip[1] # City/municipality
    project.address.line1 = ip[3] # Address

    project.dwellings_number = ip[11] # Number of flats
    project.development_stage = 'active'
    project.completion_year = ip[4] # started living

    # housing_tenure
    if ip[6] == 'tenancy':
      if ip[10] == 'municipality owned public housing company':
        project.add_housing_tenure('rental_public')
      elif ip[10] == 'private housing company':
        project.add_housing_tenure('rental_private_regulated')
      elif ip[10] == 'foundation or trust':
        project.add_housing_tenure('rental_private_regulated')
      elif ip[10] == 'private person':
        project.add_housing_tenure('rental_private_regulated')
    elif ip[6] == 'cooperative tenancy':
      project.add_housing_tenure('rental_cooperative')
    elif ip[6] == 'condominium':
      project.add_housing_tenure('ownership_co')

    # legal form
    if ip[6] == 'cooperative tenancy':
      project.add_legal_form('cooperative')
    if ip[10] == 'foundation or trust':
      project.add_legal_form('foundation')

    projects.append(project)

  print(f'Processed: {len(projects)} projects\n')
  return projects
