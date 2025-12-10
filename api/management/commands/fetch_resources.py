import requests
from django.core.management.base import BaseCommand

from .inverted_index import InvertedIndex
from .utils import GEONODE_URL, data_docs, verifyFolder, joinPath, writeJSON

class Command(BaseCommand):
  help = "Descarga resources de GeoNode y los guarda en un archivo JSON"

  def handle(self, *args, **options):
    data = self.requestUrl(GEONODE_URL)
    docs = self.cerateDocs(data)
    self.createIndex(docs)

  def requestUrl(self, url):
    self.stdout.write("Consultando GeoNode...")
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

  def cerateDocs(self, data):
    # acomodando en forma de documentos para el índice invertido
    docs = {
      resource['pk']: {
        key: resource[key]
        for key in resource
        if key in data_docs and resource[key] != ""
      } for resource in data['resources']
    }  

    # archivo para guardar los datos
    output_path = joinPath("data", "docs.json")
    # escritura del archivo
    writeJSON(output_path, docs)
    self.stdout.write(self.style.SUCCESS(f"Datos guardados en {output_path}"))
    return docs
  
  def createIndex(self, docs):
    self.stdout.write("Creando index inverso...")
    docs_join = {
      doc_id: ' '.join(
        docs[doc_id][key]
        for key in docs[doc_id]
      ) for doc_id in docs
    }
    invertedIndex = InvertedIndex(docs_join)
    index = invertedIndex.build()
    
    # archivo para guardar los datos
    output_path = joinPath("data", "index.json")
    # escritura del archivo
    writeJSON(output_path, index)
    self.stdout.write(self.style.SUCCESS(f"Datos guardados en {output_path}"))
    return index
