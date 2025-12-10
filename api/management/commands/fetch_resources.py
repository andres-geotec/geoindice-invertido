import requests
from django.core.management.base import BaseCommand

from ...classes.inverted_index import InvertedIndex
from .utils import GEONODE_URL, data_docs, writeJSON

class Command(BaseCommand):
  help = "Descarga resources de GeoNode y los guarda en un archivo JSON"

  def handle(self, *args, **options):
    resources = self.getResources()
    
    docs = self.cerateDocsFiltered(resources)
    self.saveJSON(docs, 'docs.json')

    invertedIndex = InvertedIndex()
    invertedIndex.tokenize(self.createDocsJoin(docs))
    # invertedIndex.tokens = tokenize(self.createDocsJoin(docs))
    self.saveJSON(invertedIndex.tokens, 'tokens.json')
    self.saveJSON(invertedIndex.build_index(), 'index.json')

  def createDocsJoin(self, docs):
    docs_join = {
      doc_id: ' '.join(
        docs[doc_id][key]
        for key in docs[doc_id]
      ) for doc_id in docs
    }
    return docs_join
    
  def saveJSON(self, docs, name_file):
    writeJSON(docs, name_file)
    self.stdout.write(self.style.SUCCESS(f"{name_file} creado correctamente."))
    
  def cerateDocsFiltered(self, resources):
    # acomodando en forma de documentos para el índice invertido
    return {
      resource['pk']: {
        key: resource[key]
        for key in resource
        if key in data_docs and resource[key] != ""
      } for resource in resources
    }

  def getResources(self):
    self.stdout.write("Consultando GeoNode...")

    exist_page = True
    page = 1
    resources = []
    while exist_page:
      # print(page)
      resp = requests.get(GEONODE_URL, params={
        'filter{category.identifier}':'movilidad',
        'filter{group.name}': 'dgpdi',
        'page': page
      })
      resp.raise_for_status()
    
      data = resp.json()
      if 'resources' in data:
        resources.extend(data['resources'])
        self.stdout.write(self.style.SUCCESS(f"{len(resources)} Recursos consultados :)"))

      exist_page = data['links']['next'] is not None
      page += 1
    
    if len(resources) > 0:
      return resources
    else:
      self.stdout.write(self.style.ERROR("no se encontraron los recursos :("))
      raise ValueError('Ocurrió un error')
