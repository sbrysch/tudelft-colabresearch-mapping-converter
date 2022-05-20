import re

from project import Project
from project_address import ProjectAddress
from utils.utils import get_integer


def process_uk_england(data, source_id):
  '''Process list of projects from England
  '''
  print('Processing England...')
  projects = []

  for ip in data:
    # ignore empty rows
    if ip[0]:
      # create a name as none exists
      name = f'{ip[0]}-{ip[8]}'
      project = Project(name, source_id)

      # address
      project.address = ProjectAddress('GB')
      project.address.code = ip[9] # Project Postcode Area

      project.dwellings_number = ip[12] # Total number of homes

      # status
      if ip[10] == 'Live':
        project.development_stage = 'active'
      else:
        project.development_stage = 'developing'

      # completion_year
      if project.development_stage == 'active':
        project.completion_year = ip[13]

      # housing tenure
      if get_integer(ip[14]) > 0:
        # Affordable Rent Homes > 0
        project.add_housing_tenure('rental_private_regulated')
      if get_integer(ip[15]) > 0:
        # Discounted Market Sale Homes (% income) > 0
        project.add_housing_tenure('ownership_full')
      if get_integer(ip[16]) > 0:
        # Discounted Market Sale Homes (% market) > 0
        project.add_housing_tenure('ownership_full')
      if get_integer(ip[21]) > 0:
        # Living Rent Homes > 0
        project.add_housing_tenure('rental_private_regulated')
      if get_integer(ip[20]) > 0:
        # Social Rent Homes > 0
        project.add_housing_tenure('rental_social')
      if get_integer(ip[18]) > 0:
        # Market Sale Homes > 0
        project.add_housing_tenure('ownership_full')
      if get_integer(ip[22]) > 0:
        # Market Rent Homes > 0
        project.add_housing_tenure('rental_private')
      if get_integer(ip[24]) > 0:
        # Shared Ownership Homes > 0
        project.add_housing_tenure('ownership_co')
      if get_integer(ip[23]) > 0:
        # Shared Equity Homes > 0
        project.add_housing_tenure('ownership_shares')
      if get_integer(ip[19]) > 0:
        # Mutual Home Ownership Homes > 0
        project.add_housing_tenure('ownership_shares')

      # legal_form
      if 'Registered Society' in ip[2]:
        project.add_legal_form('clt')
        project.add_legal_form('rs')
      elif 'Community Benefit Society' in ip[2]:
        project.add_legal_form('clt')
        project.add_legal_form('cbs')
      elif 'Company Limited by Guarantee' in ip[2]:
        project.add_legal_form('clt')
        project.add_legal_form('clg')

      projects.append(project)

  print(f'Processed: {len(projects)} projects\n')
  return projects
