import json
import os

GEONODE_URL = "http://ide.sedatu.gob.mx/api/v2/resources"
data_docs = ['title', 'raw_abstract']

def verifyFolder(name):
  data_dir = os.path.join(name)
  os.makedirs(data_dir, exist_ok=True)
  return data_dir

def joinPath(*args):
  for arg in args[:1]:
    verifyFolder(arg)
  return os.path.join(*args)

def writeJSON(content, name):
  output_path = joinPath("data", name)
  # escritura del archivo
  with open(output_path, "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)

# -----------------------

def readJSON(file_path):
  if not os.path.exists(file_path):
    raise ValueError(f"Aún no se ha creado {file_path}, ejecuta el comando fetch_resources.")

  with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  return data