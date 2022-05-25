import csv
import re
import json
from datetime import datetime

from slugify import slugify

import pandas as pd
from sqlalchemy.engine import engine_from_config
from tabulate import tabulate

from hierarchical_taxonomy import HierarchicalTaxonomy

from source_processing.custom.denmark import process_dk
from source_processing.custom.sweden_completed import process_se_completed
from source_processing.custom.sweden_wip import process_se_wip
from source_processing.custom.united_kingdom_england import process_uk_england

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from base import Base

from db_definitions import *
from source_processing.normal import process_normal_source

def load_source_csv_file(path, delimiter='|'):
  with open(path, encoding="utf8") as csvfile:
    return list(csv.reader(csvfile, delimiter=delimiter))[1:]


# 1. Create database
print('\n\n-> Generating database...\n')

db_path = 'data/output/co-lab-research-db.sqlite3'
engine = create_engine(f'sqlite:///{db_path}', echo=False)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


# Load taxonomy to db

taxonomy = load_source_csv_file(f'./classification/taxonomy.csv')
for s in taxonomy:
  entry = Taxonomy()
  entry.parent_id = s[1]
  entry.country = s[2]
  entry.name = s[3]
  entry.slug = slugify(s[3])
  entry.definition = s[4]
  session.add(entry)

session.commit()
print('taxonomy table created')


# Load classifications to db

development_stages = load_source_csv_file('./classification/development_stages.csv')

classifications = {
  'development_stages': DevelopmentStage,
  'housing_tenures': HousingTenure,
  'land_tenures': LandTenure,
  'legal_forms': LegalForm,
  'countries': Country,
}

for table, c_class in classifications.items():
  source = load_source_csv_file(f'./classification/{table}.csv')

  for s in source:
    entry = c_class()

    if table != 'countries':
      entry.slug = s[0]
      entry.name = s[1]
      entry.description = s[2]
    else:
      entry.id = s[0]
      entry.description = s[1]

    session.add(entry)

  session.commit()
  print(f'{table} table created')


# Load sources to db

for s in load_source_csv_file(f'./data/input/sources.csv'):
  entry = Source()
  entry.date = datetime.strptime(s[0], '%Y-%m-%d')
  entry.country_code = s[1]
  entry.name = s[2]
  entry.description = s[3]
  entry.link = s[4]
  session.add(entry)

session.commit()
print('sources table created')



# 2. Generating classification files (json)
print()
print('\n-> Generating classification files...')
print()


def export_object_to_json(object, destination, name):
  print(f'Exporting {name}...')
  entries = session.query(object).all()
  entries_serialized = []
  for e in entries:
    entries_serialized.append(e.serialized())

  filepath = destination
  sourceFile = open(filepath, 'w')
  print(json.dumps(entries_serialized), file=sourceFile)
  sourceFile.close()

  print(f'Exported to {filepath}\n')


def taxonomy_gen_str_entries(id = False):

  # set id
  if not id:
    tdb = session.query(Taxonomy).limit(1)[0]
    id = tdb['id']
    print('there was no id')

  # get entry
  e = session.query(Taxonomy).filter_by(id=id).limit(1)[0]
  entry = HierarchicalTaxonomy(e['id'], e['name'], e['country'], e['definition'])

  # get children
  entry.children = []
  for child in session.query(Taxonomy).filter_by(parent_id=id):
    res = taxonomy_gen_str_entries(child['id'])
    entry.children.append(res)

  return entry


# Structured taxonomy
print('Exporting structured taxonomy...')
tdb = session.query(Taxonomy).limit(1)[0]

parent_id = tdb['id']
entries = taxonomy_gen_str_entries(tdb['id'])

filepath = f'./data/output/taxonomy-structured.json'
sourceFile = open(filepath, 'w')
print(json.dumps(entries.serialize()), file=sourceFile)
sourceFile.close()

print(f'Exported to {filepath}\n')

# Taxonomy
export_object_to_json(Taxonomy, './data/output/taxonomy.json', 'taxonomy')

# Combined classification
print('Exporting combined classifications...')

filepath = f'./data/output/classifications.json'
temp_object = {}

for name, c_class in classifications.items():
  entries = session.query(c_class).all()
  temp_object[name] = [t.as_dict() for t in entries]

sourceFile = open(filepath, 'w')
print(json.dumps(temp_object), file=sourceFile)
sourceFile.close()

print(f'Exported to {filepath}\n')

# Sources
export_object_to_json(Source, './data/output/sources.json', 'sources')



# 3. Import and process data
print('\n-> Processing data...\n')
projects = []

# 3.1 custom imports

custom_sources = [
  [
    'sweden-projects-completed.csv',
    'process_se_completed',
    1,
  ],
  [
    'sweden-projects-wip.csv',
    'process_se_wip',
    1,
  ],
  [
    'denmark-projects.csv',
    'process_dk',
    2,
    2019
  ],
  [
    'england-projects.csv',
    'process_uk_england',
    3,
  ],
]

for cs in custom_sources:
  data = load_source_csv_file(f'./data/input/custom/{cs[0]}')
  if len(cs) > 3:
    projects += locals()[cs[1]](data, cs[2], cs[3])
  else:
    projects += locals()[cs[1]](data, cs[2])

total_projects_custom = len(projects)
print(f'[Total processed projects from custom sources: {total_projects_custom}]\n')

# 3.2 normal imports

sources = session.query(Source).all()
for s in sources[len(custom_sources) - 1:]:
  source = session.query(Source).where(Source.id == s.id).first()
  data = load_source_csv_file(f'./data/input/normal/{s.id}.csv','|')
  projects += process_normal_source(data, source)

total_projects_normal = len(projects) - total_projects_custom
print(f'[Total processed projects from normal sources: {total_projects_normal}]\n')

print(f'[Overall processed projects: {len(projects)}]\n')


# Save to DB
print('\n-> Saving projects to database...\n')
for p in projects:
  p.add_to_db(session)

session.commit()
session.close()
print(f'Saved to: ./{db_path}')

# Save projets to files
print('\n\n-> Importing projects to files...\n')

# to CSV
filepath = './data/output/aggregated_data.csv'
df = pd.DataFrame([t.to_dict() for t in projects])
df.to_csv(filepath, index=False, encoding='utf-16',sep='|')
print(f'Imported to: {filepath}')

# to JSON
filepath = './data/output/aggregated_data.json'
df.to_json(filepath, orient='records')
print(f'Imported to: {filepath}')


print('\n\nDone\n')
