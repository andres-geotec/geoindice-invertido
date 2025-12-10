import json
import os

def readJSON(file_path):
  if not os.path.exists(file_path):
    raise ValueError(f"Aún no se ha creado {file_path}, ejecuta el comando fetch_resources.")

  with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  return data