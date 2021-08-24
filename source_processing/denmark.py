import re

from project import Project
from project_address import ProjectAddress


def process_dk(data, source_name, source_year):
  '''Process list of projects from Denmark
  '''
  print('Processing Denmark...')
  projects = []

  for ip in data:
    # ignore empty rows
    if ip[0]:
      # format name
      name = re.sub("\((.*)", '', ip[0]) # remove anything in ()
      name = re.sub("\"", '', name) # remove all "
      project = Project(name, source_name)

      # address
      project.address = ProjectAddress('Denmark', 'DK')
      asplit = re.split(",", ip[5])
      project.address.line1 = asplit[0] # Adresse
      if len(asplit) > 1:
        project.region = re.sub("([0-9]+)", '', asplit[1]) # remove code
      project.address.code = ip[6]

      project.dwellings_number = ip[3] # Number of housing units

      # completion_year
      if ip[1] and int(ip[1]) <= source_year:
        project.completion_year = ip[1] # Established

      # development_stage
      if project.completion_year:
        project.development_stage = 'active'
      else:
        project.development_stage = 'developing'

      # housing_tenure
      if ip[2] == 'Andelsboliger':
        project.add_housing_tenure('ownership_shares')
      elif ip[2] == 'Almene boliger':
        project.add_housing_tenure('rental_public')
        project.add_housing_tenure('rental_social')
      elif ip[2] == 'Ejerboliger':
        project.add_housing_tenure('ownership_full')
      elif ip[2] == 'Lejeboliger':
        project.add_housing_tenure('rental_private_regulated')
      elif ip[2] == 'Medejerboliger':
        project.add_housing_tenure('ownership_co')

      # legal_form
      if ip[2] == 'Andelsboliger':
        project.add_legal_form('cooperative')

      projects.append(project)

  print(f'Processed: {len(projects)} projects\n')
  return projects
