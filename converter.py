import csv
import re
import datetime
import json

from slugify import slugify

import pandas as pd
from sqlalchemy.engine import engine_from_config
from tabulate import tabulate

from hierarchical_taxonomy import HierarchicalTaxonomy

from source_processing.denmark import process_dk
from source_processing.sweden_completed import process_se_completed
from source_processing.sweden_wip import process_se_wip
from source_processing.united_kingdom_england import process_uk_england

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from base import Base

from db_definitions import *

def load_source_csv_file(path):
  with open(path, encoding="utf8") as csvfile:
    return list(csv.reader(csvfile))[1:]


# Create database
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



print()
print('\n-> Generating classification files...')
print()


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


print('Exporting structured taxonomy...')
tdb = session.query(Taxonomy).limit(1)[0]

parent_id = tdb['id']
entries = taxonomy_gen_str_entries(tdb['id'])

filepath = f'./data/output/taxonomy-structured.json'
sourceFile = open(filepath, 'w')
print(json.dumps(entries.serialize()), file=sourceFile)
sourceFile.close()

print(f'Exported to {filepath}\n')


print('Exporting taxonomy...')
entries = session.query(Taxonomy).all()
entries_serialized = []
for e in entries:
  entries_serialized.append(e.serialized())

filepath = f'./data/output/taxonomy.json'
sourceFile = open(filepath, 'w')
print(json.dumps(entries_serialized), file=sourceFile)
sourceFile.close()

print(f'Exported to {filepath}\n')


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


# Import and process data
print('\n-> Processing data...\n')
projects = []

# Import Sweden - completed
data = load_source_csv_file('./data/input/sweden-projects-completed.csv')
source_name = 'Database CH Sweden 2020.xlsx'
projects += process_se_completed(data, source_name)

# Import Sweden - wip
data = load_source_csv_file('./data/input/sweden-projects-wip.csv')
source_name = 'Database CH Sweden 2020.xlsx'
projects += process_se_wip(data, source_name)


# Import Denemark
data = load_source_csv_file('./data/input/denmark-projects.csv')
source_name = 'Database CH Denmark 2019.xlsx'
projects += process_dk(data, source_name, source_year = 2019)

# Import England
data = load_source_csv_file('./data/input/england-projects.csv')
source_name = 'ENGLAND CLT project data-2020-11-18-10-51-57.xlsx'
projects += process_uk_england(data, source_name)

print(f'[Total processed projects: {len(projects)}]')

# Export to DB
print('\n\n-> Saving projects to database...\n')
for p in projects:
  p.add_to_db(session)

session.commit()
session.close()
print(f'Saved to: ./{db_path}')

# Exportin projets
print('\n\n-> Exporting projects to files...\n')

# to CSV
time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filepath = f'./data/output/{time}_aggregated_data.csv'

df = pd.DataFrame([t.to_dict() for t in projects])
df.to_csv(filepath, index=False, encoding='utf-16',sep='|')
print(f'Exported to: {filepath}')


# to JSON
filepath = f'./data/output/{time}_aggregated_data.json'
df.to_json(filepath, orient='records')

print(f'Exported to: {filepath}')


print('\n\nDone\n')
