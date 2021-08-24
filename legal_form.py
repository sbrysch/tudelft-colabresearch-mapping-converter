class ProjectLegalForm:
  def __init__(self, slug, name, description):
    self.slug = slug
    self.name = name
    self.description = description

  def __str__(self):
    return f'LegalForm({self.slug},{self.name})'

    # __repr__ = __str__
