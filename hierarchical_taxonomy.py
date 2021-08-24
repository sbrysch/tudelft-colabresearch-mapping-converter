from slugify import slugify

class HierarchicalTaxonomy():
  def __init__(self, id, name, country, definition):
    self.id = id
    self.name = name
    self.slug = slugify(name)
    self.country = country
    self.definition = definition
    self.children = []

  def serialize(self):

    children = []
    for e in self.children:
      children.append(e.serialize())

    return {
      'id': self.id,
      'slug': self.slug,
      'name': self.name,
      'country': self.country,
      'definition': self.definition,
      'children': children
    }
