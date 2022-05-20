from project_address import ProjectAddress

from db_definitions import HousingTenure, LegalForm, dbProject, PrjLegalAssoc, PrjHousingAssoc
from base import Base


class Project:
  def __init__(self, name, source_id):
    self.name = name
    self.geolocation = None
    self.completion_year = None
    self.dwellings_number = None
    self.housing_tenure = None
    self.legal_form = None
    self.source_id = source_id

  def add_housing_tenure(self, value):
    if self.housing_tenure == None:
      self.housing_tenure = [value]
    else:
      if value not in self.housing_tenure:
        self.housing_tenure.append(value)

  def add_legal_form(self, value):
    if self.legal_form == None:
      self.legal_form = [value]
    else:
      if value not in self.legal_form:
        self.legal_form.append(value)

  # address
  @property
  def address(self):
    return self._address

  @address.setter
  def address(self, value):
    if not isinstance(value, ProjectAddress):
      raise ValueError('Address must be an instance of ProjectAddress')
    self._address = value


  # housing_tenure
  @property
  def housing_tenure(self):
    return self._housing_tenure

  @housing_tenure.setter
  def housing_tenure(self, value):
    housing_tenures = [
      'ownership_full',
      'ownership_co',
      'ownership_shares',
      'rental_private_unregulated',
      'rental_private_regulated',
      'rental_private',
      'rental_social',
      'rental_public',
      'rental_cooperative',
      'use_right',
    ]
    if value == None:
      self._housing_tenure = None
    elif not isinstance(value, list):
      raise ValueError('housing_tenure must be a list')
    else:
      for v in value:
        if v not in housing_tenures:
          raise ValueError(f'{value} is not a valid value for housing_tenure')
      self._housing_tenure = value


  # legal_form
  @property
  def legal_form(self):
    return self._legal_form

  @legal_form.setter
  def legal_form(self, value):
    legal_forms = [
      'association',
      'cooperative',
      'foundation',
      'clt',
      'clg',
      'cbs',
      'rs',
    ]
    if value == None:
      self._legal_form = None
    elif not isinstance(value, list):
      raise ValueError('legal_form must be a list')
    else:
      for v in value:
        if v not in legal_forms:
          raise ValueError(f'{value} is not a valid value for legal_form')
      self._legal_form = value


  # development_stage
  @property
  def development_stage(self):
    return self._development_stage

  @development_stage.setter
  def development_stage(self, value):
    stages = [
      'active',
      'developing'
    ]
    if value not in stages:
      raise ValueError('Invalid development stage value.')
    self._development_stage = value


  # completion_year
  @property
  def completion_year(self):
    return self._completion_year

  @completion_year.setter
  def completion_year(self, value):
    try:
      value = int(value)
    except Exception:
      self._completion_year = None
    else:
      self._completion_year = value


  # dwellings_number
  @property
  def dwellings_number(self):
    return self._dwellings_number

  @dwellings_number.setter
  def dwellings_number(self, value):
    try:
      value = int(value)
    except Exception:
      self._dwellings_number = None
    else:
      self._dwellings_number = value


  # # source
  # @property
  # def source(self):
  #   return self._source


  def __str__(self):
    return f'Project: {self.name}'


  # For Pandas dataset and csv export
  def to_dict(self):
    return {
      'name': self.name,
      'development_stage': self.development_stage,
      'completion_year': self.completion_year,
      'address': self.address,
      'address_country_code': self.address.country_code,  # Required for mapping ng app
      'geolocation': self.geolocation,
      'dwellings_number': self.dwellings_number,
      'housing_tenure': self.housing_tenure,
      'legal_form': self.legal_form,
      'source_id': self.source_id,
    }

  # Save to database
  def add_to_db(self, session):
    dbp = dbProject()

    dbp.name = self.name
    dbp.development_stage = self.development_stage
    dbp.completion_year = self.completion_year
    dbp.dwellings_number = self.dwellings_number

    dbp.address_line1 = self.address.line1
    dbp.address_region = self.address.region
    dbp.address_code = self.address.code
    dbp.address_country_code = self.address.country_code

    if self.housing_tenure:
      for entry in self.housing_tenure:
        aa = PrjHousingAssoc()
        ht = session.query(HousingTenure).get(entry)
        aa.housing_tenure = ht
        dbp.housing_tenures.append(aa)

    if self.legal_form:
      for entry in self.legal_form:
        a = PrjLegalAssoc()
        lf = session.query(LegalForm).get(entry)
        a.legal_form = lf
        dbp.legal_forms.append(a)

    dbp.source_id = self.source_id

    session.add(dbp)
