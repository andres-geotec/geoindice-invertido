import json
import os

import requests
from django.core.management.base import BaseCommand

GEONODE_URL = "http://ide.sedatu.gob.mx/api/v2/resources"

class Command(BaseCommand):
  help = "Descarga resources de GeoNode y los guarda en un archivo JSON"

  def handle(self, *args, **options):
    self.stdout.write("Consultando GeoNode...")
    resp = requests.get(GEONODE_URL)
    resp.raise_for_status()

    data = resp.json()

    # Carpeta para guardar los datos
    data_dir = os.path.join("data")
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, "resources.json")
    with open(output_path, "w", encoding="utf-8") as f:
      json.dump(data, f, ensure_ascii=False, indent=2)

    self.stdout.write(self.style.SUCCESS(f"Datos guardados en {output_path}"))
