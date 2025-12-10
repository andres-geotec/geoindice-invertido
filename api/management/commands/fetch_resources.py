import json
import os

import requests
from django.core.management.base import BaseCommand

from .inverted_index import InvertedIndex

GEONODE_URL = "http://ide.sedatu.gob.mx/api/v2/resources"

class Command(BaseCommand):
  help = "Descarga resources de GeoNode y los guarda en un archivo JSON"

  def handle(self, *args, **options):
    self.stdout.write("Consultando GeoNode...")
    resp = requests.get(GEONODE_URL)
    resp.raise_for_status()

    data = resp.json()
    # data_filtrada = {
    #   resource['pk']: {key: resource[key]} for resource in data['resources']
    #   for key in resource
    #   if key in ['title', 'raw_abstract']
    # }
    data_filtrada = {
      resource['pk']: ' '.join([
        # key: resource[key]
        resource[key]
        for key in resource
        if key in ['title', 'raw_abstract'] and resource[key] != ""
      ]) for resource in data['resources']
    }
    invertedIndex = InvertedIndex(data_filtrada)
    index = invertedIndex.build()

    # carpeta para guardar los datos
    data_dir = os.path.join("data")
    os.makedirs(data_dir, exist_ok=True)

    # archivo para guardar los datos
    output_path = os.path.join(data_dir, "resources.json")
    with open(output_path, "w", encoding="utf-8") as f:
      json.dump(index, f, ensure_ascii=False, indent=2)

    self.stdout.write(self.style.SUCCESS(f"Datos guardados en {output_path}"))
