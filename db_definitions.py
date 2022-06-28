from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class DevelopmentStage(Base):
  __tablename__ = 'development_stages'

  slug = Column('slug', String, primary_key=True)
  name = Column('name', String)
  description = Column('description', Text)

  def as_dict(self):
    return {
      'slug': self.slug,
      'name': self.name,
      'description': self.description,
    }

class HousingTenure(Base):
  __tablename__ = 'housing_tenures'

  slug = Column('slug', String, primary_key=True)
  name = Column('name', String)
  description = Column('description', Text)

  def as_dict(self):
    return {
      'slug': self.slug,
      'name': self.name,
      'description': self.description,
    }


class LandTenure(Base):
  __tablename__ = 'land_tenures'

  slug = Column('slug', String, primary_key=True)
  name = Column('name', String)
  description = Column('description', Text)

  def as_dict(self):
    return {
      'slug': self.slug,
      'name': self.name,
      'description': self.description,
    }


class LegalForm(Base):
  __tablename__ = 'legal_forms'

  slug = Column('slug', String, primary_key=True)
  name = Column('name', String)
  description = Column('description', Text)

  def as_dict(self):
    return {
      'slug': self.slug,
      'name': self.name,
      'description': self.description,
    }

class Country(Base):
  __tablename__ = 'countries'

  id = Column('id', String, primary_key=True)
  description = Column('description', Text)

  def as_dict(self):
    return {
      'id': self.id,
      'description': self.description,
    }


class dbProject(Base):
  __tablename__ = 'projects'

  id = Column(Integer, primary_key=True)

  name = Column('name', String)
  development_stage = Column('development_stage', String)
  completion_year = Column('completion_year', Integer)
  dwellings_number = Column('dwellings_number', Integer)

  address_line1 = Column(String)
  address_region = Column(String)
  address_code = Column(String)
  address_country_code = Column(String)

  legal_forms  = relationship('PrjLegalAssoc')
  housing_tenures = relationship('PrjHousingAssoc')

  source_id = Column(Integer, ForeignKey('sources.id'))
  source = relationship("Source")


class PrjLegalAssoc(Base):
  __tablename__ = 'projects_legal_forms'
  project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
  legal_form_id = Column(String, ForeignKey('legal_forms.slug'), primary_key=True)
  legal_form = relationship('LegalForm')

class PrjHousingAssoc(Base):
  __tablename__ = 'projects_housing_tenures'
  project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
  housing_tenure_id = Column(String, ForeignKey('housing_tenures.slug'), primary_key=True)
  housing_tenure = relationship('HousingTenure')


class Taxonomy(Base):
  __tablename__ = 'taxonomy'

  id = Column(Integer, primary_key=True, autoincrement=True)
  parent_id = Column(Integer, nullable=True)
  country = Column(String, nullable=True)
  name = Column(String)
  slug = Column(String)
  definition = Column(Text, nullable=True)

  def __getitem__(self, field):
    return self.__dict__[field]

  def serialized(self):
    return {
      'id': self.id,
      'slug': self.slug,
      'parent_id': self.parent_id,
      'country': self.country,
      'name': self.name,
      'definition': self.definition
    }


class Source(Base):
  __tablename__ = 'sources'

  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(Date)
  country_code = Column(String)
  name = Column(String)
  description = Column(Text, nullable=True)
  link = Column(String, nullable=True)

  def __getitem__(self, field):
    return self.__dict__[field]

  def serialized(self):
    return {
      'id': self.id,
      'name': self.name,
      'date': self.date.strftime('%Y-%m-%d'),
      'description': self.description,
      'link': self.link,
    }
