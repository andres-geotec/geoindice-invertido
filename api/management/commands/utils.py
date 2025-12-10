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

def writeJSON(output_path, content):
  # escritura del archivo
  with open(output_path, "w", encoding="utf-8") as f:
    json.dump(content, f, ensure_ascii=False, indent=2)